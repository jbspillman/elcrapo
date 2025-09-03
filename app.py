from datetime import datetime
import pandas as pd
import timeit
import shutil
import json
import os


script_folder = os.path.dirname(os.path.abspath(__file__))
html_template = os.path.join(script_folder, 'html_template_cl01.txt')

log_folder = os.path.join(script_folder, "result-logs")
os.makedirs(log_folder, exist_ok=True)

reports_folder = os.path.join(script_folder, "result-reports")
os.makedirs(reports_folder, exist_ok=True)

target_name = "fNAS-5.2"
target_path = r"\\beastserver.beastmode.local.net\12000b"

test_list = [
    "SEQ_W",
    "SEQ_R",
    "RAN_W",
    "RAN_R"
]

date_log_stamp = datetime.now().strftime("%Y%m%d")
time_log_stamp = datetime.now().strftime("%H%M")

log_folder_dated = os.path.join(log_folder, date_log_stamp)
os.makedirs(log_folder_dated, exist_ok=True)

test_folder = os.path.join(log_folder_dated, time_log_stamp)
os.makedirs(test_folder, exist_ok=True)


def run_benchmarks():
    elbencho_exe = r'C:\Users\spillman\Documents\elbencho\elbencho.exe'

    block_sizes = ["4K"]
    threads_list = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
    test_number = 0
    io_depth = 1

    cleanup_folders = []
    for test in test_list:
        test_options = (f'--cpu --lat --direct --files "1" --dirs "1" --mkdirs '  # --dirsharing --nodelerr 
                        f'--no0usecerr --live1 --livecsvex --log "1" --liveint "1000" --timelimit "300"') # --dryrun

        pre_fix = '00'
        if 'SEQ' in test:
            block_sizes = ["256K", "512K" ,'1024K']
        elif 'RAN' in test:
            block_sizes = ["4K" , "8K", "32K"]

        test_size = 8096
        test_mode = "--write"
        
        if test == "SEQ_W":
            pre_fix = '01'
            test_mode = "--write"
            test_size = "2048"
        elif test == "SEQ_R":
            pre_fix = '02'
            test_mode = "--write --read"
            test_size = "2048"
        elif test == "RAN_W":
            pre_fix = '03'
            test_mode = "--write --rand"
            test_size = "128"
        elif test == "RAN_R":
            pre_fix = '04'
            test_mode = "--write --read --rand"
            test_size = "128"

        for block_size in block_sizes:
            for thread in threads_list:
                ztd = str(thread).zfill(3)
                test_number += 1
                test_pad = str(test_number).zfill(3)
                zbs = str(block_size).zfill(5)
                file_name = f'{pre_fix}_{test}_{zbs}'
                label_name = f'{file_name}_{ztd}'
                res_file = os.path.join(test_folder, f"{file_name}.txt")
                csv_file = os.path.join(test_folder, f"{file_name}.csv")
                csv_live = os.path.join(test_folder, f"{file_name}.live")
                
                notes_text = os.path.join(test_folder, f"product.txt")
                
                with open(notes_text, 'w', encoding='utf-8') as text_out:
                    text_out.write(f'{target_name}\n')
                
                file_size = round(int(test_size) / int(thread))

                safe_folder_path = os.path.join(target_path, 'SafeFolder', f'{test}_{zbs}')
                os.makedirs(safe_folder_path, exist_ok=True)
                if safe_folder_path not in cleanup_folders:
                    cleanup_folders.append(safe_folder_path)

                full_cmd = (f'{elbencho_exe} '
                            f'--label {label_name} '
                            f'{test_mode} '
                            f'--iodepth={io_depth} '
                            f'--threads={thread} '
                            f'--block={block_size} '
                            f'--size={file_size}M '
                            f'--csvfile {csv_file} '
                            f'--resfile {res_file} '
                            f'--livecsv {csv_live} '
                            f'{test_options} '
                            f'{safe_folder_path} '
                            )

                start_it = timeit.default_timer()
                os.system(full_cmd)
                finish_it = timeit.default_timer()
                test_time = finish_it - start_it
                print(label_name, safe_folder_path, 'test took:', test_time)
                print()


    # Delete the directory and its contents
    for folder_path in cleanup_folders:
        try:
            shutil.rmtree(folder_path)
            print(f"Directory '{folder_path}' and its contents deleted successfully.")
        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}.")


def parse_results_folders():
    list_of_folders = []
    
    for date_folder_name in sorted(os.listdir(log_folder)):
        print('Checking for data:'.ljust(30), date_folder_name)
        date_folder_path = os.path.join(log_folder, date_folder_name)
        for time_folder_name in sorted(os.listdir(date_folder_path)):
            print(' Checking for data:'.ljust(30), time_folder_name)
            time_folder_path = os.path.join(date_folder_path, time_folder_name)
            parsed_results = os.path.join(time_folder_path, "PARSED")
            os.makedirs(parsed_results, exist_ok=True)
            if time_folder_path not in list_of_folders:
                list_of_folders.append(time_folder_path)
            for file_name in sorted(os.listdir(time_folder_path)):
                test_file_path = os.path.join(time_folder_path, file_name)
                if file_name.endswith('.csv'):
                    df = pd.read_csv(test_file_path)
                    json_string = df.to_json(orient='records')
                    parsed_json = json.loads(json_string)
                    pretty_json = json.dumps(parsed_json, indent=4)
                    new_json_file_name = file_name.replace('.csv', '.json')
                    new_json_path = os.path.join(time_folder_path, new_json_file_name)
                    with open(new_json_path, 'w', encoding="utf-8") as f:
                        f.write(pretty_json)
                    print('created:'.ljust(30), new_json_path)
                    os.remove(test_file_path)
                elif file_name.endswith('.txt') or file_name.endswith('.live'):
                    os.remove(test_file_path)
                elif file_name.endswith('.json') or file_name.endswith('_parsed.json'):
                    skip = True


            for file_name in sorted(os.listdir(time_folder_path)):
                parsed_results = os.path.join(time_folder_path, "PARSED")
                os.makedirs(parsed_results, exist_ok=True)
                test_file_path = os.path.join(time_folder_path, file_name)
                if file_name.endswith('.json'):
                    print()
                    print("PARSING:".ljust(30), file_name)
                    with open(test_file_path, 'r', encoding="utf-8") as file:
                        data = json.load(file)

                    if 'SEQ_W' in file_name:
                        test_mode = 'Sequential'
                        target_operation = 'WRITE'
                    elif 'SEQ_R' in file_name:
                        test_mode = 'Sequential'
                        target_operation = 'READ'
                    elif 'RAN_W' in file_name:
                        test_mode = 'Random'
                        target_operation = 'WRITE'
                    elif 'RAN_R' in file_name:
                        test_mode = 'Random'
                        target_operation = 'READ'
                    else:
                        test_mode = 'DIRS'
                        target_operation = 'MKDIRS'

                    print("OPERATION_TARGET:".ljust(30), target_operation)
                    target_list = []
                    for item in data:
                        operation = item["operation"]
                        if operation == target_operation:
                            test_label = item["label"]
                            label_splits = test_label.split('_')
                            label_name = "_".join(label_splits[0:4])

                            iso_date = item["ISO date"]
                            threads = item["threads"]
                            file_size = item["file size"]
                            block_size = item["block size"]
                            random = item["random"]
                            io_depth = item["IO depth"]
                            iops_last = item["IOPS [last]"]
                            mibs_last = item["MiB/s [last]"]
                            io_lat_avg_us = item["IO lat us [avg]"]

                            k = {
                                "target_name": target_name,
                                "test_label": test_label,
                                "iso_date": iso_date,
                                "mode": test_mode,
                                "operation": target_operation,
                                "file_size": file_size,
                                "block_size": block_size,
                                "threads": threads,
                                "io_depth": io_depth,
                                "iops_last": iops_last,
                                "mibs_last": mibs_last,
                                "io_lat_avg_us": io_lat_avg_us,
                                "file_name": file_name
                            }
                            target_list.append(k)

                    os.remove(test_file_path)
                    print('target_list:'.ljust(30), len(target_list))

                    pretty_target_list = json.dumps(target_list, indent=4)
                    new_name = file_name.replace('.json', '_parsed.json')
                    newer_json_path = os.path.join(parsed_results, new_name)
                    with open(newer_json_path, 'w', encoding="utf-8") as f:
                        f.write(pretty_target_list)
                    print('created:'.ljust(30), newer_json_path)


def parse_to_reports():
    for dirpath, dirnames, filenames in os.walk(log_folder, topdown=False):
        for filename in sorted(filenames):
            if filename.endswith('parsed.json') and 'PARSED' in dirpath and 'ALL' not in filename:
                print()
                dirs_split = dirpath.split(os.sep)
                f_date_stamp = dirs_split[-3]
                f_time_stamp = dirs_split[-2]

                all_parsed_json_content = []
                file_name_json_path = os.path.join(dirpath, filename)
                print('file_name_json_path:'.ljust(30), file_name_json_path)
                with open(file_name_json_path, 'r', encoding="utf-8") as file:
                    data = json.load(file)
                    all_parsed_json_content.extend(data)

                new_data_path = os.path.join(reports_folder, f_date_stamp, f_time_stamp)
                os.makedirs(new_data_path, exist_ok=True)
                reports_json_file_path = os.path.join(new_data_path, filename)
                if len(data) > 0:
                    pretty_data = json.dumps(data, indent=4)
                    with open(reports_json_file_path, 'w', encoding="utf-8") as f:
                        f.write(pretty_data)
                    print('reports_json_file_path:'.ljust(30), reports_json_file_path)
                    os.remove(file_name_json_path)


def create_html_files():
    folders = []
    for dirpath, dirnames, filenames in os.walk(reports_folder):
        for filename in filenames:
            if not filename.startswith('All'):
                if dirpath not in folders:
                    folders.append(dirpath)

    for folder in sorted(folders):
        print('check folder:'.ljust(30), folder)

        for dirpath, dirnames, filenames in os.walk(folder):
            all_data_json = os.path.join(dirpath, "all_data.json")
            all_data = []
            for filename in filenames:
                if filename.startswith('all') or 'html' in filename:
                    skip = True
                else:
                    reports_data_json_path = os.path.join(dirpath, filename)
                    print('reports_data_json_path:'.ljust(30), reports_data_json_path)
                    with open(reports_data_json_path, 'r', encoding="utf-8") as file:
                        file_data = json.load(file)
                    for item in file_data:
                        if item not in all_data:
                            all_data.append(item)

            pretty_data = json.dumps(all_data, indent=4)
            print("all_data:".ljust(30), len(all_data))
            with open(all_data_json, 'w', encoding="utf-8") as f:
                f.write(pretty_data)
            print('all_data_json:'.ljust(30), all_data_json)

            if os.path.exists(all_data_json):
                json_dicts_as_string = ''
                with open(all_data_json, 'r', encoding="utf-8") as file:
                    all_data = json.load(file)
                x = 0
                for item in all_data:
                    x += 1
                    if x == len(all_data):
                        json_dicts_as_string += f'        {str(item)}'
                    else:
                        json_dicts_as_string += f'        {str(item)},\n'
                json_dicts_as_string = json_dicts_as_string.lstrip('        ')


                ''' read input template '''
                with open(html_template, 'r', encoding="utf-8") as html_file:
                    html_data_as_text = html_file.read()

                my_chart_html = ''
                for line in html_data_as_text.split('\n'):
                    if 'TEXT_JSON_DICTS' in line:
                        line = line.replace('TEXT_JSON_DICTS', json_dicts_as_string)
                        my_chart_html += f'{line}\n'
                    else:
                        my_chart_html += f'{line}\n'

                # start_sleep = False
                # for line in my_chart_html.split('\n'):
                #     if '// Create Data' in line:
                #         start_sleep = True
                #     print(line)
                #     if start_sleep:
                #         time.sleep(.01)

                ''' save to new file '''
                report_html = os.path.join(dirpath, 'test_results.html')
                with open(report_html, 'w', encoding="utf-8") as html_out_file:
                    html_out_file.write(my_chart_html)
                print('created:'.ljust(30), report_html)

            #
            #
            #         ''' read new web file '''
            #         with open(report_html, 'r', encoding="utf-8") as html_content:
            #             raw_data = html_content.read()
            #
            #         ''' loop through the json data for charts. '''
            #         with open(all_json, 'r', encoding="utf-8") as file:
            #             all_json_data = json.load(file)
            #
            #         # json_as_text = ''
            #         # for line in data:
            #         #     json_as_text += f'{line},\n'
            #         # json_as_text = json_as_text.rstrip(',\n')
            #
            #         print(all_json_data)
            #         time.sleep(2)

                    # new_html = ''
                    # for line in raw_data.split('\n'):
                    #     line = line.rstrip()
                    #     if 'TEXT_JSON_DICTS' in line:
                    #         print("RAW HTML:", line)
                    # # print(new_html)
                    # return
                    #
                    # with open(report_html, 'w', encoding="utf-8") as html_out_file:
                    #     html_out_file.write(new_html)


def remove_empty_folders(list_of_folders):
    
    for directory_to_remove in list_of_folders:
        # print('Checking:', directory_to_remove)
        for dirpath, dirnames, filenames in os.walk(directory_to_remove, topdown=False):
            if len(filenames) == 0 and len(dirnames) == 0:
                os.rmdir(dirpath)
                # print(f"Removed empty directory: {dirpath}")

            for dirname in dirnames:
                this_dir = os.path.join(dirpath, dirname)
                for dirpath2, dirnames2, filenames2 in os.walk(this_dir, topdown=False):
                    if len(filenames2) == 0 and len(dirnames2) == 0:
                        os.rmdir(dirpath2)
                        # print(f"Removed empty directory: {dirpath2}")


            # Check if the directory is empty after processing its contents (if topdown=False)
            # if not dirnames and not filenames:
            #     try:
            #         os.rmdir(dirpath)
            #         print(f"Removed empty directory: {dirpath}")
            #     except OSError as e:
            #         # Handle cases where the directory might not be truly empty (e.g., hidden files)
            #         print(f"Could not remove directory {dirpath}: {e}")


''' run benchmarking '''
print()
run_benchmarks()

''' parse the data from csv to json '''
print()
parse_results_folders()

''' move to reports location for html generation '''
print()
parse_to_reports()

''' create the html data files '''
print()
create_html_files()

''' clean up empty folders '''
print()
remove_empty_folders([log_folder, reports_folder])

exit(0)
