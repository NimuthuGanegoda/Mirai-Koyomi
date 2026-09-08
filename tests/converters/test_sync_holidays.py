import pytest
import requests
from unittest.mock import patch
from src.converters.sync_holidays import sync_year

@patch('builtins.print')
def test_sync_year_no_table(mock_print, requests_mock):
    # Mock requests to return HTML without a table
    year = 2024
    url = f"https://www.officeholidays.com/countries/sri-lanka/{year}"
    requests_mock.get(url, text="<html><body><h1>No holidays here</h1></body></html>")

    sync_year(year)

    mock_print.assert_any_call(f"No table found for {year}")

@patch('builtins.print')
def test_sync_year_connection_error(mock_print, requests_mock):
    # Mock requests to raise a ConnectionError
    year = 2024
    url = f"https://www.officeholidays.com/countries/sri-lanka/{year}"
    requests_mock.get(url, exc=requests.exceptions.ConnectionError("Connection refused"))

    sync_year(year)

    # We check that the exception is printed out
    # print(f"Error syncing {year}: {e}")
    called = False
    for call in mock_print.call_args_list:
        if f"Error syncing {year}: " in call[0][0]:
            called = True
            break
    assert called, "Error message was not printed as expected."
