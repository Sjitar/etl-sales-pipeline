from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

REPORT_DIR = BASE_DIR / "reports"

DATABASE = BASE_DIR / "data" / "warehouse.duckdb"

SQL_DIR = BASE_DIR / "sql"