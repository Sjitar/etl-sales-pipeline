import duckdb

from etl.config import DATABASE, REPORT_DIR, REPORT_FILE, SQL_DIR
from etl.logger import get_logger


logger = get_logger(__name__)


def build_report():
    report_file = REPORT_DIR / REPORT_FILE
    sql_file = SQL_DIR / "posts_by_user.sql"

    query = sql_file.read_text()

    con = duckdb.connect(DATABASE)
    df = con.execute(query).fetchdf()
    con.close()

    report_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(report_file, index=False)

    logger.info("Rows in report: %s", len(df))
    logger.info("Report saved to %s", report_file)


if __name__ == "__main__":
    build_report()