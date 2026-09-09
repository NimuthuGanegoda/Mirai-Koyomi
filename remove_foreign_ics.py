import os
import glob

to_remove = [
    "SUMMARY:Halloween",
    "SUMMARY:Earth Day",
    "SUMMARY:World Food Day",
    "SUMMARY:World Environment Day",
    "SUMMARY:Valentine's Day",
    "SUMMARY:International Women's Day"
]

for file_path in glob.glob("data/holidays/ics/20*.ics"):
    if "srilanka" in file_path:
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_lines = []
    in_remove_block = False
    
    # We need to process blocks BEGIN:VEVENT to END:VEVENT
    # If the block contains a SUMMARY in to_remove, we drop the whole block.
    
    current_block = []
    for line in lines:
        current_block.append(line)
        if line.strip() == "END:VEVENT":
            # Check if this block should be removed
            should_remove = False
            for b_line in current_block:
                if any(rem in b_line for rem in to_remove):
                    should_remove = True
                    break
            
            if not should_remove:
                new_lines.extend(current_block)
            current_block = []
            
        elif line.strip() == "BEGIN:VEVENT":
            # the block starts here, so any lines before this (like BEGIN:VCALENDAR) should be added
            # actually, current_block now has BEGIN:VEVENT.
            # lines before BEGIN:VEVENT should just be added to new_lines immediately.
            # Let's refine the logic.
            pass
            
    # better logic:
    new_lines = []
    current_block = []
    in_event = False
    
    for line in lines:
        if line.strip() == "BEGIN:VEVENT":
            in_event = True
            current_block = [line]
        elif line.strip() == "END:VEVENT":
            current_block.append(line)
            in_event = False
            
            should_remove = False
            for b_line in current_block:
                if any(rem in b_line for rem in to_remove):
                    should_remove = True
                    break
            
            if not should_remove:
                new_lines.extend(current_block)
        elif in_event:
            current_block.append(line)
        else:
            new_lines.append(line)
            
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

print("Removed from ICS")
