import duckdb

from etl.config import REPORT_DIR, DATABASE, SQL_DIR
from etl.logger import get_logger

logger = get_logger(__name__)

def build_report():
    report_file = REPORT_DIR / "sales_by_category.csv"
    sql_file = SQL_DIR / "sales_report.sql"

    query = sql_file.read_text()

    con = duckdb.connect(DATABASE)
    df = con.execute(query).fetchdf()
    con.close()

    report_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(report_file, index=False)

    logger.info("Report saved to %s", report_file)
    logger.info("Rows in report: %s", len(df))

if __name__ == "__main__":
    build_report()