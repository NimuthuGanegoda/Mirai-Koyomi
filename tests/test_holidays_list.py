import json
import pytest
from unittest.mock import patch, mock_open
from fastapi.testclient import TestClient

from src.api.app import app, verify_api_key

# Override API key validation for tests
app.dependency_overrides[verify_api_key] = lambda: "test_key"

client = TestClient(app)

# Sample holiday data for mocking
MOCK_HOLIDAYS_DATA = [
    {
        "uid": "id1",
        "summary": "Public Holiday 1",
        "categories": ["Public Holiday", "Bank Holiday"],
        "start": "2024-01-15",
        "end": "2024-01-16"
    },
    {
        "uid": "id2",
        "summary": "Poya Holiday 1",
        "categories": ["Poya Holiday"],
        "start": "2024-02-20",
        "end": "2024-02-21"
    },
    {
        "uid": "id3",
        "summary": "Another Public Holiday",
        "categories": ["Public Holiday"],
        "start": "2024-01-26",
        "end": "2024-01-27"
    }
]

MOCK_JSON_STRING = json.dumps(MOCK_HOLIDAYS_DATA)


def test_holidays_list_valid_year_full_format():
    with patch("builtins.open", mock_open(read_data=MOCK_JSON_STRING)):
        response = client.get("/api/v1/holidays?year=2024")
        assert response.status_code == 200
        data = response.json()
        assert "holidays" in data
        assert len(data["holidays"]) == 3
        # Check first item structure
        first_item = data["holidays"][0]
        assert first_item["date"] == "2024-01-15"
        assert first_item["name"] == "Public Holiday 1"
        assert first_item["type"] == ["Public Holiday", "Bank Holiday"]
        assert first_item["start"] == "2024-01-15"
        assert first_item["end"] == "2024-01-16"
        assert first_item["id"] == "id1"


def test_holidays_list_valid_year_simple_format():
    with patch("builtins.open", mock_open(read_data=MOCK_JSON_STRING)):
        response = client.get("/api/v1/holidays?year=2024&format=simple")
        assert response.status_code == 200
        data = response.json()
        assert "holidays" in data
        assert len(data["holidays"]) == 3
        # Simple format should just be a list of dates (strings)
        assert data["holidays"] == ["2024-01-15", "2024-02-20", "2024-01-26"]


def test_holidays_list_filter_by_month():
    with patch("builtins.open", mock_open(read_data=MOCK_JSON_STRING)):
        response = client.get("/api/v1/holidays?year=2024&month=1")
        assert response.status_code == 200
        data = response.json()
        assert "holidays" in data
        assert len(data["holidays"]) == 2
        assert data["holidays"][0]["start"] == "2024-01-15"
        assert data["holidays"][1]["start"] == "2024-01-26"


def test_holidays_list_filter_by_type():
    with patch("builtins.open", mock_open(read_data=MOCK_JSON_STRING)):
        response = client.get("/api/v1/holidays?year=2024&type=poya holiday")
        assert response.status_code == 200
        data = response.json()
        assert "holidays" in data
        assert len(data["holidays"]) == 1
        assert data["holidays"][0]["id"] == "id2"


def test_holidays_list_filter_by_month_and_type():
    with patch("builtins.open", mock_open(read_data=MOCK_JSON_STRING)):
        response = client.get("/api/v1/holidays?year=2024&month=1&type=public holiday")
        assert response.status_code == 200
        data = response.json()
        assert "holidays" in data
        assert len(data["holidays"]) == 2

        response = client.get("/api/v1/holidays?year=2024&month=1&type=bank holiday")
        assert response.status_code == 200
        data = response.json()
        assert len(data["holidays"]) == 1
        assert data["holidays"][0]["id"] == "id1"


def test_holidays_list_invalid_format():
    response = client.get("/api/v1/holidays?year=2024&format=invalid_format")
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid format. Use 'simple' or 'full'"}


def test_holidays_list_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        response = client.get("/api/v1/holidays?year=2024")
        assert response.status_code == 404
        assert response.json() == {"error": "Data for requested year not available"}


def test_holidays_list_invalid_json():
    with patch("builtins.open", mock_open(read_data="{invalid_json:")):
        response = client.get("/api/v1/holidays?year=2024")
        assert response.status_code == 500
        assert response.json() == {"error": "Invalid data format for requested year. Please notify the admin."}

def test_holidays_list_path_traversal():
    # If the file path resolves outside the json directory, should return 400
    # For testing, we mock the path resolution
    with patch("src.api.app.Path.samefile", return_value=False):
        response = client.get("/api/v1/holidays?year=2024")
        assert response.status_code == 400
        assert response.json() == {"error": "Invalid file path"}

def test_holidays_list_skip_invalid_entries():
    invalid_data = [
        {
            "uid": "id1",
            "summary": "Valid Holiday",
            "categories": ["Public Holiday"],
            "start": "2024-01-15",
            "end": "2024-01-16"
        },
        {
            "uid": "id2",
            # Missing start and end
        },
        {
            "uid": "id3",
            "summary": "Invalid Date Holiday",
            "start": "not-a-date",
            "end": "2024-01-16"
        }
    ]
    with patch("builtins.open", mock_open(read_data=json.dumps(invalid_data))):
        response = client.get("/api/v1/holidays?year=2024")
        assert response.status_code == 200
        data = response.json()
        assert len(data["holidays"]) == 1
        assert data["holidays"][0]["id"] == "id1"

def test_holidays_list_simple_format_duplicates():
    # Simple format should not return duplicate dates
    duplicate_data = [
        {
            "uid": "id1",
            "summary": "Holiday 1",
            "categories": ["Public Holiday"],
            "start": "2024-01-15",
            "end": "2024-01-16"
        },
        {
            "uid": "id2",
            "summary": "Holiday 2",
            "categories": ["Public Holiday"],
            "start": "2024-01-15",
            "end": "2024-01-16"
        }
    ]
    with patch("builtins.open", mock_open(read_data=json.dumps(duplicate_data))):
        response = client.get("/api/v1/holidays?year=2024&format=simple")
        assert response.status_code == 200
        data = response.json()
        assert len(data["holidays"]) == 1
        assert data["holidays"][0] == "2024-01-15"

def test_holidays_list_missing_year():
    response = client.get("/api/v1/holidays")
    assert response.status_code == 422 # FastAPI validation error for missing query param

def test_holidays_list_invalid_year_range():
    response = client.get("/api/v1/holidays?year=2020")
    assert response.status_code == 422 # Validation error, YEAR_MIN = 2021
    response = client.get("/api/v1/holidays?year=2030")
    assert response.status_code == 422 # Validation error, YEAR_MAX = 2028
