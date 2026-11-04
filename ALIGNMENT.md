# Alignment — Real-Time Rideshare Event Analytics on GCP

Main README (original LinkedIn description) vs files in this repo.
Sample data is synthetic; original production figures are NOT claimed
as results of this starter code. See CODE_AND_DATA_README.md.

| README claim | Representation in this repo | Status |
|---|---|---|
| Pub/Sub ingestion | `src/pubsub_example.py` (publisher example) | Example only, requires GCP |
| Dataflow / Apache Beam | `src/beam_pipeline.py` (Beam skeleton) + `src/stream_processor.py` (pandas simulation) | Beam example not run locally |
| 10K events/min | Sample is 2,000 events total | Demo only, NOT 10K/min |
| Windowing + deduplication, exactly-once | `src/stream_processor.py` (5-min windows, dedup by event_id) | Simulation, not production exactly-once |
| BigQuery, partitioned by date, clustered by city/type, 40% cost cut | `sql/bigquery_schema.sql` (partition + cluster DDL) | Schema example; cost cut is original context only |
| Live Streamlit dashboard | `dashboard/app.py` + `analysis/run_analysis.py` + charts in `outputs/charts/` | Streamlit app over sample CSVs |
| Anomaly alerts within 60 seconds | `src/stream_processor.py` flags anomalies at 5-min window granularity; `outputs/anomalies.csv` | Demo timing, NOT 60-second alerts |

What was fixed in the 2026-11-04 review: added Beam and Pub/Sub
example files, and clarified in stream_processor.py that the demo
does NOT reproduce 60-second alerting. No main README content was changed.
