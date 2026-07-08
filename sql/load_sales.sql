CREATE OR REPLACE TABLE sales AS
SELECT *
FROM read_csv_auto(?)
