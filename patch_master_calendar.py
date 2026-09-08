import sys
with open("src/api/app.py", "r", encoding="utf-8") as f:
    content = f.read()

if "FileResponse" not in content:
    content = content.replace("from fastapi.responses import RedirectResponse", "from fastapi.responses import RedirectResponse, FileResponse")

new_endpoint = """
@app.get("/api/v1/master_calendar")
async def master_calendar():
    \"\"\"Return the Master Sri Lanka Holidays ICS calendar\"\"\"
    import os
    file_path = "ics/srilanka-holidays.ics"
    if not os.path.exists(file_path):
        file_path = "data/holidays/ics/srilanka-holidays.ics"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/calendar", filename="srilanka-holidays.ics")
    raise HTTPException(status_code=404, detail="Master ICS file not found")

@app.get("/api/v1/combined_calendar")
"""
if "/api/v1/master_calendar" not in content:
    content = content.replace("@app.get(\"/api/v1/combined_calendar\")", new_endpoint.strip() + "\n\n@app.get(\"/api/v1/combined_calendar\")")

with open("src/api/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Added master_calendar endpoint")
