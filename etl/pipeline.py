from etl.extract import extract_api_data
from etl.load_postgres import load_api_data_to_postgres
from etl.logger import get_logger
from etl.transform import transform_api_data

logger = get_logger(__name__)


def run_pipeline() -> None:
    logger.info("Starting ETL pipeline")

    extract_api_data()
    transform_api_data()
    load_api_data_to_postgres()

    logger.info("ETL pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()
