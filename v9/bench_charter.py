import matplotlib.pyplot as plt
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
        if file_name.endswith('.json'):
            target_name = file_name.split('_')[0]
            test_number = file_name.split('_')[1]
            test_mode = file_name.split('_')[2]
            test_operation = file_name.split('_')[3]
            test_size = file_name.split('_')[5]
            test_block = file_name.split('_')[6]
            test_thread = file_name.split('_')[7].replace('T', '')
            test_depth = file_name.split('_')[8].replace('IOD.json', '')

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

            # print(the_data)
            try:
                ilat = the_data[0]["IO lat us [avg]"]
            except IndexError:
                print(the_data[0])
                exit(0)
            try:
                imib = the_data[0]["MiB/s [last]"]
            except IndexError:
                print(the_data[0])
                exit(0)
            try:
                iops = the_data[0]["IOPS [last]"]
            except IndexError:
                print(the_data[0])
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
                print(pretty_k)


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

    tmp_threads_list = get_values_from_keys_with_name(data, "test_thread")
    tmp_threads_list = set(tmp_threads_list)
    sorted_string_numbers = sorted(tmp_threads_list, key=int)

    for thread_count in sorted_string_numbers:
        thread_pad = str(thread_count).zfill(3)
        test_cases_per_threads = get_key_value_from_list(data, "test_thread", thread_count)
        df = pd.DataFrame(test_cases_per_threads)

        ''' Create the three chart types, IOPS, MIBS, LATENCY based on Threads '''

        ''' IOPs Chart --------------------------------------------------------------------------------------------- '''
        # Filter relevant columns IOPs
        df_filtered_iops = df[["chart_test_name", "target_name", "test_iop"]]

        # Pivot so that each test_name is a row, and each target_name is a column
        df_pivot_iops = df_filtered_iops.pivot(index="chart_test_name", columns="target_name", values="test_iop")

        # Plot grouped bar chart
        ax = df_pivot_iops.plot(kind="bar", figsize=(10, 6), colormap="tab20")

        # Add data labels to each bar
        for container in ax.containers:
            ax.bar_label(container, fmt='%.0f', label_type='edge', padding=-3)

        # Style the chart
        plt_iops = plt
        plt_iops.title(f"IOP/s @ Thread Count of: {thread_count}")
        plt_iops.ylabel("IOP/s")
        plt_iops.xlabel(my_x_label)
        plt_iops.xticks(rotation=0, ha="center")
        plt_iops.grid(True, axis='y', linestyle='--', linewidth=0.5)
        plt_iops.legend(title="Target", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt_iops.tight_layout()
        # Show the chart
        # plt_iops.show()
        # Save the figure
        chart_file = os.path.join(current_data_folder, f'chart_iops_threads-{thread_pad}.png')
        plt_iops.savefig(chart_file)
        images_list.append(chart_file)
        print('created:'.ljust(30), chart_file)

        ''' MiBs Chart --------------------------------------------------------------------------------------------- '''
        # Filter relevant columns MiB's
        df_filtered_mib = df[["chart_test_name", "target_name", "test_mib"]]

        # Pivot so that each test_name is a row, and each target_name is a column
        df_pivot_mib = df_filtered_mib.pivot(index="chart_test_name", columns="target_name", values="test_mib")

        # Plot grouped bar chart
        ax = df_pivot_mib.plot(kind="bar", figsize=(10, 6), colormap="tab20")

        # Add data labels to each bar
        for container in ax.containers:
            ax.bar_label(container, fmt='%.0f', label_type='edge', padding=-3)

        # Style the chart
        plt_mib = plt
        plt_mib.title(f"MiB/s @ Thread Count of: {thread_count}")
        plt_mib.ylabel("MiB/s")
        plt_mib.xlabel(my_x_label)
        plt_mib.xticks(rotation=0, ha="center")
        plt_mib.grid(True, axis='y', linestyle='--', linewidth=0.5)
        plt_mib.legend(title="Target", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt_mib.tight_layout()
        # Show the chart
        # plt_mib.show()
        # Save the figure
        chart_file = os.path.join(current_data_folder, f'chart_mibs_threads-{thread_pad}.png')
        plt_iops.savefig(chart_file)
        images_list.append(chart_file)
        print('created:'.ljust(30), chart_file)

        ''' Latency Chart ------------------------------------------------------------------------------------------ '''

        # Filter relevant columns MiB's
        df_filtered_lat = df[["chart_test_name", "target_name", "test_lat"]]

        # Pivot so that each test_name is a row, and each target_name is a column
        df_pivot_lat = df_filtered_lat.pivot(index="chart_test_name", columns="target_name", values="test_lat")

        # Plot grouped bar chart
        ax = df_pivot_lat.plot(kind="bar", figsize=(10, 6), colormap="tab20")

        # Add data labels to each bar
        for container in ax.containers:
            ax.bar_label(container, fmt='%.0f', label_type='edge', padding=-3)

        # Style the chart
        plt_lat = plt
        plt_lat.title(f"Latency [us] Average @ Thread Count of: {thread_count}")
        plt_lat.ylabel("us")
        plt_lat.xlabel(my_x_label)
        plt_lat.xticks(rotation=0, ha="center")
        plt_lat.grid(True, axis='y', linestyle='--', linewidth=0.5)
        plt_lat.legend(title="Target", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt_lat.tight_layout()
        # Show the chart
        # plt_lat.show()
        # Save the figure
        chart_file = os.path.join(current_data_folder, f'chart_lats_threads-{thread_pad}.png')
        plt_iops.savefig(chart_file)
        images_list.append(chart_file)
        print('created:'.ljust(30), chart_file)

    return images_list


def create_reports(results_folder_path):

    convert_csv_data(results_folder_path)
    json_data_path = parse_test_data_files(results_folder_path)
    chart_files = create_charts_from_json(json_data_path)
    print(chart_files)
