from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_agent_chat_reasoning_and_capabilities():
    response = client.post(
        "/api/v1/agent/chat",
        json={"message": "Hello, what features can you provide for our enterprise data?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "reasoning"
    assert "reply" in data
    assert "DataMind AI" in data["reply"]
    assert data["latency_ms"] >= 0


def test_agent_chat_dispatches_sql_query():
    response = client.post(
        "/api/v1/agent/chat",
        json={"message": "SELECT 123 AS user_count, 'Active' AS status;"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "sql"
    assert data["tool_used"] == "safe_sql_engine"
    assert data["tool_output"] is not None
    assert data["tool_output"]["row_count"] == 1
    assert "user_count" in data["tool_output"]["columns"]


def test_agent_chat_dispatches_analytics_guidance():
    response = client.post(
        "/api/v1/agent/chat",
        json={"message": "How do you profile a dataset and clean null values?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "analytics"
    assert data["tool_used"] == "data_analytics_pipeline"
    assert "Analytics" in data["reply"]
