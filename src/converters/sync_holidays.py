import requests
from bs4 import BeautifulSoup
import json
import os
import re

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

def sync_year(year):
    url = f"https://www.officeholidays.com/countries/sri-lanka/{year}"
    print(f"Syncing {year} from {url}...")
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='country-table')
        
        if not table:
            print(f"No table found for {year}")
            return
            
        holidays = []
        rows = table.find_all('tr')[1:] # Skip header
        
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
            if "*" in markers: categories.append("Public")
            if "†" in markers: categories.append("Bank")
            if "‡" in markers: categories.append("Mercantile")
            if "Poya" in name: categories.append("Poya")
            
            holidays.append({
                "uid": f"sl_{year}_{len(holidays)+1:02d}",
                "summary": summary,
                "categories": categories,
                "start": start_date,
                "end": end_date
            })
            
        if holidays:
            json_path = f"json/{year}.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(holidays, f, indent=2, ensure_ascii=False)
            print(f"Updated {json_path} with {len(holidays)} holidays.")
            
    except Exception as e:
        print(f"Error syncing {year}: {e}")

if __name__ == "__main__":
    from datetime import datetime, timedelta
    # Sync current, next, and next-next year
    current_year = datetime.now().year
    for y in range(current_year, current_year + 3):
        sync_year(y)
