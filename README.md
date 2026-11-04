# Real-Time Rideshare Event Analytics on GCP
Sep-Dec 2023
Designed a streaming pipeline that processes 10K events per minute through Pub/Sub and Dataflow, using windowing and deduplication to handle late and duplicate events with exactly-once results.
Cut BigQuery query costs by 40% by partitioning tables by event date and clustering on city and event type.
Built a live Streamlit dashboard with anomaly alerts that flag demand spikes within 60 seconds.
Tech: Google Pub/Sub, Dataflow, Apache Beam, BigQuery, Streamlit, Python
