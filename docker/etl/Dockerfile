FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv \
    && uv sync --frozen --no-dev

COPY etl ./etl
COPY sql ./sql
COPY data ./data

CMD ["/app/.venv/bin/python", "-m", "etl.pipeline"]
