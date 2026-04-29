import os
import json

def merge_all_ics():
    ics_dir = "ics"
    output_file = os.path.join(ics_dir, "srilanka-holidays.ics")
    
    # Yearly holiday files
    files = [f for f in os.listdir(ics_dir) if f.endswith(".ics") and f != "srilanka-holidays.ics"]
    files.sort()
    
    # Standard VTIMEZONE for Sri Lanka
    vtimezone = [
        "BEGIN:VTIMEZONE",
        "TZID:Asia/Colombo",
        "X-LIC-LOCATION:Asia/Colombo",
        "BEGIN:STANDARD",
        "TZOFFSETFROM:+0530",
        "TZOFFSETTO:+0530",
        "TZNAME:+0530",
        "DTSTART:19700101T000000",
        "END:STANDARD",
        "END:VTIMEZONE"
    ]
    
    master_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Dilshan-H//Sri Lanka Holidays//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Sri Lanka Master Calendar",
        "X-WR-TIMEZONE:Asia/Colombo",
        "X-WR-CALDESC:Comprehensive collection of Sri Lankan public, bank, and mercantile holidays (2021-2028)."
    ]
    master_content.extend(vtimezone)
    
    # Process yearly holiday files
    for filename in files:
        filepath = os.path.join(ics_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            in_event = False
            for line in f:
                line = line.strip()
                if line == "BEGIN:VEVENT":
                    in_event = True
                if in_event:
                    # Fix DTSTART/DTEND for Apple compatibility (ensure TZID if needed)
                    if line.startswith("DTSTART") and "VALUE=DATE" not in line:
                        line = line.replace("DTSTART:", "DTSTART;TZID=Asia/Colombo:")
                    if line.startswith("DTEND") and "VALUE=DATE" not in line:
                        line = line.replace("DTEND:", "DTEND;TZID=Asia/Colombo:")
                    
                    master_content.append(line)
                if line == "END:VEVENT":
                    in_event = False

    master_content.append("END:VCALENDAR")
    
    # Write with CRLF line endings (mandatory for some clients)
    with open(output_file, "wb") as f:
        f.write("\r\n".join(master_content).encode("utf-8"))
        f.write(b"\r\n")
    print(f"Successfully merged files into {output_file} with CRLF and VTIMEZONE")

if __name__ == "__main__":
    merge_all_ics()
