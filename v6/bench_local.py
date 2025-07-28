from datetime import datetime
from itertools import product
import time
import uuid
import os

"""
Tool assumes the access to remote folders exist from this node and nodes running the tests.
Whether this be Windows Shares or NFS Mounts.
Also assumes the elbencho client has been installed or extracted to the given path.
"""

test_id = 'beastserver_smb_nvme'  # string of text to denote what version or model we are testing.

# ----- general configuration of folder and file paths, command server, and nodes. -----
script_folder = os.path.dirname(os.path.abspath(__file__))

if os.name == 'nt':
    # ----- do the windows version tests -----
    elbencho_exe = r'C:\\Users\\spillman\\elbencho\\elbencho.exe'
    if not os.path.exists(elbencho_exe):
        print(f'elbencho not found at: {elbencho_exe}')
        exit(1)
    target_paths = [
        r'\\beastserver.beastmode.local.net\benchmark_tests_ssd',
    ]
else:
    # ----- do the unix version tests -----
    elbencho_exe = '/usr/bin/elbencho'
    if not os.path.exists(elbencho_exe):
        print(f'elbencho not found at: {elbencho_exe}')
        exit(1)
    target_paths = [
        "/mnt/elcrapo_ssd",
    ]

# ----- create new list of target folders  -----
target_test_folders = []
target_folder = 'data_testing'
for target_path in target_paths:
    tt_path = os.path.join(target_path, target_folder)
    os.makedirs(tt_path, exist_ok=True)
    target_test_folders.append(tt_path)

# ----- ensure log directory exists -----
log_folder = os.path.join(script_folder, "result-logs")
os.makedirs(log_folder, exist_ok=True)
time_log_stamp = datetime.now().strftime("%Y%m%d_%H%M")
date_log_stamp = datetime.now().strftime("%Y%m%d")
log_stamp = f'{date_log_stamp}_{test_id}'.upper()
test_folder = os.path.join(log_folder, log_stamp)
os.makedirs(test_folder, exist_ok=True)

# ----- basic four corners tests, two tests but each does write & read operations -----
four_corners_tests = [
    {
        "label": "Sequential_Large_File",
        "label_code": "SEQ_LF",
        "mode": "--write --read",
        "size": "1G",
        "extras": "--cpu --lat",
    },
    {
        "label": "Random_Small_File",
        "label_code": "RAN_SF",
        "mode": "--write --read --rand",
        "size": "64M",
        "extras": "--cpu --lat",
    }
]

# ----- default job options -----
timelimit = "1200"
log_level = "1"
target_file_path = 'f.bin'  # important to leave as bin file, cleanup job is looking for this!

# ----- threads ramp, iodepth ramp, block size ramp -----
# blocks_ramp = ["4K", "32K", "64K", "128K", "1M"]
blocks_ramp = ["4K", "64K", "1M"]
threads_list = ["1", "16"]
io_deeps = ["1"]

# ----- compute test counts -----
total_tests = sum(
    1 for _ in product(
        target_test_folders,
        blocks_ramp,
        threads_list,
        io_deeps,
        four_corners_tests
    )
)

# ----- cleanup the created files -----
def cleanup_files(files_list, remove=6):
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

# ----- housekeeping  -----
all_tests_list = []
created_files = []
test_int = 0

for block_size in blocks_ramp:                 # ----- loop for each block size option -----
    for threads in threads_list:                 # ----- loop for each threads size option -----
        for iodepth in io_deeps:                   # ----- loop for each iodepth option -----
            for test_path in target_test_folders:    #  ----- loop for each folder path option -----
                for test in four_corners_tests:        # ----- loop for each test case option -----
                    t_label = test["label"]
                    code = test["label_code"]
                    mode = test["mode"]
                    file_size = test["size"]
                    extras = test["extras"]

                    label = f"{code}_{test_id}"

                    # ----- create a randomized file name -----
                    time.sleep(.1313)
                    file_stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    random_uuid = uuid.uuid4()  # Generate a random UUID object
                    guid_string = str(random_uuid)  # Convert the UUID object to a string
                    f_name = f"{file_stamp}".upper()  # _{guid_string}
                    file_name = f'{f_name}_{code}.BIN'
                    test_file_path = os.path.join(test_path, file_name)
                    if test_file_path not in created_files:
                        created_files.append(test_file_path)
                    else:
                        print('ALREADY DID THIS FILE!!!'.ljust(30), test_file_path)
                        exit(1)

                    # ----- repeat code to announce work being done -----
                    test_int += 1
                    pct_complete = (test_int / total_tests) * 100
                    pct = round(pct_complete, 1)
                    pct_float = str(pct).zfill(3).rjust(5)
                    test_num = str(test_int).zfill(3)
                    test_total = str(total_tests).zfill(3)

                    test_file_name = f'test_number-{test_num}'
                    res_file = os.path.join(test_folder, f"{test_file_name}_results.txt")
                    csv_file = os.path.join(test_folder, f"{test_file_name}.csv")
                    csv_live = os.path.join(test_folder, f"{test_file_name}-live.csv")

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
                    print('Output Data File:'.ljust(30), test_file_path)
                    print('Results TXT:'.ljust(30), res_file)
                    print('Results CSV:'.ljust(30), csv_file)
                    print('Results Live CSV:'.ljust(30), csv_live)
                    print('how many files:'.ljust(30), len(created_files))

                    test_all_params = {
                        "label": test_id,
                        "code": code,
                        "mode": mode,
                        "block_size": block_size,
                        "file_size": file_size,
                        "threads": threads,
                        "iodepth": iodepth,
                        "extras": extras,
                        "test_file_path": test_file_path
                    }
                    if test_all_params not in all_tests_list:
                        all_tests_list.append(test_all_params)
                    else:
                        print('ALREADY DID THIS TEST!!!'.ljust(30), test_all_params)
                        exit(1)

                    full_cmd = (f'{elbencho_exe} '
                    f'--label {test_id} '
                    f'{mode} '
                    f'--iodepth={iodepth} '
                    f'--threads={threads} '
                    f'--block={block_size} '
                    f'--size={file_size} '
                    f'--timelimit {timelimit} '
                    f'--live1 --livecsvex --livecsv {csv_live} '
                    f'--csvfile {csv_file} '
                    f'--resfile {res_file} '
                    f'--log {log_level} '
                    f'{extras} '
                    f'{test_file_path} '
                    )
                    os.system(full_cmd)
                    # time.sleep(1)
                    if len(created_files) >= 6:
                        created_files = cleanup_files(created_files)


if len(created_files) > 0:
    created_files = cleanup_files(created_files, 99)
if len(created_files) > 0:
    created_files = cleanup_files(created_files, 99)



exit(0)
