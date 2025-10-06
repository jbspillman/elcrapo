
import pandas as pd
import json
import os

script_folder = os.path.dirname(os.path.abspath(__file__))
storage_analyzer = os.path.join(script_folder, 'storage_report_generator.py')


def convert_csv_data(folder_path):
    files_int = 0
    for file_name in os.listdir(folder_path):
        files_int += 1
        file_path_name = os.path.join(folder_path, file_name)
        if file_name.endswith('.liv'):
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
    parsed_results_files = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.JSON'):
            parsed_file_path = os.path.join(folder_path, file_name)
            if parsed_file_path not in parsed_results_files:
                parsed_results_files.append(parsed_file_path)

        elif file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)

            target_name = file_name.split('__')[1].replace('.json', '')
            if 'RAN' in file_name:
                test_mode = "Random"
            else:
                test_mode = "Sequential"

            writes_list = []
            reads_list = []

            with open(file_path, 'r', encoding="utf-8") as file:
                the_data = json.load(file)

            operation = "TEST"
            for item in the_data:
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
                if operation == "READ":
                    operation = "Read"
                elif operation == "WRITE":
                    operation = "Write"

                k = {
                    "iso_date": iso_date,
                    "hosts_count": hosts_count,
                    "folders_count": folders_count,
                    "files_count": files_count,
                    "target_name": target_name,
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
                if operation == "Read":
                    reads_list.append(k)

                if operation == "Write":
                    writes_list.append(k)

            pretty_reads = json.dumps(reads_list, indent=4)
            new_reads_json_file = f'{target_name}__{test_mode}_{operation}.JSON'
            new_reads_path = os.path.join(folder_path, new_reads_json_file)
            with open(new_reads_path, 'w', encoding="utf-8") as f:
                f.write(pretty_reads)

            parsed_results_files.append(new_reads_path)

            pretty_writes = json.dumps(writes_list, indent=4)
            new_writes_json_file = f'{target_name}__{test_mode}_{operation}.JSON'
            new_writes_path = os.path.join(folder_path, new_writes_json_file)
            with open(new_writes_path, 'w', encoding="utf-8") as f:
                f.write(pretty_writes)

            parsed_results_files.append(new_writes_path)

            os.remove(file_path)
    return parsed_results_files


def create_data_elements():
    results_folder_path = os.path.join(script_folder, 'test_results', '20250829', '19.32.47', 'fNAS-1.3')
    paths_supplied = [
        results_folder_path
    ]

    for results_folder_path in paths_supplied:

        convert_csv_data(results_folder_path)
        parsed_ready_list = parse_test_data_files(results_folder_path)

        for json_file in parsed_ready_list:
            tg_name = os.path.basename(json_file).split('__')[0]
            op_name = os.path.basename(json_file).split('__')[1].replace(".JSON", '')

            html_output = os.path.join(results_folder_path, f'{tg_name}_{op_name}.html')

            sa_py = f'python {storage_analyzer} "{json_file}" --output "{html_output}" --verbose'
            os.system(sa_py)

            '''
            
            usage: storage_analyzer.py [-h] [--output OUTPUT] [--csv] [--console-only] [--verbose] json_file
            
            Storage Performance Analyzer - Generate comprehensive reports from JSON benchmark data
            
            positional arguments:
              json_file            Path to JSON file containing benchmark data
            
            options:
              -h, --help           show this help message and exit
              --output, -o OUTPUT  Output HTML file path (default: auto-generated)
              --csv                Also export CSV summary
              --console-only       Only print console summary, no HTML report
              --verbose, -v        Verbose output
            
            Examples:
              python storage_analyzer.py data.json                   # Generate HTML report
              python storage_analyzer.py data.json --csv             # Also export CSV
              python storage_analyzer.py data.json --console-only    # Console output only
              python storage_analyzer.py data.json --output custom_report.html        
            
            
            '''

# manual run of the code for now.
create_data_elements()
