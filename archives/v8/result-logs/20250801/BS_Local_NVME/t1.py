import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the JSON
with open("BS_Local_NVME_PARSED-RESULTS.json") as f:
    data = json.load(f)

# Normalize data
rows = []
for entry in data:
    label = entry["label"]
    write = entry["writes"][0]
    read = entry["reads"][0]
    rows.append({
        "label": label,
        "type": "write",
        "iops": write["iops"],
        "latency": write["lat"],
        "mib": write["mib"]
    })
    rows.append({
        "label": label,
        "type": "read",
        "iops": read["iops"],
        "latency": read["lat"],
        "mib": read["mib"]
    })

df = pd.DataFrame(rows)

# Plot IOPS comparison
pivot = df.pivot(index='label', columns='type', values='iops')
pivot.plot(kind='bar', figsize=(18, 6), title='IOPS Comparison (Read vs Write)')
plt.ylabel("IOPS")
plt.tight_layout()
plt.show()