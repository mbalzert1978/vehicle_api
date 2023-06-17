import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.model.orm import (
    Address,
    Base,
    Brand,
    Color,
    Owner,
    TransportationMode,
    TransportMode,
    Vehicle,
)


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


def setup_database(session):
    brand = Brand(brand_id=1, name="Toyota")
    color = Color(color_id=1, name="Red")
    trans_mode = TransportationMode(name=TransportMode.LAND)
    address = Address(
        address_id=1,
        street="123 Main St",
        city="City",
        state="State",
        zip_code="12345",
    )
    owner = Owner(owner_id=1, name="John Doe", phone="1234567890")
    owner.address.append(address)
    vehicle = Vehicle(
        vehicle_id=1,
        model="Camry",
        year=datetime.datetime(2022, 1, 1),
        brand_id=brand.brand_id,
        color_id=color.color_id,
        owner_id=owner.owner_id,
    )
    vehicle.transportation_modes.append(trans_mode)

    session.add(brand)
    session.add(color)
    session.add(trans_mode)
    session.add(address)
    session.add(owner)
    session.add(vehicle)
    session.commit()


@pytest.fixture(scope="module")
def session(db_session):
    setup_database(db_session)
    yield db_session
