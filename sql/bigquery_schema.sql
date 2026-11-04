-- BigQuery table definition for the rideshare events stream.
-- This is an architecture / SQL example only. It is NOT a live GCP
-- deployment, and the sample CSV in this repo is synthetic data.
--
-- Cost-optimisation notes:
--  * PARTITION BY event_date: queries filtered on a date range only
--    scan the matching partitions, instead of the whole table.
--    This is the main lever behind the "partition by event date"
--    saving described in the project summary.
--  * CLUSTER BY city, event_type: within each partition, rows are
--    physically grouped by these columns, so filters such as
--    WHERE city = 'New York' AND event_type = 'ride_completed'
--    skip most blocks.
--  * event_date is a separate DATE column derived from event_time,
--    because BigQuery partition pruning works best on an explicit
--    date column (or a TIMESTAMP partition with a date filter).
--  * Prefer SELECT of only the columns you need, and avoid
--    SELECT * in dashboards / scheduled queries, to keep bytes
--    scanned — and therefore cost — down.
--  * Keep fare_amount as NUMERIC (exact) rather than FLOAT64, so
--    revenue totals do not accumulate floating-point error.

CREATE TABLE IF NOT EXISTS `your-project.rideshare.ride_events` (
  event_id STRING NOT NULL,
  event_time TIMESTAMP NOT NULL,
  event_date DATE NOT NULL,
  city STRING,
  event_type STRING,  -- ride_request, ride_completed, ride_cancelled, driver_online
  driver_id STRING,
  rider_id STRING,
  fare_amount NUMERIC,
  trip_minutes INT64
)
PARTITION BY event_date
CLUSTER BY city, event_type
OPTIONS (
  description = 'Synthetic-example schema for real-time rideshare events. Partitioned by event_date and clustered by city, event_type for cost-efficient queries.'
);

-- Example cost-efficient query: only the columns and partitions needed.
-- SELECT event_date, city, event_type, COUNT(*) AS event_count,
--        AVG(fare_amount) AS avg_fare
-- FROM `your-project.rideshare.ride_events`
-- WHERE event_date BETWEEN '2023-12-01' AND '2023-12-31'
--   AND city = 'New York'
-- GROUP BY event_date, city, event_type;
