from datetime import datetime
from itertools import product
import socket
import time
import json
import uuid
import os

# ----- general configuration and setup -----
script_folder = os.path.dirname(os.path.abspath(__file__))

# ----- installed elbencho client -----
elbencho_exe = r'C:\\Users\\spillman\\Documents\\elbencho\\elbencho.exe'
local_disk_target = r'\\beastserver.beastmode.local.net\benchmark_tests_hdd '
local_disk_folder = 'data_testing'
target_folder = os.path.join(local_disk_target, local_disk_folder)
os.makedirs(target_folder, exist_ok=True)

# ----- Ensure log directory exists -----
log_folder = os.path.join(script_folder, "result-logs")
os.makedirs(log_folder, exist_ok=True)
log_stamp = datetime.now().strftime("%Y%m%d_%H%M")
test_folder = os.path.join(log_folder, log_stamp)
os.makedirs(test_folder, exist_ok=True)

# ----- cleanup the data  -----
def cleanup_files(files_list):
    remove = 4
    y = 0
    for f_path_ddf in files_list:
        if os.path.exists(f_path_ddf):
            y += 1
            if y == remove:
                time.sleep(8)
                return files_list
            if f_path_ddf.lower().endswith('.bin'):
                print('Removing:'.ljust(30), f_path_ddf)
                os.remove(f_path_ddf)
                files_list.remove(f_path_ddf)
    return files_list


# ----- basic four corners tests -----
four_corners_tests = [
    {
        "label": "Sequential_Large_File",
        "label_code": "SLF",
        "mode": "--write --read",
        "size": "1G",
        "extras": "--cpu --lat",
    },
    {
        "label": "Random_Small_File",
        "label_code": "RSF",
        "mode": "--write --read --rand",
        "size": "32M",
        "extras": "--cpu --lat",
    }
]

# ----- default job options -----
timelimit = "1200"
loglevel = "0"

# ----- threads ramp, iodepth ramp, block size ramp -----
blocks_ramp = ["4K", "32K", "64K", "128K", "1M"]
threads_list = ["1", "4", "8", "16"]
io_deeps = ["1"]

# ----- mathy stuff -----
total_tests = sum(
    1 for _ in product(
        blocks_ramp,
        threads_list,
        io_deeps,
        four_corners_tests
    )
)
print('total_tests:'.ljust(30), total_tests)

log_level = "0"
target_file_path = 'f.bin'

# ----- housekeeping lists -----
all_tests_list = []
created_files = []

print('Using disk target of:'.ljust(30), target_folder)
test_int = 0

for block_size in blocks_ramp:               # ----- loop for each block size option -----
    for threads in threads_list:               # ----- loop for each threads size option -----
        for iodepth in io_deeps:                 # ----- loop for each iodepth option -----
            for test in four_corners_tests:        # ----- loop for each test case option -----
                label = test["label"]
                code = test["label_code"]
                mode = test["mode"]
                file_size = test["size"]
                extras = test["extras"]

                if 'Sequential' in label:
                    prefix = 'SEQ'
                else:
                    prefix = 'RAN'

                time.sleep(.33333333)
                file_stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                random_uuid = uuid.uuid4()  # Generate a random UUID object
                guid_string = str(random_uuid)  # Convert the UUID object to a string
                f_name = f"{file_stamp}".upper()  # _{guid_string}
                file_name = f'{f_name}_{code}.BIN'
                target_file_path = os.path.join(target_folder, file_name)
                if target_file_path not in created_files:
                    created_files.append(target_file_path)
                else:
                    print('ALREADY DID THIS FILE!!!'.ljust(30), target_file_path)
                    exit(1)

                # ----- repeat code to announce work being done -----
                test_int += 1
                pct_complete = (test_int / total_tests) * 100
                pct = round(pct_complete, 1)
                pct_float = str(pct).zfill(3).rjust(5)
                test_num = str(test_int).zfill(3)
                test_total = str(total_tests).zfill(3)
                res_file = os.path.join(test_folder, f"{log_stamp}_{code}.txt")
                csv_file = os.path.join(test_folder, f"{log_stamp}_{code}.csv")
                csv_live = os.path.join(test_folder, f"{log_stamp}_{code}-live.csv")

                test_all_params = {
                    "label": label,
                    "code": code,
                    "mode": mode,
                    "block_size": block_size,
                    "file_size": file_size,
                    "threads": threads,
                    "iodepth": iodepth,
                    "extras": extras
                }
                if test_all_params not in all_tests_list:
                    all_tests_list.append(test_all_params)
                else:
                    print('ALREADY DID THIS TEST!!!'.ljust(30), test_all_params)
                    exit(1)

                print()
                print('Percent Complete:'.ljust(30), f'{pct}%', f'[{test_num} of {test_total}]')
                print('Test Label:'.ljust(30), label)
                print('Test Code:'.ljust(30), code)
                print('Test Mode:'.ljust(30), mode)
                print('Using block size of:'.ljust(30), block_size)
                print('Using file size of:'.ljust(30), file_size)
                print('Using threads size of:'.ljust(30), threads)
                print('Using iodepth size of:'.ljust(30), iodepth)
                print('Extras:'.ljust(30), extras)
                print('Logging Level:'.ljust(30), log_level)
                print('Output Data File:'.ljust(30), target_file_path)
                print('Results TXT:'.ljust(30), res_file)
                print('Results CSV:'.ljust(30), csv_file)
                print('Results Live CSV:'.ljust(30), csv_live)
                print('how many files:'.ljust(30), len(created_files))

                full_cmd = (f'{elbencho_exe} '
                f'--label {label} '
                f'{mode} '
                f'--iodepth={iodepth} '
                f'--threads={threads} '
                f'--block={block_size} '
                f'--size={file_size} '
                f'--timelimit {timelimit} '
                f'--live1 --livecsvex --livecsv {csv_live} '
                f'--csvfile {csv_file} '
                f'--resfile {res_file} '
                f'--log {loglevel} '
                f'{extras} '
                f'{target_file_path} '
                )
                os.system(full_cmd)
                time.sleep(2)
                if len(created_files) >= 6:
                    created_files = cleanup_files(created_files)




print('how many files:'.ljust(30), len(created_files))
if len(created_files) > 0:
    created_files = cleanup_files(created_files)

for remaining_file in os.listdir(target_folder):
    if remaining_file.lower().endswith('.bin'):
        remainder = os.path.join(target_folder, remaining_file)
        print('Removing File:'.ljust(30), remainder)
        os.remove(remainder)


exit(0)
