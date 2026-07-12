import duckdb
import pandas as pd

from etl.load import load_dataframe_to_duckdb


def test_load_dataframe_to_duckdb():
    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["Alice", "Bob"],
        }
    )

    connection = duckdb.connect(":memory:")

    load_dataframe_to_duckdb(
        connection=connection,
        table_name="users",
        dataframe=dataframe,
    )

    result = connection.execute("SELECT id, name FROM users ORDER BY id").fetchall()

    connection.close()

    assert result == [
        (1, "Alice"),
        (2, "Bob"),
    ]
