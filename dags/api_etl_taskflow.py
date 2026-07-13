import subprocess
from datetime import datetime, timedelta

from airflow.decorators import dag, task

PROJECT_DIR = "/Users/sergeji/Projects/airflow-airbyte-lab"
PYTHON = "/Users/sergeji/miniforge3/envs/analytics/bin/python"
DBT = "/Users/sergeji/miniforge3/envs/dbt-lab/bin/dbt"
DBT_DIR = "/Users/sergeji/Projects/airflow-airbyte-lab/dbt/analytics"

def run_dbt_build() -> None:
    result = subprocess.run(
        [DBT, "build"],
        cwd=DBT_DIR,
        capture_output=True,
        text=True,
        check=True,
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)

def run_module(module_name: str) -> None:
    result = subprocess.run(
        [PYTHON, "-m", module_name],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True,
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)


@dag(
    dag_id="api_etl_taskflow",
    start_date=datetime(2026, 7, 6),
    schedule=None,
    catchup=False,
    tags=["etl", "duckdb", "taskflow", "learning"],
)
def api_etl_taskflow():

    @task(execution_timeout=timedelta(minutes=2))
    def extract_api_data():
        run_module("etl.extract")

    @task(execution_timeout=timedelta(minutes=2))
    def transform_api_data():
        run_module("etl.transform")

    @task(execution_timeout=timedelta(minutes=2))
    def load_to_postgres():
        run_module("etl.load_postgres")

    @task(execution_timeout=timedelta(minutes=2))
    def validate_postgres_data():
        run_module("etl.quality")

    @task(execution_timeout=timedelta(minutes=2))
    def load_to_duckdb():
        run_module("etl.transform")

    @task(execution_timeout=timedelta(minutes=5))
    def build_dbt_models():
        run_dbt_build()

    extract = extract_api_data()
    transform = transform_api_data()
    postgres = load_to_postgres()
    quality = validate_postgres_data()
    duckdb = load_to_duckdb()
    dbt = build_dbt_models()

    extract >> transform >> postgres >> quality >> duckdb >> dbt


api_etl_taskflow()
