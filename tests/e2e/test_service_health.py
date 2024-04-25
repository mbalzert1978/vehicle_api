from fastapi.testclient import TestClient


def test_service_health_happy_path(client: TestClient):
    # Test service health
    result = client.get("/api/v1/health")
    assert result.json() == {"status": "OK"}
