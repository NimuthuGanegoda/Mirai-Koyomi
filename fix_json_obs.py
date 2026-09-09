import json
import glob
from datetime import datetime, date, timedelta
import os

def get_observances(year):
    static_obs = [
        {"month": 4, "day": 22, "name": "Earth Day"},
        {"month": 10, "day": 16, "name": "World Food Day"},
        {"month": 10, "day": 31, "name": "Halloween"},
    ]
    observances = []
    for obs in static_obs:
        observances.append({
            "name": obs["name"],
            "date": date(year, obs["month"], obs["day"])
        })
    return observances

for file_path in glob.glob("json/20*.json"):
    year = int(os.path.basename(file_path).split('.')[0])
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    existing_names = [d.get("summary", "") for d in data]
    
    observances = get_observances(year)
    for obs in observances:
        if obs["name"] not in existing_names:
            uid = f"sl_obs_{obs['date'].strftime('%Y%m%d')}@srilanka-holidays.api"
            new_event = {
                "uid": uid,
                "summary": obs["name"],
                "categories": ["Observance"],
                "start": obs["date"].strftime("%Y-%m-%d"),
                "end": (obs["date"] + timedelta(days=1)).strftime("%Y-%m-%d")
            }
            data.append(new_event)
            
    data.sort(key=lambda x: x["start"])
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
print("Fixed missing observances in all JSON files")
