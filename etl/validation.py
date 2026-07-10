from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "customer",
    "product",
    "category",
    "quantity",
    "price",
]


def validate_file_exists(file_path: Path) -> None:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.stat().st_size == 0:
        raise ValueError(f"File is empty: {file_path}")


def validate_columns(df: pd.DataFrame) -> None:
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")


def validate_nulls(df: pd.DataFrame) -> None:
    null_counts = df[REQUIRED_COLUMNS].isna().sum()
    columns_with_nulls = null_counts[null_counts > 0]

    if not columns_with_nulls.empty:
        raise ValueError(f"Null values found: {columns_with_nulls.to_dict()}")


def validate_positive_numbers(df: pd.DataFrame) -> None:
    invalid_quantity = df[df["quantity"] <= 0]
    invalid_price = df[df["price"] <= 0]

    if not invalid_quantity.empty:
        raise ValueError("Quantity must be greater than 0")

    if not invalid_price.empty:
        raise ValueError("Price must be greater than 0")


def validate_duplicates(df: pd.DataFrame) -> None:
    duplicated_orders = df[df["order_id"].duplicated()]

    if not duplicated_orders.empty:
        raise ValueError("Duplicate order_id values found")


def validate_sales_data(df: pd.DataFrame) -> None:
    validate_columns(df)
    validate_nulls(df)
    validate_positive_numbers(df)
    validate_duplicates(df)
