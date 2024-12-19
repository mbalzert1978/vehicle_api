from collections.abc import Generator, Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Connection, Engine, StaticPool, create_engine

from app.database import get_connection, metadata
from app.main import app
from app.vehicles.services import insert_vehicle
from tests.data import I30, Q7


@pytest.fixture()
def example_data(connection: Connection) -> None:
    insert_vehicle(connection, Q7)
    insert_vehicle(connection, I30)


@pytest.fixture()
def db_engine() -> Engine:
    return create_engine(
        "sqlite:///:memory:",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


@pytest.fixture()
def connection(db_engine: Engine) -> Generator[Connection, None]:
    with db_engine.begin() as conn:
        metadata.drop_all(bind=conn)
        metadata.create_all(bind=conn)
        yield conn
        conn.close()
        db_engine.dispose()


@pytest.fixture()
def client(connection: Connection) -> Iterator[TestClient]:
    app.dependency_overrides[get_connection] = lambda: connection
    with TestClient(app) as c:
        yield c
