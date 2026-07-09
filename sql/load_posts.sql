CREATE OR REPLACE TABLE posts AS
SELECT *
FROM read_csv_auto(?)
