import json

import requests

from etl.config import RAW_DIR
from etl.logger import get_logger


logger = get_logger(__name__)

API_URL = "https://jsonplaceholder.typicode.com/users"


def extract_users():
    output_file = RAW_DIR / "users.json"

    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    data = response.json()

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    logger.info("Extracted %s users to %s", len(data), output_file)


if __name__ == "__main__":
    extract_users()
