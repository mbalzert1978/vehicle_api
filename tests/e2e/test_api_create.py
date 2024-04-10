import json

from fastapi import status
from fastapi.testclient import TestClient

from tests.data import BODY, PARAMS, UPDATE


def test_CRUD_happy_path(client: TestClient):
    expected = {**PARAMS, "id": 1}
    updated = {**UPDATE, "id": 1}

    # Create a new vehicle
    create = client.post("/api/vehicles", content=json.dumps(PARAMS))
    assert create.status_code == status.HTTP_200_OK

    # Retrieve vehicles
    get = client.get("/api/vehicles")

    assert create.status_code == status.HTTP_200_OK
    assert expected == get.json()["data"].pop()

    # filter vehicles
    filtered = client.get("/api/vehicles/?name=test_vehicle")

    assert create.status_code == status.HTTP_200_OK
    assert expected == filtered.json()["data"].pop()

    # Retrieve specific vehicle
    specific = client.get("/api/vehicles/1")

    assert create.status_code == status.HTTP_200_OK
    assert expected == specific.json()["data"]

    # Update vehicle
    update = client.put("/api/vehicles/1", content=json.dumps(UPDATE))

    assert update.status_code == status.HTTP_200_OK
    assert updated == update.json()["data"]

    # Delete vehicle
    delete = client.delete("/api/vehicles/1")
    assert delete.status_code == status.HTTP_204_NO_CONTENT
