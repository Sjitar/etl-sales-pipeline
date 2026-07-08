PROJECT_DIR := $(HOME)/Projects/airflow-airbyte-lab
AIRFLOW_HOME := $(PROJECT_DIR)
AIRFLOW_ENV := airflow-lab
ANALYTICS_PYTHON := $(HOME)/miniforge3/envs/analytics/bin/python

airflow-start:
	conda run -n $(AIRFLOW_ENV) env AIRFLOW_HOME=$(AIRFLOW_HOME) airflow standalone

airflow-stop:
	pkill -f airflow || true
	@echo "Airflow stopped."

airflow-dags:
	conda run -n $(AIRFLOW_ENV) env AIRFLOW_HOME=$(AIRFLOW_HOME) airflow dags list

etl-transform:
	cd $(PROJECT_DIR) && $(ANALYTICS_PYTHON) -m etl.transform

etl-load:
	cd $(PROJECT_DIR) && $(ANALYTICS_PYTHON) -m etl.load

etl-report:
	cd $(PROJECT_DIR) && $(ANALYTICS_PYTHON) -m etl.report

etl: etl-transform etl-load etl-report

clean:
	rm -f data/processed/*.csv
	rm -f reports/*.csv
	rm -f data/warehouse.duckdb
	@echo "Cleaned generated files."
