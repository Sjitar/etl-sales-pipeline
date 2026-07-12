PROJECT_DIR := $(HOME)/Projects/airflow-airbyte-lab
AIRFLOW_HOME := $(PROJECT_DIR)
AIRFLOW_ENV := airflow-lab
ANALYTICS_PYTHON := $(HOME)/miniforge3/envs/analytics/bin/python

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

etl-report:
	cd $(PROJECT_DIR) && $(ANALYTICS_PYTHON) -m etl.report

etl-load-postgres:
	cd $(PROJECT_DIR) && $(ANALYTICS_PYTHON) -m etl.load_postgres

etl: etl-extract etl-transform etl-load-postgres etl-quality etl-load etl-report

clean:
	rm -f data/processed/*.csv
	rm -f reports/*.csv
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