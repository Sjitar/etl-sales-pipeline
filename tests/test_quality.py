from unittest.mock import MagicMock

import pytest

from etl.quality import get_scalar


def test_get_scalar_returns_integer():
    cursor = MagicMock()
    cursor.fetchone.return_value = (10,)

    cursor_context = MagicMock()
    cursor_context.__enter__.return_value = cursor

    connection = MagicMock()
    connection.cursor.return_value = cursor_context

    result = get_scalar(
        connection,
        "SELECT COUNT(*) FROM users",
    )

    assert result == 10
    cursor.execute.assert_called_once_with("SELECT COUNT(*) FROM users")


def test_get_scalar_raises_when_query_returns_nothing():
    cursor = MagicMock()
    cursor.fetchone.return_value = None

    cursor_context = MagicMock()
    cursor_context.__enter__.return_value = cursor

    connection = MagicMock()
    connection.cursor.return_value = cursor_context

    with pytest.raises(ValueError, match="Query returned no result"):
        get_scalar(
            connection,
            "SELECT COUNT(*) FROM users",
        )
