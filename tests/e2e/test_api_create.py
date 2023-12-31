import json

from fastapi import status
from fastapi.testclient import TestClient

from tests.data import BODY, PARAMS, UPDATE


def test_CRUD_happy_path(client: TestClient):
    # Create a new vehicle
    create = client.post("/api/vehicle", content=json.dumps(PARAMS))
    assert create.status_code == status.HTTP_200_OK

    # Retrieve vehicles
    get = client.get("/api/vehicle")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 1
    assert isinstance(get.json(), list)

    # filter vehicles
    filtered = client.get("/api/vehicle/?name=test_vehicle")
    assert filtered.status_code == status.HTTP_200_OK
    assert len(filtered.json()) == 1

    # Retrieve specific vehicle
    get = client.get("/api/vehicle/1")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == {
        **PARAMS,
        "body": BODY,
        "id": create.json()["id"],
    }

    # Update vehicle
    update = client.put("/api/vehicle/1", content=json.dumps(UPDATE))
    assert update.status_code == status.HTTP_200_OK
    assert update.json() == {**UPDATE, "id": 1}

    # Delete vehicle
    delete = client.delete("/api/vehicle/1")
    assert delete.status_code == status.HTTP_204_NO_CONTENT
