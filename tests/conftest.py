from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from tests.data import I30, Q7
from vehicle_api.api.dependecies.database import get_session
from vehicle_api.crud.sqlalchemy_repo import SQLAlchemyRepository
from vehicle_api.main import app
from vehicle_api.model.sql_alchemy import mapper_registry
from vehicle_api.model.vehicle import Vehicle


@pytest.fixture()
def example_data(session: Session) -> None:
    SQLAlchemyRepository(session, Vehicle).create(to_create=I30)
    SQLAlchemyRepository(session, Vehicle).create(to_create=Q7)


@pytest.fixture()
def db_engine() -> Iterator[Engine]:
    engine = create_engine(
        "sqlite:///:memory:",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    mapper_registry.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture()
def session(db_engine) -> Iterator[Session]:
    Session = sessionmaker(bind=db_engine)  # noqa: N806
    session = Session()
    yield session
    session.close()


@pytest.fixture()
def client(session) -> Iterator[TestClient]:
    app.dependency_overrides[get_session] = lambda: session
    with TestClient(app) as c:
        yield c
