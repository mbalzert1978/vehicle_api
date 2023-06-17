import datetime

from sqlalchemy.orm import Session

from src.model.orm import (
    Brand,
    Color,
    TransportationMode,
    TransportMode,
    Vehicle,
)


def test_create_vehicle(session: Session) -> None:
    """
    Given: A database session with pre-existing test data
    When: Creating a new vehicle
    Then: The vehicle should be added to the database
    """
    brand = session.query(Brand).first()
    color = session.query(Color).first()
    vehicle = Vehicle(
        model="I30",
        year=datetime.datetime(1999, 1, 1),
        brand=brand,
        color=color,
    )
    vehicle.transportation_modes.append(
        TransportationMode(name=TransportMode.LAND),
    )
    session.add(vehicle)
    session.commit()

    created_vehicle = session.query(Vehicle).filter_by(model="I30").first()
    assert created_vehicle is not None
    assert created_vehicle.model == "I30"
    assert created_vehicle.year == datetime.datetime(1999, 1, 1)
    assert created_vehicle.brand == brand
    assert created_vehicle.color == color


def test_read_vehicle(session: Session) -> None:
    """
    Given: A database session with pre-existing test data
    When: Reading a vehicle
    Then: The vehicle should be retrieved from the database
    """

    vehicle = session.query(Vehicle).all()

    assert vehicle is not None


def test_update_vehicle(session: Session) -> None:
    """
    Given: A database session with pre-existing test data
    When: Updating a vehicle's model
    Then: The vehicle's model should be successfully updated in the database
    """
    vehicle = session.query(Vehicle).filter_by(vehicle_id=1).first()
    vehicle.model = "Corolla"
    session.commit()
    updated_vehicle = session.query(Vehicle).filter_by(vehicle_id=1).first()
    assert updated_vehicle.model == "Corolla"


def test_delete_vehicle(session: Session) -> None:
    """
    Given: A database session with pre-existing test data
    When: Deleting a vehicle
    Then: The vehicle should be successfully deleted from the database
    """
    vehicle = session.query(Vehicle).filter_by(vehicle_id=1).first()
    session.delete(vehicle)
    session.commit()

    assert session.query(Vehicle).filter_by(vehicle_id=1).first() is None
