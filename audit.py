# Step 1: Open and read the log file
with open("server_access.log", "r") as log_file:
    lines = log_file.readlines()

# Step 2 & 3: Find failed logins and extract each IP address
failed_counts = {}

for line in lines:
    if "FAILED LOGIN" in line:
        # IP comes right after "from " on these log lines
        ip = line.split("from ")[1].split()[0]
        failed_counts[ip] = failed_counts.get(ip, 0) + 1

# Step 4 & 5: Sort by count (most to fewest) and print the summary
print("=== Failed Login Summary ===")

sorted_ips = sorted(failed_counts.items(), key=lambda item: item[1], reverse=True)

for ip, count in sorted_ips:
    print(f"{ip}      {count} failed attempts")
