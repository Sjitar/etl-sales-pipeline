import duckdb

from etl.config import DATABASE, PROCESSED_DIR, SQL_DIR
from etl.logger import get_logger


logger = get_logger(__name__)


def load_table(table_name: str):
    csv_file = PROCESSED_DIR / f"{table_name}.csv"
    sql_file = SQL_DIR / f"load_{table_name}.sql"

    query = sql_file.read_text()

    con = duckdb.connect(DATABASE)
    con.execute(query, [str(csv_file)])
    con.close()

    logger.info("Loaded %s table into %s", table_name, DATABASE)


def load_api_data():
    load_table("users")
    load_table("posts")


if __name__ == "__main__":
    load_api_data()