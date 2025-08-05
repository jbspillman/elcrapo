from datetime import datetime
import time
import os

# ---- the local elbencho executable -----
script_folder = os.path.dirname(os.path.abspath(__file__))
if os.name == 'nt':
    elbencho_exe = os.path.join(script_folder, 'elbencho-windows', 'elbencho.exe')
else:
    elbencho_exe = '/usr/bin/elbencho'

nt_remote_hdd = r'\\beastserver.beastmode.local.net\benchmark_tests_hdd'
nt_remote_ssd = r'\\beastserver.beastmode.local.net\benchmark_tests_ssd'

# ---- the elbencho nodes ----- 
host_servers = [
    "centos01.beastmode.local.net",
    "centos02.beastmode.local.net",
    "centos03.beastmode.local.net",
    "centos04.beastmode.local.net",
    "centos05.beastmode.local.net",
    "centos06.beastmode.local.net",
    "centos07.beastmode.local.net"
]
hosts_string = ""
for node in host_servers:
    hosts_string += f'{node},'
hosts_string = hosts_string.rstrip(',')

# threads_list = [1, 4, 8]
threads_list = [1]
# io_deeps = [1, 2, 4, 6, 8, 10, 12, 16]
io_deeps = [1]

# ---- the remote file systems ----- 
ssd_path = "/mnt/elcrapo_ssd"
hdd_path = "/mnt/elcrapo_hdd"

# remote_file_systems = [ssd_path, hdd_path]  #
remote_file_systems = [ssd_path, hdd_path]  #


# ----- Ensure log directory exists -----
logdir = os.path.join(script_folder, "result-logs")
os.makedirs(logdir, exist_ok=True)
# log_stamp = datetime.now().strftime("%Y%m%d_%H%M")
log_stamp = datetime.now().strftime("%Y%m%d_%H")
file_stamp = datetime.now().strftime("%Y%m%d%H%M%S")

def cleanup_folders(files_list):
    for f_path in files_list:
        if os.path.exists(f_path):
            print('Removing:'.ljust(30), f_path)
            os.remove(f_path)
    time.sleep(3)  # give the disk a brief relax.


four_corners_tests = [
    {
        "label": "Sequential_Write_Large_File",
        "mode": "--write",
        "block": "1M",
        "size": "256M",
        "extras": "--cpu --lat --direct",
    },
    {
        "label": "Sequential_Read_Large_File",
        "mode": "--read",
        "block": "1M",
        "size": "256M",
        "extras": "--cpu --lat --direct",
    },
    {
        "label": "Random_Write_Small_File",
        "mode": "--write --rand",
        "block": "4K",
        "size": "256M",
        "extras": "--cpu --lat --direct",
    },
    {
        "label": "Random_Read_Small_File",
        "mode": "--read --rand",
        "block": "4K",
        "size": "256M",
        "extras": "--cpu --lat --direct",
    }
]
# ----- Default Job Options -----
timelimit = "300"
loglevel = "0"

created_files = []
live_csvs = []
test_int = 0
group_int = 0

for nfs_path in remote_file_systems:
    # print(f' --> path = {nfs_path} ')
    for threads in threads_list:

        threads_str = str(threads).zfill(4)
        # print(f' ----> threads = {threads_str} ')

        for iodepth in io_deeps:
            iodepth_str = str(iodepth).zfill(4)
            # print(f' --------> iodepth = {iodepth_str} ')


            for test in four_corners_tests:
                test_int += 1
                test_number = str(test_int).zfill(4)
                test_label = test["label"]
                mode = test["mode"]
                block = test["block"]
                size = test["size"]
                extras = test["extras"]

                if nfs_path == ssd_path:
                    disk_type = 'SSD'
                else:
                    disk_type = 'HDD'

                label_f = f'{test_label}_Disk[{disk_type}]_Threads[{threads}]_IODepth[{iodepth}]_Blocks[{block}]_Size[{size}]'
                print(f' ------------> label_f = {label_f}')

                if 'Write' in test_label:
                    # set new timestamp
                    file_stamp = datetime.now().strftime("%Y%m%d%H%M%S")

                file_string = f"{file_stamp}_{threads_str}_{block}_{size}.bin"
                if 'Sequential' in test_label:
                    file_name = f"seq_{file_string}"
                else:
                    file_name = f"ran_{file_string}"


                win_s = os.path.join(nt_remote_ssd, file_name)
                win_h = os.path.join(nt_remote_hdd, file_name)
                file_path = f'{nfs_path}/{file_name}'
                # Keep a file listing to delete...
                created_files.append(file_path)
                created_files.append(win_h)
                created_files.append(win_s)

                # generic label
                # label_str = f'{test_label}_Disk[{disk_type}]_Threads[RAMP]_IODepth[RAMP]_Blocks[{block}]_Size[{size}]'
                label_str = f'{test_label}_Disk[{disk_type}]_Threads[RAMP]_IODepth[RAMP]_Blocks[RAMP]_Size[RAMP]'

                # output files
                logfile = os.path.join(logdir, f"{log_stamp}_{label_str}.log")
                csvfile = os.path.join(logdir, f"{log_stamp}_{label_str}.csv")
                livecsv = os.path.join(logdir, f"{log_stamp}_{label_str}-live.csv")
                if livecsv not in live_csvs:
                    live_csvs.append(livecsv)

                # print(' ')
                # print('-------------------------'.ljust(30), '-------------------------')
                # print('Test Group:'.ljust(30), f'{test_group}')
                # print('Test Number:'.ljust(30), f'{test_number}')
                # print('Test Label:'.ljust(30), f'{label_f}')
                # print('Test Path:'.ljust(30), f'{nfs_path}')
                # print('Test File:'.ljust(30), f'{file_name}')
                # print('Threads:'.ljust(30), f'{threads}')
                # print('Block Size:'.ljust(30), f'{block}')
                # print('File Size:'.ljust(30), f'{size}')
                # print('IO Depth:'.ljust(30), f'{iodepth}')
                # print('Log File:'.ljust(30), f'{logfile}')
                # print('CSV File:'.ljust(30), f'{csvfile}')
                # print('CSV Live File:'.ljust(30), f'{livecsv}')
                # print(' ')

                full_cmd = (f'{elbencho_exe} '
                f'--hosts {hosts_string} '
                f'--label {label_f} '
                f'{mode} '
                f'--iodepth={iodepth} '
                f'--threads={threads} '
                f'--block={block} '
                f'--size={size} '
                f'--timelimit {timelimit} '
                f'--livecsvex --liveint 1000 --live1 --livecsv {livecsv} '
                f'--csvfile {csvfile} '
                f'--resfile {logfile} '
                f'--log {loglevel} '
                f'{extras} '
                f'{file_path} '
                )
                os.system(full_cmd)

            # End of test, run cleanup.
            cleanup_folders(created_files)
            created_files = []

# ----- END OF LOOPS -----
if len(created_files) > 0:
    cleanup_folders(created_files)


for file_name in os.listdir(logdir):
    if file_name.endswith('-live.csv'):
        print(file_name)
        keep = True
    else:
        if os.path.exists(file_name):
            os.remove(file_name)


# print(' ')
# print(' ')
# print('created_files'.ljust(30), len(created_files))
# print(' ')
# print(' ')
    
# for live_csv_file in live_csvs:
#     print(live_csv_file)

            




    
            
            


                
                
                
                


    
        