import os
import glob
from datetime import datetime, date, timedelta

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
        "date": get_nth_weekday_of_month(year, 5, 6, 2)
    })
    observances.append({
        "name": "Father's Day",
        "date": get_nth_weekday_of_month(year, 6, 6, 3)
    })
    return observances

def generate_vevent(obs):
    dtstart = obs['date'].strftime('%Y%m%d')
    dtend = (obs['date'] + timedelta(days=1)).strftime('%Y%m%d')
    dtstamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    uid = f"sl_obs_{dtstart}@srilanka-holidays.api"
    summary = obs['name']
    
    return f"""BEGIN:VEVENT
SUMMARY:{summary}
DTSTART;VALUE=DATE:{dtstart}
DTEND;VALUE=DATE:{dtend}
DTSTAMP:{dtstamp}
UID:{uid}
CATEGORIES:Observance
END:VEVENT
"""

for file_path in glob.glob("ics/20*.ics"):
    filename = os.path.basename(file_path)
    year = int(filename.split('.')[0])
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    observances = get_observances(year)
    added_events = ""
    for obs in observances:
        if obs["name"] not in content:
            added_events += generate_vevent(obs)
            
    if added_events:
        # Insert before END:VCALENDAR
        content = content.replace("END:VCALENDAR", added_events + "END:VCALENDAR")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
print("ICS files updated directly")
