from etl.logger import get_logger
from etl.postgres import get_postgres_connection

logger = get_logger(__name__)


def get_scalar(connection, query: str) -> int:
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()

    if result is None:
        raise ValueError("Query returned no result")

    return int(result[0])


def validate_postgres_data() -> None:
    with get_postgres_connection() as connection:
        users_count = get_scalar(
            connection,
            "SELECT COUNT(*) FROM users",
        )

        posts_count = get_scalar(
            connection,
            "SELECT COUNT(*) FROM posts",
        )

        orphaned_posts_count = get_scalar(
            connection,
            """
            SELECT COUNT(*)
            FROM posts AS p
            LEFT JOIN users AS u
                ON u.id = p.user_id
            WHERE u.id IS NULL
            """,
        )

        users_with_nulls = get_scalar(
            connection,
            """
            SELECT COUNT(*)
            FROM users
            WHERE
                name IS NULL
                OR username IS NULL
                OR email IS NULL
            """,
        )

        posts_with_nulls = get_scalar(
            connection,
            """
            SELECT COUNT(*)
            FROM posts
            WHERE
                user_id IS NULL
                OR title IS NULL
                OR body IS NULL
            """,
        )

    if users_count == 0:
        raise ValueError("PostgreSQL users table is empty")

    if posts_count == 0:
        raise ValueError("PostgreSQL posts table is empty")

    if orphaned_posts_count > 0:
        raise ValueError(f"Found {orphaned_posts_count} posts without matching users")

    if users_with_nulls > 0:
        raise ValueError(f"Found {users_with_nulls} users with null required fields")

    if posts_with_nulls > 0:
        raise ValueError(f"Found {posts_with_nulls} posts with null required fields")

    logger.info("Users count: %s", users_count)
    logger.info("Posts count: %s", posts_count)
    logger.info("Orphaned posts: %s", orphaned_posts_count)
    logger.info("PostgreSQL data quality checks passed")


if __name__ == "__main__":
    validate_postgres_data()
