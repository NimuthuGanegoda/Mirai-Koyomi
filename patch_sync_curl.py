import sys

with open("src/converters/sync_holidays.py", "r") as f:
    code = f.read()

# Replace:
# response = requests.get(url, timeout=10)
# soup = BeautifulSoup(response.text, 'html.parser')
# with subprocess curl call

new_code = """
        import subprocess
        result = subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", url], capture_output=True, text=True)
        html_text = result.stdout
        soup = BeautifulSoup(html_text, 'html.parser')
"""

old_code = """
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
"""

code = code.replace(old_code.strip(), new_code.strip())
with open("src/converters/sync_holidays.py", "w") as f:
    f.write(code)

