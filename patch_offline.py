import re
with open("src/api/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the fetching part
content = re.sub(
    r'# Fetch Sri Lanka Holidays Master ICS.*?sl_response = await client\.get\(sl_holidays_url\).*?if sl_response\.status_code != 200:.*?raise HTTPException\(.*?detail="Failed to fetch the Sri Lanka Holidays Master ICS",.*?\)',
    r'''# Fetch Sri Lanka Holidays Master ICS locally for offline support
            sl_ics_path = "ics/srilanka-holidays.ics"
            import aiofiles
            try:
                async with aiofiles.open(sl_ics_path, "r", encoding="utf-8") as sl_file:
                    sl_response_text = await sl_file.read()
            except FileNotFoundError:
                sl_ics_path = "data/holidays/ics/srilanka-holidays.ics"
                try:
                    async with aiofiles.open(sl_ics_path, "r", encoding="utf-8") as sl_file:
                        sl_response_text = await sl_file.read()
                except FileNotFoundError:
                    raise HTTPException(
                        status_code=500,
                        detail="Local Sri Lanka Holidays Master ICS file not found",
                    )''',
    content,
    flags=re.DOTALL
)

# Replace sl_response.text with sl_response_text
content = content.replace("sl_response.text", "sl_response_text")

# Also replace user_response.text with user_text in the merge_calendars call
content = content.replace("user_response.text", "user_text")

with open("src/api/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched successfully")
