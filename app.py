from datetime import datetime
import pandas as pd
import timeit
import shutil
import time
import json
import os


''' Options to keep control. '''
run_as_dryrun = False  # runs as dryrun, to see if your command syntax is correct.
run_multiple_tests = True  # if this is False, it will only process the last item in list.
run_create_execute_commands = True  # runs the list of commands generated.
run_parse_result_logs = True  # removes or strips a lot of fields out of output files.
run_html_creates = True  # creates html friendly json files.
keep_logs = False    # helpful in case you want to reparse the data or check it.
keep_reports = False  # helpful in case you want to reparse the data or check it.
run_cleanup_folders_files = True   # keeps the targets free of capacity issues.


title_string = f'''
####################################################### 
##    ELBENCHO and FIO Tests and Report Generator    ##   
####################################################### 
'''
print(title_string)

all_folders_list = []
elbencho_exe = r'C:\Users\spillman\Documents\elbencho\elbencho.exe'
fio_exe = r'C:\Program Files\fio\fio.exe'

script_folder = os.path.dirname(os.path.abspath(__file__))
log_folder = os.path.join(script_folder, "result-logs")
os.makedirs(log_folder, exist_ok=True)

reports_folder = os.path.join(script_folder, "result-reports")
os.makedirs(reports_folder, exist_ok=True)



def create_testing_commands():
    print('## Creating Commands List. ##')

    ''' Need to have something defined in here if running actual tests or dryrun. '''
    list_of_targets = [
        # {
        #     "product_vendor": "ASUS",
        #     "product_name": "Ubuntu Server LTS",
        #     "product_version": "HDD 24.04",
        #     "product_test_protocol": "SMB",
        #     "product_storage_path": r'\\beastserver.beastmode.local.net\12000b'
        # },
        {
            "product_vendor": "ASUS",
            "product_name": "Ubuntu Server LTS",
            "product_version": "NVMe 24.04",
            "product_test_protocol": "SMB",
            "product_storage_path": r'\\beastserver.beastmode.local.net\spillman'
        },
        {
            "product_vendor": "HP",
            "product_name": "Ubuntu Server LTS",
            "product_version": "NVMe 24.04",
            "product_test_protocol": "SMB",
            "product_storage_path":  r'\\mediaserver.beastmode.local.net\00500a\benchmark_tests'
        }
        # {
        #     "product_vendor": "HP",
        #     "product_name": "Ubuntu Server LTS",
        #     "product_version": "HDD 24.04",
        #     "product_test_protocol": "SMB",
        #     "product_storage_path":  r'\\mediaserver.beastmode.local.net\02000a\benchmark_tests'
        # },
        # {
        #     "product_vendor": "Western Digital",
        #     "product_name": "SN770",
        #     "product_version": "NVMe 731130WD",
        #     "product_test_protocol": "SMB",
        #     "product_storage_path": r'D:\FileTests'
        # },
        # {
        #     "product_vendor": "Samsung",
        #     "product_name": "980 PRO",
        #     "product_version": "SSD 1.0",
        #     "product_test_protocol": "SMB",
        #     "product_storage_path": r'C:\FileTests'
        # }
    ]
    if not run_multiple_tests:
        list_of_targets = [list_of_targets[-1]]

    all_commands_json = []
    if len(list_of_targets) == 0:
        return all_commands_json

    for item in list_of_targets:

        date_log_stamp = datetime.now().strftime("%Y.%m.%d")
        time_log_stamp = datetime.now().strftime("%H.%M")

        test_folder = os.path.join(log_folder, date_log_stamp, time_log_stamp)
        os.makedirs(test_folder, exist_ok=True)
        all_folders_list.append(test_folder)

        product_vendor = item["product_vendor"]
        product_name = item["product_name"]
        product_version = item["product_version"]
        product_test_protocol = item["product_test_protocol"]
        product_storage_path = item["product_storage_path"]


        # Define the Test Configurations Options.
        svc_hosts = 0
        svc_host_names = f''

        threads_list = [1, 4, 8, 16, 32, 64]
        max_data_size = 1024

        sizes_list = [] # list(reversed(threads_list)):
        for thread in threads_list:
            factor_size = int(max_data_size / thread)
            sizes_list.append(factor_size)

        # file_counts = [1, 2, 8, 16, 32]
        # folder_counts = list(reversed(file_counts))

        file_counts = [1]
        folder_counts = list(reversed(file_counts))

        random_block_sizes = ["4K", "32K", "64K"]
        sequential_block_sizes = ["4K", "32K", "64K"]

        log_level = 0         # Log level. (Default: 0; Verbose: 1; Debug: 2)
        log_interval = 2000   # Update interval for console and csv file live statistics in milliseconds. (Default: 2000)
        time_limit = 600      # Time limit in seconds for each phase. If the limit is exceeded for a phase
                              #   then no further phases will run.
        io_depth = 1          # Depth of I/O queue per thread for asynchronous I/O.
                              #   Setting this to 2 or higher turns on async I/O.

        default_options = (f'--cpu --lat --direct --dirsharing --mkdirs --no0usecerr '
                           f'--log "{log_level}" --live1 --livecsvex '
                           f'--liveint "{log_interval}" --timelimit "{time_limit}"')

        res_file = os.path.join(test_folder, f"{date_log_stamp}_{time_log_stamp}.txt")
        csv_file = os.path.join(test_folder, f"{date_log_stamp}_{time_log_stamp}.csv")
        live_file = os.path.join(test_folder, f"{date_log_stamp}_{time_log_stamp}.lve")


        """ RANDOM STARTS HERE """
        z = 0
        for block_size in random_block_sizes:
            test_type = 'random'
            zbs = str(block_size).zfill(4)

            for thread, size in zip(threads_list, sizes_list):

                zthreadsize = str(thread).zfill(4)
                zfilesize = str(size).zfill(4)

                for file_count, folder_count in zip(file_counts, folder_counts):
                    z += 1
                    test_number = str(z).zfill(3)

                    zfile_count = str(file_count).zfill(4)
                    zfolder_count = str(folder_count).zfill(4)

                    output_dir =  f'{test_type}_{zbs}_{zthreadsize}_{zfilesize}_{zfolder_count}_{zfile_count}'
                    label_name = f'{test_number} | {product_vendor} | {product_name} | {product_version} | {product_test_protocol}'

                    safe_folder_path = os.path.join(product_storage_path, 'SafeFolder')
                    safe_folder_test_path = os.path.join(safe_folder_path, output_dir)

                    test_mode = "--write --read --rand"
                    full_cmd = (f'{elbencho_exe} '
                                f'--dryrun '
                                f'--label "{label_name}" '
                                f'--hosts "{svc_host_names}" '
                                f'--numhost "{svc_hosts}" '
                                f'{test_mode} '
                                f'--iodepth={io_depth} '
                                f'--threads={thread} '
                                f'--block={block_size} '
                                f'--files "{file_count}" '
                                f'--dirs "{folder_count}" '
                                f'--size={size}M '
                                f'--csvfile {csv_file} '
                                f'--resfile {res_file} '
                                f'--livecsv {live_file} '
                                f'{default_options} '
                                f'{safe_folder_test_path} '
                                )
                    k = {
                        "test_number": test_number,
                        "test_type": test_type,
                        "label_name": label_name,
                        "product_vendor": product_vendor,
                        "product_name": product_name,
                        "product_version": product_version,
                        "product_test_protocol": product_test_protocol,
                        "block_size": block_size,
                        "thread_count": thread,
                        "file_size": f'{size}M',
                        "folder_count": f'{folder_count}',
                        "file_count": f'{file_count}',
                        "service_hosts": f'{svc_host_names}',
                        "service_hosts_count": f'{svc_hosts}',
                        "live_file": f'{live_file}',
                        "results_file": f'{res_file}',
                        "csv_file": f'{csv_file}',
                        "target_path": f'{safe_folder_test_path}',
                        "full_cmd": full_cmd
                    }
                    all_commands_json.append(k)

        """ SEQUENTIAL STARTS HERE """
        for block_size in sequential_block_sizes:
            test_type = 'sequential'
            zbs = str(block_size).zfill(4)
            for thread, size in zip(threads_list, sizes_list):
                zthreadsize = str(thread).zfill(4)
                zfilesize = str(size).zfill(4)

                for file_count, folder_count in zip(file_counts, folder_counts):
                    z += 1
                    test_number = str(z).zfill(3)

                    zfile_count = str(file_count).zfill(4)
                    zfolder_count = str(folder_count).zfill(4)

                    output_dir =  f'{test_type}_{zbs}_{zthreadsize}_{zfilesize}_{zfolder_count}_{zfile_count}'
                    label_name = f'{test_number} | {product_vendor} | {product_name} | {product_version} | {product_test_protocol}'

                    safe_folder_path = os.path.join(product_storage_path, 'SafeFolder')
                    safe_folder_test_path = os.path.join(safe_folder_path, output_dir)

                    test_mode = "--write --read"
                    full_cmd = (f'{elbencho_exe} '
                                f'--dryrun '
                                f'--label "{label_name}" '
                                f'--hosts "{svc_host_names}" '
                                f'--numhost "{svc_hosts}" '
                                f'{test_mode} '
                                f'--iodepth={io_depth} '
                                f'--threads={thread} '
                                f'--block={block_size} '
                                f'--files "{file_count}" '
                                f'--dirs "{folder_count}" '
                                f'--size={size}M '
                                f'--csvfile {csv_file} '
                                f'--resfile {res_file} '
                                f'--livecsv {live_file} '
                                f'{default_options} '
                                f'{safe_folder_test_path} '
                                )

                    k = {
                        "test_number": test_number,
                        "test_type": test_type,
                        "label_name": label_name,
                        "product_vendor": product_vendor,
                        "product_name": product_name,
                        "product_version": product_version,
                        "product_test_protocol": product_test_protocol,
                        "block_size": block_size,
                        "thread_count": thread,
                        "file_size": f'{size}M',
                        "folder_count": f'{folder_count}',
                        "file_count": f'{file_count}',
                        "service_hosts": f'{svc_host_names}',
                        "service_hosts_count": f'{svc_hosts}',
                        "live_file": f'{live_file}',
                        "results_file": f'{res_file}',
                        "csv_file": f'{csv_file}',
                        "target_path": f'{safe_folder_test_path}',
                        "full_cmd": full_cmd
                    }
                    all_commands_json.append(k)

    return all_commands_json


def execute_commands(cmds_json):
    print('## Executing Commands List. ##')

    total_commands = len(cmds_json)
    zttl = str(total_commands).zfill(4)

    pk = json.dumps(cmds_json, indent=4)

    for d in cmds_json:
        full_command = d["full_cmd"].strip()
        test_number = d["test_number"]
        test_type = d["test_type"]
        block_size = d["block_size"]
        thread_count = d["thread_count"]
        file_size = d["file_size"]
        product_vendor_a = d["product_vendor"]
        product_name_a = d["product_name"]
        product_version_a = d["product_version"]
        product_test_protocol_a = d["product_test_protocol"]
        target_path = d["target_path"]

        if not run_as_dryrun:
            full_command = full_command.replace(' --dryrun ', ' ')

        if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)
            all_folders_list.append(target_path)

        if test_number == '001':
            print('## Preparing Launch. ##')
            time.sleep(5)

        print()
        print('==' * 60)
        print('Starting:'.ljust(30), f'{test_number} of {zttl}')
        print('product_vendor:'.ljust(30), product_vendor_a)
        print('product_name:'.ljust(30), product_name_a)
        print('product_version:'.ljust(30), product_version_a)
        print('product_test_protocol:'.ljust(30), product_test_protocol_a)
        print('test_type:'.ljust(30), test_type)
        print('block_size:'.ljust(30), block_size)
        print('thread_count:'.ljust(30), thread_count)
        print('file_size:'.ljust(30), file_size)
        print()

        start_it = timeit.default_timer()
        os.system(full_command)
        finish_it = timeit.default_timer()
        test_time = finish_it - start_it
        print(f"Finished:".ljust(30), f'{test_number} of {zttl} Took: {test_time} seconds.')


def parse_results_folder():
    print('## Parsing Results Folders. ##')


    folders_to_process = []
    for root, folders, files in os.walk(log_folder, topdown=True):
        for folder in folders:
            full_path = os.path.join(root, folder)
            folders_or_files = os.listdir(full_path)
            all_folders_list.append(full_path)
            for fld_fle in folders_or_files:
                full_sub_path = os.path.join(full_path, fld_fle)
                if not os.path.isdir(full_sub_path):
                    if full_path not in folders_to_process:
                        folders_to_process.append(full_path)

    json_data_files_list = []
    for folder_path in folders_to_process:
        for file_name in sorted(os.listdir(folder_path)):
            if file_name.endswith('.csv'):
                csv_file_path = str(os.path.join(folder_path, file_name))
                df = pd.read_csv(csv_file_path)
                json_string = df.to_json(orient='records')
                parsed_json = json.loads(json_string)
                pretty_json = json.dumps(parsed_json, indent=4)
                new_json_file_name = file_name.replace('.csv', '.json')

                time_stamp_file = os.path.basename(folder_path)
                date_stamp_file = os.path.basename(os.path.dirname(folder_path))
                reports_location = os.path.join(reports_folder, f'{date_stamp_file}_{time_stamp_file}')
                os.makedirs(reports_location, exist_ok=True)

                new_json_path = os.path.join(reports_location, new_json_file_name)
                with open(new_json_path, 'w', encoding="utf-8") as f:
                    f.write(pretty_json)
                print('Created:'.ljust(30), new_json_path)
                json_data_files_list.append(new_json_path)
                if not keep_logs:
                    os.remove(csv_file_path)

                all_folders_list.append(folder_path)


            elif file_name.endswith('.lve') or file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                if not keep_logs:
                    os.remove(file_path)
            elif file_name.endswith('.json'):
                time_stamp_file = os.path.basename(folder_path)
                date_stamp_file = os.path.basename(os.path.dirname(folder_path))
                reports_location = os.path.join(reports_folder, f'{date_stamp_file}_{time_stamp_file}')
                os.makedirs(reports_location, exist_ok=True)

                src_json_path = str(os.path.join(folder_path, file_name))
                dst_json_path = str(os.path.join(reports_location, file_name))

                if not keep_logs:
                    shutil.move(src_json_path, dst_json_path)
                else:
                    shutil.copy(src_json_path, dst_json_path)

                print('Created:'.ljust(30), dst_json_path)
                json_data_files_list.append(dst_json_path)

            else:
                file_path = os.path.join(folder_path, file_name)
                print('WHAT DO WE DO WITH: ', file_path)
    return json_data_files_list


def create_html_reports():
    print('## Parsing Report Folders. ##')

    for fs_object in os.listdir(reports_folder):
        if '.json' in fs_object:
            print(f'JSON is already parsed:'.ljust(30), fs_object)
        else:
            fs_path = os.path.join(reports_folder, fs_object)
            if os.path.isdir(fs_path):
                if fs_object == 'By_Product':
                    continue
                print(f'Checking folder for JSON files:'.ljust(30), fs_object)
                for file_name in os.listdir(fs_path):
                    if '.json' in file_name:
                        json_file_path = os.path.join(fs_path, file_name)
                        with open(json_file_path, 'r', encoding="utf-8") as j_file:
                            data = json.load(j_file)

                        parsed_data = []
                        for item in data:
                            test_label = item["label"]
                            random_bool = item["random"]
                            iso_date = item["ISO date"]
                            hosts_count = item["hosts"]
                            folders_count = item["dirs"]
                            files_count = item["files"]
                            threads = item["threads"]
                            file_size = item["file size"]
                            block_size = item["block size"]
                            io_depth = item["IO depth"]
                            operation = item["operation"]
                            iops = item["IOPS [last]"]
                            mibs = item["MiB/s [last]"]
                            lat = item["IO lat us [avg]"]

                            target_from_label = test_label.split(' | ')
                            product_vendor_from_label = target_from_label[1]
                            product_name_from_label = target_from_label[2]
                            product_version_from_label = target_from_label[3]
                            product_test_protocol_from_label = target_from_label[4]

                            if 'random' in test_label.lower() or random_bool == 1:
                                test_mode = 'Random'

                            else:
                                test_mode = 'Sequential'

                            if operation == "READ":
                                operation = "Read"
                                keep = True
                            elif operation == "WRITE":
                                operation = "Write"
                                keep = True
                            else:
                                keep = False

                            if keep:
                                k = {
                                    "iso_date": iso_date,
                                    "hosts_count": hosts_count,
                                    "folders_count": folders_count,
                                    "files_count": files_count,
                                    "product_vendor": product_vendor_from_label,
                                    "product_name": product_name_from_label,
                                    "product_version": product_version_from_label,
                                    "product_test_protocol": product_test_protocol_from_label,
                                    "test_mode": test_mode,
                                    "operation": operation,
                                    "block_size": block_size,
                                    "threads": threads,
                                    "file_size": file_size,
                                    "io_depth": io_depth,
                                    "iops": iops,
                                    "mibs": mibs,
                                    "lat": lat
                                }
                                parsed_data.append(k)

                        if len(parsed_data) > 0:
                            ppd = json.dumps(parsed_data, indent=4)
                            parsed_data_json = os.path.join(reports_folder, f'{fs_object}.json' )
                            print('parsed_data_json:', parsed_data_json)
                            with open(parsed_data_json, 'w', encoding="utf-8") as f:
                                f.write(ppd)

                            if not keep_reports:
                                os.remove(json_file_path)


def cleanup_folders_files(folders_list=None):
    """
    :param folders_list:
    :return:
    """
    print('## Cleaning Folders and Files. ##')
    time.sleep(3)

    ''' process the logs folder '''
    for root, folders, files in os.walk(log_folder, topdown=False):
        for folder in folders:
            full_path = os.path.join(root, folder)
            # print('full_path1:', full_path)
            folders_or_files = os.listdir(full_path)
            if len(folders_or_files) == 0:
                if os.path.exists(full_path):
                    # print('full_path2:', full_path)
                    shutil.rmtree(full_path)

    ''' process the reports folder '''
    for root, folders, files in os.walk(reports_folder, topdown=False):
        for folder in folders:
            full_path = os.path.join(root, folder)
            # print('full_path1:', full_path)
            folders_or_files = os.listdir(full_path)
            if len(folders_or_files) == 0:
                if os.path.exists(full_path):
                    # print('full_path2:', full_path)
                    shutil.rmtree(full_path)


    ''' process the target for tests folder. '''
    folders_list = set(folders_list)
    for folder_path in folders_list:
        # print('folder_path:', folder_path)
        if 'random' in folder_path or 'sequential' in folder_path:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)



if run_create_execute_commands:
    commands_json = create_testing_commands()
    execute_commands(commands_json)

if run_parse_result_logs:
    parse_results_folder()

if run_html_creates:
    create_html_reports()

if run_cleanup_folders_files:
    cleanup_folders_files(all_folders_list)






