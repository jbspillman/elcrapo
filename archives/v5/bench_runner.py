from datetime import datetime
from itertools import product
import socket
import time
import json
import uuid
import os

"""
probably the simplest version yet..... 
Use the SetUp.sh script to help this ....
echo " ########## MENU ##########   "
echo " Ping Hosts      :     1      "
echo " Start Hosts     :     2      "
echo " Start Services  :     3      "
echo " Stop Services   :     4      "
echo " Mount Paths     :     5      "
echo " UnMount Paths   :     6      "
echo " Reboot Hosts    :     7      "
echo " Shutdown Hosts  :     8      "
echo " ##########################   "
"""


# ----- the remote file systems ----- 
ssd_path = "/mnt/elcrapo_ssd"
hdd_path = "/mnt/elcrapo_hdd"
remote_file_systems = [ssd_path]  # hdd_path

hostname = socket.gethostname()
if hostname == "beastserver":
    local_ssd_path="/benchmark_tests/ssd"
    local_hdd_path="/mnt/Drives/12000a/benchmark_tests/hdd"
else:
    local_ssd_path="/mnt/elcrapo_ssd"
    local_hdd_path="/mnt/elcrapo_hdd"

# ----- the local elbencho executable ----- 
elbencho_exe = '/usr/bin/elbencho'

# ----- the elbencho nodes ----- 
host_servers = [
    "centos01.beastmode.local.net",
    "centos02.beastmode.local.net",
    "centos03.beastmode.local.net",
    "centos04.beastmode.local.net",
    # "centos05.beastmode.local.net",
    # "centos06.beastmode.local.net",
    # "centos07.beastmode.local.net",
]
hosts_string = ""
for node in host_servers:
    hosts_string += f'{node},'
hosts_string = hosts_string.rstrip(',')
total_nodes=len(host_servers)

# ----- general configuration and setup -----
script_folder = os.path.dirname(os.path.abspath(__file__))

# ----- Ensure log directory exists -----
logdir = os.path.join(script_folder, "result-logs")
os.makedirs(logdir, exist_ok=True)
log_stamp = datetime.now().strftime("%Y%m%d_%H%M")
testdir = os.path.join(logdir, log_stamp)
os.makedirs(testdir, exist_ok=True)

# ----- cleanup the data  -----
def cleanup_folders(files_list):   
    
    for f_name in files_list:

        f_path_ddf = os.path.join(local_ssd_path, f_name)
        if os.path.exists(f_path_ddf):
            print('Removing:'.ljust(30), f_path_ddf)
            os.remove(f_path_ddf)
            
        f_path_ddf = os.path.join(local_hdd_path, f_name)
        if os.path.exists(f_path_ddf):
            print('Removing:'.ljust(30), f_path_ddf)
            os.remove(f_path_ddf)
            

# ----- basic four corners tests -----
four_corners_tests = [
    {
        "label": "Sequential_Write_LargeFile",
        "label_code": "SW_LF",
        "mode": "--write",
        "size": "1G",
        "extras": "--cpu --lat --direct",
    },
    {
        "label": "Sequential_Read_LargeFile",
        "label_code": "SR_LF",
        "mode": "--read",
        "block": "1M",
        "size": "1G",
        "extras": "--cpu --lat --direct",
    },
    {
        "label": "Random_Write_SmallFile",
        "label_code": "RW_SF",
        "mode": "--write --rand",
        "size": "64M",
        "extras": "--cpu --lat --direct",
    },
    {
        "label": "Random_Read_SmallFile",
        "label_code": "RR_SF",
        "mode": "--read --rand",
        "size": "64M",
        "extras": "--cpu --lat --direct",
    }
]
# ----- split these out if you want to do them in different order -----
sequential_tests = []
random_tests = []
for test in four_corners_tests:
    if "Sequential" in test["label"]:
        sequential_tests.append(test)
    elif "Random" in test["label"]:   
        random_tests.append(test) 


# ----- default job options -----
timelimit = "300"
loglevel = "0"
block_size = "4K"
threads = "1"
iodepth = "1"

# ----- threads ramp, iodepth ramp, block size ramp -----
blocks_ramp = ["4K", "8K", "16K", "32K", "64K", "128K", "256K", "512K", "1M"]
threads_list = ["1"]
io_deeps = ["1"]


# ----- housekeeping lists -----
created_files = []
live_csvs = []
test_int = 0
group_int = 0


# ----- if you only want a cetain test list -----
test_mode = "seq"  # "seq", "ran"
if test_mode == "all":
    test_list = four_corners_tests
elif test_mode == "seq":
    test_list = sequential_tests
elif test_mode == "ran":
    test_list = random_tests
else:
    test_list = four_corners_tests


# ----- mathy stuff -----
total_tests = sum(
    1 for _ in product(
        remote_file_systems,
        blocks_ramp,
        threads_list,
        io_deeps,
        test_list
    )
)

# ----- loop for each nfs path -----
for nfs_path in remote_file_systems:

    # ----- loop for each block size option -----
    for block_size in blocks_ramp:
        bs_str = block_size.rjust(4)
        group_int += 1
        test_group = str(group_int).zfill(4)
        print()

        # ----- loop for each threads option -----
        for threads in threads_list:
            threads_str = str(threads).zfill(4)

            # ----- loop for each iodepth option -----
            for iodepth in io_deeps:
                iodepth_str = str(iodepth).zfill(4)

                # ----- loop for each test job -----
                file_stamp = None
                for test in test_list:
                    test_int += 1
                    test_number = str(test_int).zfill(4)

                    pct_complete = (test_int / total_tests) * 100
                    pct = round(pct_complete, 1)
                    pct_float = str(pct).zfill(3).rjust(5)

                    test_label = test["label"]
                    label_code = test["label_code"]
                    mode = test["mode"]
                    size = test["size"]
                    extras = test["extras"]
                    size_str = size.rjust(4)

                    if 'Sequential' in test_label:
                        prefix = 'SEQ'
                    else:
                        prefix = 'RAN'

                    if str('write').lower() in test_label.lower(): # set new timestamp
                        time.sleep(1.01)
                        file_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
                        # Generate a random UUID object
                        random_uuid = uuid.uuid4()
                        # Convert the UUID object to a string
                        guid_string = str(random_uuid)
                        f_name = f"{log_stamp}_{guid_string}".upper()
                        file_name = f'{f_name}.BIN'
                        
                    if 'ssd' in nfs_path:
                        disk_type = 'SSD'
                    else:
                        disk_type = 'HDD'
                        
                    
                    tgt_file_path = f'{nfs_path}/{file_name}'
                    created_files.append(file_name)
                    
                    label_for_files = f'{label_code}_{disk_type}_RampTest'
                    label_for_data = f'{label_code}_HOSTS[{total_nodes}]_THREADS[{threads}]_BLOCKSIZE[{block_size}]_FILESIZE[{size}]_IODEPTH[{iodepth}]'
                   
                    logfile = os.path.join(testdir, f"{log_stamp}_{label_for_files}.log")
                    csvfile = os.path.join(testdir, f"{log_stamp}_{label_for_files}.csv")
                    livecsv = os.path.join(testdir, f"{log_stamp}_{label_for_files}-live.csv")
                    if livecsv not in live_csvs:
                        live_csvs.append(livecsv)
            
                    print(' ')
                    print('--------------------------'.ljust(30), '--------------------------')
                    print('Percent Complete:'.ljust(30), f'{pct}%')
                    print('Test Group:'.ljust(30), f'{test_group}')
                    print('Test Number:'.ljust(30), f'{test_int} of {total_tests}')
                    print('Label:'.ljust(30), f'{test_label}')
                    print('Data:'.ljust(30), f'{label_for_data}')
                    print('Test Code:'.ljust(30), f'{label_code}')
                    print('Disk Type:'.ljust(30), f'{disk_type}')
                    print('Test Path:'.ljust(30), f'{nfs_path}')
                    print('Test File:'.ljust(30), f'{file_name}')
                    print('Threads:'.ljust(30), f'{threads}')
                    print('Block Size:'.ljust(30), f'{block_size}')
                    print('File Size:'.ljust(30), f'{size}')
                    print('IO Depth:'.ljust(30), f'{iodepth}')
                    print('Log File:'.ljust(30), f'{logfile}')
                    print('CSV File:'.ljust(30), f'{csvfile}')
                    print('CSV Live File:'.ljust(30), f'{livecsv}')
                    print(' ')

                    full_cmd = (f'{elbencho_exe} '
                    f'--hosts {hosts_string} '
                    f'--label {label_for_data} '
                    f'{mode} '
                    f'--iodepth={iodepth} '
                    f'--threads={threads} '
                    f'--block={block_size} '
                    f'--size={size} '
                    f'--timelimit {timelimit} '
                    f'--live1 --livecsvex --livecsv {livecsv} '  #
                    f'--csvfile {csvfile} '
                    f'--resfile {logfile} '
                    f'--log {loglevel} '
                    f'{extras} '
                    f'{tgt_file_path} '
                    )
                                        
                    os.system(full_cmd)
                    time.sleep(5)  # let disk activity come to halt.
                    
        # ----- end of test, run cleanup -----
        if len(created_files) > 0:
            cleanup_folders(created_files)
            created_files = []

time.sleep(10)  # let disk activity come to halt.
if len(created_files) > 0:
    cleanup_folders(created_files)

