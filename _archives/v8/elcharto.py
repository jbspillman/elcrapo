import shutil
from datetime import datetime
import pandas as pd
import json
import time
import os

'''
https://chatgpt.com/share/688c6300-cf7c-800d-ad52-87634941fc6e

'''

''' default top level folder '''
script_folder = os.path.dirname(os.path.abspath(__file__))

''' directory should exist '''
log_folder = os.path.join(script_folder, "result-logs")
os.makedirs(log_folder, exist_ok=True)
date_log_stamp = datetime.now().strftime("%Y%m%d")
log_folder_dated = os.path.join(log_folder, date_log_stamp)
os.makedirs(log_folder_dated, exist_ok=True)

''' directories of data to compare, from bench_runner.py '''
n1_compare_folder = 'BS_Local_NVME'
n2_compare_folder = 'MS_NFS3_HDD'
n1_folder = os.path.join(log_folder_dated, n1_compare_folder)
n2_folder = os.path.join(log_folder_dated, n2_compare_folder)
folders_list = [
    n1_folder,
    n2_folder
]

def get_keys_with_name_of(data_list, target_key):
    print()

def get_keys_with_value_of(data_list, target_key):
    found_key_values = []
    for dictionary in data_list:
        if isinstance(dictionary, dict):  # Ensure the item is a dictionary
            for key, value in dictionary.items():
                if key == target_key:
                    found_key_values.append(value)
    return found_key_values


parsed_files_list = []
for folder_path in folders_list:
    folder_name = os.path.basename(folder_path)
    for file_name in os.listdir(folder_path):
        dir_name = os.path.basename(folder_path)
        if file_name.endswith('a_result.log'):
            log_file = os.path.join(folder_path, file_name)
            new_txt_path = os.path.join(log_folder_dated, dir_name, f"{dir_name}_result.log")
            print(new_txt_path)
            shutil.move(log_file, new_txt_path)
            parsed_files_list.append(new_txt_path)

        elif file_name.endswith('b_plain.csv'):
            new_json_path = os.path.join(log_folder_dated, dir_name, f"{dir_name}_result.json")
            df = pd.read_csv(os.path.join(folder_path, file_name))
            json_string = df.to_json(orient='records')
            parsed_json = json.loads(json_string)
            pretty_json = json.dumps(parsed_json, indent=4)
            with open(new_json_path, 'w', encoding="utf-8") as f:
                f.write(pretty_json)
            print(new_json_path)
            parsed_files_list.append(new_json_path)
            os.remove(os.path.join(folder_path, file_name))

        elif file_name.endswith('c_live.csv'):
            new_json_path = os.path.join(log_folder_dated, dir_name, f"{dir_name}_live.json")
            df = pd.read_csv(os.path.join(folder_path, file_name))
            json_string = df.to_json(orient='records')
            parsed_json = json.loads(json_string)
            pretty_json = json.dumps(parsed_json, indent=4)
            with open(new_json_path, 'w', encoding="utf-8") as f:
                f.write(pretty_json)
            print(new_json_path)
            parsed_files_list.append(new_json_path)
            os.remove(os.path.join(folder_path, file_name))
        else:
            file_is_ready = os.path.join(folder_path, file_name)
            parsed_files_list.append(file_is_ready)

for file_to_parse in parsed_files_list:

    ##########################
    ### FOLDER FILES 0001  ###
    ##########################

    if n1_compare_folder in file_to_parse:
        if 'live' in file_to_parse:
            with open(file_to_parse, 'r', encoding="utf-8") as file:
                live_data = json.load(file)

            all_test_labels = get_keys_with_value_of(live_data, "Label")
            the_labels = sorted(set(all_test_labels))
            the_tests_data = []
            for test_label in the_labels:
                tests_writes = []
                tests_reads = []

                print(f'Live in Folder 1 - Parse for: {test_label}')
                for item in live_data:
                    if item["Label"] == test_label and item["Rank"] == "Total":
                        idate = item["ISO Date"]
                        idone = item["Done%"]
                        iphase = item["Phase"]
                        ilat = item["Lat IO us"]
                        imib = item["MiB/s"]
                        iops = item["IOPS"]

                        if item["Phase"] == "WRITE":
                            w = {
                                "date": idate,
                                "done": idone,
                                "iops": iops,
                                "mib": imib,
                                "lat": ilat
                            }
                            tests_writes.append(w)
                        elif item["Phase"] == "READ":
                            r = {
                                "date": idate,
                                "done": idone,
                                "iops": iops,
                                "mib": imib,
                                "lat": ilat
                            }
                            tests_reads.append(r)
                tl = {
                    "label": test_label,
                    "writes": tests_writes,
                    "reads": tests_reads
                }
                the_tests_data.append(tl)

            pretty_json = json.dumps(the_tests_data, indent=4)
            new_json_path = os.path.join(log_folder_dated, n1_compare_folder, f"{n1_compare_folder}_PARSED-LIVE.json")
            with open(new_json_path, 'w', encoding="utf-8") as f:
                f.write(pretty_json)
            os.remove(file_to_parse)

        if 'result.json' in file_to_parse:
            with open(file_to_parse, 'r', encoding="utf-8") as file:
                result_data = json.load(file)
            all_test_labels = get_keys_with_value_of(result_data, "label")
            the_labels = sorted(set(all_test_labels))
            the_tests_data = []
            for test_label in the_labels:
                tests_writes = []
                tests_reads = []

                print(f'Results in Folder 1 - Parse for: {test_label}')
                for item in result_data:
                    if item["label"] == test_label:
                        idate = item["ISO date"]
                        ilat = item["IO lat us [avg]"]
                        imib = item["MiB/s [last]"]
                        iops = item["IOPS [last]"]
                        if item["operation"] == "WRITE":
                            w = {
                                "date": idate,
                                "iops": iops,
                                "mib": imib,
                                "lat": ilat
                            }
                            tests_writes.append(w)
                        if item["operation"] == "READ":
                            r = {
                                "date": idate,
                                "iops": iops,
                                "mib": imib,
                                "lat": ilat
                            }
                            tests_reads.append(r)
                tl = {
                    "label": test_label,
                    "writes": tests_writes,
                    "reads": tests_reads
                }
                the_tests_data.append(tl)

            pretty_json = json.dumps(the_tests_data, indent=4)
            new_json_path = os.path.join(log_folder_dated, n1_compare_folder, f"{n1_compare_folder}_PARSED-RESULTS.json")
            with open(new_json_path, 'w', encoding="utf-8") as f:
                f.write(pretty_json)
            os.remove(file_to_parse)

    ##########################
    ### FOLDER FILES 0002  ###
    ##########################

    if n2_compare_folder in file_to_parse:
        if 'live' in file_to_parse:
            with open(file_to_parse, 'r', encoding="utf-8") as file:
                live_data = json.load(file)

            all_test_labels = get_keys_with_value_of(live_data, "Label")
            the_labels = sorted(set(all_test_labels))
            the_tests_data = []
            for test_label in the_labels:
                tests_writes = []
                tests_reads = []

                print(f'Live in Folder 2 - Parse for: {test_label}')
                for item in live_data:
                    if item["Label"] == test_label and item["Rank"] == "Total":
                        idate = item["ISO Date"]
                        idone = item["Done%"]
                        iphase = item["Phase"]
                        ilat = item["Lat IO us"]
                        imib = item["MiB/s"]
                        iops = item["IOPS"]

                        if item["Phase"] == "WRITE":
                            w = {
                                "date": idate,
                                "done": idone,
                                "iops": iops,
                                "mib": imib,
                                "lat": ilat
                            }
                            tests_writes.append(w)
                        elif item["Phase"] == "READ":
                            r = {
                                "date": idate,
                                "done": idone,
                                "iops": iops,
                                "mib": imib,
                                "lat": ilat
                            }
                            tests_reads.append(r)
                tl = {
                    "label": test_label,
                    "writes": tests_writes,
                    "reads": tests_reads
                }
                the_tests_data.append(tl)

            pretty_json = json.dumps(the_tests_data, indent=4)
            new_json_path = os.path.join(log_folder_dated, n2_compare_folder, f"{n2_compare_folder}_PARSED-LIVE.json")
            with open(new_json_path, 'w', encoding="utf-8") as f:
                f.write(pretty_json)
            os.remove(file_to_parse)

        if 'result.json' in file_to_parse:
            with open(file_to_parse, 'r', encoding="utf-8") as file:
                result_data = json.load(file)
            all_test_labels = get_keys_with_value_of(result_data, "label")
            the_labels = sorted(set(all_test_labels))
            the_tests_data = []
            for test_label in the_labels:
                tests_writes = []
                tests_reads = []

                print(f'Results in Folder 2 - Parse for: {test_label}')
                for item in result_data:
                    if item["label"] == test_label:
                        idate = item["ISO date"]
                        ilat = item["IO lat us [avg]"]
                        imib = item["MiB/s [last]"]
                        iops = item["IOPS [last]"]
                        if item["operation"] == "WRITE":
                            w = {
                                "date": idate,
                                "iops": iops,
                                "mib": imib,
                                "lat": ilat
                            }
                            tests_writes.append(w)
                        if item["operation"] == "READ":
                            r = {
                                "date": idate,
                                "iops": iops,
                                "mib": imib,
                                "lat": ilat
                            }
                            tests_reads.append(r)
                tl = {
                    "label": test_label,
                    "writes": tests_writes,
                    "reads": tests_reads
                }
                the_tests_data.append(tl)

            pretty_json = json.dumps(the_tests_data, indent=4)
            new_json_path = os.path.join(log_folder_dated, n2_compare_folder, f"{n2_compare_folder}_PARSED-RESULTS.json")
            with open(new_json_path, 'w', encoding="utf-8") as f:
                f.write(pretty_json)
            os.remove(file_to_parse)


def reparse_data(the_data, the_device):
    new_list = []
    for nitem in the_data:
        label = nitem["label"]
        writes = nitem["writes"]
        reads = nitem["reads"]
        del writes[0]['date']
        del reads[0]['date']

        test_number = label.split("_")[0]
        test_mode = label.split("_")[1]
        test_size = label.split("_")[2].replace('Size', '').replace('[', '').replace(']', '')
        test_block = label.split("_")[3].replace('Block', '').replace('[', '').replace(']', '')
        test_thread = label.split("_")[4].replace('Thread', '').replace('[', '').replace(']', '')
        test_depth = label.split("_")[5].replace('Depth', '').replace('[', '').replace(']', '')

        if test_mode == "SEQ":
            test_mode = "Sequential"
        else:
            test_mode = "Random"

        k = {
            "number": test_number,
            "device": the_device,
            "mode": test_mode,
            "file_size": test_size,
            "block_size": test_block,
            "threads": test_thread,
            "io_depth": test_depth,
            "writes": writes,
            "reads": reads
        }
        new_list.append(k)
    pretty_new_list = json.dumps(new_list, indent=4)
    re_json_path = os.path.join(log_folder_dated, the_device, f"{the_device}_RE-PARSED_RESULTS.json")
    with open(re_json_path, 'w', encoding="utf-8") as f:
        f.write(pretty_new_list)

n1_parsed_results_path = os.path.join(log_folder_dated, n1_compare_folder, f"{n1_compare_folder}_PARSED-RESULTS.json")
with open(n1_parsed_results_path, 'r', encoding="utf-8") as file:
    n1_data = json.load(file)



n2_parsed_results_path = os.path.join(log_folder_dated, n2_compare_folder, f"{n2_compare_folder}_PARSED-RESULTS.json")
with open(n2_parsed_results_path, 'r', encoding="utf-8") as file:
    n2_data = json.load(file)

reparse_data(n1_data, n1_compare_folder)
reparse_data(n2_data, n2_compare_folder)
