CREATE OR REPLACE TABLE users AS
SELECT *
FROM read_csv_auto(?)
