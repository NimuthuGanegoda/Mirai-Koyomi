import json
import datetime
import glob
import os
import hashlib

def get_nth_weekday(year, month, weekday_target, n):
    first_day = datetime.date(year, month, 1)
    first_weekday = first_day.weekday()
    days_to_target = (weekday_target - first_weekday) % 7
    first_target_date = first_day + datetime.timedelta(days=days_to_target)
    return first_target_date + datetime.timedelta(weeks=n-1)

def get_observances(year):
    mothers_day = get_nth_weekday(year, 5, 6, 2)
    fathers_day = get_nth_weekday(year, 6, 6, 3)
    
    return [
        {"name": "Valentine's Day", "date": datetime.date(year, 2, 14)},
        {"name": "International Women's Day", "date": datetime.date(year, 3, 8)},
        {"name": "Mother's Day", "date": mothers_day},
        {"name": "World Environment Day", "date": datetime.date(year, 6, 5)},
        {"name": "Father's Day", "date": fathers_day},
        {"name": "Children's Day", "date": datetime.date(year, 10, 1)},
        {"name": "Teachers' Day", "date": datetime.date(year, 10, 6)}
    ]

for file_path in glob.glob("json/*.json"):
    try:
        year = int(os.path.basename(file_path).split('.')[0])
    except:
        continue
        
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
                "end": (obs["date"] + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            }
            data.append(new_event)
            
    # sort by start date
    data.sort(key=lambda x: x["start"])
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
        
print("JSON files updated")
