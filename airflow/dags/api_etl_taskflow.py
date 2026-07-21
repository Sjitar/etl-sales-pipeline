from datetime import UTC, datetime, timedelta

from airflow.sdk import dag, task

from etl.extract import extract_api_data as run_extract
from etl.load_postgres import load_api_data_to_postgres as run_load
from etl.quality import validate_postgres_data as run_quality_checks
from etl.transform import transform_api_data as run_transform


@dag(
    dag_id="api_etl_taskflow",
    start_date=datetime(2026, 7, 6, tzinfo=UTC),
    schedule=None,
    catchup=False,
    tags=["etl", "taskflow", "learning"],
)
def api_etl_taskflow():

    @task(execution_timeout=timedelta(minutes=2))
    def extract_api_data() -> list[str]:
        extracted_files = run_extract()

        # pathlib.Path нельзя надёжно сохранять в XCom,
        # поэтому преобразуем пути в строки.
        return [str(file_path) for file_path in extracted_files]

    @task(execution_timeout=timedelta(minutes=2))
    def transform_api_data() -> list[str]:
        processed_files = run_transform()

        return [str(file_path) for file_path in processed_files]

    @task(execution_timeout=timedelta(minutes=2))
    def load_to_postgres() -> dict[str, int]:
        return run_load()

    @task(execution_timeout=timedelta(minutes=2))
    def validate_postgres_data() -> dict[str, int]:
        return run_quality_checks()

    extract = extract_api_data()
    transform = transform_api_data()
    postgres = load_to_postgres()
    quality = validate_postgres_data()

    extract >> transform >> postgres >> quality


api_etl_taskflow()
