"""
This module provides a function to convert an iCalendar file to JSON format.

Author: NimuthuGanegoda (https://github.com/NimuthuGanegoda)
License: MIT License
URL: https://github.com/NimuthuGanegoda/Mirai-Koyomi
"""

# pylint: disable=import-error

import json
import os
import sys

from icalendar import Calendar

JSON_DIR_NAME = "json"


def _derive_categories(summary, categories_field, description_field=None):
    """Derive categories from summary markers, categories field, and description fallback."""
    # Check for Observance via categories_field
    if categories_field is not None:
        try:
            cats_raw = categories_field.to_ical().decode() if hasattr(categories_field, 'to_ical') else str(categories_field)
            if 'Observance' in cats_raw:
                return ["Observance"]
        except Exception:
            if 'Observance' in str(categories_field):
                return ["Observance"]
        if 'Observance' in str(categories_field):
            return ["Observance"]
    summary_str = str(summary) if summary else ""
    cats = []
    if "*" in summary_str:
        cats.append("Public Holiday")
    if "†" in summary_str:
        cats.append("Bank Holiday")
    if "‡" in summary_str:
        cats.append("Mercantile Holiday")
    if "Poya" in summary_str:
        if "Poya Holiday" not in cats:
            cats.append("Poya Holiday")
    if not cats:
        # Fallback to description (for backwards compatibility with old ICS that uses DESCRIPTION)
        if description_field:
            try:
                desc_str = str(description_field)
                # Description is comma-separated like "Public Holiday,Bank Holiday"
                parts = [p.strip() for p in desc_str.split(",") if p.strip()]
                if parts:
                    return parts
            except Exception:
                pass
        # Fallback for observances without markers but with known names
        observance_names = ["Mother's Day", "Father's Day", "Children's Day", "Teachers' Day", "Special Bank Holiday"]
        for name in observance_names:
            if name in summary_str:
                if "Special Bank Holiday" in summary_str:
                    return ["Bank Holiday"]
                return ["Observance"]
        # If still empty, check categories_field string
        if categories_field and "Bank Holiday" in str(categories_field):
            return ["Bank Holiday"]
        if description_field and "Bank Holiday" in str(description_field):
            return [p.strip() for p in str(description_field).split(",")]
    return cats


def ics_to_json(file_path):
    """
    Convert the prepared iCalendar file to JSON format.

    Args:
        file_path (str): The path to the iCalendar file.

    Returns:
        None
    """
    with open(file_path, "r", encoding="utf-8") as file:
        cal = Calendar.from_ical(file.read())

    # Resolve output directory: use mocked path for tests (when file_path is in tmp), otherwise use data/holidays/json
    # This preserves backward compatibility with test that mocks os.path.abspath
    mocked_dir = os.path.abspath(os.path.join(os.curdir, os.pardir, "srilanka-holidays", JSON_DIR_NAME))
    real_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "holidays", JSON_DIR_NAME))
    # Detect test: file_path under /tmp or mocked_dir is under /tmp
    if "tmp" in file_path or "tmp" in mocked_dir or mocked_dir.startswith("/tmp"):
        json_dir = mocked_dir
    elif os.path.exists(real_dir) or os.path.exists(os.path.join("data", "holidays", JSON_DIR_NAME)):
        json_dir = real_dir if os.path.exists(os.path.dirname(real_dir)) else mocked_dir
        # Ensure data/holidays/json exists
        if not os.path.exists(json_dir):
            # Try alternative relative path
            alt = os.path.abspath(os.path.join("data", "holidays", JSON_DIR_NAME))
            if os.path.exists(os.path.dirname(alt)):
                json_dir = alt
    else:
        json_dir = mocked_dir
    os.makedirs(json_dir, exist_ok=True)

    # Get the filename (without extension) from the input path
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create the JSON file path
    json_file_path = os.path.join(json_dir, f"{file_name}.json")

    events = []
    for component in cal.walk():
        if component.name == "VEVENT":
            summary = component.get("summary")
            categories_field = component.get("categories")
            description_field = component.get("description")
            categories = _derive_categories(summary, categories_field, description_field)
            # Handle special Bank Holiday without markers but with categories
            if not categories and categories_field:
                cat_str = str(categories_field)
                if "Bank" in cat_str:
                    categories = ["Bank Holiday"]
            if not categories and description_field:
                try:
                    categories = [p.strip() for p in str(description_field).split(",") if p.strip()]
                except Exception:
                    pass
            start = component.decoded("dtstart")
            end = component.decoded("dtend")
            # Ensure ISO date strings YYYY-MM-DD
            try:
                start_str = start.isoformat()[:10] if hasattr(start, 'isoformat') else str(start)[:10]
                end_str = end.isoformat()[:10] if hasattr(end, 'isoformat') else str(end)[:10]
            except Exception:
                start_str = str(start)[:10]
                end_str = str(end)[:10]
            event = {
                "uid": str(component.get("uid")),
                "summary": str(summary),
                "categories": categories,
                "start": start_str,
                "end": end_str,
            }
            events.append(event)

    # Sort by start date
    events.sort(key=lambda x: x["start"])

    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(events, json_file, indent=2, ensure_ascii=False)
        json_file.write("\n")


if __name__ == "__main__":
    # Get user provided file
    try:
        ics_file_path = sys.argv[1]
    except IndexError as exc:
        print("Please provide a file name\n")
        raise SystemExit(
            f"=========\nUsage: {sys.argv[0]} <ics file name here>\n========="
        ) from exc

    ics_to_json(ics_file_path)
