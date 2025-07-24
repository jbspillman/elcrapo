from datetime import datetime
import time
import json
import os

# ---- the local elbencho executable ----- 
elbencho_exe = '/usr/bin/elbencho'

# ---- the elbencho nodes ----- 
host_servers = [
    "centos01.beastmode.local.net",
    "centos02.beastmode.local.net",
    "centos03.beastmode.local.net",
    "centos04.beastmode.local.net",
    "centos05.beastmode.local.net",
    "centos06.beastmode.local.net",
]
hosts_string = ""
for node in host_servers:
    hosts_string += f'{node},'
hosts_string = hosts_string.rstrip(',')

threads_list = [1, 2, 4, 8, 16, 32, 64]
threads_list = [1, 2]


# ---- the remote file systems ----- 
ssd_path = "/mnt/elcrapo_ssd"
hdd_path = "/mnt/elcrapo_hdd"

remote_file_systems = [ssd_path, hdd_path]  #  
script_folder = os.path.dirname(os.path.abspath(__file__))

# ----- Ensure log directory exists -----
logdir = os.path.join(script_folder, "result-logs")
os.makedirs(logdir, exist_ok=True)
log_stamp = datetime.now().strftime("%Y%m%d_%H%M")




def cleanup_folders(files_list):
    for f_path in files_list:
        print('If File Exists, Removing:'.ljust(30), f_path)
        if os.path.exists(f_path):
            print('Removing:'.ljust(30), f_path)
        time.sleep(2)


four_corners_tests = [
    {
        "label": "Sequential_Write_Large_File",
        "mode": "--write",
        "block": "1M",
        "size": "1G",
        "iodepth": "1",
        "extras": "--cpu --lat --direct",
    },
    {
        "label": "Sequential_Read_Large_File",
        "mode": "--read",
        "block": "1M",
        "size": "1G",
        "iodepth": "1",
        "extras": "--cpu --lat --direct",
        
    },
    {
        "label": "Random_Write_Small_File",
        "mode": "--write --rand",
        "block": "4K",
        "size": "1G",
        "iodepth": "1",
        "extras": "--cpu --lat --direct",        
    },    
    {
        "label": "Random_Read_Small_File",
        "mode": "--read --rand",
        "block": "4K",
        "size": "1G",
        "iodepth": "1",
        "extras": "--cpu --lat --direct",
    }
]
# ----- Default Job Options -----
timelimit = "600"
loglevel = "0"


created_files = []
live_csvs = []
test_int = 0
group_int = 0

for nfs_path in remote_file_systems:
    print()
    print('-------------------------'.ljust(30), '-------------------------')
    
    for threads in threads_list:
    
        group_int += 1
        threads_str = str(threads).zfill(4)   
        test_group = str(group_int).zfill(4)
    
        for test in four_corners_tests:
            
            test_int += 1
            test_number = str(test_int).zfill(4)
            
            test_label = test["label"]
            mode = test["mode"]
            block = test["block"]
            size = test["size"]
            iodepth = test["iodepth"]
            extras = test["extras"]
            
            if 'Write' in test_label:
                # set new timestamp
                file_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
                
            file_string = f"{file_stamp}_{threads_str}_{block}_{size}.bin"
            if 'Sequential' in test_label:
                file_name = f"seq_{file_string}"
            else:
                file_name = f"ran_{file_string}"
                
            file_path = f'{nfs_path}/{file_name}'
            if file_path not in created_files:
                created_files.append(file_path)

            if nfs_path == ssd_path:
                disk_type = 'SSD'
            else:
                disk_type = 'HDD'
            
            label_str = f'{test_label}_Disk[{disk_type}]_Threads[{threads}]_Blocks[{block}]_Size[{size}]'
            
            logfile = os.path.join(logdir, f"{log_stamp}_{label_str}.log")
            csvfile = os.path.join(logdir, f"{log_stamp}_{label_str}.csv")
            livecsv = os.path.join(logdir, f"{log_stamp}_{label_str}-live.csv")
            if livecsv not in live_csvs:
                live_csvs.append(livecsv)
            
            print(' ')
            print('-------------------------'.ljust(30), '-------------------------')
            print('Test Group:'.ljust(30), f'{test_group}')
            print('Test Number:'.ljust(30), f'{test_number}')
            print('Test Label:'.ljust(30), f'{label_str}')
            print('Test Path:'.ljust(30), f'{nfs_path}')
            print('Test File:'.ljust(30), f'{file_name}')
            print('Threads:'.ljust(30), f'{threads}')
            print('Block Size:'.ljust(30), f'{block}')
            print('File Size:'.ljust(30), f'{size}')
            print('IO Depth:'.ljust(30), f'{iodepth}')
            print('Log File:'.ljust(30), f'{logfile}')
            print('CSV File:'.ljust(30), f'{csvfile}')
            print('CSV Live File:'.ljust(30), f'{livecsv}')
            print(' ')
            
            full_cmd = (f'{elbencho_exe} '
            f'--hosts {hosts_string} '
            f'--label {label_str} '
            f'{mode} '
            f'--iodepth={iodepth} '
            f'--threads={threads} '
            f'--block={block} '
            f'--size={size} '
            f'--timelimit {timelimit} '
            f'--live1 --livecsv {livecsv} '
            f'--csvfile {csvfile} '
            f'--resfile {logfile} '
            f'--log {loglevel} '
            f'{extras} '
            f'{file_path} '
            )
            os.system(full_cmd)
            print('------------------------------------------------')
            
            time.sleep(.2)
        
        # End of test, run cleanup.
        print(f'END OF TEST GROUP:'.ljust(30), test_group)
        if len(created_files) > 0:
            cleanup_folders(created_files)
            created_files = []
        time.sleep(1)
        
    
    if group_int != len(threads_list):
        print(' ')
        print('#######################'.ljust(30), '#######################')
        print('Doubling thread count:'.ljust(30), f'{threads} -> {threads * 2} ')
        print('#######################'.ljust(30), '#######################')
        print(' ')
        time.sleep(2)

       
# ----- END OF LOOPS -----       
       
print(' ')
print(' ')    
print('created_files'.ljust(30), len(created_files))
print(' ')
print(' ')
    
for live_csv_file in live_csvs:
    print(live_csv_file)

            




    
            
            


                
                
                
                


    
        