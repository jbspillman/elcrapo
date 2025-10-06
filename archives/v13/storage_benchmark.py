from datetime import datetime
import shutil
import os


script_folder = os.path.dirname(os.path.abspath(__file__))
date_stamp = datetime.now().strftime("%Y%m%d")
#file_stamp = datetime.now().strftime("%H.%M.%S.%f")
file_stamp = datetime.now().strftime("%H.%M.%S")


def remove_folder_path(the__path):
    if os.path.exists(the__path):
        try:
            shutil.rmtree(the__path)
            return True
        except OSError as e:
            print(f"Error deleting directory {the__path}: {e}")
            return False
    return True


def check_if_folder_empty(the__path):
    if os.path.exists(the__path):
        file_objects = os.listdir(the__path)
        if len(file_objects) == 0:
            remove_result = remove_folder_path(the__path)
            return remove_result
        else:
            return False
    else:
        return True


def setup_environment():


    testing_results_folder = os.path.join(script_folder, "test_results", date_stamp)

    if os.name == 'nt':
        elbencho_exe = r'C:\Users\spillman\elbencho\elbencho.exe'
        storage_targets = [
            {
                "target_name": "fNAS-1.3",
                "target_host": "rogstrix.beastmode.local.net",
                "target_path": "D:\\fNAS-1.3"
            },
            {
                "target_name": "fNAS-2.4",
                "target_host": "beastserver.beastmode.local.net",
                "target_path": r"\\beastserver.beastmode.local.net\12000b\fNAS-2.4"
            }
        ]
    
    else:
        elbencho_exe = r'/usr/bin/elbencho'
        storage_targets = [
            {
                "target_name": "fNAS-1.3",
                "target_host": "mediaserver.beastmode.local.net",
                "target_path": "/mnt/Drives/ms_00240a"
            },
            # {
            #     "target_name": "fNAS-2.4",
            #     "target_host": "mediaserver.beastmode.local.net",
            #     "target_path": "/mnt/Drives/ms_spillman"
            # }
        ]
        
    tgt_configs = {
        "elbencho_exe": elbencho_exe,
        "testing_results_folder": testing_results_folder,
        "storage_targets": storage_targets
    }
    return tgt_configs


def setup_storage_tests(tgts):
    """ setup the test jobs or commands. """

    all_commands = []
    all_test_destinations = []
    all_results_folders = []

    elbencho_exe = tgts["elbencho_exe"]
    storage_targets = tgts["storage_targets"]
    results_folder = tgts["testing_results_folder"]

    sizes_threads = [
        (1024, 1),
        (512, 2),
        (256, 4),
        (128, 8),
        (64, 16),
        (32, 32)
    ]
    block_sizes = [
        "4K",
        "32K",
        "64K",
        "128K",
        "512K",
        "1024K"
    ]

    ### <---- LOOP STARTS HERE ----> ###
    test_number = 0
    for storage_target_test in storage_targets:
        target_name = storage_target_test["target_name"]
        target_host = storage_target_test["target_host"]
        target_path = storage_target_test["target_path"]

        product_results_folder = os.path.join(results_folder, file_stamp, target_name)
        if product_results_folder not in all_results_folders:
            all_results_folders.append(product_results_folder)


        bs = 0
        for block_size in block_sizes:
            bs += 1

            if bs < 3:
                test_type = "Random"
                test_code = "RAN"

            else:
                test_type = "Sequential"
                test_code = "SEQ"

            for size_thread in sizes_threads:
                size = size_thread[0]
                thread = size_thread[1]
                total_put = thread * size
                test_number += 1
                ptn = str(test_number).zfill(3)

                test_label = f'{ptn}_{test_code}_{str(block_size).zfill(5)}_{str(size).zfill(5)}M_{str(thread).zfill(3)}T'

                file_output_label = f'{test_code}__{target_name}'
                csv_file = os.path.join(str(product_results_folder), f'{file_output_label}.csv')
                txt_file = os.path.join(str(product_results_folder), f'{file_output_label}.txt')
                csv_live = os.path.join(str(product_results_folder), f'{file_output_label}.liv')

                safe_folder = 'elBencho_Test'
                target_safe_path = os.path.join(os.path.dirname(target_path), safe_folder, os.path.basename(target_path), test_code, ptn)
                if not os.path.exists(target_safe_path):
                    os.makedirs(results_folder, exist_ok=True)
                if target_safe_path not in all_test_destinations:
                    all_test_destinations.append(target_safe_path)

                files_count = 1
                folders_count = 1
                live_int = 1000
                log_level = 1
                time_limit = 300
                io_depth = 1
                job_options = [
                    f'label "{test_label}"',
                    f'write',
                    f'read',
                    f'rand',
                    f'files "{files_count}"',
                    f'dirs "{folders_count}"',
                    f'size="{size}M"',
                    f'threads="{thread}"',
                    f'block="{block_size}"',
                    f'iodepth="{io_depth}"',
                    f'cpu',
                    f'lat',
                    f'direct',
                    f'dirsharing',
                    f'trunctosize',
                    f'no0usecerr',
                    f'mkdirs',
                    f'live1',
                    f'livecsvex',
                    f'csvfile "{csv_file}"',
                    f'resfile "{txt_file}"',
                    f'livecsv "{csv_live}"',
                    f'liveint "{live_int}"',
                    f'log "{log_level}"',
                    f'timelimit "{time_limit}"'
                ]

                job_copy = job_options
                if test_code == "SEQ":
                    job_copy.remove('rand')

                delimiter = " --"
                joined_string = delimiter.join(job_copy)
                job_copy_string = delimiter + joined_string
                job_copy_string = job_copy_string.lstrip()

                full_command = f'{elbencho_exe} {job_copy_string} "{target_safe_path}"'
                all_commands.append(full_command)
                # print(f'{full_command}')

    return all_test_destinations, all_results_folders, all_commands


def run_bench_mark_tests(target_folders, results_folders, commands_list):
    """ run the list of commands and track the work. """

    ''' pre-cleanup the folder structures if it exists. '''
    for tgt_folder in target_folders:
        remove_folder_path(tgt_folder)
        os.makedirs(tgt_folder, exist_ok=True)

    result_parents = []
    for results_folder in results_folders:
        parent = os.path.dirname(results_folder)
        os.makedirs(results_folder, exist_ok=True)
        if parent not in result_parents:
            result_parents.append(parent)

    ''' run the tests. '''
    total = len(commands_list)
    zt = str(total).zfill(3)
    x = 0
    for command in commands_list:
        x += 1
        zx = str(x).zfill(3)
        print(f'Run Test [{zx} of {zt}] ')
        os.system(command)

    ''' clean up empty result folders if we were testing.'''
    for results_folder in results_folders:
        was_empty = check_if_folder_empty(results_folder)
        print(was_empty, results_folder)
        if was_empty:
            remove_folder_path(results_folder)
    for parent_folder in result_parents:
        was_empty = check_if_folder_empty(parent_folder)
        print(was_empty, parent_folder)
        if was_empty:
            remove_folder_path(parent_folder)

    for target_folder in target_folders:
        remove_folder_path(target_folder)


def main():
    targets = setup_environment()
    testing_folders, testing_results, testing_commands = setup_storage_tests(targets)
    run_bench_mark_tests(testing_folders, testing_results, testing_commands)




if __name__ == "__main__":
    main()        

exit(0)
