import pandas as pd

from etl.config import PROCESSED_DIR, SQL_DIR
from etl.logger import get_logger
from etl.postgres import get_postgres_connection

logger = get_logger(__name__)


def create_tables(connection) -> None:
    sql_file = SQL_DIR / "create_postgres_tables.sql"
    query = sql_file.read_text(encoding="utf-8")

    with connection.cursor() as cursor:
        cursor.execute(query)

    connection.commit()
    logger.info("PostgreSQL tables created or already exist")


def load_users(connection) -> None:
    users_file = PROCESSED_DIR / "users.csv"
    users_df = pd.read_csv(users_file)

    query = """
        INSERT INTO users (id, name, username, email)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            username = EXCLUDED.username,
            email = EXCLUDED.email
    """

    records = list(
        users_df[["id", "name", "username", "email"]].itertuples(index=False, name=None)
    )

    with connection.cursor() as cursor:
        cursor.executemany(query, records)

    connection.commit()
    logger.info("Loaded %s users into PostgreSQL", len(records))


def load_posts(connection) -> None:
    posts_file = PROCESSED_DIR / "posts.csv"
    posts_df = pd.read_csv(posts_file)

    query = """
        INSERT INTO posts (id, user_id, title, body)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            user_id = EXCLUDED.user_id,
            title = EXCLUDED.title,
            body = EXCLUDED.body
    """

    records = list(
        posts_df[["id", "user_id", "title", "body"]].itertuples(index=False, name=None)
    )

    with connection.cursor() as cursor:
        cursor.executemany(query, records)

    connection.commit()
    logger.info("Loaded %s posts into PostgreSQL", len(records))


def load_api_data_to_postgres() -> None:
    with get_postgres_connection() as connection:
        create_tables(connection)
        load_users(connection)
        load_posts(connection)


if __name__ == "__main__":
    load_api_data_to_postgres()
