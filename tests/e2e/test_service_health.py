from fastapi.testclient import TestClient

from src.schemas.status import DatabaseStatus


def test_service_health_happy_path(client: TestClient):
    # Test service health
    result = client.get("/api/service")
    assert result.json() == DatabaseStatus().model_dump()
