import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.model.vehicle import Vehicle
from src.schemas.vehicle import VehicleUpdate

DATA = {
    "color": "black",
    "kilometer": 10000,
    "price": 15000,
    "vehicle_type": "limusine",
}
UPDATE_DATA = {
    "color": "white",
    "kilometer": 125_000,
    "price": 20_000,
    "vehicle_type": "convertible",
}


def test_create_vehicle(session: Session) -> None:
    """
    Given: A database session
    When: Creating a new vehicle
    Then: The vehicle should be added to the database
    """
    expected = {
        "name": "expected",
        "year_of_manufacture": 2022,
        "body": DATA,
        "ready_to_drive": True,
    }

    vehicle = Vehicle(**expected)
    session.add(vehicle)
    session.commit()

    result = session.execute(
        select(Vehicle).filter_by(name="expected"),
    ).scalar_one()

    assert result.name == expected["name"]
    assert result.year_of_manufacture == expected["year_of_manufacture"]
    assert result.body == expected["body"]
    assert result.ready_to_drive is expected["ready_to_drive"]


@pytest.mark.usefixtures("example_data")
def test_read_vehicle(session: Session) -> None:
    """
    Given: A database session with a vehicle
    When: Reading the vehicle from the database
    Then: The vehicle data should match the expected values
    """
    expected = session.execute(select(Vehicle)).scalars().first()

    assert expected is not None
    assert expected.id
    assert expected.name == "I30"
    assert expected.year_of_manufacture == 2017
    assert expected.body == DATA
    assert expected.ready_to_drive


@pytest.mark.usefixtures("example_data")
def test_update_vehicle(session: Session) -> None:
    """
    Given: A database session with a vehicle
    When: Updating the vehicle data
    Then: The vehicle data should be updated in the database
    """
    to_update = session.execute(select(Vehicle)).scalars().first()

    serialized = jsonable_encoder(to_update)

    update = VehicleUpdate(
        name="Car3 Updated",
        year_of_manufacture=2025,
        body=UPDATE_DATA,
        ready_to_drive=False,
    ).dict(exclude_unset=True)

    for field in serialized:
        if field not in update:
            continue
        setattr(to_update, field, update[field])

    session.add(to_update)
    session.commit()
    session.refresh(to_update)

    assert to_update.name == "Car3 Updated"
    assert to_update.year_of_manufacture == 2025
    assert to_update.body == UPDATE_DATA
    assert to_update.ready_to_drive is False
