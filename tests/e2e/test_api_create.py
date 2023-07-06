import json

from fastapi import status
from fastapi.testclient import TestClient

from tests.data import BODY, I30, PARAMS, Q7, UPDATE


def create_vehicle(client: TestClient, model: dict):
    body = model.pop("body")
    return client.post("/vehicle", content=json.dumps(body), params=model)


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


def test_CRUD_happy_filter(client: TestClient) -> None:
    # Create a vehicle
    result = create_vehicle(client, I30.dict())
    assert result.status_code == status.HTTP_200_OK

    # Create a vehicle
    result = create_vehicle(client, Q7.dict())
    assert result.status_code == status.HTTP_200_OK

    # filter vehicles by name
    result = client.post(
        "/vehicle/filter",
        content=json.dumps({"name": "I30"}),
    )

    i30 = next(iter(result.json()))

    assert result.status_code == status.HTTP_200_OK
    assert i30["id"]
    assert i30["name"] == I30.name
    assert i30["year_of_manufacture"] == I30.year_of_manufacture
    assert i30["body"] == I30.body


def test_CRUD_unhappy_filter_bad_request(client: TestClient) -> None:
    # Create a new vehicle
    result = create_vehicle(client, I30.dict())
    assert result.status_code == status.HTTP_200_OK

    # Create a new vehicle
    result = create_vehicle(client, Q7.dict())
    assert result.status_code == status.HTTP_200_OK

    # filter vehicles by nonsense
    result = client.post("/vehicle/filter", content=json.dumps({"foo": "bar"}))

    assert result.status_code == status.HTTP_400_BAD_REQUEST
