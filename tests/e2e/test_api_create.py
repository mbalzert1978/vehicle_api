import json

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from tests.data import PARAMS, UPDATE


def is_expected(vehicle: dict, expected: dict) -> None:
    match vehicle:
        case {
            "name": "test_vehicle",
            "manufacturing_year": 2020,
            "is_drivable": False,
            "id": _,
            "body": body,
            "created_at": created_at,
            "updated_at": updated_at,
        }:
            assert body == expected["body"]
            assert created_at
            assert updated_at is None
        case {
            "name": "updated_vehicle",
            "manufacturing_year": 2010,
            "is_drivable": True,
            "body": body,
            "created_at": created_at,
            "updated_at": updated_at,
        }:
            assert body == expected["body"]
            assert created_at
            assert updated_at
        case _:
            pytest.fail(f"Unexpected vehicle: {vehicle}")


def test_crud_happy_path(client: TestClient) -> None:
    # Create a new vehicle
    create = client.post("/api/v1/vehicles", content=json.dumps(PARAMS))
    id_ = create.json()["data"]["id"]

    assert create.status_code == status.HTTP_201_CREATED

    # Retrieve vehicles
    all_vehicle = client.get("/api/v1/vehicles")

    assert all_vehicle.status_code == status.HTTP_200_OK

    [expected] = all_vehicle.json()["data"]
    is_expected(expected, PARAMS)

    # filter vehicles
    filtered = client.get("/api/v1/vehicles/?name=test_vehicle")

    assert filtered.status_code == status.HTTP_200_OK

    [expected] = all_vehicle.json()["data"]
    is_expected(expected, PARAMS)

    # Retrieve specific vehicle
    specific = client.get(f"/api/v1/vehicles/{id_}")

    assert specific.status_code == status.HTTP_200_OK

    expected = specific.json()["data"]

    is_expected(expected, PARAMS)

    # Update vehicle
    result = client.put(f"/api/v1/vehicles/{id_}", content=json.dumps(UPDATE))

    assert result.status_code == status.HTTP_204_NO_CONTENT

    # Retrieve updated vehicle
    all_vehicle = client.get("/api/v1/vehicles")

    assert all_vehicle.status_code == status.HTTP_200_OK

    [expected] = all_vehicle.json()["data"]
    is_expected(expected, UPDATE)

    # Delete vehicle
    delete = client.delete(f"/api/v1/vehicles/{id_}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT
