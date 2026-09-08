import os
import glob

files_to_check = [
    "public/terms-of-use.html",
    "public/index.html",
    "src/api/app.py",
    "src/converters/icalendar_to_xml.py",
    "src/converters/icalendar_to_json.py",
    "src/converters/icalendar_to_csv.py",
    "src/converters/merge_ics.py",
    ".github/dependabot.yml",
    ".github/workflows/update_master_ics.yml",
    ".github/workflows/convert_ics.yaml"
]

# add all ICS files
ics_files = glob.glob("data/holidays/ics/*.ics")
files_to_check.extend(ics_files)

replacements = {
    "Dilshan-H/srilanka-holidays/tree/main": "NimuthuGanegoda/Mirai-Koyomi/tree/master",
    "Dilshan-H/srilanka-holidays": "NimuthuGanegoda/Mirai-Koyomi",
    "Dilshan-H": "NimuthuGanegoda",
    "dilshan-h": "nimuthuganegoda",
    "srilanka-holidays.vercel.app": "mirai-koyomi.vercel.app"
}

for file_path in files_to_check:
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Links modified successfully.")
