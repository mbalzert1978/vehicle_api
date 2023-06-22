import json

import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.model.vehicle import Vehicle
from src.schemas.vehicle import VehicleData, VehicleUpdate

DATA = {
    "color": "black",
    "kilometer": 10000,
    "price": 15000,
    "vehicle_type": "limusine",
}


def test_create_vehicle(session: Session) -> None:
    """
    Given: A database session
    When: Creating a new vehicle
    Then: The vehicle should be added to the database
    """
    expected = {
        "name": "Car1",
        "year_of_manufacture": 2022,
        "body": json.dumps(DATA),
        "ready_to_drive": True,
    }

    vehicle = Vehicle(**expected)
    session.add(vehicle)
    session.commit()

    if not (result := session.query(Vehicle).get(vehicle.id)):
        pytest.fail("Vehicle not added to database")

    assert result.name == expected["name"]
    assert result.year_of_manufacture == expected["year_of_manufacture"]
    assert result.body == expected["body"]
    assert result.ready_to_drive is expected["ready_to_drive"]


def test_read_vehicle(db: Session) -> None:
    """
    Given: A database session with a vehicle
    When: Reading the vehicle from the database
    Then: The vehicle data should match the expected values
    """
    if not (expected := db.query(Vehicle).first()):
        pytest.fail("No vehicle in database.")

    assert expected is not None
    assert expected.id == 1
    assert expected.name == "I30"
    assert expected.year_of_manufacture == 2017
    assert expected.body == DATA
    assert expected.ready_to_drive


def test_update_vehicle(db: Session) -> None:
    """
    Given: A database session with a vehicle
    When: Updating the vehicle data
    Then: The vehicle data should be updated in the database
    """
    if not (to_update := db.query(Vehicle).first()):
        pytest.fail("No vehicle in database.")

    serialized = jsonable_encoder(to_update)

    update = VehicleUpdate(
        name="Car3 Updated",
        year_of_manufacture=2025,
        body=VehicleData(
            color="white",
            kilometer=125_000,
            price=20_000,
            vehicle_type="convertible",
        ),
        ready_to_drive=False,
    ).dict(exclude_unset=True)

    for field in serialized:
        if field not in update:
            continue
        setattr(to_update, field, update[field])

    db.add(to_update)
    db.commit()
    db.refresh(to_update)

    assert to_update.name == "Car3 Updated"
    assert to_update.year_of_manufacture == 2025
    assert to_update.body == VehicleData(
        color="white",
        kilometer=125_000,
        price=20_000,
        vehicle_type="convertible",
    )
    assert to_update.ready_to_drive is False
