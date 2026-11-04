"""Pandas simulation of the streaming logic (no live Pub/Sub/Dataflow).

Steps:
1. Read data/sample_events.csv.
2. Deduplicate by event_id, keeping the first occurrence — this
   simulates exactly-once processing for the deliberate duplicates
   in the sample file.
3. Bucket events into 5-minute tumbling windows by city and event_type.
4. For each window, compute event count and average fare.
5. Flag a demand-spike anomaly when a window's count exceeds the
   rolling mean + 2 * rolling std of the previous 12 windows for the
   same city/event_type (minimum 3 prior windows required).

Outputs:
- outputs/windowed_counts.csv
- outputs/anomalies.csv (header only if no window meets the rule)
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "sample_events.csv"
OUTPUT_DIR = ROOT / "outputs"


def main() -> None:
    df = pd.read_csv(INPUT, parse_dates=["event_time"])
    input_rows = len(df)

    deduped = df.drop_duplicates(subset=["event_id"], keep="first").copy()
    deduped_rows = len(deduped)
    duplicates_removed = input_rows - deduped_rows

    deduped["window_start"] = deduped["event_time"].dt.floor("5min")
    windowed = (
        deduped.groupby(["window_start", "city", "event_type"], as_index=False)
        .agg(event_count=("event_id", "count"), avg_fare=("fare_amount", "mean"))
        .sort_values(["city", "event_type", "window_start"])
        .reset_index(drop=True)
    )
    windowed["avg_fare"] = windowed["avg_fare"].round(2)

    # Rolling statistics from *prior* windows only, per city/event_type.
    def add_rolling(group: pd.DataFrame) -> pd.DataFrame:
        group = group.copy()
        shifted = group["event_count"].shift(1)
        group["rolling_mean"] = shifted.rolling(12, min_periods=3).mean()
        group["rolling_std"] = shifted.rolling(12, min_periods=3).std()
        return group

    windowed = windowed.groupby(["city", "event_type"], group_keys=False).apply(add_rolling)
    windowed["rolling_mean"] = windowed["rolling_mean"].round(2)
    windowed["rolling_std"] = windowed["rolling_std"].round(2)
    windowed["is_anomaly"] = (
        windowed["rolling_mean"].notna()
        & (windowed["event_count"] > windowed["rolling_mean"] + 2 * windowed["rolling_std"])
    )

    anomalies = windowed[windowed["is_anomaly"]].copy()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    windowed_path = OUTPUT_DIR / "windowed_counts.csv"
    anomalies_path = OUTPUT_DIR / "anomalies.csv"
    windowed.to_csv(windowed_path, index=False)
    anomalies.to_csv(anomalies_path, index=False)

    print(f"Input rows: {input_rows}")
    print(f"Rows after deduplication: {deduped_rows}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Windowed rows: {len(windowed)}")
    print(f"Anomaly windows: {len(anomalies)}")
    print(f"Wrote {windowed_path}")
    print(f"Wrote {anomalies_path}")


if __name__ == "__main__":
    main()
