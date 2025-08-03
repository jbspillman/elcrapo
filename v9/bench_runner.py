from bench_charter import create_reports
from datetime import datetime
import timeit
import os
import json
import time

''' the storage targets for tests.
    > the targets are local to the server running the script.
    > Simple A vs B test environment here.
'''
storage_targets = [
    {
        "target_name": "SSDv2",
        "target_host": "mediaserver.beastmode.local.net",
        "target_path_nfs": "/mnt/benchmark_tests/ssd",
        "target_path_smb": r"\\mediaserver.beastmode.local.net\spillman"
    },
    {
        "target_name": "HDDv1",
        "target_host": "mediaserver.beastmode.local.net",
        "target_path_nfs": "/mnt/benchmark_tests/hdd",
        "target_path_smb": r"\\mediaserver.beastmode.local.net\02000a"
    }
]

''' defined basic test parameters '''
basic_four_corners_tests = [
    {
        "label": "Sequential_Write_Large_File",
        "label_code": "SEQ_WRITE_LF",
        "mode": "--write",
    },
    {
        "label": "Sequential_Read_Large_File",
        "label_code": "SEQ_READ_LF",
        "mode": "--read --trunctosize",
    },
    {
        "label": "Random_Write_Small_File",
        "label_code": "RAN_WRITE_SF",
        "mode": "--write --rand",
    },
    {
        "label": "Random_Read_Small_File",
        "label_code": "RAN_READ_SF",
        "mode": "--read --rand --trunctosize",
    }
]

extras_options = "--cpu --lat --log 0 --timelimit 300 --no0usecerr"
small_file_size = "256M"
small_block_size = "4K"
large_file_size = "1G"
large_block_size = "1M"
threads_list = ["1", "32"]
iodepth_list = ["1"]


total_tests = len(storage_targets) * len(threads_list) * len(iodepth_list) * len(basic_four_corners_tests)
tests_per_target = round(total_tests / len(storage_targets))
tests_per_target = str(tests_per_target).zfill(3)
total_tests = str(total_tests).zfill(3)

''' default top level folder '''
script_folder = os.path.dirname(os.path.abspath(__file__))

''' ensure log, log date directory exists '''
log_folder = os.path.join(script_folder, "result-logs")
os.makedirs(log_folder, exist_ok=True)
date_log_stamp = datetime.now().strftime("%Y%m%d")
log_folder_dated = os.path.join(log_folder, date_log_stamp)
os.makedirs(log_folder_dated, exist_ok=True)
time_log_stamp = datetime.now().strftime("%Y%m%d_%H%M")
test_folder = os.path.join(log_folder_dated, time_log_stamp)
os.makedirs(test_folder, exist_ok=True)


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
    time.sleep(5)


def run_bench_marks():
    test_file_path = ''
    cleanup_files_list = []

    show_the_text()
    data_file_name = 'fake.BIN'
    target_names = []

    ''' perform the tests on the storage targets '''
    for tgt in storage_targets:
        print('')
        test_number = 0  # reset each storage target.
        target_name = tgt["target_name"]
        target_host = tgt["target_host"]

        target_names.append(target_name)

        if os.name == 'nt':
            elbencho_exe = r'C:\Users\spillman\Documents\elbencho\elbencho.exe'
            target_path = tgt["target_path_smb"]
        else:
            elbencho_exe = r'/usr/bin/elbencho'
            target_path = tgt["target_path_nfs"]

        target_test_directory = os.path.join(target_path, 'benchmark_tests', 'data_testing', target_name)
        os.makedirs(target_test_directory, exist_ok=True)

        ''' create test commands '''
        for test_threads in threads_list:
            for test_iodepth in iodepth_list:
                for test_item in basic_four_corners_tests:

                    test_number += 1
                    test_pad = str(test_number).zfill(3)

                    ''' get the test parameters '''
                    test_label = test_item["label"]
                    test_code =  test_item["label_code"]
                    test_mode = test_item["mode"]

                    if 'Large_File' in test_label:
                        file_id_name = "Sequential_Large_File"
                        test_size = large_file_size
                        test_block = large_block_size
                    else:
                        file_id_name = "Random_Small_File"
                        test_size = small_file_size
                        test_block = small_block_size

                    test_code = f'{test_code}_{test_size}_{test_block}_{test_threads}T_{test_iodepth}IOD'
                    file_label = f'{test_pad}_{test_code}'



                    res_file = os.path.join(test_folder, f"{target_name}_{test_pad}_{test_code}.txt")
                    csv_file = os.path.join(test_folder, f"{target_name}_{test_pad}_{test_code}.csv")
                    csv_live = os.path.join(test_folder, f"{target_name}_{test_pad}_{test_code}-live.csv")
                    # json_out = os.path.join(test_folder, f"{target_name}_{test_pad}_{test_code}.json")

                    ''' create random file name for test '''
                    if 'WRITE' in test_code:  # writes must come before reads to create the file.
                        file_stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                        data_file_name = f'{file_stamp}_{test_code}.BIN'.upper()
                        test_file_path = os.path.join(target_test_directory, data_file_name)
                        cleanup_files_list.append(test_file_path)

                    if 'benchmark_tests' not in target_test_directory:
                        print('output files are not going where you think they are.')
                        print("test_file_path:", test_file_path)
                        exit(1)

                    test_time = 0
                    test_time += 0
                    start_it = timeit.default_timer()
                    print()
                    print('======================================================================================= ')
                    print('test_number                  : ', test_pad, f'of {tests_per_target} Total: {total_tests}')
                    print('target_name                  : ', target_name)
                    print('test_label                   : ', file_label)
                    print('test_code                    : ', test_code)
                    print('test_mode                    : ', test_mode)
                    print('test_block                   : ', test_block)
                    print('test_size                    : ', test_size)
                    print('test_threads                 : ', test_threads)
                    print('test_iodepth                 : ', test_iodepth)
                    print('target_test_directory        : ', target_test_directory)
                    print('data_file_name               : ', data_file_name)

                    full_cmd = (f'{elbencho_exe} '
                        f'--label {file_label} '
                        f'{test_mode} '
                        f'--iodepth={test_iodepth} '
                        f'--threads={test_threads} '
                        f'--block={test_block} '
                        f'--size={test_size} '
                        f'--live1 --livecsvex --livecsv {csv_live} '
                        f'--csvfile {csv_file} '
                        f'--resfile {res_file} '
                        # f'--jsonfile {json_out} '
                        f'{extras_options} '
                        f'{test_file_path} '
                        )
                    os.system(full_cmd)
                    finish_it = timeit.default_timer()
                    test_time = finish_it - start_it
                    print('test_time                    : ', test_time)
                    print()
                    time.sleep(5)

        for file_to_delete in cleanup_files_list:
            if os.path.exists(file_to_delete):
                print('removing test files:', file_to_delete)
                os.remove(file_to_delete)
        time.sleep(3)
    return target_names


def main():
    run_bench_marks()
    create_reports(test_folder)


if __name__ == "__main__":
    main()

