from collections.abc import Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.api.dependencies import get_session
from src.crud.base import CRUDBase
from src.main import app
from src.model.vehicle import Base, Vehicle
from src.schemas.vehicle import VehicleCreate

I30 = VehicleCreate(
    name="I30",
    year_of_manufacture=2017,
    body={
        "color": "black",
        "kilometer": 10000,
        "price": 15000,
        "vehicle_type": "limusine",
    },
    ready_to_drive=True,
)
Q7 = VehicleCreate(
    name="Q7",
    year_of_manufacture=2020,
    body={
        "color": "red",
        "kilometer": 100_000,
        "price": 75_000,
        "vehicle_type": "suv",
    },
    ready_to_drive=True,
)


@pytest.fixture()
def example_data(session: Session) -> None:
    CRUDBase(Vehicle).create(session, to_create=I30)  # type: ignore[arg-type]
    CRUDBase(Vehicle).create(session, to_create=Q7)  # type: ignore[arg-type]


@pytest.fixture()
def db_engine() -> Generator[Engine, Any, None]:
    engine = create_engine(
        "sqlite:///:memory:",
        echo=True,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
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
    app.dependency_overrides[get_session] = lambda: session
    with TestClient(app) as c:
        yield c
