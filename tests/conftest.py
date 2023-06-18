import json

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.crud.base import CRUDBase
from src.model.base import Base
from src.model.vehicle import Vehicle
from src.schemas.vehicle import VehicleCreate

I30 = VehicleCreate(
    name="I30",
    year_of_manufacture=2017,
    body=json.dumps(
        {
            "color": "black",
            "mileage": 10000,
            "price": 15000,
            "type": "limusine",
        },
    ),
    ready_to_drive=True,
)
Q7 = VehicleCreate(
    name="Q7",
    year_of_manufacture=2020,
    body=json.dumps(
        {
            "color": "red",
            "kilometer": 100,
            "price": 75000,
            "type": "suv",
        },
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
