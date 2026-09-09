import re

with open("src/converters/sync_holidays.py", "r") as f:
    code = f.read()

# Replace the static_obs list
new_static_obs = """    static_obs = [
        {"month": 10, "day": 1, "name": "Children's Day"},
        {"month": 10, "day": 6, "name": "Teachers' Day"},
    ]"""

code = re.sub(r'static_obs = \[.*?\]', new_static_obs, code, flags=re.DOTALL)

with open("src/converters/sync_holidays.py", "w") as f:
    f.write(code)

print("Patched sync_holidays.py")
