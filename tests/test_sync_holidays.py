import pytest
import sys
import os

# Add src directory to path to allow importing src.converters.sync_holidays
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from converters.sync_holidays import get_markers

def test_get_markers_public_holiday():
    # "public" triggers all three: is_public, is_bank, is_merc
    # markers: *†‡
    assert get_markers("Some Public Holiday", "Holiday") == "*†‡"
    assert get_markers("Holiday", "Public") == "*†‡"

def test_get_markers_national_holiday():
    # "national" triggers is_public only
    # markers: *
    assert get_markers("National Day", "Holiday") == "*"
    assert get_markers("Holiday", "National") == "*"

def test_get_markers_poya_holiday():
    # "poya" triggers is_public and is_bank
    # markers: *†
    assert get_markers("Duruthu Full Moon Poya Day", "Holiday") == "*†"
    assert get_markers("Holiday", "Poya") == "*†"

def test_get_markers_bank_holiday():
    # "bank" triggers is_bank only
    # markers: †
    assert get_markers("Special Bank Holiday", "Holiday") == "†"
    assert get_markers("Holiday", "Bank") == "†"

def test_get_markers_mercantile_holiday():
    # "mercantile" triggers is_merc only
    # markers: ‡
    assert get_markers("Special Mercantile Holiday", "Holiday") == "‡"
    assert get_markers("Holiday", "Mercantile") == "‡"

def test_get_markers_specific_mercantile_holidays():
    # "new year", "thai pongal", "may day", "christmas" trigger is_merc only
    # markers: ‡
    assert get_markers("Sinhala and Tamil New Year", "Holiday") == "‡"
    assert get_markers("Thai Pongal Day", "Holiday") == "‡"
    assert get_markers("May Day", "Holiday") == "‡"
    assert get_markers("Christmas Day", "Holiday") == "‡"

def test_get_markers_case_insensitivity():
    # Should be case insensitive
    assert get_markers("NATIONAL", "holiday") == "*"
    assert get_markers("holiday", "BANK") == "†"
    assert get_markers("mErCaNtIlE", "holiday") == "‡"
    assert get_markers("pUBLic", "holiday") == "*†‡"
    assert get_markers("POYA", "holiday") == "*†"

def test_get_markers_no_match():
    # No matching keywords
    assert get_markers("Regular Day Off", "Holiday") == ""
    assert get_markers("Weekend", "Weekly") == ""
    assert get_markers("", "") == ""

def test_get_markers_multiple_matches_different_fields():
    # Both summary and type have matching keywords
    # summary="National" (*), type="Bank" (†) -> "*†"
    assert get_markers("National Holiday", "Bank Holiday") == "*†"
    # summary="Poya" (*†), type="Mercantile" (‡) -> "*†‡"
    assert get_markers("Full Moon Poya", "Mercantile") == "*†‡"
