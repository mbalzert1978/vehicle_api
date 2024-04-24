from collections.abc import Iterator
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from src.database import get_connection
from src.main import app
from src.vehicles.database import metadata
from tests.data import I30, Q7


@pytest.fixture()
def example_data(connection: AsyncConnection) -> None:
    pass


@pytest.fixture()
def db_engine() -> Iterator[AsyncEngine]:
    engine = create_async_engine(
        "sqlite:///:memory:",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture()
async def connection(db_engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    async with db_engine.begin() as conn:
        yield conn
        await conn.close()


@pytest.fixture()
def client(connection: AsyncConnection) -> Iterator[TestClient]:
    app.dependency_overrides[get_connection] = lambda: connection
    with TestClient(app) as c:
        yield c
