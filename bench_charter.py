from collections import defaultdict
import pandas as pd
import json
import os


def get_values_from_keys_with_name(data_list, key_name):
    found_key_values = []
    for dictionary in data_list:
        if isinstance(dictionary, dict):  # Ensure the item is a dictionary
            for key, value in dictionary.items():
                if key == key_name:
                    found_key_values.append(value)
    return found_key_values


def get_key_value_from_list(data_list, key_name, value_check):
    list_of_dicts = []
    for dictionary in data_list:
        if isinstance(dictionary, dict):  # Ensure the item is a dictionary
            for key, value in dictionary.items():
                if key == key_name:
                    if value == value_check:
                        list_of_dicts.append(dictionary)
    return list_of_dicts


def convert_csv_data(folder_path):
    files_int = 0
    for file_name in os.listdir(folder_path):
        files_int += 1
        file_path_name = os.path.join(folder_path, file_name)
        if file_name.endswith('.live'):
            os.remove(file_path_name)
        elif file_name.endswith('.txt'):
            os.remove(file_path_name)
        elif file_name.endswith('.html'):
            os.remove(file_path_name)
        elif file_name.endswith('.json'):
            skip = True
        elif file_name.endswith('.JSON'):
            skip = True       
        elif file_name.endswith('.csv'):
            csv_file_path = file_path_name
            new_json_file_name = file_name.replace('.csv', '.json')
            new_json_path = os.path.join(folder_path, new_json_file_name)
            df = pd.read_csv(csv_file_path)
            json_string = df.to_json(orient='records')
            parsed_json = json.loads(json_string)
            pretty_json = json.dumps(parsed_json, indent=4)
            with open(new_json_path, 'w', encoding="utf-8") as f:
                f.write(pretty_json)
            os.remove(csv_file_path)
        else:
            print('OTHER file_path_name:'.ljust(30), file_path_name)


def parse_test_data_files(folder_path):
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            
            target_name = file_name.split('_')[0]
            if 'RANDOM' in file_name:
                test_mode = "Random"
            else:
                test_mode = "Sequential"
            if 'FILE_BASED' in file_name:
                test_type = "File"
            else:
                test_type = "Directory"

            writes_list = []
            reads_list = []

            with open(file_path, 'r', encoding="utf-8") as file:
                the_data = json.load(file)
                
            for item in the_data:
                threads = item["threads"]
                file_size = item["file size"]
                block_size = item["block size"]
                io_depth = item["IO depth"]
                operation = item["operation"]
                iops = item["IOPS [last]"]
                mibs = item["MiB/s [last]"]
                lat = item["IO lat us [avg]"]
                if operation == "READ":
                    operation = "Read"
                elif operation == "WRITE":
                    operation = "Write"
                k = {
                    "target_name": target_name,
                    "test_mode": test_mode,
                    "operation": operation,
                    "test_type": test_type,
                    "threads": threads,
                    "file_size": file_size,
                    "block_size": block_size,
                    "io_depth": io_depth,
                    "iops": iops,
                    "mibs": mibs,
                    "lat": lat
                }
                if operation == "Read":
                    reads_list.append(k)

                if operation == "Write":
                    writes_list.append(k)

            pretty_reads = json.dumps(reads_list, indent=4)
            new_reads_json_file = f'{target_name}__{test_mode}_Read_{test_type}.JSON'
            new_reads_path = os.path.join(folder_path, new_reads_json_file)
            with open(new_reads_path, 'w', encoding="utf-8") as f:
                f.write(pretty_reads)

            pretty_writes = json.dumps(writes_list, indent=4)
            new_writes_json_file = f'{target_name}__{test_mode}_Write_{test_type}.JSON'
            new_writes_path = os.path.join(folder_path, new_writes_json_file)
            with open(new_writes_path, 'w', encoding="utf-8") as f:
                f.write(pretty_writes)          
            os.remove(file_path)



def create_report_data(folder_path):

    test_types_ordered = [
        "Sequential_Write",
        "Sequential_Read",
        "Random_Write",
        "Random_Read"
    ]

    test_results_directory_sw = []
    test_results_directory_sr = []
    test_results_directory_rw = []
    test_results_directory_rr = []
    tests_results_directory_ot = []
    
    results_folder = ''
    
    directory_tests = []
    file_tests = []
    tmp_names_list = []
    for file_name in os.listdir(folder_path):
        file_path_name = os.path.join(folder_path, file_name)
        if file_name.endswith(".JSON"):
            tgt_name = file_name.split('_')[0]
            if tgt_name not in tmp_names_list:
                tmp_names_list.append(tgt_name)
          
            if '_Directory.' in file_name:
                directory_tests.append(file_path_name)
                
            elif '_File.' in file_name:
                file_tests.append(file_path_name)

    print('Process Directory Tests:')
    for test_type in test_types_ordered:
        if test_type == "Sequential_Write":
            list_to_use = test_results_directory_sw
        elif test_type == "Sequential_Read":
            list_to_use = test_results_directory_sr
        elif test_type == "Random_Write":
            list_to_use = test_results_directory_rw
        elif test_type == "Random_Read":
            list_to_use = test_results_directory_rr
        else:
            list_to_use = tests_results_directory_ot

        for file_name_path in directory_tests:
            file_name = os.path.basename(file_name_path)
            with open(file_name_path, 'r', encoding="utf-8") as file:
                result_data = json.load(file)
            if test_type in file_name:
                target_name = file_name.split('_')[0]
                for result in result_data:
                    k = {
                        "target_name": target_name,
                        "threads": result["threads"],
                        "iops": result["iops"],
                        "mibs": result["mibs"],
                        "lat": result["lat"],
                    }
                    list_to_use.append(k)
                    
                    
    print('test_results_directory_sw:', len(test_results_directory_sw))
    print('test_results_directory_sr:', len(test_results_directory_sr))
    print('test_results_directory_rw:', len(test_results_directory_rw))
    print('test_results_directory_rr:', len(test_results_directory_rr))
    print('tests_results_directory_ot:', len(tests_results_directory_ot))

    grouped_dsw = defaultdict(dict)
    for entry in test_results_directory_sw:
        threads = str(entry["threads"])  # Use string keys for JSON compatibility
        target = entry["target_name"]
        grouped_dsw[threads][target] = {
            "iops": entry["iops"],
            "mibs": entry["mibs"],
            "lat": entry["lat"]
        }

    grouped_dsr = defaultdict(dict)
    for entry in test_results_directory_sr:
        threads = str(entry["threads"])  # Use string keys for JSON compatibility
        target = entry["target_name"]
        grouped_dsr[threads][target] = {
            "iops": entry["iops"],
            "mibs": entry["mibs"],
            "lat": entry["lat"]
        }

    grouped_drw = defaultdict(dict)
    for entry in test_results_directory_rw:
        threads = str(entry["threads"])  # Use string keys for JSON compatibility
        target = entry["target_name"]
        grouped_drw[threads][target] = {
            "iops": entry["iops"],
            "mibs": entry["mibs"],
            "lat": entry["lat"]
        }

    grouped_drr = defaultdict(dict)
    for entry in test_results_directory_rr:
        threads = str(entry["threads"])  # Use string keys for JSON compatibility
        target = entry["target_name"]
        grouped_drr[threads][target] = {
            "iops": entry["iops"],
            "mibs": entry["mibs"],
            "lat": entry["lat"]
        }

    ''' write the template data to the new file.'''
    script_folder = os.path.dirname(os.path.abspath(__file__))
    template_file_for_charts = os.path.join(script_folder, 'template_single_chart.html')
    with open(template_file_for_charts, "r", encoding="utf-8") as html_template:
        html_content = html_template.read()


    str_grouped_dsw = str(dict(grouped_dsw))
    str_grouped_dsr = str(dict(grouped_dsr))
    str_grouped_drw = str(dict(grouped_drw))
    str_grouped_drr = str(dict(grouped_drr))

    new_content = html_content
    new_content = new_content.replace('GROUPED_SEQ_WRITE_DICTIONARY', str_grouped_dsw)
    new_content = new_content.replace('GROUPED_SEQ_READ_DICTIONARY', str_grouped_dsr)
    new_content = new_content.replace('GROUPED_RAN_WRITE_DICTIONARY', str_grouped_drw)
    new_content = new_content.replace('GROUPED_RAN_READ_DICTIONARY', str_grouped_drr)

    ver_name_x = tmp_names_list[0]
    ver_name_y = tmp_names_list[1]
    
    new_content = new_content.replace("XXXXX_VERSION_XXXXX", ver_name_x)
    new_content = new_content.replace("YYYYY_VERSION_YYYYY", ver_name_y)

    new_website_charts_file = os.path.join(folder_path, 'charted_results.html')
    with open(new_website_charts_file, "w", encoding="utf-8") as html_chart:
        html_chart.write(new_content)
    print('created:', new_website_charts_file)
    print('')
    


def create_reports(results_folder_path):

    convert_csv_data(results_folder_path)    
    parse_test_data_files(results_folder_path)
    create_report_data(results_folder_path)
   


