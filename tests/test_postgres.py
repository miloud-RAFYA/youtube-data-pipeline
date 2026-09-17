from src.database.postgres import get_connection


def test_postgres_connection():
    connection = get_connection()

    assert connection is not None

    connection.close()