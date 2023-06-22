import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.crud.base import CRUDBase
from src.main import app
from src.model.vehicle import Base, Vehicle
from src.schemas.vehicle import VehicleCreate, VehicleData

I30 = VehicleCreate(
    name="I30",
    year_of_manufacture=2017,
    body=VehicleData(
        color="black",
        kilometer=10000,
        price=15000,
        vehicle_type="limusine",
    ),
    ready_to_drive=True,
)
Q7 = VehicleCreate(
    name="Q7",
    year_of_manufacture=2020,
    body=VehicleData(
        color="red",
        kilometer=100_000,
        price=75_000,
        vehicle_type="suv",
    ),
    ready_to_drive=True,
)


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


def setup_database(session: Session) -> None:
    CRUDBase(Vehicle).create(session, to_create=I30)
    CRUDBase(Vehicle).create(session, to_create=Q7)


@pytest.fixture(scope="module")
def db(session: Session):
    setup_database(session)
    yield session


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
