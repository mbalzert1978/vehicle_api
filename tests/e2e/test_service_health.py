from fastapi import status
from fastapi.testclient import TestClient


def test_service_health_happy_path(client: TestClient):
    # Test service health
    result = client.get("/service")
    assert result.status_code == status.HTTP_200_OK
