import asyncio
import os
import pytest
from fastapi.testclient import TestClient

# Ensure test uses a valid API key config
os.environ["API_KEYS"] = "test"

# Import app after setting environment variables
from src.api.app import app

client = TestClient(app)

def test_combined_calendar_ssrf():
    # Attempt to access a loopback address using SSRF
    response = client.get("/api/v1/combined_calendar?ics_url=http://127.0.0.1:8000/", headers={"X-API-Key": "test"})
    assert response.status_code == 400
    assert "Invalid or unreachable URL provided" in response.json()["detail"]

    # Attempt to access an invalid URL via SSRF
    response = client.get("/api/v1/combined_calendar?ics_url=http://192.168.1.1/", headers={"X-API-Key": "test"})
    assert response.status_code == 400
    assert "Invalid or unreachable URL provided" in response.json()["detail"]


def test_combined_calendar_invalid_scheme():
    # Attempt to access a non-http/https URL
    response = client.get("/api/v1/combined_calendar?ics_url=file:///etc/passwd", headers={"X-API-Key": "test"})
    assert response.status_code == 400
    assert "Invalid URL scheme" in response.json()["detail"]

def test_combined_calendar_no_api_key():
    response = client.get("/api/v1/combined_calendar?ics_url=http://example.com/cal.ics")
    assert response.status_code == 401
