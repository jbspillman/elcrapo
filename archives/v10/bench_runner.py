from datetime import datetime
import timeit
import os
import json
import time
from doctest import testsource

''' the storage targets for tests.
    > the targets are local to the server running the script or remote nodes.
    > i.e. Command Server needs to be able to access either "target_path_nfs" or "target_path_smb"
'''
storage_targets = [
    {
        "target_name": "wv10.1.33",
        "target_host": "beastserver.beastmode.local.net",
        "target_path_nfs": "/mnt/benchmark_tests/hdd",
        "target_path_smb": r"D:\DumbData"
    },
    # {
    #     "target_name": "wv11.2.19",
    #     "target_host": "beastserver.beastmode.local.net",
    #     "target_path_nfs": "/mnt/benchmark_tests/ssd",
    #     "target_path_smb": r"C:\DumbData"
    # }
]

def show_the_text():
    print(r'                                       |                                        ')
    print(r'                                      /|\                                       ')
    print(r'                                     //|\\                                      ')
    print(r'                                   ////|\\\\                                    ')
    print(r'                                ///////|\\\\\\\\                                ')
    print(r'                            ///////////|\\\\\\\\\\\\                            ')
    print(r'                        ///////////////|\\\\\\\\\\\\\\\\                        ')
    print(r'                    ///////////////////|\\\\\\\\\\\\\\\\\\\\                    ')
    print(r'                ///////////////////////|\\\\\\\\\\\\\\\\\\\\\\\\                ')
    print(r'            ///////////////////////////|\\\\\\\\\\\\\\\\\\\\\\\\\\\\            ')
    print(r'        ///////////////////////////////|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\        ')
    print(r'    ///////////////////////////////////|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\    ')
    print(r'///////////////////////////////////////|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
    print(r'|                     ________    __________  ___    ____  ____                |')
    print(r'|                    / ____/ /   / ____/ __ \/   |  / __ \/ __ \               |')
    print(r'|                   / __/ / /   / /   / /_/ / /| | / /_/ / / / /               |')
    print(r'|                  / /___/ /___/ /___/ _, _/ ___ |/ ____/ /_/ /                |')
    print(r'|                 /_____/_____/\____/_/ |_/_/  |_/_/    \____/                 |')
    print(r'|                                                                              |')
    print(r'\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|////////////////////////////////////////')
    print(r'    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|////////////////////////////////////    ')
    print(r'        \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|////////////////////////////////        ')
    print(r'            \\\\\\\\\\\\\\\\\\\\\\\\\\\|////////////////////////////            ')
    print(r'                \\\\\\\\\\\\\\\\\\\\\\\|////////////////////////                ')
    print(r'                    \\\\\\\\\\\\\\\\\\\|////////////////////                    ')
    print(r'                        \\\\\\\\\\\\\\\|////////////////                        ')
    print(r'                            \\\\\\\\\\\|////////////                            ')
    print(r'                                \\\\\\\|////////                                ')
    print(r'                                   \\\\|////                                    ')
    print(r'                                     \\|//                                      ')
    print(r'                                      \|/                                       ')
    print(r'                                       |                                        ')
    time.sleep(2)


def run_bench_marks():

    """ show text stuff. """
    show_the_text()

    ''' default top level folder '''
    script_folder = os.path.dirname(os.path.abspath(__file__))

    if os.name == 'nt':
        elbencho_exe = r'C:\Users\spillman\Documents\elbencho\elbencho.exe'
    else:
        elbencho_exe = r'/usr/bin/elbencho'

    ''' defined basic test parameters '''
    two_corners_x_write_read = [
        {
            "test_name": "Sequential",
            "test_code": "SEQ",
            "test_mode": "--write --read --trunctosize",
            "test_block": "1M"
        },
        {
            "test_name": "Random",
            "test_code": "RAN",
            "test_mode": "--write --read --rand --randalgo fast --trunctosize",
            "test_block": "4K"
        },
    ]
    threads_list = [32, 16, 8, 4, 1]
    sizes_list = sorted(list(threads_list), reverse=True)
    sizes_list = [4]
    iodepth = 1

    extras_00 = "--cpu --lat --log 0 --direct --timelimit 300 --no0usecerr --dirsharing --files 1 --dirs 1"
    extras_01 = "--live1 --livecsvex --liveint 1000" # --dryrun
    full_cmd = ""
    cleanup_files_list = []
    target_names = []
    all_labels = []

    # total_tests = (len(storage_targets) * len(threads_list) * len(two_corners_x_write_read))
    # tests_per_target = round(total_tests / len(storage_targets))
    # tests_per_target = str(tests_per_target).zfill(3)
    # total_tests = str(total_tests).zfill(3)

    ''' Threads and File Sizes are same length of a list. '''
    threads_sizes = len(threads_list)
    file_sizes = len(sizes_list)
    types_of_jobs = 2  # RANDOM 4K and SEQUENTIAL 1M
    total_tests = len(storage_targets) * threads_sizes * file_sizes * types_of_jobs
    tests_per_target = round(total_tests / len(storage_targets))
    print("storage_targets:".ljust(30), len(storage_targets))
    print("threads_sizes:".ljust(30), threads_sizes)
    print("types_of_jobs:".ljust(30), types_of_jobs)
    print("tests_per_target:".ljust(30), tests_per_target)
    print("total_tests:".ljust(30), total_tests)
    time.sleep(3)

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
    for tgt in storage_targets:
        print('')
        test_number = 0  # reset each storage target.
        target_name = tgt["target_name"]
        target_names.append(target_name)

        if os.name == 'nt':
            target_path = tgt["target_path_smb"]
        else:
            target_path = tgt["target_path_nfs"]

        target_test_directory = os.path.join(target_path, 'benchmark_tests', 'data_testing', target_name)
        os.makedirs(target_test_directory, exist_ok=True)

        ''' create test commands '''
        for test_item in two_corners_x_write_read:
            ''' get the test parameters '''
            test_name = test_item["test_name"]
            test_code =  test_item["test_code"]
            test_mode = test_item["test_mode"]
            block_size = test_item["test_block"]

            for file_size in sizes_list:
                for threads in threads_list:
                    test_number += 1
                    test_pad = str(test_number).zfill(3)
                    test_label = f'{test_pad}_{test_name}__{file_size}G_{block_size}_{threads}T_{iodepth}D__{target_name}'.upper()
                    res_file = os.path.join(test_folder, f"{target_name}_{test_label}.txt")
                    csv_file = os.path.join(test_folder, f"{target_name}_{test_label}.csv")
                    csv_live = os.path.join(test_folder, f"{target_name}_{test_label}.live")

                    ''' create random file name for test '''
                    file_stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    data_file_name = f'{file_stamp}_{test_label}.BIN'.upper()
                    test_file_path = os.path.join(target_test_directory, data_file_name)
                    cleanup_files_list.append(test_file_path)

                    print()
                    print('test_number                  : ', test_pad, f'of {tests_per_target} Total: {total_tests}')
                    print('target_name                  : ', target_name)
                    print('test_name                    : ', test_name)
                    print('test_code                    : ', test_code)
                    print('test_label                   : ', test_label)
                    print('test_mode                    : ', test_mode)
                    print('file_size                    : ', f'{file_size}G')
                    print('threads                      : ', threads)
                    print('block_size                   : ', block_size)
                    print('iodepth                      : ', iodepth)
                    print('res_file                     : ', res_file)
                    print('csv_file                     : ', csv_file)
                    print('csv_live                     : ', csv_live)
                    print('extras_00                    : ', extras_00)
                    print('extras_01                    : ', extras_01)
                    print('target_test_directory        : ', target_test_directory)
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
                                f'{extras_00} '
                                f'{extras_01} '
                                f'--iodepth={iodepth} '
                                f'--threads={threads} '
                                f'--block={block_size} '
                                f'--size={file_size}G '
                                f'--csvfile {csv_file} '
                                f'--resfile {res_file} '
                                f'--livecsv {csv_live} '
                                f'{target_test_directory} '
                                )
                    start_it = timeit.default_timer()
                    os.system(full_cmd)
                    finish_it = timeit.default_timer()
                    test_time = finish_it - start_it
                    print('test_time                    : ', test_time)
                    print()
                    if 'dryrun' not in full_cmd:
                        for file_to_delete in cleanup_files_list:
                            if os.path.exists(file_to_delete):
                                print('removing test files:', file_to_delete)
                                try:
                                    os.remove(file_to_delete)
                                except FileNotFoundError:
                                    pass
                        time.sleep(5)

    if 'dryrun' in full_cmd:
        os.rmdir(test_folder)
        for file_to_delete in cleanup_files_list:
            if os.path.exists(file_to_delete):
                print('removing test files:', file_to_delete)
                try:
                    os.remove(file_to_delete)
                except FileNotFoundError:
                    pass

    return target_names


def main():
    run_bench_marks()



if __name__ == "__main__":
    main()

