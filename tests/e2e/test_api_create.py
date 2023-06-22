import pytest
from fastapi.testclient import TestClient


def test_happy_path_create(client: TestClient):
    client.get("/vehicle")

    assert client.get("/vehicle").status_code == 200
