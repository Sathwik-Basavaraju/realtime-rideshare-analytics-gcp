"""Apache Beam pipeline skeleton (EXAMPLE ONLY, not run locally).

Mirrors src/stream_processor.py in Beam form:
  Pub/Sub -> Dataflow (Beam) -> BigQuery, with 5-minute fixed windows,
  deduplication by event_id, and demand-spike flagging.

This file is NOT executed in the local demo. It requires apache-beam
(and, for a real GCP run, a GCP project, Pub/Sub subscription and
BigQuery dataset). It is included so the Beam part of the LinkedIn
project description has a code representation in this repo, alongside
the runnable pandas simulation in src/stream_processor.py.

Install (for a real run only):
    pip install apache-beam[gcp]
"""

try:
    import apache_beam as beam
    from apache_beam.options.pipeline_options import PipelineOptions
    from apache_beam.transforms.window import FixedWindows
    _BEAM_AVAILABLE = True
except ImportError:  # pragma: no cover - Beam is not installed locally
    beam = None  # type: ignore
    PipelineOptions = None  # type: ignore
    FixedWindows = None  # type: ignore
    _BEAM_AVAILABLE = False


def run(argv=None):
    """Define (do not run locally without Beam + GCP) the Beam pipeline."""
    if not _BEAM_AVAILABLE:
        raise RuntimeError(
            "apache-beam is not installed. This is an example pipeline only; "
            "run src/stream_processor.py for the local pandas simulation."
        )
    # Example pipeline definition (placeholders for project/subscription/table):
    # with beam.Pipeline(options=PipelineOptions(argv)) as p:
    #     events = (
    #         p
    #         | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(
    #             subscription="projects/<project>/subscriptions/<subscription>")
    #         | "Parse JSON" >> beam.Map(lambda x: __import__("json").loads(x))
    #         | "Deduplicate by event_id" >> beam.Distinct()  # simplified; see note below
    #         | "Window 5 min" >> beam.WindowInto(FixedWindows(300))
    #         | "Count by city/type" >> beam.combiners.Count.PerKey(
    #             lambda e: (e["city"], e["event_type"]))
    #         | "Write to BigQuery" >> beam.io.WriteToBigQuery(
    #             table="project:dataset.rideshare_windowed",
    #             schema="window_start:TIMESTAMP,city:STRING,event_type:STRING,event_count:INTEGER")
    # )
    # Note: true exactly-once deduplication in Beam needs stateful
    # processing / a keyed state store; the local simulation in
    # src/stream_processor.py deduplicates by event_id with pandas
    # drop_duplicates, which is the demo equivalent.
    raise NotImplementedError(
        "Beam pipeline definition is an example skeleton. "
        "Fill in project/subscription/table and run on Dataflow for a real deployment."
    )


if __name__ == "__main__":
    print(f"Apache Beam available: {_BEAM_AVAILABLE}")
    print("Example only — see docstring. Local demo: python src/stream_processor.py")
