import requests
url = "https://www.officeholidays.com/countries/sri-lanka/2026"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
print("fetching...")
r = requests.get(url, headers=headers, timeout=10)
print(r.status_code)
