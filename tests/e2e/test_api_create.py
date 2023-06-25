import pytest
from fastapi.testclient import TestClient


@pytest.mark.usefixtures("example_data")
def test_happy_path_create(client: TestClient):
    client.get("/vehicle")

    result = client.get("/vehicle")

    assert result.status_code == 200
