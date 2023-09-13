from collections.abc import Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.api.dependencies import session_factory
from src.crud.repository import SQLAlchemyRepository
from src.main import app
from src.model.sql_alchemy import mapper_registry
from src.model.vehicle import Vehicle
from tests.data import I30, Q7


@pytest.fixture()
def example_data(session: Session) -> None:
    SQLAlchemyRepository(Vehicle).create(session, to_create=I30)  # type: ignore[arg-type]
    SQLAlchemyRepository(Vehicle).create(session, to_create=Q7)  # type: ignore[arg-type]


@pytest.fixture()
def db_engine() -> Generator[Engine, Any, None]:
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
def session(db_engine) -> Generator[Session, Any, None]:
    Session = sessionmaker(bind=db_engine)  # noqa: N806
    session = Session()
    yield session
    session.close()


@pytest.fixture()
def client(session) -> Generator[TestClient, Any, None]:
    app.dependency_overrides[session_factory] = lambda: session
    with TestClient(app) as c:
        yield c
