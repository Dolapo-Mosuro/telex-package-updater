from fastapi.testclient import TestClient
from app.main import app
import os
import pytest

client = TestClient(app)
os.environ["TELEX_API_KEY"] = "test-key-123"  # Fixed var name

def test_unauthorized_access():
	response = client.get("/check/pip/requests")
	assert response.status_code == 403

def test_valid_check():
	api_key = os.getenv("TELEX_API_KEY", "test-key-123")  # Use the correct API key
	response = client.get(
		"/check/pip/requests",
		headers={"X-API-Key": "test-key-123"}  # Correct header
	)
	assert response.status_code == 200
	assert "current" in response.json()
