import json
import pandas as pd
import matplotlib.pyplot as plt

# Load JSON data
with open("BS_Local_NVME_PARSED-RESULTS.json") as f:
    data = json.load(f)

# Normalize and structure the data
rows = []
for entry in data:
    label = entry["label"]
    write = entry["writes"][0]
    read = entry["reads"][0]
    for io_type, record in [("write", write), ("read", read)]:
        rows.append({
            "label": label,
            "type": io_type,
            "iops": record["iops"],
            "latency": record["lat"],
            "mib": record["mib"],
            "size": label.split('_')[3].strip('[]'),
            "block": label.split('_')[5].strip('[]'),
            "pattern": label.split('_')[1]
        })

# Convert to DataFrame
df = pd.DataFrame(rows)

# Summary of best-performing tests (highest IOPS and lowest latency)
best_iops = df.loc[df.groupby('type')["iops"].idxmax()]
best_latency = df.loc[df.groupby('type')["latency"].idxmin()]

# IOPS Comparison Chart
pivot_iops = df.pivot(index='label', columns='type', values='iops')
fig1, ax1 = plt.subplots(figsize=(20, 6))
pivot_iops.plot(kind='bar', ax=ax1, title='IOPS Comparison (Read vs Write)')
plt.ylabel("IOPS")
plt.xticks(rotation=90)
plt.tight_layout()

# Latency Comparison Chart
pivot_latency = df.pivot(index='label', columns='type', values='latency')
fig2, ax2 = plt.subplots(figsize=(20, 6))
pivot_latency.plot(kind='bar', ax=ax2, title='Latency Comparison (Read vs Write)')
plt.ylabel("Latency (µs)")
plt.xticks(rotation=90)
plt.tight_layout()

# Group by block size and summarize averages
grouped_block = df.groupby(['block', 'type']).agg({'iops': 'mean', 'latency': 'mean'}).reset_index()

# Group by test size and summarize averages
grouped_size = df.groupby(['size', 'type']).agg({'iops': 'mean', 'latency': 'mean'}).reset_index()

# (grouped_block, grouped_size, best_iops, best_latency)

print(grouped_block)
print(grouped_size)
print(best_iops)
print(best_latency)


