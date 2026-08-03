from datetime import datetime

# Step 1: Read all lines from both log files
with open("auth_events.log", "r") as auth_file:
    auth_lines = auth_file.readlines()

with open("file_events.log", "r") as file_file:
    file_lines = file_file.readlines()

# Step 2: Merge events from both files into one list
events = auth_lines + file_lines

# Step 3: Sort events chronologically by the date/time at the start of each line
events.sort(key=lambda line: datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S"))

# Step 4: Print the unified timeline, marking key events
print("=== Unified Timeline ===")
for line in events:
    line = line.rstrip("\n")
    if "SUCCESS LOGIN" in line or ".locked" in line or "READ_ME" in line:
        print(f"*** KEY EVENT *** {line}")
    else:
        print(line)
