import json
from unittest.mock import patch

from src.converters.icalendar_to_json import ics_to_json

def test_ics_to_json(tmp_path):
    # Create a temporary ICS file
    ics_file = tmp_path / "test_holidays.ics"
    ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//My Calendar//EN
BEGIN:VEVENT
UID:12345
SUMMARY:Test Holiday
DESCRIPTION:Public Holiday,Bank Holiday
DTSTART;VALUE=DATE:20240101
DTEND;VALUE=DATE:20240102
END:VEVENT
END:VCALENDAR
"""
    ics_file.write_text(ics_content, encoding="utf-8")

    # Create a temporary output directory
    out_dir = tmp_path / "out_json"

    # Safely mock abspath to return the temp directory only for the json_dir target
    original_abspath = __import__("os").path.abspath
    def side_effect_abspath(path):
        if "srilanka-holidays" in path or "json" in path:
            return str(out_dir)
        return original_abspath(path)

    with patch("src.converters.icalendar_to_json.os.path.abspath", side_effect=side_effect_abspath) as mock_abspath:
        ics_to_json(str(ics_file))

    # Check output
    assert mock_abspath.called

    json_file_path = out_dir / "test_holidays.json"
    assert json_file_path.exists()

    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1
    event = data[0]
    assert event["uid"] == "12345"
    assert event["summary"] == "Test Holiday"
    assert event["categories"] == ["Public Holiday", "Bank Holiday"]
    assert event["start"] == "2024-01-01"
    assert event["end"] == "2024-01-02"
