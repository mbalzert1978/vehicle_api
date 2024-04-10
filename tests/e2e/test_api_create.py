import json

from fastapi import status
from fastapi.testclient import TestClient

from tests.data import PARAMS, UPDATE


def test_CRUD_happy_path(client: TestClient):
    expected = {**PARAMS, "id": 1}
    expected_after_update = {**UPDATE, "id": 1}

    # Create a new vehicle
    create = client.post("/api/vehicles", content=json.dumps(PARAMS))
    assert create.status_code == status.HTTP_201_CREATED

    # Retrieve vehicles
    updated = client.get("/api/vehicles")

    assert updated.status_code == status.HTTP_200_OK
    assert expected == updated.json()["data"].pop()

    # filter vehicles
    filtered = client.get("/api/vehicles/?name=test_vehicle")

    assert filtered.status_code == status.HTTP_200_OK
    assert expected == filtered.json()["data"].pop()

    # Retrieve specific vehicle
    specific = client.get("/api/vehicles/1")

    assert specific.status_code == status.HTTP_200_OK
    assert expected == specific.json()["data"]

    # Update vehicle
    result = client.put("/api/vehicles/1", content=json.dumps(UPDATE))

    assert result.status_code == status.HTTP_204_NO_CONTENT

    # Retrieve updated vehicle
    updated = client.get("/api/vehicles/1")

    assert expected_after_update == updated.json()["data"]

    # Delete vehicle
    delete = client.delete("/api/vehicles/1")
    assert delete.status_code == status.HTTP_204_NO_CONTENT
