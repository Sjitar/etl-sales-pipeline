import json

import pandas as pd

from etl.config import RAW_DIR, PROCESSED_DIR
from etl.logger import get_logger
from etl.validation import validate_file_exists


logger = get_logger(__name__)


def transform_users_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result = result[["id", "name", "username", "email"]]

    return result


def transform_posts_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result = result[["id", "userId", "title", "body"]]
    result = result.rename(columns={"userId": "user_id"})

    return result


def read_json_file(file_path):
    validate_file_exists(file_path)

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def transform_api_data():
    users_raw = RAW_DIR / "users.json"
    posts_raw = RAW_DIR / "posts.json"

    users_processed = PROCESSED_DIR / "users.csv"
    posts_processed = PROCESSED_DIR / "posts.csv"

    users_df = pd.DataFrame(read_json_file(users_raw))
    posts_df = pd.DataFrame(read_json_file(posts_raw))

    users_df = transform_users_dataframe(users_df)
    posts_df = transform_posts_dataframe(posts_df)

    users_processed.parent.mkdir(parents=True, exist_ok=True)

    users_df.to_csv(users_processed, index=False)
    posts_df.to_csv(posts_processed, index=False)

    logger.info("Saved users to %s", users_processed)
    logger.info("Saved posts to %s", posts_processed)


if __name__ == "__main__":
    transform_api_data()