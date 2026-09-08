import pytest
from fastapi.testclient import TestClient
from src.api.app import app, verify_api_key
import socket
from unittest.mock import patch

client = TestClient(app)

# Override the verify_api_key dependency to always return a valid key
app.dependency_overrides[verify_api_key] = lambda: "test_key"

@pytest.fixture
def mock_dns_resolve():
    with patch("socket.gethostbyname") as mock:
        yield mock

def test_combined_calendar_local_ip_127(mock_dns_resolve):
    mock_dns_resolve.return_value = "127.0.0.1"
    response = client.get("/api/v1/combined_calendar?ics_url=http://example.com/test.ics")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid URL provided"

def test_combined_calendar_local_ip_192(mock_dns_resolve):
    mock_dns_resolve.return_value = "192.168.1.1"
    response = client.get("/api/v1/combined_calendar?ics_url=http://example.com/test.ics")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid URL provided"

def test_combined_calendar_local_ip_10(mock_dns_resolve):
    mock_dns_resolve.return_value = "10.0.0.1"
    response = client.get("/api/v1/combined_calendar?ics_url=http://example.com/test.ics")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid URL provided"

def test_combined_calendar_local_ip_172(mock_dns_resolve):
    mock_dns_resolve.return_value = "172.16.0.1"
    response = client.get("/api/v1/combined_calendar?ics_url=http://example.com/test.ics")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid URL provided"

def test_combined_calendar_local_ip_0(mock_dns_resolve):
    mock_dns_resolve.return_value = "0.0.0.0"
    response = client.get("/api/v1/combined_calendar?ics_url=http://example.com/test.ics")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid URL provided"

def test_combined_calendar_local_ip_169(mock_dns_resolve):
    mock_dns_resolve.return_value = "169.254.169.254"
    response = client.get("/api/v1/combined_calendar?ics_url=http://example.com/test.ics")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid URL provided"

def test_combined_calendar_invalid_scheme():
    response = client.get("/api/v1/combined_calendar?ics_url=ftp://example.com/test.ics")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid URL scheme. Must be http or https."

def test_combined_calendar_unknown_host(mock_dns_resolve):
    mock_dns_resolve.side_effect = socket.gaierror
    with patch("httpx.AsyncClient.get") as mock_get:
        # Since it passes the gaierror, it tries to fetch the URL, so mock it.
        mock_get.return_value.status_code = 400
        mock_get.return_value.content = b""
        response = client.get("/api/v1/combined_calendar?ics_url=http://unknown-host.com/test.ics")
        # In this case it should fail at the fetch step since status_code is 400
        assert response.status_code == 400
        assert response.json()["detail"] == "Failed to fetch the provided ICS URL"
