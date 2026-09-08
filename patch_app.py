import sys

def main():
    with open("app.py", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 1. Fix duplicate aiofiles imports
    # Lines 41-45:
    # 41: import aiofiles
    # 42: from secrets import compare_digest
    # ...
    # 45: import aiofiles
    
    # We will just write a completely clean version of app.py to be safe, 
    # taking the good parts from the original.
    
    clean_lines = []
    skip = False
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # skip duplicate imports around line 41-45
        if line_num in [41, 44, 45]:
            continue
            
        # Fix _validate_and_read_json_file
        # It ends at 181. We want to append the try block from 191 to 211 right there.
        # But wait, 183-187 is read_json_file_sync. Let's just drop 183-190.
        if 183 <= line_num <= 190:
            continue
            
        # Lines 191-211 is the try block that belongs to _validate_and_read_json_file
        if 191 <= line_num <= 211:
            clean_lines.append(line)
            continue
            
        # Lines 255-283 is the floating try block. Let's drop it.
        # Line 254 is: "    return holiday_data, None, None"
        if 255 <= line_num <= 282:
            continue
            
        # Lines 662-695 is redundant parsing in combined_calendar
        # We drop these and just let it fall through to 696: ical_content = merge_calendars(user_response.text, sl_response.text)
        if 662 <= line_num <= 695:
            continue
            
        clean_lines.append(line)
        
    with open("app_fixed.py", "w", encoding="utf-8") as f:
        f.writelines(clean_lines)

if __name__ == "__main__":
    main()
