from bench_charter import create_reports
from datetime import datetime
import timeit
import os
import time

''' the storage targets for tests.
    > the targets are local to the server running the script or remote nodes.
    > i.e. Command Server needs to be able to access either "target_path_nfs" or "target_path_smb"
'''
storage_targets = [
    {
        "target_name": "fNAS-1.3",
        "target_host": "mediaserver.beastmode.local.net",
        "target_path_nfs": "/mnt/Drives/ms_00240a"
    },
    {
        "target_name": "fNAS-2.4",
        "target_host": "mediaserver.beastmode.local.net",
        "target_path_nfs": "/mnt/Drives/ms_spillman"
    }    
]
'''
    {
        "target_name": "fNAS-4.6",
        "target_host": "mediaserver.beastmode.local.net",
        "target_path_nfs": "/mnt/Drives/ms_spillman"
    },    
    {
        "target_name": "FreeNAS-2.4",
        "target_host": "beastserver.beastmode.local.net",
        "target_path_nfs": "/mnt/Local/nvme0"
    }
'''


def show_the_text():
    print()
    print(r'                                            |                                             ')
    print(r'                                           /|\                                            ')
    print(r'                                          //|\\                                           ')
    print(r'                                        (///|\\\)                                         ')
    print(r'                                     (//////|\\\\\\\)                                     ')
    print(r'                                 (//////////|\\\\\\\\\\\)                                 ')
    print(r'                           (////////////////|\\\\\\\\\\\\\\\\\)                           ')
    print(r'                         (//////////////////|\\\\\\\\\\\\\\\\\\\)                         ')
    print(r'                         (//////////////////|\\\\\\\\\\\\\\\\\\\)                         ')
    print(r'                     (//////////////////////|\\\\\\\\\\\\\\\\\\\\\\\)                     ')
    print(r'                 (//////////////////////////|\\\\\\\\\\\\\\\\\\\\\\\\\\\)                 ')
    print(r'         (//////////////////////////////////|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\)         ')
    print(r'     (//////////////////////////////////////|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\)     ')
    print(r'    (||                    ________    __________  ___    ____  ____               ||)    ')
    print(r'   ((||                   / ____/ /   / ____/ __ \/   |  / __ \/ __ \              ||)    ')
    print(r'   ((||                  / __/ / /   / /   / /_/ / /| | / /_/ / / / /              ||)    ')
    print(r'   ((||                 / /___/ /___/ /___/ _, _/ ___ |/ ____/ /_/ /               ||)    ')
    print(r'   ((||                /_____/_____/\____/_/ |_/_/  |_/_/    \____/                ||))   ')
    print(r'  (((||                                                                            ||)))  ')
    print(r'  ((((\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|////////////////////////////////////////)))) ')
    print(r' (((((\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|////////////////////////////////////////)))))')
    print(r' (((((\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|////////////////////////////////////////)))))')
    print(r' (((((\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|////////////////////////////////////////)))))')

    time.sleep(3)
    print()


def the_cleaner(list_of_things):

    for folder_or_file_to_delete in list_of_things:
        if os.path.exists(folder_or_file_to_delete):
            if os.path.isdir(folder_or_file_to_delete):
                try:
                    os.rmdir(folder_or_file_to_delete)
                except OSError as err_msg:
                    if 'Errno 39' in str(err_msg):
                        for f_name in os.listdir(folder_or_file_to_delete):
                            fp = os.path.join(folder_or_file_to_delete, f_name)
                            if os.path.exists(fp) and f_name.endswith(".BIN"):
                                print('removing test file in folder:', fp)
                                try:
                                    os.remove(fp)
                                except FileNotFoundError:
                                    pass
            else:

                if os.path.exists(folder_or_file_to_delete) and folder_or_file_to_delete.endswith(".BIN"):
                    print('removing test file in folder:', folder_or_file_to_delete)
                    try:
                        os.remove(folder_or_file_to_delete)
                    except FileNotFoundError:
                        pass
    time.sleep(5)


def run_bench_marks():

    """ show text stuff. """
    show_the_text()

    ''' default top level folder '''
    script_folder = os.path.dirname(os.path.abspath(__file__))
    with open('pid.lock', 'w') as pi:
         pi.write(' ')

    elbencho_exe = r'/usr/bin/elbencho'

    ''' defined basic test parameters '''
    two_corners_x_write_read = [
        {
            "test_name": "Sequential",
            "test_code": "SEQ",
            "test_mode": "--write --read --trunctosize",  # 
            "test_block": "1M"
        },
        {
            "test_name": "Random",
            "test_code": "RAN",
            "test_mode": "--write --read --rand --trunctosize",   # --trunctosize --randalgo fast
            "test_block": "4K"
        },
    ]
    test_target_types = ["directory_based"]  # "directory_based", "file_based"
    iodepth = 1
    
    threads_list = [1, 4, 16]      # number
    sizes_list = [2048, 512, 128]  # MB

    directory_extras = "--cpu --lat --dirsharing --files 2 --dirs 4 --mkdirs "  # --deldirs --delfiles
    file_extras = "--cpu --lat"
    extra_options = "--no0usecerr --live1 --livecsvex --liveint 1000 --log 0 --direct --timelimit 1500" # --dryrun --direct
    full_cmd = ""
    cleanup_list = []
    target_names = []
    all_labels = []

    ''' Threads and File Sizes are same length of a list. '''
    threads_sizes = len(threads_list)
    types_of_jobs = len(two_corners_x_write_read)  # RANDOM 4KB and SEQUENTIAL 1MB
    total_tests = len(storage_targets) * threads_sizes * types_of_jobs * len(test_target_types)
    tests_per_target = round(total_tests / len(storage_targets))
    
    tests_per_target = str(tests_per_target).zfill(3)
    total_tests = str(total_tests).zfill(3)
    
    print('')
    print("storage_targets:".ljust(30), len(storage_targets))
    print("test_target_types:".ljust(30), len(test_target_types))
    print("types_of_jobs:".ljust(30), types_of_jobs)
    print("threads_and_sizes:".ljust(30), threads_sizes)
    print("tests_per_target:".ljust(30), tests_per_target)
    print("total_tests:".ljust(30), total_tests)
    time.sleep(5)

    ''' ensure log, log date directory exists '''
    log_folder = os.path.join(script_folder, "result-logs")
    os.makedirs(log_folder, exist_ok=True)
    date_log_stamp = datetime.now().strftime("%Y%m%d")
    log_folder_dated = os.path.join(log_folder, date_log_stamp)
    os.makedirs(log_folder_dated, exist_ok=True)
    time_log_stamp = datetime.now().strftime("%Y%m%d_%H%M")
    test_folder = os.path.join(log_folder_dated, time_log_stamp)
    os.makedirs(test_folder, exist_ok=True)

    ''' perform the tests on the storage targets '''
    group = 0
    for tgt in storage_targets:
        group += 1
        group_pad = str(group).zfill(3)
        test_number = 0  # reset each storage target.
        target_name = tgt["target_name"]
        target_names.append(target_name)
        target_path = tgt["target_path_nfs"]

        target_test_directory = os.path.join(target_path, 'benchmark_tests', 'data_testing', target_name)
        os.makedirs(target_test_directory, exist_ok=True)

        ''' Easier to ramp up the thread count per test then move on, for parsing later. '''
        for thread_size, file_size in zip(threads_list, sizes_list):

            for test_target_type in  test_target_types:
                ''' create test commands '''
                for test_item in two_corners_x_write_read:
                    ''' get the test parameters '''
                    test_name = test_item["test_name"]
                    test_code =  test_item["test_code"]
                    test_mode = test_item["test_mode"]
                    block_size = test_item["test_block"]
                    test_number += 1
                    test_pad = str(test_number).zfill(3)
                    test_label = f'{test_pad}_{test_name}_{target_name}_{file_size}M_{block_size}_{thread_size}T_{iodepth}D'.upper()
                    file_label = f'{target_name}_{test_name}_{test_target_type}'.upper()
                    res_file = os.path.join(test_folder, f"{file_label}.txt")
                    csv_file = os.path.join(test_folder, f"{file_label}.csv")
                    csv_live = os.path.join(test_folder, f"{file_label}.live")

                    ''' create random file name for test '''
                    file_stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    data_file_name = f'{file_stamp}_{test_label}.BIN'.upper()
                    test_file_path = os.path.join(target_test_directory, data_file_name)
                    if test_target_type == "directory_based":
                        data_file_name = None
                        extras = directory_extras
                        test_target_path = f'{target_test_directory}'
                        cleanup_list.append(str(target_test_directory))
                    else:
                        extras = file_extras
                        test_target_path = test_file_path
                        cleanup_list.append(str(test_target_path))

                    print()
                    print()
                    print('test_number                  : ', test_pad, f'of {tests_per_target} | Group: [{group_pad}] Total: {total_tests}')
                    print('target_name                  : ', target_name)
                    print('test_name                    : ', test_name)
                    print('test_code                    : ', test_code)
                    print('test_label                   : ', test_label)
                    print('test_mode                    : ', test_mode)
                    print('file_size                    : ', f'{file_size}M')
                    print('thread_size                  : ', thread_size)
                    print('block_size                   : ', block_size)
                    print('iodepth                      : ', iodepth)
                    print('file_label                   : ', file_label)
                    print('res_file                     : ', res_file)
                    print('csv_file                     : ', csv_file)
                    print('csv_live                     : ', csv_live)
                    print('extras                       : ', extras)
                    print('extra_options                : ', extra_options)
                    print('test_target_type             : ', test_target_type)
                    print('test_target_path             : ', test_target_path)
                    print('data_file_name               : ', data_file_name)

                    if test_label not in all_labels:
                        all_labels.append(test_label)
                    else:
                        print('#################################')
                        print('#################################')
                        print('test_label has already been done!')
                        print('#################################')
                        print('#################################')
                        time.sleep(5)
                    
                    full_cmd = (f'{elbencho_exe} '
                                f'--label {test_label} '
                                f'{test_mode} '
                                f'{extras} '
                                f'{extra_options} '
                                f'--iodepth={iodepth} '
                                f'--threads={thread_size} '
                                f'--block={block_size} '
                                f'--size={file_size}M '
                                f'--csvfile {csv_file} '
                                f'--resfile {res_file} '
                                f'--livecsv {csv_live} '
                                f'{test_target_path} '
                                )
                    start_it = timeit.default_timer()
                    os.system(full_cmd)
                    finish_it = timeit.default_timer()
                    test_time = finish_it - start_it
                    print('test_time                    : ', test_time)
                    print()

                    ''' use find command to clean folders and files. '''
                    find_cmd_files = f'find {test_target_path}/ -type f -delete ;'
                    os.system(find_cmd_files)
                    
                    find_cmd_dirs = f'find {test_target_path}/ -mindepth 1 -type d -delete ;'
                    os.system(find_cmd_dirs)


    if 'dryrun' in full_cmd:
        os.rmdir(test_folder)
        test_folder = None
    return test_folder


def main():
    results_folder = run_bench_marks()
    
    time.sleep(3)
    
    create_reports(results_folder)


if __name__ == "__main__":
    main()

