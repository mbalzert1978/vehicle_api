from fastapi.testclient import TestClient


def test_service_health_happy_path(client: TestClient) -> None:
    # Test service health
    result = client.get("/api/v1/health")
    assert result.json() == {"status": "OK"}
