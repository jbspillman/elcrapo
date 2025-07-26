from datetime import datetime
import time
import json
import os

# ----- the local elbencho executables ----- 
elbencho_exe = '/usr/bin/elbencho'
elbencho_chart = '/usr/bin/elbencho-chart'

# ----- general configuration and setup -----
script_folder = os.path.dirname(os.path.abspath(__file__))

# ----- Ensure log directory exists -----
logdir = os.path.join(script_folder, "result-logs")
os.makedirs(logdir, exist_ok=True)

# ---- Ensure test directory exists ------
log_stamp = datetime.now().strftime("%Y%m%d_%H%M")


def generate_sample_data():
    testdir = os.path.join(logdir, "Chart_Sample_Data_00")
    os.makedirs(testdir, exist_ok=True)

    label_for_data = "Chart_Sample_Data_00"
    mode = "--write --read"
    iodepth = "1"
    threads = "1"
    size = "1g"
    timelimit = "900"
    
    log_stamp = "YYYYMMDD_HHMM"
    csvfile = os.path.join(testdir, f"{log_stamp}_{label_for_data}.csv")
    logfile = os.path.join(testdir, f"{log_stamp}_{label_for_data}.log")
    livecsv = os.path.join(testdir, f"{log_stamp}_{label_for_data}-live.csv")
    loglevel = "1"
    extras = "--cpu --lat --direct"
    local_ssd_path = f"/benchmark_tests/ssd/{label_for_data}.bin"  # ----- just use the local ssd file for this example. -----

    if os.path.exists(csvfile):
        return csvfile
    
    blocks_ramp = ["4K", "64K", "256K", "1M"]
    for block_size in blocks_ramp:
        example_chart_data_cmd = (
            f'{elbencho_exe} '
            f'--label {label_for_data} '
            f'{mode} '
            f'--iodepth={iodepth} '
            f'--threads={threads} '
            f'--block={block_size} '
            f'--size={size} '
            f'--timelimit {timelimit} '
            f'--live1 --livecsvex --livecsv {livecsv} '
            f'--csvfile {csvfile} '
            f'--resfile {logfile} '
            f'--log {loglevel} '
            f'{extras} '
            f'{local_ssd_path} '
        )
        os.system(example_chart_data_cmd)

    if os.path.exists(local_ssd_path):
        os.remove(local_ssd_path)
        
    return csvfile
    
    
csv_out = generate_sample_data()


list_columns = f'{elbencho_chart} -c {csv_out}'
# os.system(list_columns)
"""
 2) Generate read throughput (left y-axis) and IOPS (right y-axis) graphs for
     different blocks sizes from elbencho-results.csv:
     $ elbencho-chart -x "block size" -y "MiB/s [last]:READ" \
         -Y "IOPS [last]:READ" elbencho-results.csv
"""

chart_read_throuput = f'{elbencho_chart} -x "block size" -y "MiB/s [last]:READ" -Y "IOPS [last]:READ" {csv_out}'
print(chart_read_throuput)
os.system(chart_read_throuput)
