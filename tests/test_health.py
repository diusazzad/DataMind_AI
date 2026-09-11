from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home_portal_loads_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "DataMind AI" in response.text
    assert "API Online" in response.text


def test_api_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert data["app_name"] == "DataMind AI"
    assert data["version"] == "1.0.0"
    assert "database_connected" in data
