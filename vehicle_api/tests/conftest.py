from collections.abc import Iterator
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from presentation.database import get_connection, metadata
from presentation.main import app
from presentation.vehicles.services import insert_vehicle
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine
from tests.data import I30, Q7


@pytest.fixture()
async def example_data(connection: AsyncConnection) -> None:
    await insert_vehicle(connection, Q7)
    await insert_vehicle(connection, I30)


@pytest.fixture()
def db_engine() -> AsyncEngine:
    return create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


@pytest.fixture()
async def connection(db_engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    async with db_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
        yield conn
        await conn.close()
        await db_engine.dispose()


@pytest.fixture()
def client(connection: AsyncConnection) -> Iterator[TestClient]:
    app.dependency_overrides[get_connection] = lambda: connection
    with TestClient(app) as c:
        yield c
