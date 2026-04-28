import json
import os
from datetime import datetime

def generate_rich_ics(year):
    json_path = f"json/{year}.json"
    if not os.path.exists(json_path):
        return
        
    with open(json_path, "r") as f:
        holidays = json.load(f)
        
    ics_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Mommy//SL Holidays Master//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Sri Lanka Holidays " + str(year),
        "X-WR-TIMEZONE:Asia/Colombo"
    ]
    
    for h in holidays:
        # Markers: * Public, † Bank, ‡ Mercantile
        markers = ""
        if "Public" in h["categories"]: markers += "*"
        if "Bank" in h["categories"]: markers += "†"
        if "Mercantile" in h["categories"]: markers += "‡"
        
        summary = f"{h['summary']} {markers}".strip()
        start = h["start"].replace("-", "")
        end = h["end"].replace("-", "")
        
        desc = "\\n".join([f"- {cat} Holiday" for cat in h["categories"]])
        
        event = [
            "BEGIN:VEVENT",
            f"UID:{h['uid']}@mommy.internal",
            f"DTSTART;VALUE=DATE:{start}",
            f"DTEND;VALUE=DATE:{end}",
            f"SUMMARY:{summary}",
            f"DESCRIPTION:{desc}",
            "STATUS:CONFIRMED",
            "BEGIN:VALARM",
            "ACTION:AUDIO",
            "TRIGGER:-PT15H", # Alarm at 9 AM the day before (since it is a whole day event)
            "END:VALARM",
            "END:VEVENT"
        ]
        ics_content.extend(event)
        
    ics_content.append("END:VCALENDAR")
    
    os.makedirs("ics_rich", exist_ok=True)
    with open(f"ics_rich/{year}.ics", "w") as f:
        f.write("\n".join(ics_content))

if __name__ == "__main__":
    for y in range(2021, 2028):
        generate_rich_ics(y)
    print("Rich ICS files generated in ics_rich/")
