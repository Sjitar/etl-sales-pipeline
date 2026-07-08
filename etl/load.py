import duckdb

from etl.config import PROCESSED_DIR, DATABASE, SQL_DIR
from etl.logger import get_logger

logger = get_logger(__name__)

def load_sales():
    processed_file = PROCESSED_DIR / "sales_clean.csv"
    sql_file = SQL_DIR / "load_sales.sql"

    query = sql_file.read_text()

    con = duckdb.connect(DATABASE)
    con.execute(query, [str(processed_file)])
    con.close()

    logger.info("Loaded sales table into %s", DATABASE)

if __name__ == "__main__":
    load_sales()