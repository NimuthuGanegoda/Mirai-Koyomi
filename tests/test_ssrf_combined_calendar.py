import pytest
from fastapi.testclient import TestClient

from src.api.app import app, verify_api_key

# Mock verify_api_key to avoid needing a real API key for testing SSRF
async def mock_verify_api_key():
    return "test-api-key"

@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[verify_api_key] = mock_verify_api_key
    yield
    app.dependency_overrides.clear()

client = TestClient(app)

@pytest.mark.parametrize(
    "malicious_ip",
    [
        "127.0.0.1",
        "127.0.0.2",
        "192.168.1.1",
        "192.168.0.254",
        "10.0.0.1",
        "10.255.255.255",
        "172.16.0.1",
        "172.31.255.255",
        "0.0.0.0",
        "169.254.169.254",
    ]
)
def test_combined_calendar_ssrf_protection_ip_addresses(malicious_ip: str):
    """
    Test that the /api/v1/combined_calendar endpoint blocks SSRF attempts
    using various local/private IP addresses directly in the URL.
    """
    ics_url = f"http://{malicious_ip}/calendar.ics"

    response = client.get(f"/api/v1/combined_calendar?ics_url={ics_url}")

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid URL provided"}


def test_combined_calendar_ssrf_protection_localhost_domain():
    """
    Test that the /api/v1/combined_calendar endpoint blocks SSRF attempts
    using localhost domain which resolves to 127.0.0.1.
    """
    ics_url = "http://localhost/calendar.ics"

    response = client.get(f"/api/v1/combined_calendar?ics_url={ics_url}")

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid URL provided"}
