#!/usr/bin/env bash

set -euo pipefail

echo "Starting Airflow initialization..."

echo "Running metadata database migrations..."
airflow db migrate

echo "Airflow initialization completed successfully."
echo "The Simple Auth Manager user will be initialized by the API server."
