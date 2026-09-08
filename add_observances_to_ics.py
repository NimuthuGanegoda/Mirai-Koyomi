import os
import glob
from datetime import datetime, date, timedelta
from icalendar import Calendar, Event

def get_nth_weekday_of_month(year, month, weekday, n):
    count = 0
    d = date(year, month, 1)
    while count < n:
        if d.weekday() == weekday:
            count += 1
        if count == n:
            return d
        d += timedelta(days=1)

def get_observances(year):
    static_obs = [
        {"month": 2, "day": 14, "name": "Valentine's Day"},
        {"month": 3, "day": 8, "name": "International Women's Day"},
        {"month": 4, "day": 22, "name": "Earth Day"},
        {"month": 6, "day": 5, "name": "World Environment Day"},
        {"month": 10, "day": 1, "name": "Children's Day"},
        {"month": 10, "day": 6, "name": "Teachers' Day"},
        {"month": 10, "day": 16, "name": "World Food Day"},
        {"month": 10, "day": 31, "name": "Halloween"},
    ]
    observances = []
    for obs in static_obs:
        observances.append({
            "name": obs["name"],
            "date": date(year, obs["month"], obs["day"])
        })
    observances.append({
        "name": "Mother's Day",
        "date": get_nth_weekday_of_month(year, 5, 6, 2) # 2nd Sunday of May (6=Sunday)
    })
    observances.append({
        "name": "Father's Day",
        "date": get_nth_weekday_of_month(year, 6, 6, 3) # 3rd Sunday of June
    })
    return observances

for file_path in glob.glob("ics/20*.ics"):
    filename = os.path.basename(file_path)
    year = int(filename.split('.')[0])
    
    with open(file_path, "r", encoding="utf-8") as f:
        cal = Calendar.from_ical(f.read())
        
    existing_summaries = [component.get("summary", "") for component in cal.walk("vevent")]
    
    observances = get_observances(year)
    for obs in observances:
        if obs["name"] not in existing_summaries:
            event = Event()
            event.add('summary', obs["name"])
            event.add('dtstart', obs["date"])
            event.add('dtend', obs["date"] + timedelta(days=1))
            uid = f"sl_obs_{obs['date'].strftime('%Y%m%d')}@srilanka-holidays.api"
            event.add('uid', uid)
            event.add('categories', ["Observance"])
            cal.add_component(event)
            
    with open(file_path, "wb") as f:
        f.write(cal.to_ical())
        
print("ICS files updated")
