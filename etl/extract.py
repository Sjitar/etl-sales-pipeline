import json
from pathlib import Path

import requests

from etl.config import RAW_DIR
from etl.logger import get_logger


logger = get_logger(__name__)

from etl.config import API_BASE_URL, API_RESOURCES, RAW_DIR


def extract_resource(resource: str) -> Path:
    output_file = RAW_DIR / f"{resource}.json"
    url = f"{API_BASE_URL}/{resource}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    logger.info("Extracted %s records from %s to %s", len(data), url, output_file)
    return output_file


def extract_api_data():
    for resource in API_RESOURCES:
        extract_resource(resource)


if __name__ == "__main__":
    extract_api_data()