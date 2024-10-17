from unittest.mock import MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncConnection

from vehicle_api.health import services


@pytest.mark.asyncio
async def test_health_execute() -> None:
    async_conn = MagicMock(spec=AsyncConnection)

    await services.get_database_status(async_conn)

    assert async_conn.execute.called
    assert async_conn.execute.return_value.one.called
