from fastapi.testclient import TestClient
from src.api.app import app, verify_api_key, API_VERSION, YEAR_MIN, YEAR_MAX

client = TestClient(app)

def test_api_status_success():
    # Mock the verify_api_key dependency
    app.dependency_overrides[verify_api_key] = lambda: "test-api-key"

    response = client.get("/api/v1/status")

    # Assert successful response
    assert response.status_code == 200

    # Assert response structure and content
    data = response.json()
    assert data["status"] == "ok"
    assert data["api_version"] == API_VERSION
    assert data["API_Key_Validation"] == "successful"
    assert "timestamp" in data
    assert "redis_connected" in data
    assert data["data_store_year_min"] == YEAR_MIN
    assert data["data_store_year_max"] == YEAR_MAX
    assert "message" in data

    # Clear dependency override
    app.dependency_overrides.clear()

def test_api_status_missing_api_key():
    # Make request without mocking verify_api_key and without sending key
    response = client.get("/api/v1/status")

    # Assert unauthorized response
    assert response.status_code == 401
    assert response.json()["detail"] == "Missing API key. Use 'X-API-Key' header with a valid key."

def test_api_status_invalid_api_key():
    # Make request with an invalid key
    response = client.get("/api/v1/status", headers={"X-API-Key": "invalid-key"})

    # Assert unauthorized response
    assert response.status_code == 401
    assert response.json()["detail"] == "No valid API keys configured. Please contact the admin."
