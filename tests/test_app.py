import pytest
from fastapi.testclient import TestClient
from src.api.app import app
from src.api.app import verify_api_key

client = TestClient(app)

@pytest.fixture
def override_api_key():
    app.dependency_overrides[verify_api_key] = lambda: "dummy_key"
    yield
    app.dependency_overrides.clear()

def test_api_status_unauthorized():
    response = client.get("/api/v1/status")
    assert response.status_code == 401

def test_api_status_authorized(override_api_key):
    response = client.get("/api/v1/status")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "api_version" in data
    assert data["API_Key_Validation"] == "successful"
    assert "timestamp" in data
    assert "redis_connected" in data
    assert "data_store_year_min" in data
    assert "data_store_year_max" in data
    assert data["message"] == "The Sri Lanka Holidays API is operational and running smoothly."
