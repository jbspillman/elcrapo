from datetime import datetime
import os


""" JUST RUN SOME TESTS """


elbencho_exe = '/usr/bin/elbencho'

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

remote_file_systems = ["/bench/nfs3_data", "/bench/nfs4_data"]
script_folder = os.path.dirname(os.path.abspath(__file__))

# ----- Ensure log directory exists -----
logdir = os.path.join(script_folder, "result-logs")
os.makedirs(logdir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# ----- Default Job Options -----
timelimit = "300"
loglevel = "0"

# ----- Four Corners Test Matrix -----
four_corners_tests = [
    {
        "label": "Sequential_Write_Large_File",
        "timestamp": f"{timestamp}",
        "mode": "--write",
        "threads": "8",
        "block": "1M",
        "size": "1G",
        "iodepth": "1",
        "timelimit": f"{timelimit}",
        "extras": "--cpu --lat",
    },
    {
        "label": "Sequential_Read_Large_File",
        "timestamp": f"{timestamp}",
        "mode": "--read",
        "threads": "8",
        "block": "1M",
        "size": "1G",
        "iodepth": "1",
        "timelimit": f"{timelimit}",
        "extras": "--cpu --lat",
        
    },
    {
        "label": "Random_Write_Large_File",
        "timestamp": f"{timestamp}",
        "mode": "--write --rand",
        "threads": "64",
        "block": "4K",
        "size": "1G",
        "iodepth": "1",
        "timelimit": f"{timelimit}",
        "extras": "--cpu --lat",
    },
    {
        "label": "Random_Read_Large_File",
        "timestamp": f"{timestamp}",
        "mode": "--read --rand",
        "threads": "64",
        "block": "4K",
        "size": "1G",
        "iodepth": "1",
        "timelimit": f"{timelimit}",
        "extras": "--cpu --lat",
    },
    {
        "label": "MetaData_Write_Empty_Directory",
        "timestamp": f"{timestamp}",
        "mode": "--write",
        "threads": "1",
        "block": "1M",
        "size": "0",
        "iodepth": "1",
        "files": "10000",
        "extras": "--cpu --lat --mkdirs --write --delfiles --deldirs",
        "timelimit": f"{timelimit}",
    },
    {
        "label": "Million_4K_Single_Directory",
        "timestamp": f"{timestamp}",
        "mode": "--write",
        "threads": "1",
        "block": "4k",
        "size": "4k",
        "iodepth": "1",
        "files": "1000000",
        "extras": "--cpu --lat --dirs 1 --mkdirs",
        "timelimit": "0",
    },
    
    # "extras": "--cpu --lat --dirs 1 --mkdirs --delfiles --deldirs",
    # {
        # "label": "Random_Write_Large_Directory",
        # "timestamp": f"{timestamp}",
        # "mode": "--write --rand",
        # "threads": "64",
        # "block": "4K",
        # "size": "1G",
        # "iodepth": "1",
        # "timelimit": f"{timelimit}",        
    # },    
    # {
        # "label": "Random_Read_Large_Directory",
        # "timestamp": f"{timestamp}",
        # "mode": "--read --rand",
        # "threads": "64",
        # "block": "4K",
        # "size": "1G",
        # "iodepth": "1",
        # "timelimit": f"{timelimit}",
    # }    
]
# threads = "4"  # $(nproc)
# dirs_i=1
# file_i=1
# other_params="--cpu --lat --mkdirs --nodelerr --trunctosize --direct --log 1"
# --dirsharing --nodiocheck --nofdsharing --dryrun --deldirs --delfiles

default_extra_params="--cpu --lat --direct"
folders_extra_params="--cpu --lat --mkdirs --delfiles --deldirs"
# ----- create all tests -----
x = 0
for test in four_corners_tests:       
    x += 1
    
    test_name = test["label"]
    mode = test["mode"]
    threads = test["threads"]
    block = test["block"]
    size = test["size"]
    iodepth = test["iodepth"]
    timelimit = test["timelimit"]
    
    for nfs_path in remote_file_systems:
        if 'nfs3' in nfs_path:
            label_prefix = f'NFS3'
        elif 'nfs4' in nfs_path:
            label_prefix = f'NFS4'
        else:
            label_prefix = f'XXX'
                
        logfile = os.path.join(logdir, f"{timestamp}_{label_prefix}_{test_name}.txt")
        csvfile = os.path.join(logdir, f"{timestamp}_{label_prefix}_{test_name}.csv")
        livecsv = os.path.join(logdir, f"{timestamp}_{label_prefix}_{test_name}-live.csv")
            
        label_string = f"{label_prefix}_{test_name}"

        if '_File' in label_string:
            print()
            print(f'############### {label_string} ###############')
            print()
            extra_params = f'{default_extra_params}'
            if 'Sequential' in label_string:
                nfs_path = f"{nfs_path}/sequentialfilename.bin"
            else:
                nfs_path = f"{nfs_path}/randomfilename.bin"
                
            full_cmd = (f'{elbencho_exe} '
                        f'--hosts {hosts_string} '
                        f'--label {label_string} '
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
                        f'{extra_params} '
                        f'{nfs_path} '
                        )
            os.system(full_cmd)
            print('------------------------------------------------')
        
        elif '_Directory' in label_string:
            print()
            print(f'############### {label_string} ###############')
            print()
            files_count = test["files"]
            extra_params = f'{folders_extra_params}'
            full_cmd = (f'{elbencho_exe} '
                        f'--hosts {hosts_string} '
                        f'--label {label_string} '
                        f'{mode} '
                        f'--iodepth={iodepth} '
                        f'--threads={threads} '
                        f'--block={block} '
                        f'--size={size} '
                        f'--files {files_count} '
                        f'--timelimit {timelimit} '
                        f'--live1 --livecsv {livecsv} '
                        f'--csvfile {csvfile} '
                        f'--resfile {logfile} '
                        f'--log {loglevel} '
                        f'{extra_params} '
                        f'{nfs_path}/ '
                        )
            print(full_cmd)
            os.system(full_cmd)
            print('------------------------------------------------')
