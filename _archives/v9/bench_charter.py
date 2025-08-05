import matplotlib.pyplot as plt
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
    parsed_file_check = []
    files_int = 0
    for file_name in os.listdir(folder_path):
        files_int += 1
        if file_name.endswith('.txt') or file_name.endswith('.json'):
            if file_name.endswith('-live.json'):
                live_json_path = os.path.join(folder_path, file_name)
                os.remove(live_json_path)
            else:
                skip = True
        elif file_name.endswith('.csv'):
            print()
            print('found file:'.ljust(30), file_name)
            csv_file_path = os.path.join(folder_path, file_name)
            if csv_file_path not in parsed_file_check:
                parsed_file_check.append(csv_file_path)

                df = pd.read_csv(csv_file_path)
                json_string = df.to_json(orient='records')
                parsed_json = json.loads(json_string)
                pretty_json = json.dumps(parsed_json, indent=4)

                new_json_file_name = file_name.replace('.csv', '.json')
                new_json_path = os.path.join(folder_path, new_json_file_name)
                with open(new_json_path, 'w', encoding="utf-8") as f:
                    f.write(pretty_json)
                os.remove(csv_file_path)
                print('created file:'.ljust(30), new_json_file_name)


def parse_test_data_files(folder_path):
    parsed_json_path = os.path.join(folder_path, "__PARSED.JSON")
    if os.path.exists(parsed_json_path):
        os.remove(parsed_json_path)

    the_tests_data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('-live.json'):
            os.remove(os.path.join(folder_path, file_name))

        elif file_name.endswith('.json'):

            # Note do not delimit test name by underscores...
            # if 'smb_lan' in file_name:
            #     file_to_parse = os.path.join(folder_path, file_name)
            #     new_file_name = file_name.replace('smb_lan', 'smb-lan')
            #     new_file_name_path = os.path.join(folder_path, new_file_name)
            #     os.rename(file_to_parse, new_file_name_path)
            #     file_name = new_file_name
            # if 'smb_wan' in file_name:
            #     file_to_parse = os.path.join(folder_path, file_name)
            #     new_file_name = file_name.replace('smb_wan', 'smb-wan')
            #     new_file_name_path = os.path.join(folder_path, new_file_name)
            #     os.rename(file_to_parse, new_file_name_path)
            #     file_name = new_file_name

            target_name = file_name.split('_')[0]
            test_number = file_name.split('_')[1]
            test_mode = file_name.split('_')[2]
            test_operation = file_name.split('_')[3]
            test_size = file_name.split('_')[5]
            test_block = file_name.split('_')[6]
            test_thread = file_name.split('_')[7].replace('T', '')
            test_depth = file_name.split('_')[8].replace('IOD.json', '')

            # print()
            # print(file_name)
            # print(0, target_name)
            # print(1, test_number)
            # print(2, test_mode)
            # print(3, test_operation)
            # print(4, test_size)
            # print(5, test_block)
            # print(6, test_thread)
            # print(7, test_depth)

            test_name = f'{test_mode}_{test_operation}_{test_size}_{test_block}_{test_thread}_{test_depth}'

            if test_mode == "RAN":
                mode_string = 'Random'
            else:
                mode_string = 'Sequential'
            if test_operation == "READ":
                operation_string = "Read:"
            else:
                operation_string = "Write:"

            chart_test_name = f'{test_number} {mode_string} {operation_string}\n'
            chart_test_name += f'File Size: {test_size}\n'
            chart_test_name += f'Block Size: {test_block}\n'
            chart_test_name += f'Threads: {test_thread}\n'
            chart_test_name += f'Depth: {test_depth}'

            test_title = f'{test_number}_{test_name}'
            file_to_parse = os.path.join(folder_path, file_name)
            with open(file_to_parse, 'r', encoding="utf-8") as file:
                the_data = json.load(file)

            try:
                ilat = the_data[0]["IO lat us [avg]"]
            except IndexError:
                print(the_data)
                print(file_to_parse)
                exit(0)
            try:
                imib = the_data[0]["MiB/s [last]"]
            except IndexError:
                print(the_data)
                print(file_to_parse)
                exit(0)
            try:
                iops = the_data[0]["IOPS [last]"]
            except IndexError:
                print(the_data)
                print(file_to_parse)
                exit(0)

            k = {
                "test_title": test_title,
                "chart_test_name": chart_test_name,
                "test_name": test_name,
                "test_mode": test_mode,
                "test_operation": test_operation,
                "test_size": test_size,
                "test_block": test_block,
                "test_thread": test_thread,
                "test_depth": test_depth,
                "target_name": target_name,
                "test_iop": iops,
                "test_mib": imib,
                "test_lat": ilat
            }
            if k not in the_tests_data:
                the_tests_data.append(k)
                pretty_k = json.dumps(k, indent=4)
                # print(pretty_k)

    pretty_test_data = json.dumps(the_tests_data, indent=4)
    with open(parsed_json_path, 'w', encoding="utf-8") as f:
        f.write(pretty_test_data)
    return parsed_json_path


def create_charts_from_json(json_file_path):
    images_list = []

    my_x_label = "\n\nFour Corner Tests\n(need to play with ordering).."

    current_data_folder = os.path.dirname(json_file_path)
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    ''' get devices in the data. '''
    test_device_names = set(get_values_from_keys_with_name(data, "target_name"))
    test_device_names = sorted(list(test_device_names))

    ''' get the test names in the data. '''
    test_names = set(get_values_from_keys_with_name(data, "test_name"))
    test_names = sorted(list(test_names))
    test_names_uniq = []
    for tn in test_names:
        if 'SEQ_WRITE' in tn:
            test_category = 'Sequential Write'
        elif 'SEQ_READ' in tn:
            test_category = 'Sequential Read'
        elif 'RAN_WRITE' in tn:
            test_category = 'Random Write'
        elif 'RAN_READ' in tn:
            test_category = 'Random Read'
        else:
            test_category = 'Unknown Test'
        if test_category not in test_names_uniq:
            test_names_uniq.append(test_category)
    test_names = sorted(test_names_uniq, reverse=True)


    ''' group by block size for charts. '''
    tmp_blocks_list = get_values_from_keys_with_name(data, "test_block")
    int_blocks_list = []
    for x in tmp_blocks_list:
        y = x.replace('K', '').replace('M', '')
        int_blocks_list.append(y)
    tmp_blocks_list = int_blocks_list
    tmp_blocks_list = set(tmp_blocks_list)
    sorted_block_sizes = sorted(tmp_blocks_list, key=int)

    for block_size in sorted_block_sizes:
        print()
        block_size = f'{block_size}K'

        for tcat in test_names:
            big_dict_of_data = {}
            cat_label = f'{tcat} @ {block_size}'
            big_dict_of_data["category"] = cat_label

            print(big_dict_of_data)

    exit(0)





# test_size = item["test_size"]
# test_thread = item["test_thread"]
# test_depth = item["test_depth"]
# test_iop = item["test_iop"]
# test_mib = item["test_mib"]
# test_lat = item["test_lat"]


            # print()
            # print('test_category:'.ljust(30), test_category)
            # ddict['category'] = test_category
            # ddict[target_name] = test_iop
            #
            # print(ddict)


            # category_string = f'{test_category} @ {block_size} Blocks'
            # ddict['category'] = category_string
            # ddict[target_name] = test_iop
            # print(ddict)

            # new_list.append(ddict)
    # pretty_list = json.dumps(new_list, indent=4)
    # print(pretty_list)



    # ''' group by threads for charts '''
    # tmp_threads_list = get_values_from_keys_with_name(data, "test_thread")
    # tmp_threads_list = set(tmp_threads_list)
    # sorted_string_numbers = sorted(tmp_threads_list, key=int)
    # for thread_count in sorted_string_numbers:
    #     thread_pad = str(thread_count).zfill(3)
    #     test_cases_per_threads = get_key_value_from_list(data, "test_thread", thread_count)
    #     df_threads = pd.DataFrame(test_cases_per_threads)
    #     print(df_threads)

        # ''' Create the three chart types, IOPS, MIBS, LATENCY based on Threads '''

        # ''' IOPs Chart --------------------------------------------------------------------------------------------- '''
        # # Filter relevant columns IOPs
        # df_filtered_iops = df[["chart_test_name", "target_name", "test_iop"]]
        #
        # # Pivot so that each test_name is a row, and each target_name is a column
        # df_pivot_iops = df_filtered_iops.pivot(index="chart_test_name", columns="target_name", values="test_iop")
        #
        # # Plot grouped bar chart
        # ax = df_pivot_iops.plot(kind="bar", figsize=(10, 6), colormap="tab20")
        #
        # # Add data labels to each bar
        # for container in ax.containers:
        #     ax.bar_label(container, fmt='%.0f', label_type='edge', padding=-3)
        #
        # # Style the chart
        # plt_iops = plt
        # plt_iops.title(f"IOP/s @ Thread Count of: {thread_count}")
        # plt_iops.ylabel("IOP/s")
        # plt_iops.xlabel(my_x_label)
        # plt_iops.xticks(rotation=0, ha="center")
        # plt_iops.grid(True, axis='y', linestyle='--', linewidth=0.5)
        # plt_iops.legend(title="Target", bbox_to_anchor=(1.05, 1), loc='upper left')
        # plt_iops.tight_layout()
        # # Show the chart
        # # plt_iops.show()
        # # Save the figure
        # chart_file = os.path.join(current_data_folder, f'chart_iops_threads-{thread_pad}.png')
        # plt_iops.savefig(chart_file)
        # images_list.append(chart_file)
        # print('created:'.ljust(30), chart_file)


    ''' group by threads for charts '''
    #
    # tmp_threads_list = get_values_from_keys_with_name(data, "test_thread")
    # tmp_threads_list = set(tmp_threads_list)
    # print(tmp_threads_list)
    # sorted_string_numbers = sorted(tmp_threads_list, key=int)
    # for thread_count in sorted_string_numbers:
    #     thread_pad = str(thread_count).zfill(3)
    #     test_cases_per_threads = get_key_value_from_list(data, "test_thread", thread_count)
    #     df = pd.DataFrame(test_cases_per_threads)
    #
    #     ''' Create the three chart types, IOPS, MIBS, LATENCY based on Threads '''
    #
    #     ''' IOPs Chart --------------------------------------------------------------------------------------------- '''
    #     # Filter relevant columns IOPs
    #     df_filtered_iops = df[["chart_test_name", "target_name", "test_iop"]]
    #
    #     # Pivot so that each test_name is a row, and each target_name is a column
    #     df_pivot_iops = df_filtered_iops.pivot(index="chart_test_name", columns="target_name", values="test_iop")
    #
    #     # Plot grouped bar chart
    #     ax = df_pivot_iops.plot(kind="bar", figsize=(10, 6), colormap="tab20")
    #
    #     # Add data labels to each bar
    #     for container in ax.containers:
    #         ax.bar_label(container, fmt='%.0f', label_type='edge', padding=-3)
    #
    #     # Style the chart
    #     plt_iops = plt
    #     plt_iops.title(f"IOP/s @ Thread Count of: {thread_count}")
    #     plt_iops.ylabel("IOP/s")
    #     plt_iops.xlabel(my_x_label)
    #     plt_iops.xticks(rotation=0, ha="center")
    #     plt_iops.grid(True, axis='y', linestyle='--', linewidth=0.5)
    #     plt_iops.legend(title="Target", bbox_to_anchor=(1.05, 1), loc='upper left')
    #     plt_iops.tight_layout()
    #     # Show the chart
    #     # plt_iops.show()
    #     # Save the figure
    #     chart_file = os.path.join(current_data_folder, f'chart_iops_threads-{thread_pad}.png')
    #     plt_iops.savefig(chart_file)
    #     images_list.append(chart_file)
    #     print('created:'.ljust(30), chart_file)
    #
    #     ''' MiBs Chart --------------------------------------------------------------------------------------------- '''
    #     # Filter relevant columns MiB's
    #     df_filtered_mib = df[["chart_test_name", "target_name", "test_mib"]]
    #
    #     # Pivot so that each test_name is a row, and each target_name is a column
    #     df_pivot_mib = df_filtered_mib.pivot(index="chart_test_name", columns="target_name", values="test_mib")
    #
    #     # Plot grouped bar chart
    #     ax = df_pivot_mib.plot(kind="bar", figsize=(10, 6), colormap="tab20")
    #
    #     # Add data labels to each bar
    #     for container in ax.containers:
    #         ax.bar_label(container, fmt='%.0f', label_type='edge', padding=-3)
    #
    #     # Style the chart
    #     plt_mib = plt
    #     plt_mib.title(f"MiB/s @ Thread Count of: {thread_count}")
    #     plt_mib.ylabel("MiB/s")
    #     plt_mib.xlabel(my_x_label)
    #     plt_mib.xticks(rotation=0, ha="center")
    #     plt_mib.grid(True, axis='y', linestyle='--', linewidth=0.5)
    #     plt_mib.legend(title="Target", bbox_to_anchor=(1.05, 1), loc='upper left')
    #     plt_mib.tight_layout()
    #     # Show the chart
    #     # plt_mib.show()
    #     # Save the figure
    #     chart_file = os.path.join(current_data_folder, f'chart_mibs_threads-{thread_pad}.png')
    #     plt_iops.savefig(chart_file)
    #     images_list.append(chart_file)
    #     print('created:'.ljust(30), chart_file)
    #
    #     ''' Latency Chart ------------------------------------------------------------------------------------------ '''
    #
    #     # Filter relevant columns MiB's
    #     df_filtered_lat = df[["chart_test_name", "target_name", "test_lat"]]
    #
    #     # Pivot so that each test_name is a row, and each target_name is a column
    #     df_pivot_lat = df_filtered_lat.pivot(index="chart_test_name", columns="target_name", values="test_lat")
    #
    #     # Plot grouped bar chart
    #     ax = df_pivot_lat.plot(kind="bar", figsize=(10, 6), colormap="tab20")
    #
    #     # Add data labels to each bar
    #     for container in ax.containers:
    #         ax.bar_label(container, fmt='%.0f', label_type='edge', padding=-3)
    #
    #     # Style the chart
    #     plt_lat = plt
    #     plt_lat.title(f"Latency [us] Average @ Thread Count of: {thread_count}")
    #     plt_lat.ylabel("us")
    #     plt_lat.xlabel(my_x_label)
    #     plt_lat.xticks(rotation=0, ha="center")
    #     plt_lat.grid(True, axis='y', linestyle='--', linewidth=0.5)
    #     plt_lat.legend(title="Target", bbox_to_anchor=(1.05, 1), loc='upper left')
    #     plt_lat.tight_layout()
    #     # Show the chart
    #     # plt_lat.show()
    #     # Save the figure
    #     chart_file = os.path.join(current_data_folder, f'chart_lats_threads-{thread_pad}.png')
    #     plt_iops.savefig(chart_file)
    #     images_list.append(chart_file)
    #     print('created:'.ljust(30), chart_file)

    return images_list


def chatgpt_chart(json_file_path):

    current_data_folder = os.path.dirname(json_file_path)

    # Load the input data
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Organize by block size and then by test type + operation
    # Structure: {block_size: {category: {version: iops}}}
    results = defaultdict(lambda: defaultdict(dict))

    ########################
    ## IOPS BY BLOCK SIZE ##
    ########################

    for entry in data:
        block = entry["test_block"]
        mode = entry["test_mode"]  # SEQ or RAN
        operation = entry["test_operation"]  # READ or WRITE
        version = f'version {entry["target_name"].replace("onp-", "")}'
        iops = entry["test_iop"]

        category = f"{mode.title()} {operation.title()} @ {block} Blocks"
        results[block][category][version] = iops

    output = []
    for block_size in sorted(results.keys(), key=lambda b: int(b.replace("K", ""))):
        for category, version_data in results[block_size].items():
            row = {"category": category}
            row.update(version_data)
            output.append(row)

    pretty_json = json.dumps(output, indent=4)
    json_data_out_file = os.path.join(current_data_folder, 'IOPS_Grouped_BlockSize.json')
    with open(json_data_out_file, 'w', encoding="utf-8") as f:
        f.write(pretty_json)


    ########################
    ## MIBS BY BLOCK SIZE ##
    ########################

    for entry in data:
        block = entry["test_block"]
        mode = entry["test_mode"]  # SEQ or RAN
        operation = entry["test_operation"]  # READ or WRITE
        version = f'version {entry["target_name"].replace("onp-", "")}'
        mibs = entry["test_mib"]

        category = f"{mode.title()} {operation.title()} @ {block} Blocks"
        results[block][category][version] = mibs

    output = []
    for block_size in sorted(results.keys(), key=lambda b: int(b.replace("K", ""))):
        for category, version_data in results[block_size].items():
            row = {"category": category}
            row.update(version_data)
            output.append(row)

    pretty_json = json.dumps(output, indent=4)
    json_data_out_file = os.path.join(current_data_folder, 'MIBS_Grouped_BlockSize.json')
    with open(json_data_out_file, 'w', encoding="utf-8") as f:
        f.write(pretty_json)


    ###########################
    ## LATENCY BY BLOCK SIZE ##
    ###########################

    for entry in data:
        block = entry["test_block"]
        mode = entry["test_mode"]  # SEQ or RAN
        operation = entry["test_operation"]  # READ or WRITE
        version = f'version {entry["target_name"].replace("onp-", "")}'
        lats = entry["test_lat"]

        category = f"{mode.title()} {operation.title()} @ {block} Blocks"
        results[block][category][version] = lats

    output = []
    for block_size in sorted(results.keys(), key=lambda b: int(b.replace("K", ""))):
        for category, version_data in results[block_size].items():
            row = {"category": category}
            row.update(version_data)
            output.append(row)

    pretty_json = json.dumps(output, indent=4)
    json_data_out_file = os.path.join(current_data_folder, 'LATS_Grouped_BlockSize.json')
    with open(json_data_out_file, 'w', encoding="utf-8") as f:
        f.write(pretty_json)




def create_reports(results_folder_path):

    convert_csv_data(results_folder_path)
    json_data_path = parse_test_data_files(results_folder_path)

    chatgpt_chart(json_data_path)

    # json_data_path = r'C:\Users\spillman\PythonProjects\elcrapo\v9\result-logs\20250803\20250803_1012\99_PARSED.JSON'
    # chart_files = create_charts_from_json(json_data_path)
# create_reports(r'C:\Users\spillman\PythonProjects\elcrapo\v9\result-logs\20250803\20250803_1012')

