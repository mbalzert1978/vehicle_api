import datetime

import pytest
from pydantic import ValidationError

from src.model.model import (
    Address,
    Brand,
    Color,
    Owner,
    Vehicle,
    VehicleCreate,
    VehicleUpdate,
)
from src.model.orm import TransportMode


def test_create_vehicle() -> None:
    """
    Given: A set of vehicle data
    When: Creating a new vehicle object
    Then: The vehicle object should be created successfully with the provided data
    """
    vehicle_data = {
        "model": "Camry",
        "year": datetime.datetime(2022, 1, 1),
        "transportation_modes": [
            {"transportation_mode_id": 1, "name": TransportMode.LAND},
            {"transportation_mode_id": 2, "name": TransportMode.AIR},
        ],
        "brand": {"brand_id": 1, "name": "Toyota"},
        "color": {"color_id": 1, "name": "Red"},
    }

    address_data = {
        "address_id": 1,
        "street": "123 Main St",
        "city": "City",
        "state": "State",
        "zip_code": "12345",
    }

    address = Address(**address_data)
    owner = Owner(name="John Doe", phone="1234567890", address=address)
    vehicle = Vehicle(**vehicle_data, owner=owner)

    assert vehicle.model == "Camry"
    assert vehicle.year == datetime.datetime(2022, 1, 1)
    assert len(vehicle.transportation_modes) == 2
    assert isinstance(vehicle.brand, Brand)
    assert isinstance(vehicle.color, Color)
    assert isinstance(vehicle.owner, Owner)
    assert vehicle.owner.address == address


def test_create_vehicle_invalid_data() -> None:
    """
    Given: A set of invalid vehicle data
    When: Creating a new vehicle object with the invalid data
    Then: A validation error should be raised
    """

    vehicle_data = {
        "model": "Camry",
        "year": "2022-01-01",
        "brand": {"brand_id": 1, "name": "Toyota"},
        "color": {"color_id": 1, "name": "Red"},
    }

    with pytest.raises(ValidationError):
        Vehicle(**vehicle_data)


def test_create_vehicle_create_model() -> None:
    """
    Given: A set of vehicle data for creation
    When: Creating a new vehicle using the create model
    Then: The vehicle create model should be populated correctly
    """

    vehicle_data = {
        "model": "Camry",
        "year": datetime.datetime(2022, 1, 1),
        "brand_id": 1,
        "color_id": 1,
    }

    vehicle = VehicleCreate(**vehicle_data)

    assert vehicle.model == "Camry"
    assert vehicle.year == datetime.datetime(2022, 1, 1)
    assert vehicle.transportation_modes == [TransportMode.LAND]
    assert vehicle.brand_id == 1
    assert vehicle.color_id == 1
    assert vehicle.owner_id is None


def test_create_vehicle_update_model() -> None:
    """
    Given: A set of vehicle data for creation
    When: Creating a new vehicle using the create model
    Then: The vehicle create model should be populated correctly
    """

    vehicle_data = {
        "model": "Camry",
        "year": datetime.datetime(2022, 1, 1),
        "brand_id": 1,
        "color_id": 1,
    }

    vehicle = VehicleUpdate(**vehicle_data)

    assert vehicle.model == "Camry"
    assert vehicle.year == datetime.datetime(2022, 1, 1)
    assert vehicle.transportation_modes == [TransportMode.LAND]
    assert vehicle.brand_id == 1
    assert vehicle.color_id == 1
    assert vehicle.owner_id is None


def test_create_vehicle_create_model_invalid_data() -> None:
    """
    Given: A set of invalid vehicle data for creation
    When: Creating a new vehicle using the create model with the invalid data
    Then: A validation error should be raised
    """

    vehicle_data = {
        "model": "Camry",
        "year": "2022-01-01",
        "brand_id": 1,
        "color_id": 1,
    }

    with pytest.raises(ValidationError):
        VehicleCreate(**vehicle_data)
