"""Google Pub/Sub publisher example (EXAMPLE ONLY, not run locally).

Shows how sample events from data/sample_events.csv would be
published to a Pub/Sub topic, matching the LinkedIn project
description (Pub/Sub -> Dataflow -> BigQuery).

Requires google-cloud-pubsub and a real GCP project/topic.
It is NOT executed in the local demo; the runnable local
simulation is src/stream_processor.py.
"""

import csv
import json
from pathlib import Path

try:
    from google.cloud import pubsub_v1
    _PUBSUB_AVAILABLE = True
except ImportError:  # pragma: no cover
    pubsub_v1 = None  # type: ignore
    _PUBSUB_AVAILABLE = False

ROOT = Path(__file__).resolve().parent.parent
SAMPLE_PATH = ROOT / "data" / "sample_events.csv"


def publish_sample_events(project_id, topic_id, limit=10):
    """Publish the first `limit` sample events as JSON messages (example)."""
    if not _PUBSUB_AVAILABLE:
        raise RuntimeError("google-cloud-pubsub is not installed.")
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    with open(SAMPLE_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= limit:
                break
            data = json.dumps(row).encode("utf-8")
            future = publisher.publish(topic_path, data, event_id=row["event_id"])
            print(f"Published {row['event_id']}: {future.result()}")


if __name__ == "__main__":
    print(f"Pub/Sub client available: {_PUBSUB_AVAILABLE}")
    print("Example only — fill in project_id/topic_id and run on GCP for a real deployment.")
    print("Local demo: python src/stream_processor.py")
