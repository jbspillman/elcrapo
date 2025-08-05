from datetime import datetime
from itertools import product
# import uuid
import json
import time
import os

''' default top level folder '''
script_folder = os.path.dirname(os.path.abspath(__file__))

''' arguments to perform system checks '''
check_local_paths = False
check_nfs_paths = False
mount_nfs_clients = False
unmount_nfs_clients = False
check_elbencho = False
run_the_tool = True


def create_nodes_lists():
    t_elbencho_nodes_list = []
    t_el_hosts = ""
    elbencho_nodes_text = os.path.join(script_folder, 'host_list.txt')
    if not os.path.exists(elbencho_nodes_text):
        t_elbencho_nodes_list = [
            "centos01.beastmode.local.net",
            "centos02.beastmode.local.net",
            "centos03.beastmode.local.net",
            "centos04.beastmode.local.net"
        ]
        t_el_hosts = ""
        for ix in t_elbencho_nodes_list:
            t_el_hosts += f'{ix},'
        t_el_hosts = t_el_hosts.rstrip(',')
        return t_el_hosts, t_elbencho_nodes_list

    else:
        with open(elbencho_nodes_text, 'r', encoding="utf-8") as input:
            nodes = input.read()
            for ix in nodes.split('\n'):
                ix = ix.strip()
                if ix:
                    if not ix.startswith('#'):
                        t_el_hosts += f'{ix},'
                        t_elbencho_nodes_list.append(ix)
        t_el_hosts = t_el_hosts.rstrip(',')
        return t_el_hosts, t_elbencho_nodes_list


def create_benchmark_targets():
    the_benchtest_targets = [
        {
            "test_id": 'V01_NVME',
            "command_server_disk_path": '/benchmark_tests/nvme',
            "nfs_server_name": 'beastserver.beastmode.local.net',
            "nfs_server_export_path": '/benchmark_tests/nvme',
            "mount_to_folder": '/mnt/benchmark_tests/nvme',
            "nfs_client_mount_options": '-o vers=3,rsize=131072,wsize=131072,hard,intr'
        },
        {
            "test_id": 'V02_HDD1',
            "command_server_disk_path": '/mnt/Drives/12000a/benchmark_tests/hdd',
            "nfs_server_name": 'beastserver.beastmode.local.net',
            "nfs_server_export_path": '/mnt/Drives/12000a/benchmark_tests/hdd',
            "mount_to_folder": '/mnt/benchmark_tests/hdd1',
            "nfs_client_mount_options": '-o vers=3,rsize=131072,wsize=131072,hard,intr'
        },
        {
            "test_id": 'V03_HDD2',
            "command_server_disk_path": '/mnt/Drives/ms_02000a/benchmark_tests/hdd',
            "nfs_server_name": 'mediaserver.beastmode.local.net',
            "nfs_server_export_path": '/mnt/Drives/02000a/benchmark_tests/hdd',
            "mount_to_folder": '/mnt/benchmark_tests/hdd2',
            "nfs_client_mount_options": '-o vers=3,rsize=131072,wsize=131072,hard,intr'
        }
    ]
    return the_benchtest_targets


def create_local_tools():
    t_elbencho_exe = '/usr/bin/elbencho'
    if not os.path.exists(t_elbencho_exe):
        print(f'elbencho not found at: {t_elbencho_exe}')
        exit(1)

    t_ssh_exe = '/usr/bin/sshpass'
    if not os.path.exists(t_ssh_exe):
        print(f'ssh_pass not found at: {t_ssh_exe}')
        exit(2)

    generic_creds = '/home/spillman/.config/generic.json'
    if not os.path.exists(generic_creds):
        print(f'creds not found at: {generic_creds}')
        exit(3)

    t_ssh_w_psw = f"{t_ssh_exe} -f {generic_creds} ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no -l"
    return t_elbencho_exe, t_ssh_w_psw


def check_local_drives(n_server_paths):
    all_paths_checker = True
    for item in n_server_paths:
        my_local_path = item["command_server_disk_path"]
        if os.path.exists(my_local_path):
            skip = True
            # print('my_local_path exists:'.ljust(30), my_local_path)
        else:
            print('my_local_path does not exist:'.ljust(30), my_local_path)
            all_paths_checker = False
            exit(911)

    return all_paths_checker


def nfs_check_drives(n_hosts, n_server_paths, ssh_w_psw):
    local_nfs_paths = []
    for item in n_server_paths:
        nfs_export_path = item["nfs_server_export_path"]
        local_nfs_paths.append(nfs_export_path)

    for node in n_hosts:
        print()
        print('Checking Node:'.ljust(30), node)

        with os.popen(f'{ssh_w_psw} root {node} "df -h" 2>&1') as f:
            dfh_output = f.read()

        how_many_nfs = len(local_nfs_paths)
        how_many = 0
        for line in dfh_output.split('\n'):
            line = line.rstrip()
            if line:
                for np in local_nfs_paths:
                    if np in line:
                        lpath = line.split(" ")[-1]
                        ndir = os.path.join(lpath, 'data_testing')
                        with os.popen(f'{ssh_w_psw} root {node} "mkdir -p {ndir}" 2>&1') as f:
                            ndir_output = f.read()
                        print(f' ndir_output: [{ndir_output}]')
                        how_many += 1

        if mount_nfs_clients and how_many != how_many_nfs:
            print('  Found:', how_many, "of", how_many_nfs)
            print(f'   Create the nfs mount paths on:'.ljust(30), node)
            nfs_mount_drive(node, n_server_paths, ssh_w_psw)

        else:
            print('found:', how_many, "of", how_many_nfs)


def nfs_unmount_drive(n_hosts, n_server_paths, ssh_w_psw):
    for node in n_hosts:
        print()
        print('Checking Node:'.ljust(30), node)
        for item in n_server_paths:
            nfs_export_path = item["nfs_server_export_path"]
            mount_to_folder = item["mount_to_folder"]
            print('  Checking Mount:', mount_to_folder)
            with os.popen(f'{ssh_w_psw} root {node} "df -h" | grep {nfs_export_path} 2>&1') as f:
                output = f.read()
            if ':/' in output:
                lpath = output.split(" ")[-1]
                print('  Attempting UnMount of:'.ljust(30), output)
                with os.popen(f'{ssh_w_psw} root {node} "umount -fl {lpath}" 2>&1') as f:
                    unmount_output = f.read()
                unmount_output = unmount_output.strip()
                print(f"  UnMmount Status: [{unmount_output}]")


def nfs_mount_drive(n_host, n_server_paths, ssh_w_psw):
    print()
    print('Mounting NFS on Node:'.ljust(30), n_host)
    for item in n_server_paths:
        nfs_svr = item["nfs_server_name"]
        nfs_exp =  item["nfs_server_export_path"]
        lcl_disk = item["mount_to_folder"]
        mnt_opts = item["nfs_client_mount_options"]

        with os.popen(f'{ssh_w_psw} root {n_host} "mkdir -p {lcl_disk}" 2>&1') as f:
            mkdir_output = f.read()
        print(f'  mkdir:  [{mkdir_output}]')

        with os.popen(f'{ssh_w_psw} root {n_host} "chmod -R 777 {lcl_disk}" 2>&1') as f:
            chmod_output = f.read()
        print(f'  chmod:  [{chmod_output}]')

        mnt_path_command = f'mount -t nfs {mnt_opts} {nfs_svr}:{nfs_exp} {lcl_disk}'
        with os.popen(f'{ssh_w_psw} root {n_host} "{mnt_path_command}" 2>&1') as f:
            mnt_output = f.read()
        print(f'  mount:  [{mnt_output}]')


def check_service_status(n_hosts, ssh_w_psw):
    for node in n_hosts:
        print()
        print('Checking Node for service status:'.ljust(30), node)
        with os.popen(f'{ssh_w_psw} root {node} "which elbencho" 2>&1') as f:
            output = f.read()
            if 'elbencho' in output:
                el_exe = output.strip()
                start_it = f"{el_exe} --service"
                with os.popen(f'{ssh_w_psw} root {node} "{start_it}" 2>&1') as f:
                    el_service = f.read()
                if 'SysErr: Address in use' in el_service:
                    print('el_service:'.ljust(30), 'already running...')
                elif 'Daemonizing' in el_service:
                    print('el_service:'.ljust(30), el_service)
                else:
                    print('ERROR:'.ljust(30), el_service)
                    exit(912)
            else:
                print('did not find elbencho binary!')
                exit(913)


def check_service_stop(n_hosts, ssh_w_psw):
    print()
    for node in n_hosts:
        print()
        print('Checking Node for service status:'.ljust(30), node)
        with os.popen(f'{ssh_w_psw} root {node} "which elbencho" 2>&1') as f:
            output = f.read()
            if 'elbencho' in output:
                el_exe = output.strip()
                start_it = f"{el_exe} --service"
                with os.popen(f'{ssh_w_psw} root {node} "{start_it}" 2>&1') as f:
                    el_service = f.read()


def cleanup_files(files_list, remove_int=6, default_ext=".bin"):
    y = 0
    i_nim = 0
    is_max = 19
    for f_path_ddf in files_list:

        if os.path.exists(f_path_ddf):
            if f_path_ddf.lower().endswith(default_ext):
                y += 1
                print(' > Removing:'.ljust(30), f_path_ddf)
                os.remove(f_path_ddf)
                time.sleep(1)
                files_list.remove(f_path_ddf)
                i_nim += 1
                if y == remove_int:
                    time.sleep(1)
                return files_list
            elif f_path_ddf.endswith("data_testing"):
                for fp in os.listdir(f_path_ddf):
                    f_path_ddf = os.path.join(f_path_ddf, fp)
                    if os.path.exists(f_path_ddf):
                        if f_path_ddf.lower().endswith(default_ext):
                            files_list.append(f_path_ddf)
                            y += 1
                            print(' >>> Removing:'.ljust(30), f_path_ddf)
                            os.remove(f_path_ddf)
                            i_nim += 1
                            time.sleep(1)
                            files_list.remove(f_path_ddf)
                            if y == remove_int:
                                time.sleep(1)
                            return files_list
                    else:
                        print('! WTF ! ', fp)
                        time.sleep(1)
        if i_nim == is_max:
            print('>> hit max remove limit:'.ljust(30), is_max)
            time.sleep(1)
            return files_list
    return files_list


def get_keys_with_value_of(data_list, target_key):
    found_key_values = []
    for dictionary in data_list:
        if isinstance(dictionary, dict):  # Ensure the item is a dictionary
            for key, value in dictionary.items():
                if key == target_key:
                    found_key_values.append(value)
    return found_key_values


def run_benchmarking_tests(elbencho, el_nodes, targets):
    """ lets go! """

    ''' ensure log, log date directory exists '''
    log_folder = os.path.join(script_folder, "result-logs")
    os.makedirs(log_folder, exist_ok=True)
    date_log_stamp = datetime.now().strftime("%Y%m%d")
    log_folder_dated = os.path.join(log_folder, date_log_stamp)
    os.makedirs(log_folder_dated, exist_ok=True)
    time_log_stamp = datetime.now().strftime("%Y%m%d_%H%M")
    test_sequence = 0

    ''' basic four corners tests, two tests but each does write & read operations '''
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
            "size": "32M",
            "extras": "--cpu --lat",
        }
    ]
    meta_data_tests = [
        {
            "label": "MetaData_10K_1Thread",
            "label_code": "MD_10K_1T",
            "extras": "--write --cpu --lat --threads=1 --size=0 --files 10000 --mkdirs --delfiles --deldirs"
        },
        {
            "label": "MetaData_10K_2Thread",
            "label_code": "MD_10K_2T",
            "extras": "--write --cpu --lat --threads=2 --size=0 --files 10000 --mkdirs --delfiles --deldirs"
        },
        {
            "label": "MetaData_10K_2Thread_1Folder",
            "label_code": "MD_10K_2T_1Fldr",
            "extras": "--write --cpu --lat --threads=2 --size=0 --files 10000 --mkdirs --delfiles --deldirs --dirsharing"
        },
        {
            "label": "MetaData_File_Per_Process",
            "label_code": "MD_1F_32T_1Fldr",
            "extras": "--write --cpu --lat  --sync --threads 32 --files 1 --size 64m --block 1m --mkdirs --delfiles --deldirs --dirsharing"
        }
    ]

    ''' default job options, threads ramp, iodepth ramp, block size ramp '''
    timelimit = "300"
    log_level = "1"
    target_file_ext = '.bin'  # important to leave as bin file, cleanup job is looking for this!
    blocks_ramp = ["4K", "1M"]
    threads_ramp = ["1", "2"]
    io_depth_ramp = ["1", "2"]

    ''' compute test counts '''
    total_tests = sum(
        1 for _ in product(
            targets,
            blocks_ramp,
            threads_ramp,
            io_depth_ramp,
            four_corners_tests
        )
    )

    md_tests = sum(
        1 for _ in product(
            targets,
            meta_data_tests
        )
    )
    total_tests += md_tests


    ''' housekeeping '''
    all_tests_list = []
    created_files = []
    total_test_progress = 0
    group_number = 0
    total_tests_str = str(total_tests).zfill(3)
    total_groups = str(len(targets)).zfill(3)

    for tgt in targets:                            #  ----- loop for each folder path option -----
        test_sequence = 0
        group_number += 1
        group_num = str(group_number).zfill(3)
        for block_size in blocks_ramp:                 # ----- loop for each block size option -----
            for threads in threads_ramp:                 # ----- loop for each threads size option -----
                for iodepth in io_depth_ramp:              # ----- loop for each iodepth option -----
                    for test in four_corners_tests:          # ----- loop for each test case option -----
                        test_sequence += 1
                        test_sequence_str = str(test_sequence).zfill(3)
                        total_test_progress += 1
                        total_test_progress_str = str(total_test_progress).zfill(3)
                        total_pct_complete = (total_test_progress / total_tests) * 100
                        total_pct = round(total_pct_complete, 1)
                        total_pct_float = str(total_pct).zfill(3).rjust(5)

                        test_id = tgt["test_id"]
                        test_path = tgt["mount_to_folder"]
                        t_label = test["label"]
                        label = f"TEST{test_sequence_str}_{test_id}__{t_label}"
                        mode = test["mode"]
                        file_size = test["size"]
                        extras = test["extras"]

                        log_stamp = f'{date_log_stamp}_{test_id}'.upper()
                        test_folder = os.path.join(log_folder_dated, log_stamp)
                        os.makedirs(test_folder, exist_ok=True)

                        test_file_name = f'test_number-{test_sequence_str}'
                        res_file = os.path.join(test_folder, f"{test_file_name}_results.txt")
                        csv_file = os.path.join(test_folder, f"{test_file_name}.csv")
                        csv_live = os.path.join(test_folder, f"{test_file_name}-live.csv")
                        json_out = os.path.join(test_folder, f"{test_file_name}.json")

                        ''' create a randomized file name '''
                        time.sleep(.111)
                        file_stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                        f_name = f"{file_stamp}".upper()
                        file_name = f'{f_name}_{test_id}.BIN'
                        test_file_path = os.path.join(test_path, 'data_testing', file_name)
                        if test_file_path not in created_files:
                            created_files.append(test_file_path)
                        else:
                            print('!!! ALREADY DID THIS FILE !!!'.ljust(30), test_file_path)
                            exit(1)

                        cmd_local_dir_path = os.path.join(tgt["command_server_disk_path"], 'data_testing')
                        created_files.append(cmd_local_dir_path)

                        ''' validate test not already done '''
                        test_all_params = {
                            "label": label,
                            "test_id": test_id,
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
                            print('!!! ALREADY DID THIS TEST !!!'.ljust(30), test_all_params)
                            exit(1)

                        ''' test parameters generated '''
                        print()
                        print('=======================================================================================================')
                        print(f'total_progress:'.ljust(30), f'[{total_test_progress_str} of {total_tests_str}] | Group [{group_num} of {total_groups}] = Completed: {total_pct_float}%')
                        print('test_code'.ljust(30), test_sequence_str)
                        print('label:'.ljust(30), label)
                        print('mode:'.ljust(30), mode)
                        print('file_size:'.ljust(30), file_size)
                        print('block_size:'.ljust(30), block_size)
                        print('threads:'.ljust(30), threads)
                        print('iodepth:'.ljust(30), iodepth)
                        print('extras:'.ljust(30), extras)
                        print('test_file_path:'.ljust(30), test_file_path)
                        print('res_file:'.ljust(30), res_file)
                        print('csv_file:'.ljust(30), csv_file)
                        print('csv_live:'.ljust(30), csv_live)
                        print('json_out:'.ljust(30), json_out)
                        print('hosts:'.ljust(30), el_nodes)
                        print('=======================================================================================================')
                        print()
                        time.sleep(.111)

                        full_cmd = (f'{elbencho} '
                                    f'--hosts {el_nodes} '
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
                                    f'--jsonfile {json_out} '
                                    f'--log {log_level} '
                                    f'{extras} '
                                    f'{test_file_path} '
                                    )
                        os.system(full_cmd)
                        time.sleep(5)
                        if len(created_files) >= 6:
                            created_files = cleanup_files(created_files)
    cf_int = 0
    while len(created_files) > 0:
        cf_int += 1
        print('created_files loop!'. ljust(30), cf_int)
        created_files = cleanup_files(created_files, 99)
        print(len(created_files))
        time.sleep(4)
        if cf_int == 10:
            created_files = -1
            break

    ##############################################################################################################
    md_int = 0
    for tgt in targets:                    #  loop for each folder path option
        for test in meta_data_tests:       #  loop for each test case option
            test_sequence += 1
            test_sequence_str = str(test_sequence).zfill(3)
            md_int += 1
            test_id = tgt["test_id"]
            test_path = str(tgt["mount_to_folder"]) + '/'
            t_label = test["label"]
            label = f"TEST{test_sequence_str}_{test_id}__{t_label}"
            extras = test["extras"]

            log_stamp = f'{date_log_stamp}_{test_id}'.upper()
            test_folder = os.path.join(log_folder_dated, log_stamp)
            os.makedirs(test_folder, exist_ok=True)
            test_file_name = f'test_number-{test_sequence_str}'
            res_file = os.path.join(test_folder, f"{test_file_name}_results.txt")
            csv_file = os.path.join(test_folder, f"{test_file_name}.csv")
            csv_live = os.path.join(test_folder, f"{test_file_name}-live.csv")
            json_out = os.path.join(test_folder, f"{test_file_name}.json")

            ''' validate test not already done '''
            test_all_params = {
                "label": label,
                "test_id": test_id,
                "extras": extras,
                "test_path": test_path
            }
            if test_all_params not in all_tests_list:
                all_tests_list.append(test_all_params)
            else:
                print('!!! ALREADY DID THIS TEST !!!'.ljust(30), test_all_params)
                exit(1)

            print('=======================================================================================================')
            print()
            print(json.dumps(test_all_params, indent=4))
            print()
            print('=======================================================================================================')
            time.sleep(.111)
            full_cmd = (f'{elbencho} '
                        f'--hosts {el_nodes} '
                        f'--label {test_id} '
                        f'--timelimit {timelimit} '
                        f'{extras} '
                        f'--live1 --livecsvex --livecsv {csv_live} '
                        f'--csvfile {csv_file} '
                        f'--resfile {res_file} '
                        f'--jsonfile {json_out} '
                        f'--log {log_level} '
                        f'{test_path} '
                        )
            os.system(full_cmd)



    print('completed test routines.')

''' ##################################################################################################### '''
elbencho_exe, ssh_exe = create_local_tools()
el_targets = create_benchmark_targets()
el_hosts, elbencho_nodes_list = create_nodes_lists()

if check_local_paths:
    local_paths_exist = check_local_drives(el_targets)
if unmount_nfs_clients:
    nfs_unmount_drive(elbencho_nodes_list, el_targets, ssh_exe)
if check_nfs_paths:
    nfs_check_drives(elbencho_nodes_list, el_targets, ssh_exe)
if check_elbencho:
    check_service_status(elbencho_nodes_list, ssh_exe)
if run_the_tool:
    run_benchmarking_tests(elbencho_exe, el_hosts, el_targets)

''' ##################################################################################################### '''

exit(0)

