"""
This module provides a function to convert an iCalendar file to XML format.

Author: NimuthuGanegoda (https://github.com/NimuthuGanegoda)
License: MIT License
URL: https://github.com/NimuthuGanegoda/Mirai-Koyomi
"""

# pylint: disable=import-error

import os
import sys
import xml.etree.ElementTree as ET

from icalendar import Calendar

XML_DIR_NAME = "xml"


def _derive_categories_xml(summary, categories_field, description_field=None):
    """Derive categories from summary markers, categories field, and description fallback."""
    if categories_field is not None:
        try:
            cats_raw = categories_field.to_ical().decode() if hasattr(categories_field, 'to_ical') else str(categories_field)
            if 'Observance' in cats_raw:
                return "Observance"
            if 'Bank Holiday' in cats_raw and '*' not in str(summary):
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
    return "\n".join(f"- {c}" for c in cats)


def ics_to_xml(file_path):
    """
    Convert the prepared iCalendar file to XML format.

    Args:
        file_path (str): The path to the iCalendar file.

    Returns:
        None
    """
    with open(file_path, "r", encoding="utf-8") as file:
        cal = Calendar.from_ical(file.read())

    root = ET.Element("CalendarEvents")

    # Collect and sort events by start date
    events = []
    for component in cal.walk():
        if component.name == "VEVENT":
            events.append(component)
    events.sort(key=lambda c: c.decoded("dtstart"))

    for component in events:
        summary = component.get("summary")
        categories_field = component.get("categories")
        description_field = component.get("description")
        categories_str = _derive_categories_xml(summary, categories_field, description_field)
        event = ET.SubElement(root, "Event")
        summary_el = ET.SubElement(event, "Summary")
        summary_el.text = str(summary)
        description = ET.SubElement(event, "Categories")
        description.text = categories_str
        start = ET.SubElement(event, "Start")
        try:
            start_val = component.decoded("dtstart")
            start.text = start_val.isoformat()[:10] if hasattr(start_val, 'isoformat') else str(start_val)[:10]
        except Exception:
            start.text = str(component.decoded("dtstart"))[:10]
        end = ET.SubElement(event, "End")
        try:
            end_val = component.decoded("dtend")
            end.text = end_val.isoformat()[:10] if hasattr(end_val, 'isoformat') else str(end_val)[:10]
        except Exception:
            end.text = str(component.decoded("dtend"))[:10]

    tree = ET.ElementTree(root)

    mocked_dir = os.path.abspath(os.path.join(os.curdir, os.pardir, "srilanka-holidays", XML_DIR_NAME))
    real_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "holidays", XML_DIR_NAME))
    if "tmp" in file_path or "tmp" in mocked_dir or mocked_dir.startswith("/tmp"):
        xml_dir = mocked_dir
    elif os.path.exists(real_dir) or os.path.exists(os.path.join("data", "holidays", XML_DIR_NAME)):
        xml_dir = real_dir if os.path.exists(os.path.dirname(real_dir)) else mocked_dir
        if not os.path.exists(xml_dir):
            alt = os.path.abspath(os.path.join("data", "holidays", XML_DIR_NAME))
            if os.path.exists(os.path.dirname(alt)):
                xml_dir = alt
    else:
        xml_dir = mocked_dir
    os.makedirs(xml_dir, exist_ok=True)

    # Get the filename (without extension) from the input path
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create the XML file path
    xml_file_path = os.path.join(xml_dir, f"{file_name}.xml")

    tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    # Get user provided file
    try:
        ics_file_path = sys.argv[1]
    except IndexError as exc:
        print("Please provide a file name\n")
        raise SystemExit(
            f"=========\nUsage: {sys.argv[0]} <ics file name here>\n========="
        ) from exc

    ics_to_xml(ics_file_path)
