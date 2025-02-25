import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_get_integration_json():
    response = client.get("/integration.json")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["integration_type"] == "interval"
    assert "tick_url" in data["data"]

def test_monitor_tick_with_mocked_return_url(monkeypatch):
    mock_post = lambda url, json: None
    monkeypatch.setattr("httpx.AsyncClient.post", mock_post)

    payload = {
        "channel_id": "test-channel",
        "return_url": "https://mock.telex.im/v1/return/test-channel",
        "settings": [
            {
                "label": "tracked_packages",
                "type": "json",
                "required": True,
                "default": "{\"pip\": [\"requests\"], \"npm\": [\"react\"], \"cargo\": []}"
            }
        ]
    }

    response = client.post("/tick", json=payload)
    assert response.status_code == 200
