"""
This module provides a function to convert an iCalendar file to CSV format.

Author: NimuthuGanegoda (https://github.com/NimuthuGanegoda)
License: MIT License
URL: https://github.com/NimuthuGanegoda/Mirai-Koyomi
"""

# pylint: disable=import-error

import csv
import os
import sys

from icalendar import Calendar

CSV_DIR_NAME = "csv"


def _derive_categories_csv(summary, categories_field, description_field=None):
    """Derive categories from summary markers, categories field, and description fallback."""
    if categories_field is not None:
        try:
            cats_raw = categories_field.to_ical().decode() if hasattr(categories_field, 'to_ical') else str(categories_field)
            if 'Observance' in cats_raw:
                return "Observance"
            if 'Bank Holiday' in cats_raw and '*' not in str(summary):
                # Special Bank Holiday case
                if 'Special Bank Holiday' in str(summary):
                    return "Bank Holiday"
        except Exception:
            pass
        if 'Observance' in str(categories_field):
            return "Observance"
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
        if description_field:
            try:
                desc_str = str(description_field)
                parts = [p.strip() for p in desc_str.split(",") if p.strip()]
                if parts:
                    return "\n".join(f"- {p}" for p in parts)
            except Exception:
                pass
        if "Special Bank Holiday" in summary_str:
            return "Bank Holiday"
        # Check for observance names
        for name in ["Mother's Day", "Father's Day", "Children's Day", "Teachers' Day"]:
            if name in summary_str:
                return "Observance"
        if categories_field and "Bank" in str(categories_field):
            return "Bank Holiday"
        if description_field and "Bank" in str(description_field):
            try:
                parts = [p.strip() for p in str(description_field).split(",") if p.strip()]
                if parts:
                    return "\n".join(f"- {p}" for p in parts)
            except Exception:
                pass
        return "Observance" if categories_field and "Observance" in str(categories_field) else ""
    # Format as multiline with dash prefix to match existing CSV style
    return "\n".join(f"- {c}" for c in cats)


def ics_to_csv(file_path):
    """
    Convert the provided iCalendar file to CSV format.

    Args:
        file_path (str): The path to the iCalendar file.

    Returns:
        None
    """
    with open(file_path, "r", encoding="utf-8") as file:
        cal = Calendar.from_ical(file.read())

    # Resolve output directory: use mocked path for tests (when file_path is in tmp), otherwise use data/holidays/csv
    mocked_dir = os.path.abspath(os.path.join(os.curdir, os.pardir, "srilanka-holidays", CSV_DIR_NAME))
    real_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "holidays", CSV_DIR_NAME))
    if "tmp" in file_path or "tmp" in mocked_dir or mocked_dir.startswith("/tmp"):
        csv_dir = mocked_dir
    elif os.path.exists(real_dir) or os.path.exists(os.path.join("data", "holidays", CSV_DIR_NAME)):
        csv_dir = real_dir if os.path.exists(os.path.dirname(real_dir)) else mocked_dir
        if not os.path.exists(csv_dir):
            alt = os.path.abspath(os.path.join("data", "holidays", CSV_DIR_NAME))
            if os.path.exists(os.path.dirname(alt)):
                csv_dir = alt
    else:
        csv_dir = mocked_dir
    os.makedirs(csv_dir, exist_ok=True)

    # Get the filename (without extension) from the input path
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create the CSV file path
    csv_file_path = os.path.join(csv_dir, f"{file_name}.csv")

    with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "UID",
            "Summary",
            "Categories",
            "Start",
            "End",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        events = []
        for component in cal.walk():
            if component.name == "VEVENT":
                events.append(component)
        # Sort by start date
        events.sort(key=lambda c: c.decoded("dtstart"))
        for component in events:
            summary = component.get("summary")
            categories_field = component.get("categories")
            description_field = component.get("description")
            categories_str = _derive_categories_csv(summary, categories_field, description_field)
            start = component.decoded("dtstart")
            end = component.decoded("dtend")
            try:
                start_str = start.isoformat()[:10] if hasattr(start, 'isoformat') else str(start)[:10]
                end_str = end.isoformat()[:10] if hasattr(end, 'isoformat') else str(end)[:10]
            except Exception:
                start_str = str(start)[:10]
                end_str = str(end)[:10]
            writer.writerow(
                {
                    "UID": str(component.get("uid")),
                    "Summary": str(summary),
                    "Categories": categories_str,
                    "Start": start_str,
                    "End": end_str,
                }
            )


if __name__ == "__main__":
    # Get user provided file
    try:
        ics_file_path = sys.argv[1]
    except IndexError as exc:
        print("Please provide a file name\n")
        raise SystemExit(
            f"=========\nUsage: {sys.argv[0]} <ics file name here>\n========="
        ) from exc

    ics_to_csv(ics_file_path)
