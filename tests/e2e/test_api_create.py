import json

from fastapi import status
from fastapi.testclient import TestClient

from tests.data import BODY, PARAMS, UPDATE


def test_CRUD_happy_path(client: TestClient):
    # Create a new vehicle
    create = client.post("/vehicle", content=json.dumps(BODY), params=PARAMS)
    assert create.status_code == status.HTTP_200_OK

    # Retrieve vehicles
    get = client.get("/vehicle")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 1
    assert isinstance(get.json(), list)

    # Retrieve specific vehicle
    get = client.get("/vehicle/1")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == {
        **PARAMS,
        "body": BODY,
        "id": create.json()["id"],
    }

    # Update vehicle
    update = client.put("/vehicle/1", content=json.dumps(UPDATE))
    assert update.status_code == status.HTTP_200_OK
    assert update.json() == {**UPDATE, "id": 1}

    # Delete vehicle
    delete = client.delete("/vehicle/1")
    assert delete.status_code == status.HTTP_204_NO_CONTENT
