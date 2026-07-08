import pandas as pd
import pytest

from etl.transform import transform_dataframe


def valid_sales_df():
    return pd.DataFrame({
        "order_id": [1],
        "order_date": ["2026-07-01"],
        "customer": ["Alice"],
        "product": ["Laptop"],
        "category": ["Electronics"],
        "quantity": [2],
        "price": [100],
    })


def test_negative_price_raises_error():
    df = valid_sales_df()
    df.loc[0, "price"] = -100

    with pytest.raises(ValueError, match="Price must be greater than 0"):
        transform_dataframe(df)


def test_zero_quantity_raises_error():
    df = valid_sales_df()
    df.loc[0, "quantity"] = 0

    with pytest.raises(ValueError, match="Quantity must be greater than 0"):
        transform_dataframe(df)


def test_missing_column_raises_error():
    df = valid_sales_df().drop(columns=["customer"])

    with pytest.raises(ValueError, match="Missing columns"):
        transform_dataframe(df)


def test_duplicate_order_id_raises_error():
    df = pd.concat([valid_sales_df(), valid_sales_df()], ignore_index=True)

    with pytest.raises(ValueError, match="Duplicate order_id"):
        transform_dataframe(df)
