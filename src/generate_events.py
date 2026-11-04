"""Generate synthetic rideshare events for demonstration only.

Deterministic: seed 42, so re-running produces the same CSV.
The data is synthetic. It does NOT reproduce the original project's
production throughput (10K events/min) or any cost savings.

Output: data/sample_events.csv — 2,000 rows in total, made up of
1,990 unique events plus 10 deliberate duplicate rows (copies of the
first 10 events, with the same event_id) to test deduplication.
"""

import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "sample_events.csv"

CITIES = ["New York", "San Francisco", "Chicago", "Austin"]
CITY_WEIGHTS = [0.35, 0.25, 0.25, 0.15]
EVENT_TYPES = ["ride_request", "ride_completed", "ride_cancelled", "driver_online"]
EVENT_WEIGHTS = [0.35, 0.40, 0.10, 0.15]


def main() -> None:
    rng = random.Random(42)

    # 1,990 unique events, spread over 2023-12-15 08:00-12:00 UTC.
    # A 4-hour window keeps the 5-minute windows in stream_processor.py
    # reasonably dense for a small demo file.
    base_minutes = 8 * 60  # 08:00
    rows = []
    for i in range(1, 1991):
        minute_offset = rng.randrange(0, 4 * 60)
        second = rng.randrange(0, 60)
        hour = (base_minutes + minute_offset) // 60
        minute = (base_minutes + minute_offset) % 60
        event_time = f"2023-12-15 {hour:02d}:{minute:02d}:{second:02d}"
        city = rng.choices(CITIES, weights=CITY_WEIGHTS, k=1)[0]
        event_type = rng.choices(EVENT_TYPES, weights=EVENT_WEIGHTS, k=1)[0]
        if event_type == "ride_completed":
            fare_amount = round(rng.uniform(8, 65), 2)
            trip_minutes = rng.randrange(5, 61)
        elif event_type == "ride_request":
            fare_amount = round(rng.uniform(5, 50), 2)
            trip_minutes = 0
        else:
            fare_amount = 0.0
            trip_minutes = 0
        rows.append(
            {
                "event_id": f"EVT-{i:06d}",
                "event_time": event_time,
                "city": city,
                "event_type": event_type,
                "driver_id": f"D{rng.randrange(1, 501):04d}",
                "rider_id": f"R{rng.randrange(1, 2001):04d}",
                "fare_amount": fare_amount,
                "trip_minutes": trip_minutes,
            }
        )

    rows.sort(key=lambda r: r["event_time"])
    # Deliberate duplicates: exact copies of the first 10 events.
    # stream_processor.py must drop these by event_id (exactly-once simulation).
    rows.extend(rows[:10])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "event_id",
        "event_time",
        "city",
        "event_type",
        "driver_id",
        "rider_id",
        "fare_amount",
        "trip_minutes",
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    unique_ids = len({r["event_id"] for r in rows})
    print(f"Wrote {len(rows)} rows to {OUTPUT}")
    print(f"Unique event_ids: {unique_ids} (duplicates: {len(rows) - unique_ids})")


if __name__ == "__main__":
    main()
