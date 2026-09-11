from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_sql_schema_endpoint():
    response = client.get("/api/v1/sql/schema")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_sql_safe_query_execution():
    response = client.post(
        "/api/v1/sql/query",
        json={"query_text": "SELECT 100 AS number, 'DataMind' AS name;"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["row_count"] == 1
    assert data["columns"] == ["number", "name"]
    assert data["results"][0]["number"] == 100
    assert data["results"][0]["name"] == "DataMind"


def test_sql_forbidden_operation_blocked():
    response = client.post(
        "/api/v1/sql/query",
        json={"query_text": "DROP TABLE users;"}
    )
    assert response.status_code == 400
    assert "Security Exception" in response.json()["detail"]
