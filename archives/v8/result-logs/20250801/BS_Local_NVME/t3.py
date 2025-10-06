import json
import pandas as pd

# Load the updated JSON structure
with open("BS_Local_NVME_RE-PARSED_RESULTS.json") as f:
    updated_data = json.load(f)

# Convert to normalized DataFrame
updated_rows = []
for entry in updated_data:
    for io_type, record in [("write", entry["writes"][0]), ("read", entry["reads"][0])]:
        updated_rows.append({
            "label": entry["number"],
            "device": entry["device"],
            "mode": entry["mode"],
            "file_size": entry["file_size"],
            "block_size": entry["block_size"],
            "threads": entry["threads"],
            "io_depth": entry["io_depth"],
            "type": io_type,
            "iops": record["iops"],
            "latency": record["lat"],
            "mib": record["mib"]
        })

df_updated = pd.DataFrame(updated_rows)

# Recalculate groupings
grouped_mode = df_updated.groupby(['mode', 'type']).agg({'iops': 'mean', 'latency': 'mean'}).reset_index()
grouped_block = df_updated.groupby(['block_size', 'type']).agg({'iops': 'mean', 'latency': 'mean'}).reset_index()
grouped_size = df_updated.groupby(['file_size', 'type']).agg({'iops': 'mean', 'latency': 'mean'}).reset_index()

# Identify best-performing tests
best_iops_updated = df_updated.loc[df_updated.groupby('type')["iops"].idxmax()]
best_latency_updated = df_updated.loc[df_updated.groupby('type')["latency"].idxmin()]

#(grouped_mode, grouped_block, grouped_size, best_iops_updated, best_latency_updated)
print("grouped_mode")
print(grouped_mode)

print("grouped_block")
print(grouped_block)

print("grouped_size")
print(grouped_size)

print("best_iops_updated")
print(best_iops_updated)

print("best_latency_updated")
print(best_latency_updated)
