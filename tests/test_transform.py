import pandas as pd

from etl.transform import transform_dataframe


def test_total_column_created():
    df = pd.DataFrame({
        "order_id": [1],
        "order_date": ["2026-07-01"],
        "customer": ["Alice"],
        "product": ["Laptop"],
        "category": ["Electronics"],
        "quantity": [2],
        "price": [100],
    })

    result = transform_dataframe(df)

    assert "total" in result.columns
    assert result.loc[0, "total"] == 200
