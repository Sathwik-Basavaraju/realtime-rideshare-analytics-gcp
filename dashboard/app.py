"""Streamlit dashboard for the synthetic rideshare sample data.

Run from the project root with:
    streamlit run dashboard/app.py

This is a local demo over the synthetic CSV files in this repo.
It is not connected to Pub/Sub, Dataflow, or BigQuery.
"""

import streamlit as st

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLE_PATH = ROOT / "data" / "sample_events.csv"
WINDOWED_PATH = ROOT / "outputs" / "windowed_counts.csv"
ANOMALIES_PATH = ROOT / "outputs" / "anomalies.csv"


def main() -> None:
    st.title("Real-Time Rideshare Event Analytics (Demo)")
    st.write(
        "Synthetic sample data for demonstration only. "
        "Run `python src/stream_processor.py` first to generate "
        "the windowed counts and anomaly alerts."
    )

    if not SAMPLE_PATH.exists():
        st.error(f"Sample data not found: {SAMPLE_PATH}. Run src/generate_events.py first.")
        return

    df = pd.read_csv(SAMPLE_PATH, parse_dates=["event_time"])

    st.header("Events by city")
    st.bar_chart(df["city"].value_counts())

    st.header("Events over time")
    over_time = df.set_index("event_time").resample("1h").size()
    st.line_chart(over_time)

    st.header("Events by type")
    st.bar_chart(df["event_type"].value_counts())

    st.header("Windowed counts (5-minute windows)")
    if WINDOWED_PATH.exists():
        windowed = pd.read_csv(WINDOWED_PATH)
        st.dataframe(windowed.head(100))
    else:
        st.info("No windowed counts yet. Run src/stream_processor.py to create them.")

    st.header("Anomaly alerts")
    if ANOMALIES_PATH.exists():
        anomalies = pd.read_csv(ANOMALIES_PATH)
        if anomalies.empty:
            st.info("No demand-spike anomalies flagged in the current windowed data.")
        else:
            st.dataframe(anomalies)
    else:
        st.info("No anomaly file yet. Run src/stream_processor.py to create it.")


if __name__ == "__main__":
    main()
