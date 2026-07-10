import pandas as pd

from etl.transform import transform_posts_dataframe, transform_users_dataframe


def test_transform_users_dataframe_keeps_expected_columns():
    df = pd.DataFrame(
        {
            "id": [1],
            "name": ["Leanne Graham"],
            "username": ["Bret"],
            "email": ["test@example.com"],
            "phone": ["123"],
            "website": ["example.com"],
        }
    )

    result = transform_users_dataframe(df)

    assert list(result.columns) == ["id", "name", "username", "email"]


def test_transform_posts_dataframe_renames_user_id_column():
    df = pd.DataFrame(
        {
            "id": [1],
            "userId": [10],
            "title": ["Post title"],
            "body": ["Post body"],
        }
    )

    result = transform_posts_dataframe(df)

    assert list(result.columns) == ["id", "user_id", "title", "body"]
    assert result.loc[0, "user_id"] == 10
