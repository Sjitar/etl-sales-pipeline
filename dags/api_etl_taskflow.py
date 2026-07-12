import subprocess
from datetime import datetime, timedelta

from airflow.decorators import dag, task

PROJECT_DIR = "/Users/sergeji/Projects/airflow-airbyte-lab"
PYTHON = "/Users/sergeji/miniforge3/envs/analytics/bin/python"


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
    def load_to_duckdb():
        run_module("etl.transform")

    @task(execution_timeout=timedelta(minutes=2))
    def build_report():
        run_module("etl.transform")

    extract = extract_api_data()
    transform = transform_api_data()
    postgres = load_to_postgres()
    duckdb = load_to_duckdb()
    report = build_report()

    extract >> transform >> postgres >> duckdb >> report


api_etl_taskflow()
