import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from converters.sync_holidays import get_markers

@pytest.mark.parametrize(
    "summary, type_text, expected",
    [
        # Only Public (national)
        ("National Day", "Holiday", "*"),
        ("Independence Day", "National Holiday", "*"),

        # Only Mercantile
        ("Christmas Day", "Holiday", "‡"),
        ("May Day", "Observance", "‡"),
        ("Thai Pongal Day", "Festival", "‡"),
        ("Sinhala and Tamil New Year", "Festival", "‡"),
        ("Regular Day", "Mercantile Holiday", "‡"),

        # Public and Bank (Poya matches both, but not Mercantile unless 'public' is present)
        ("Duruthu Full Moon Poya Day", "Poya Day", "*†"),
        ("Poya", "Holiday", "*†"),

        # Public, Bank, Mercantile ("Public" in name or type matches all)
        ("Some Holiday", "Public Holiday", "*†‡"),
        ("Public Event", "Holiday", "*†‡"),

        # Case insensitivity
        ("pOyA Day", "holiday", "*†"),
        ("MAY DAY", "Observance", "‡"),
        ("chrIstMas", "holiday", "‡"),
        ("NaTiOnAl DaY", "holiday", "*"),

        # Empty or non-matching
        ("Regular Day", "Working Day", ""),
        ("", "", ""),
        ("Some Festival", "Observance", ""),

        # Checking edge cases where keywords are substrings (the logic uses 'in', so it should match)
        ("Specialbankholiday", "Event", "†"), # Note: 'bank' is a substring
        ("National Holiday", "Bank Holiday", "*†"),
        ("Full Moon Poya", "Mercantile", "*†‡"),
    ]
)
def test_get_markers(summary, type_text, expected):
    """
    Test the get_markers heuristic used for official Sri Lankan markers.

    The logic:
    is_public = any(x in type_text.lower() or x in summary.lower() for x in ["public", "national", "poya"])
    is_bank = any(x in type_text.lower() or x in summary.lower() for x in ["public", "bank", "poya"])
    is_merc = any(x in type_text.lower() or x in summary.lower() for x in ["public", "mercantile", "new year", "thai pongal", "may day", "christmas"])

    Markers:
    Public = *
    Bank = †
    Mercantile = ‡
    """
    assert get_markers(summary, type_text) == expected
