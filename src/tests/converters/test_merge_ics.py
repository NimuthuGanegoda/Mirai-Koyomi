import os
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
from src.converters.merge_ics import merge_all_ics

def test_merge_all_ics():
    # Setup dummy file contents
    file_contents = {
        os.path.join("ics", "2023.ics"): (
            "BEGIN:VCALENDAR\n"
            "BEGIN:VEVENT\n"
            "DTSTART;VALUE=DATE:20230101\n"
            "DTEND;VALUE=DATE:20230102\n"
            "SUMMARY:New Year's Day\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n"
        ),
        os.path.join("ics", "2024.ics"): (
            "BEGIN:VCALENDAR\n"
            "BEGIN:VEVENT\n"
            "DTSTART:20240101T000000\n"
            "DTEND:20240101T235959\n"
            "SUMMARY:New Year's Day (Time-based)\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n"
        )
    }

    dummy_listdir = ["2024.ics", "srilanka-holidays.ics", "2023.ics", "not_ics.txt"]

    written_data = []

    def fake_open(filepath, mode="r", encoding=None):
        if mode == "r":
            if filepath in file_contents:
                return StringIO(file_contents[filepath])
            return StringIO("")
        elif mode == "wb":
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file

            def write_side_effect(data):
                written_data.append(data)

            mock_file.write.side_effect = write_side_effect
            return mock_file

    with patch("os.listdir", return_value=dummy_listdir):
        with patch("builtins.open", side_effect=fake_open) as mock_open_func:
            merge_all_ics()

    # Verify os.listdir was called
    # output file logic
    output_file = os.path.join("ics", "srilanka-holidays.ics")
    mock_open_func.assert_any_call(output_file, "wb")

    # Ensure written data was recorded
    assert len(written_data) > 0

    # The output is constructed as strings joined by CRLF, encoded to bytes
    combined_bytes = b"".join(written_data)
    combined_text = combined_bytes.decode("utf-8")

    lines = combined_text.split("\r\n")

    # Basic validations
    assert lines[0] == "BEGIN:VCALENDAR"
    assert lines[-2] == "END:VCALENDAR"  # Because there's an extra empty string from final b"\r\n" if we split by \r\n

    # Check timezone info exists
    assert "BEGIN:VTIMEZONE" in lines
    assert "TZID:Asia/Colombo" in lines

    # Check that events from 2023 are present
    assert "DTSTART;VALUE=DATE:20230101" in lines

    # Check that events from 2024 are transformed
    # For 2024, DTSTART doesn't have VALUE=DATE, so it should be replaced with DTSTART;TZID=Asia/Colombo:
    assert "DTSTART;TZID=Asia/Colombo:20240101T000000" in lines
    assert "DTEND;TZID=Asia/Colombo:20240101T235959" in lines

    # Verify the order of events - 2023 should be before 2024 because of files.sort()
    idx_2023 = lines.index("DTSTART;VALUE=DATE:20230101")
    idx_2024 = lines.index("DTSTART;TZID=Asia/Colombo:20240101T000000")
    assert idx_2023 < idx_2024
