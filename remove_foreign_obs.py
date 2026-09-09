import json
import glob
import os

to_remove = [
    "Halloween",
    "Earth Day",
    "World Food Day",
    "World Environment Day",
    "Valentine's Day",
    "International Women's Day"
]

# Update JSON
for file_path in glob.glob("data/holidays/json/20*.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    new_data = [d for d in data if d.get("summary") not in to_remove]
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)
        f.write("\n")

print("Removed from JSON")
