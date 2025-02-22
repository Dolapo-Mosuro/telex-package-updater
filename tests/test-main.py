from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)
os.environ["API_KEY"] = "test_key"

def test_unauthorized_access():
    response = client.post("/check-updates")
    assert response.status_code == 401

def test_authorized_access():
    response = client.post(
        "/check-updates",
        headers={"x-api-key": "test_key"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)