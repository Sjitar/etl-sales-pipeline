.PHONY: \
	help \
	airflow-start airflow-stop airflow-dags \
	docker-up docker-down docker-ps \
	etl-extract etl-transform etl-load-postgres etl-quality etl-load etl \
	dbt-debug dbt-run dbt-test dbt-build dbt-clean \
	dbt-docs-generate dbt-docs-serve \
	lint format format-check test check \
	clean

PROJECT_DIR := $(CURDIR)
AIRFLOW_HOME := $(PROJECT_DIR)
DBT_DIR := $(PROJECT_DIR)/dbt/analytics

UV_RUN := uv run

.DEFAULT_GOAL := help


# ----------------------------
# Help
# ----------------------------

help:
	@echo "Available commands:"
	@echo ""
	@echo "  make airflow-start       Start Airflow"
	@echo "  make airflow-stop        Stop Airflow"
	@echo "  make airflow-dags        List Airflow DAGs"
	@echo ""
	@echo "  make docker-up           Start PostgreSQL and Adminer"
	@echo "  make docker-down         Stop PostgreSQL and Adminer"
	@echo "  make docker-ps           Show Docker Compose services"
	@echo ""
	@echo "  make etl                 Run the full ETL pipeline"
	@echo "  make etl-extract         Extract data from REST API"
	@echo "  make etl-transform       Transform API data"
	@echo "  make etl-load-postgres   Load data into PostgreSQL"
	@echo "  make etl-quality         Run PostgreSQL data checks"
	@echo "  make etl-load            Load PostgreSQL data into DuckDB"
	@echo ""
	@echo "  make dbt-debug           Check dbt configuration"
	@echo "  make dbt-run             Run dbt models"
	@echo "  make dbt-test            Run dbt tests"
	@echo "  make dbt-build           Run dbt models and tests"
	@echo "  make dbt-clean           Remove dbt generated artifacts"
	@echo "  make dbt-docs-generate   Generate dbt documentation"
	@echo "  make dbt-docs-serve      Serve dbt docs on port 8082"
	@echo ""
	@echo "  make lint                Run Ruff linter"
	@echo "  make format              Fix and format Python code"
	@echo "  make format-check        Check Python formatting"
	@echo "  make test                Run pytest"
	@echo "  make check               Run lint, format check and tests"
	@echo ""
	@echo "  make clean               Remove generated local data"


# ----------------------------
# Airflow
# ----------------------------

airflow-start:
	cd $(PROJECT_DIR) && \
		AIRFLOW_HOME=$(AIRFLOW_HOME) $(UV_RUN) airflow standalone

airflow-stop:
	@pkill -f airflow || true
	@echo "Airflow stopped."

airflow-dags:
	cd $(PROJECT_DIR) && \
		AIRFLOW_HOME=$(AIRFLOW_HOME) $(UV_RUN) airflow dags list


# ----------------------------
# Docker
# ----------------------------

docker-up:
	cd $(PROJECT_DIR) && docker compose up -d

docker-down:
	cd $(PROJECT_DIR) && docker compose down

docker-ps:
	cd $(PROJECT_DIR) && docker compose ps


# ----------------------------
# ETL
# ----------------------------

etl-extract:
	cd $(PROJECT_DIR) && \
		$(UV_RUN) python -m etl.extract

etl-transform:
	cd $(PROJECT_DIR) && \
		$(UV_RUN) python -m etl.transform

etl-load-postgres:
	cd $(PROJECT_DIR) && \
		$(UV_RUN) python -m etl.load_postgres

etl-quality:
	cd $(PROJECT_DIR) && \
		$(UV_RUN) python -m etl.quality

etl-load:
	cd $(PROJECT_DIR) && \
		$(UV_RUN) python -m etl.load

etl: etl-extract etl-transform etl-load-postgres etl-quality etl-load dbt-build


# ----------------------------
# dbt
# ----------------------------

dbt-debug:
	cd $(DBT_DIR) && \
		$(CONDA_RUN) -n $(DBT_ENV) dbt debug

dbt-run:
	cd $(DBT_DIR) && \
		$(CONDA_RUN) -n $(DBT_ENV) dbt run

dbt-test:
	cd $(DBT_DIR) && \
		$(CONDA_RUN) -n $(DBT_ENV) dbt test

dbt-build:
	cd $(DBT_DIR) && \
		$(CONDA_RUN) -n $(DBT_ENV) dbt build

dbt-clean:
	cd $(DBT_DIR) && \
		$(CONDA_RUN) -n $(DBT_ENV) dbt clean

dbt-docs-generate:
	cd $(DBT_DIR) && \
		$(CONDA_RUN) -n $(DBT_ENV) dbt docs generate

dbt-docs-serve:
	cd $(DBT_DIR) && \
		$(CONDA_RUN) -n $(DBT_ENV) dbt docs serve --port 8082


# ----------------------------
# Code quality
# ----------------------------

lint:
	cd $(PROJECT_DIR) && \
		$(UV_RUN) ruff check .

format:
	cd $(PROJECT_DIR) && \
		$(UV_RUN) ruff check . --fix
	cd $(PROJECT_DIR) && \
		$(UV_RUN) ruff format .

format-check:
	cd $(PROJECT_DIR) && \
		$(UV_RUN) ruff format --check .

test:
	cd $(PROJECT_DIR) && \
		$(UV_RUN) pytest

check: lint format-check test


# ----------------------------
# Cleanup
# ----------------------------

clean:
	rm -rf $(PROJECT_DIR)/data/processed/*
	rm -f $(PROJECT_DIR)/data/warehouse.duckdb
	rm -rf $(DBT_DIR)/target
	rm -rf $(DBT_DIR)/logs
	@echo "Generated files removed."
