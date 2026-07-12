import duckdb
import pandas as pd

from etl.config import DATABASE
from etl.logger import get_logger
from etl.postgres import get_postgres_connection

logger = get_logger(__name__)


def read_postgres_table(table_name: str) -> pd.DataFrame:
    query = f"SELECT * FROM {table_name}"

    with get_postgres_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)

            columns = [column.name for column in cursor.description]
            records = cursor.fetchall()

    return pd.DataFrame(records, columns=columns)


def load_dataframe_to_duckdb(
    connection: duckdb.DuckDBPyConnection,
    table_name: str,
    dataframe: pd.DataFrame,
) -> None:
    temporary_view = f"{table_name}_df"

    connection.register(temporary_view, dataframe)

    connection.execute(
        f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT *
        FROM {temporary_view}
        """
    )

    connection.unregister(temporary_view)

    logger.info(
        "Loaded %s rows into DuckDB table %s",
        len(dataframe),
        table_name,
    )


def load_postgres_data_to_duckdb() -> None:
    users_df = read_postgres_table("users")
    posts_df = read_postgres_table("posts")

    with duckdb.connect(str(DATABASE)) as connection:
        load_dataframe_to_duckdb(connection, "users", users_df)
        load_dataframe_to_duckdb(connection, "posts", posts_df)

    logger.info("PostgreSQL data loaded into %s", DATABASE)


if __name__ == "__main__":
    load_postgres_data_to_duckdb()
