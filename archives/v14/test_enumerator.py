from helpers import *
from datetime import datetime
import shutil
import time
import os

target_name = "fNAS-2.4"
target_host = "beastserver.beastmode.local.net"
target_path = r"\\beastserver.beastmode.local.net\12000b\fNAS-2.4"
if os.name != 'nt':
    elbencho_exe = r'/usr/bin/elbencho'
else:
    elbencho_exe = r'C:\Users\spillman\elbencho\elbencho.exe'

modes = [
    {
        "operation": "SEQ Write",
        "block_size": "1M",
        "measure_in": "MiBs"
    },
    {
        "operation": "SEQ Read",
        "block_size": "1M",
        "measure_in": "MiBs"
    },
    {
        "operation": "RAN Write",
        "block_size": "4K",
        "measure_in": "IOPs",
    },
    {
        "operation": "RAN Read",
        "block_size": "4K",
        "measure_in": "IOPs",
    }
]

"""
Low-concurrency, low-latency test
This test mimics a single-threaded application that needs to perform a few I/O operations at a time.
    $ elbencho --threads 1 --iodepth 1 ...
    
High-concurrency, high-throughput test
This test uses a high iodepth to discover the maximum IOPS of a single, fast NVMe device.     
    $ elbencho --threads 1 --iodepth 64 --direct ...

High-concurrency, distributed workload
This test simulates multiple users or processes hammering the storage system simultaneously.
    $ elbencho --threads 32 --iodepth 16 ...
"""

""" 

Sequentially write 4 large files
    $ elbencho -w -b 4M -t 16 --direct -s 20g "/mnt/myfs/file[1-4]"

Test random read IOPS for max 20 seconds:
    $ elbencho -r -b 4k -t 16 --iodepth 16 --direct --rand --timelimit 20 "/mnt/myfs/file[1-4]"

Test 4KiB multi-threaded write IOPS of devices /dev/nvme0n1 & /dev/nvme1n1:
    $ elbencho -w -b 4K -t 16 --iodepth 16 --direct --rand /dev/nvme0n1 /dev/nvme1n1

Test 4KiB block random read latency of device /dev/nvme0n1:
    $ elbencho -r -b 4K --lat --direct --rand /dev/nvme0n1
    
Small Block Performance
By default, elbencho will use a 1MiB block size (fio’s default block size is 8k!). We can specify a smaller block size to simulate other workloads:    
    # 8k blocks
    $ elbencho --write --read --size 20G --direct --threads $(nproc) --iodepth 16 --block 8k /mnt/vast/elbencho-files/file
    
Small File Performance
elbencho can be used to generate many small files in different directories as well. 
Use --dryrun to make sure you will be generating the number of files that you expect before you run it!
    # note that we're passing elbencho a directory!
    $ elbencho  --write --read --mkdirs --delfiles --deldirs --size 4k --files 100 --dirs 1000 --threads 32 --direct /mnt/vast/elbencho-files/
       
Metadata Performance
elbencho can be used to generate some high-level metadata numbers by reading and writing zero-length files. 
To ensure that we bypass the client-side cache, we need to use --sync and --dropcache, which requires us running it as root.    
    # note that we're passing elbencho a directory! 
    $ elbencho --sync --dropcache --mkdirs --write --stat --read --delfiles --deldirs --block 0k --size 0k --files 100 --dirs 1000 --threads 32 --direct /mnt/vast/elbencho-files/
    
"""

date_stamp = datetime.now().strftime("%Y%m%d")
file_stamp = datetime.now().strftime("%H.%M.%S")
script_folder = os.path.dirname(os.path.abspath(__file__))

results_folder = os.path.join(script_folder, "test_results", f'{date_stamp}_{file_stamp}')
os.makedirs(results_folder, exist_ok=True)

target_safe_path = os.path.join(target_path, 'bench')
os.makedirs(target_safe_path, exist_ok=True)

threads_list = [1, 16, 32]
io_depth_list = [1, 2, 4]
i = 0
for mode in modes:

    for thread in threads_list:
        for io_depth in io_depth_list:
            if os.name == 'nt':
                io_depth = 1

            tpd = str(thread).zfill(2)
            iod = str(io_depth).zfill(2)
            i += 1
            zi = str(i).zfill(3)
            operation = mode["operation"]
            block_size = "4K"
            size = "1M"
            files_count = 1
            folders_count = 1
            live_int = 500
            time_limit = 300
            log_level = 1

            if operation == "SEQ Write":
                size = "512M"
                block_size = "1M"
                test_label = f'{zi}_{target_name}_{operation}_{size}B_{block_size}_{tpd}T'
                csv_file = os.path.join(results_folder, f'{test_label}.csv')
                txt_file = os.path.join(results_folder, f'{test_label}.txt')
                csv_live = os.path.join(results_folder, f'{test_label}.live.txt')
                if os.path.exists(csv_file):
                    continue
                file_string = f"{tpd}Tx{iod}D"
                safe_path = os.path.join(target_safe_path, file_string)

                print(f'[{zi}]'.ljust(30), f'{target_name} {operation} {size}')
                print(f'      '.ljust(30), f'{block_size}B x {tpd}TH x {iod}ID')
                print(f'      '.ljust(30), csv_file)
                print(f'      '.ljust(30), txt_file)
                print(f'      '.ljust(30), csv_live)
                print(f'      '.ljust(30), safe_path)
                job_options = [
                    f'label "{test_label}"',
                    f'write',
                    f'size="{size}"',
                    f'threads="{thread}"',
                    f'block="{block_size}"',
                    f'iodepth="{io_depth}"',
                    f'cpu',
                    f'lat',
                    f'direct',
                    f'live1',
                    # f'livecsvex',
                    # f'csvfile "{csv_file}"',
                    # f'resfile "{txt_file}"',
                    # f'livecsv "{csv_live}"',
                    # f'liveint "{live_int}"',
                    # f'log "{log_level}"',
                    f'timelimit "{time_limit}"'
                ]
                delimiter = " --"
                joined_string = delimiter.join(job_options)
                job_copy_string = joined_string.lstrip()
                full_command = f'{elbencho_exe} {job_copy_string} "{safe_path}[1-4]"'
                os.system(full_command)
                time.sleep(5)
                safe_path = ""


                exit(0)