# Step 1: Open and read the network traffic log
with open("network_traffic.log", "r") as log_file:
    lines = log_file.readlines()

# Step 2: Count connections and collect timestamps per (source -> destination:port) pair
connections = {}

for line in lines:
    parts = line.split()
    timestamp = parts[0]
    source_ip = parts[1]
    destination = parts[3]  # IP:port after the "->"

    pair = (source_ip, destination)

    if pair not in connections:
        connections[pair] = []
    connections[pair].append(timestamp)

# Step 3: Find the pair with the most connections
top_pair = max(connections, key=lambda pair: len(connections[pair]))
top_count = len(connections[top_pair])
top_timestamps = connections[top_pair]

# Step 4: Print the beaconing suspect summary
print("=== Beaconing Suspect ===")
print(f"{top_pair[0]} -> {top_pair[1]}")
print(top_count)
print(top_timestamps)
