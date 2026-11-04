"""Offline analysis of the synthetic rideshare sample data.

Uses pandas + matplotlib only. Creates charts in outputs/charts/:
- events_by_city.png
- events_by_type.png
- events_over_time.png
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "sample_events.csv"
CHART_DIR = ROOT / "outputs" / "charts"


def save_bar(series: pd.Series, title: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    series.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_ylabel("Events")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    df = pd.read_csv(INPUT, parse_dates=["event_time"])
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    by_city = df["city"].value_counts().sort_values(ascending=False)
    save_bar(by_city, "Events by city", CHART_DIR / "events_by_city.png")

    by_type = df["event_type"].value_counts().sort_values(ascending=False)
    save_bar(by_type, "Events by type", CHART_DIR / "events_by_type.png")

    over_time = df.set_index("event_time").resample("1h").size()
    fig, ax = plt.subplots(figsize=(10, 5))
    over_time.plot(ax=ax)
    ax.set_title("Events over time (hourly)")
    ax.set_ylabel("Events")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "events_over_time.png")
    plt.close(fig)

    print(f"Rows analysed: {len(df)}")
    print("Events by city:")
    print(by_city.to_string())
    print("Events by type:")
    print(by_type.to_string())
    print(f"Charts written to {CHART_DIR}:")
    for name in ["events_by_city.png", "events_by_type.png", "events_over_time.png"]:
        print(f"  - {CHART_DIR / name}")


if __name__ == "__main__":
    main()
