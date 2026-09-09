import json
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup


def get_nth_weekday_of_month(year, month, weekday, n):
    count = 0
    date = datetime(year, month, 1)
    while count < n:
        if date.weekday() == weekday:
            count += 1
        if count == n:
            return date
        date += timedelta(days=1)

def get_observances(year):
    # Static observances
        static_obs = [
        {"month": 10, "day": 1, "name": "Children's Day"},
        {"month": 10, "day": 6, "name": "Teachers' Day"},
    ]

    observances = []

    for obs in static_obs:
        d = datetime(year, obs["month"], obs["day"])
        observances.append({
            "name": obs["name"],
            "start": d.strftime("%Y-%m-%d"),
            "end": (d + timedelta(days=1)).strftime("%Y-%m-%d")
        })

    # Dynamic observances
    # Mother's Day (2nd Sunday in May)
    md = get_nth_weekday_of_month(year, 5, 6, 2)
    observances.append({
        "name": "Mother's Day",
        "start": md.strftime("%Y-%m-%d"),
        "end": (md + timedelta(days=1)).strftime("%Y-%m-%d")
    })

    # Father's Day (3rd Sunday in June)
    fd = get_nth_weekday_of_month(year, 6, 6, 3)
    observances.append({
        "name": "Father's Day",
        "start": fd.strftime("%Y-%m-%d"),
        "end": (fd + timedelta(days=1)).strftime("%Y-%m-%d")
    })

    return observances

def get_markers(summary, type_text):
    markers = ""
    # Official Sri Lankan markers based on type/category
    # This is a heuristic based on common naming/typing on holiday sites
    is_public = any(x in type_text.lower() or x in summary.lower() for x in ["public", "national", "poya"])
    is_bank = any(x in type_text.lower() or x in summary.lower() for x in ["public", "bank", "poya"])
    is_merc = any(x in type_text.lower() or x in summary.lower() for x in ["public", "mercantile", "new year", "thai pongal", "may day", "christmas"])
    
    if is_public: markers += "*"
    if is_bank: markers += "†"
    if is_merc: markers += "‡"
    return markers

def _parse_holiday_rows(rows, year):
    holidays_count = 0
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 4: continue

        # Format: Day, Date, Holiday Name, Type, Comments
        date_raw = cols[1].text.strip() # e.g., "Jan 15"
        name = cols[2].text.strip()
        h_type = cols[3].text.strip()

        # Parse date to ISO
        try:
            date_obj = datetime.strptime(f"{date_raw} {year}", "%b %d %Y")
            start_date = date_obj.strftime("%Y-%m-%d")
            end_date = (date_obj + timedelta(days=1)).strftime("%Y-%m-%d")
        except:
            continue

        markers = get_markers(name, h_type)
        summary = f"{name} {markers}".strip()

        categories = []
        if "*" in markers: categories.append("Public Holiday")
        if "†" in markers: categories.append("Bank Holiday")
        if "‡" in markers: categories.append("Mercantile Holiday")
        if "Poya" in name: categories.append("Poya Holiday")

        holidays_count += 1
        yield {
            "uid": f"sl_{year}_{holidays_count:02d}",
            "summary": summary,
            "categories": categories,
            "start": start_date,
            "end": end_date
        }

def sync_year(year):
    url = f"https://www.officeholidays.com/countries/sri-lanka/{year}"
    print(f"Syncing {year} from {url}...")
    
    try:
        import subprocess
        result = subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", url], capture_output=True, text=True)
        html_text = result.stdout
        soup = BeautifulSoup(html_text, 'html.parser')
        table = soup.find('table', class_='country-table')
        
        if not table:
            print(f"No table found for {year}")
            return
            
        rows = table.find_all('tr')[1:] # Skip header
        holidays = list(_parse_holiday_rows(rows, year))
            
        if holidays:
            # Add observances that don't conflict with existing holidays
            existing_starts = {h["start"] for h in holidays}
            observances = get_observances(year)

            for obs in observances:
                if obs["start"] not in existing_starts:
                    holidays.append({
                        "uid": f"sl_{year}_{len(holidays)+1:02d}",
                        "summary": obs["name"],
                        "categories": ["Observance"],
                        "start": obs["start"],
                        "end": obs["end"]
                    })

            # Sort holidays by start date, keeping UIDs intact
            holidays.sort(key=lambda x: x["start"])

            json_path = f"json/{year}.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(holidays, f, indent=2, ensure_ascii=False)
            print(f"Updated {json_path} with {len(holidays)} holidays.")
            
    except Exception as e:
        print(f"Error syncing {year}: {e}")

if __name__ == "__main__":
    # Sync current, next, and next-next year
    current_year = datetime.now().year
    for y in range(current_year, current_year + 3):
        sync_year(y)
