from unittest.mock import MagicMock

from sqlalchemy import Connection

from app.health import services


def test_health_execute() -> None:
    connection = MagicMock(spec=Connection)

    services.get_database_status(connection)

    assert connection.execute.called
