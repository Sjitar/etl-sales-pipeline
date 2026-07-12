import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR = BASE_DIR / "reports"
SQL_DIR = BASE_DIR / "sql"

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://jsonplaceholder.typicode.com",
)

API_RESOURCES = os.getenv(
    "API_RESOURCES",
    "users,posts",
).split(",")

DATABASE_NAME = os.getenv("DATABASE_NAME", "warehouse.duckdb")
DATABASE = BASE_DIR / "data" / DATABASE_NAME

REPORT_FILE = os.getenv("REPORT_FILE", "posts_by_user.csv")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "etl")
POSTGRES_USER = os.getenv("POSTGRES_USER", "etl")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "etl")
