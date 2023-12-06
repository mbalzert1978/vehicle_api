from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.api.dependecies.database import get_session
from src.crud.sqlalchemy_repo import SQLAlchemyRepository
from src.main import app
from src.model.sql_alchemy import mapper_registry
from src.model.vehicle import Vehicle
from tests.data import I30, Q7


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
