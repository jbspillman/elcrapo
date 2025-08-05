from jinja2 import Template
from pathlib import Path
import json
import pandas as pd

# Prepare SEQ vs RAN grouping
grouped_pattern = df.groupby(['pattern', 'type']).agg({'iops': 'mean', 'latency': 'mean'}).reset_index()

# Create an HTML report with charts and tables using Jinja2
template_str = """
<!DOCTYPE html>
<html>
<head>
    <title>Storage Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h2 { color: #2c3e50; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 30px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background-color: #f2f2f2; }
        img { max-width: 100%; height: auto; margin-bottom: 30px; }
    </style>
</head>
<body>
    <h1>Storage Performance Test Report</h1>

    <h2>IOPS Comparison</h2>
    <img src="iops_comparison.png" alt="IOPS Comparison Chart">

    <h2>Latency Comparison</h2>
    <img src="latency_comparison.png" alt="Latency Comparison Chart">

    <h2>Best-Performing Tests</h2>
    <h3>Highest IOPS</h3>
    {{ best_iops_table | safe }}
    <h3>Lowest Latency</h3>
    {{ best_latency_table | safe }}

    <h2>Average by Block Size</h2>
    {{ grouped_block_table | safe }}

    <h2>Average by Test Size</h2>
    {{ grouped_size_table | safe }}

    <h2>Average by Access Pattern (SEQ vs RAN)</h2>
    {{ grouped_pattern_table | safe }}
</body>
</html>
"""

# Helper to convert DataFrame to HTML table
def render_table(df):
    return df.to_html(index=False, classes="table table-striped", border=0)

# Render HTML with Jinja2
template = Template(template_str)
html_content = template.render(
    best_iops_table=render_table(best_iops),
    best_latency_table=render_table(best_latency),
    grouped_block_table=render_table(grouped_block),
    grouped_size_table=render_table(grouped_size),
    grouped_pattern_table=render_table(grouped_pattern)
)

# Save HTML and charts
report_path = Path("storage_test_report.html")
chart1_path = Path("iops_comparison.png")
chart2_path = Path("latency_comparison.png")

fig1.savefig(chart1_path)
fig2.savefig(chart2_path)
report_path.write_text(html_content)

report_path.name  # Return just the name for download link
