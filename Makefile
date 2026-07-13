PROJECT_DIR := $(HOME)/Projects/airflow-airbyte-lab
AIRFLOW_HOME := $(PROJECT_DIR)
AIRFLOW_ENV := airflow-lab
ANALYTICS_PYTHON := $(HOME)/miniforge3/envs/analytics/bin/python
DBT_ENV = dbt-lab
DBT_DIR = $(PROJECT_DIR)/dbt/analytics

airflow-start:
	conda run --no-capture-output -n $(AIRFLOW_ENV) \
		env AIRFLOW_HOME=$(AIRFLOW_HOME) \
		airflow standalone

airflow-stop:
	pkill -f airflow || true
	@echo "Airflow stopped."

airflow-dags:
	conda run -n $(AIRFLOW_ENV) env AIRFLOW_HOME=$(AIRFLOW_HOME) airflow dags list

etl-extract:
	cd $(PROJECT_DIR) && $(ANALYTICS_PYTHON) -m etl.extract

etl-transform:
	cd $(PROJECT_DIR) && $(ANALYTICS_PYTHON) -m etl.transform

etl-quality:
	cd $(PROJECT_DIR) && $(ANALYTICS_PYTHON) -m etl.quality

etl-load:
	cd $(PROJECT_DIR) && $(ANALYTICS_PYTHON) -m etl.load

etl-load-postgres:
	cd $(PROJECT_DIR) && $(ANALYTICS_PYTHON) -m etl.load_postgres

etl: etl-extract etl-transform etl-load-postgres etl-quality etl-load dbt-build

clean:
	rm -f data/processed/*.csv
	rm -f data/warehouse.duckdb
	@echo "Cleaned generated files."

lint:
	ruff check .

format:
	ruff check . --fix
	ruff format .

format-check:
	ruff format --check .

test:
	pytest

check: lint format-check test

dbt-debug:
	conda run --no-capture-output -n $(DBT_ENV) \
		sh -c "cd $(DBT_DIR) && dbt debug"

dbt-run:
	conda run --no-capture-output -n $(DBT_ENV) \
		sh -c "cd $(DBT_DIR) && dbt run"

dbt-test:
	conda run --no-capture-output -n $(DBT_ENV) \
		sh -c "cd $(DBT_DIR) && dbt test"

dbt-build:
	conda run --no-capture-output -n $(DBT_ENV) \
		sh -c "cd $(DBT_DIR) && dbt build"

dbt-clean:
	conda run --no-capture-output -n $(DBT_ENV) \
		sh -c "cd $(DBT_DIR) && dbt clean"

dbt-docs-generate:
	conda run --no-capture-output -n $(DBT_ENV) \
		sh -c "cd $(DBT_DIR) && dbt docs generate"

dbt-docs-serve:
	conda run --no-capture-output -n $(DBT_ENV) \
		sh -c "cd $(DBT_DIR) && dbt docs serve --port 8082"