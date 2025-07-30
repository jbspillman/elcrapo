import time
import os
import csv
import json

# ----- general configuration of folder and file paths, command server, and nodes. -----
script_folder = os.path.dirname(os.path.abspath(__file__))

# ----- ensure a log directory exists -----
log_folder = os.path.join(script_folder, "result-logs")
os.makedirs(log_folder, exist_ok=True)

test_folder_a = "20250727_BEASTSERVER_SMB_HDD"
test_folder_b = "20250727_BEASTSERVER_SMB_NVME"

testing_data_sets_a = os.path.join(log_folder, test_folder_a)
testing_data_sets_b = os.path.join(log_folder, test_folder_b)
verbose = False

# ----- enumerate tests that were done -----
def convert_tests_to_json(folder_path_string):
    test_list = []
    for test_file in os.listdir(folder_path_string):
        if test_file.endswith('.csv'):
            csv_file_path = os.path.join(folder_path_string, test_file)
            json_file = str(test_file).replace('.csv', '.json')
            json_file_path_t = os.path.join(folder_path_string, json_file)
            with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                data = list(csv.DictReader(csvfile))
            with open(json_file_path_t, 'w', encoding = 'utf-8') as jfh:
                jfh.write(json.dumps(data, indent = 4))
            if os.path.exists(json_file_path_t):
                test_list.append(json_file_path_t)
                #os.remove(csv_file_path)
        elif test_file.endswith('_results.txt'):
            file_path = os.path.join(folder_path_string, test_file)
            #os.remove(file_path)
        elif test_file.endswith('.json'):
            json_file_path_t = os.path.join(folder_path_string, test_file)
            test_list.append(json_file_path_t)
    return test_list

# ----- the list of test files in json format -----
test_list_a = convert_tests_to_json(testing_data_sets_a)
test_list_b = convert_tests_to_json(testing_data_sets_b)

# ----- match the tests from two directories -----
test_sets = []
for json_file_path_a in test_list_a:
    test_file_name_a = os.path.basename(json_file_path_a)
    for json_file_path_b in test_list_b:
        test_file_name_b = os.path.basename(json_file_path_b)
        if test_file_name_a == test_file_name_b:
            test_tuple = (json_file_path_a, json_file_path_b)
            test_sets.append(test_tuple)
#
# test_results_list = []
# for test_pair in test_sets:
#     fp_a = test_pair[0]
#     fp_b = test_pair[1]
#     with open(fp_a, 'r', encoding='utf-8') as f:
#         data_a = json.load(f)
#     with open(fp_b, 'r', encoding='utf-8') as f:
#         data_b = json.load(f)
#
#     a0_label = data_a[0]["label"]
#     a0_hosts = data_a[0]["hosts"]
#     a0_threads = data_a[0]["threads"]
#     a0_filesize = data_a[0]["file size"]
#     a0_blocksize = data_a[0]["block size"]
#     a0_random = data_a[0]["random"]
#     a0_iodepth = data_a[0]["IO depth"]
#     a0_operation = data_a[0]["operation"]
#
#     b0_label = data_b[0]["label"]
#     b0_hosts = data_b[0]["hosts"]
#     b0_threads = data_b[0]["threads"]
#     b0_filesize = data_b[0]["file size"]
#     b0_blocksize = data_b[0]["block size"]
#     b0_random = data_b[0]["random"]
#     b0_iodepth = data_b[0]["IO depth"]
#     b0_operation = data_b[0]["operation"]
#
#     tests_match = True
#     if a0_hosts != b0_hosts:
#         tests_match = False
#     if a0_threads != b0_threads:
#         tests_match = False
#     if a0_filesize != b0_filesize:
#         tests_match = False
#     if a0_blocksize != b0_blocksize:
#         tests_match = False
#     if a0_random != b0_random:
#         tests_match = False
#     if a0_iodepth != b0_iodepth:
#         tests_match = False
#     if a0_operation != b0_operation:
#         tests_match = False
#     if not tests_match:
#         print(f'files do not match testing configurations: {test_pair}')
#     else:
#
#         test_number =  str(os.path.basename(fp_a)).replace('.json', '')
#         print()
#         print(f'Compare Test Results for:'.ljust(30), test_number)
#
#         a0_operation = data_a[0]["operation"]
#         if a0_operation == "WRITE":
#             a0_operation = "Write"
#         else:
#             a0_operation = "Read"
#
#         a0_threads = data_a[0]["threads"]
#         a0_filesize = data_a[0]["file size"]
#         a0_filesize = round(int(a0_filesize) / 1024 / 1024)
#         if a0_filesize == 1024:
#             a0_filesize = "1GB"
#         else:
#             a0_filesize = f'{a0_filesize}MB'
#
#         a0_blocksize = data_a[0]["block size"]
#         a0_blocksize = round(int(a0_blocksize) / 1024)
#         if a0_blocksize == 1024:
#             a0_blocksize = "1MB"
#         else:
#             a0_blocksize = f'{a0_blocksize}K'
#
#         a0_random = data_a[0]["random"]
#         if a0_random == "1":
#             a0_operation = f'Random {a0_operation}'
#         elif a0_random == "0":
#             a0_operation = f'Sequential {a0_operation}'
#
#         a0_iodepth = data_a[0]["IO depth"]
#         a0_iops = data_a[0]['IOPS [last]']
#         a0_mib_per_sec = data_a[0]['MiB/s [last]']
#         a0_lat_us_avg = data_a[0]['IO lat us [avg]']
#         a0_lat_ms_avg = int(a0_lat_us_avg) / 1000
#
#         #========================================================
#         # a1_threads = data_a[1]["threads"]
#         # a1_filesize = data_a[1]["file size"]
#         # a1_blocksize = data_a[1]["block size"]
#         # a1_iodepth = data_a[1]["IO depth"]
#
#         a1_operation = data_a[1]["operation"]
#         if a1_operation == "WRITE":
#             a1_operation = "Write"
#         else:
#             a1_operation = "Read"
#
#         a1_random = data_a[1]["random"]
#         if a1_random == "1":
#             a1_operation = f'Random {a1_operation}'
#         elif a1_random == "0":
#             a1_operation = f'Sequential {a1_operation}'
#
#         a1_iops = data_a[1]['IOPS [last]']
#         a1_mib_per_sec = data_a[1]['MiB/s [last]']
#         a1_lat_us_avg = data_a[1]['IO lat us [avg]']
#         a1_lat_ms_avg = int(a1_lat_us_avg) / 1000
#
#         #----------------------------------------------------------------------------------------#
#         b0_operation = data_b[0]["operation"]
#         if b0_operation == "WRITE":
#             b0_operation = "Write"
#         else:
#             b0_operation = "Read"
#
#         b0_threads = data_b[0]["threads"]
#         b0_filesize = data_b[0]["file size"]
#         b0_filesize = round(int(b0_filesize) / 1024 / 1024)
#         if b0_filesize == 1024:
#             b0_filesize = "1GB"
#         else:
#             b0_filesize = f'{b0_filesize}MB'
#
#         b0_blocksize = data_b[0]["block size"]
#         b0_blocksize = round(int(b0_blocksize) / 1024)
#         if b0_blocksize == 1024:
#             b0_blocksize = "1MB"
#         else:
#             b0_blocksize = f'{b0_blocksize}K'
#
#         b0_random = data_b[0]["random"]
#         if b0_random == "1":
#             b0_operation = f'Random {b0_operation}'
#         elif b0_random == "0":
#             b0_operation = f'Sequential {b0_operation}'
#
#         b0_iodepth = data_b[0]["IO depth"]
#         b0_iops = data_b[0]['IOPS [last]']
#         b0_mib_per_sec = data_b[0]['MiB/s [last]']
#         b0_lat_us_avg = data_b[0]['IO lat us [avg]']
#         b0_lat_ms_avg = int(b0_lat_us_avg) / 1000
#
#         #========================================================
#         # b1_threads = data_b[1]["threads"]
#         # b1_filesize = data_b[1]["file size"]
#         # b1_blocksize = data_b[1]["block size"]
#         # b1_iodepth = data_b[1]["IO depth"]
#
#         b1_operation = data_b[1]["operation"]
#         if b1_operation == "WRITE":
#             b1_operation = "Write"
#         else:
#             b1_operation = "Read"
#
#         b1_random = data_b[1]["random"]
#         if b1_random == "1":
#             b1_operation = f'Random {b1_operation}'
#         elif b1_random == "0":
#             b1_operation = f'Sequential {b1_operation}'
#
#         b1_iops = data_b[1]['IOPS [last]']
#         b1_mib_per_sec = data_b[1]['MiB/s [last]']
#         b1_lat_us_avg = data_b[1]['IO lat us [avg]']
#         b1_lat_ms_avg = int(b1_lat_us_avg) / 1000
#
#
#         if verbose:
#             print('')
#             print('Device Label A:'.ljust(30), a0_label)
#             print(' Test Options:')
#             print('  Block Size:'.ljust(30), f'{a0_blocksize}')
#             print('  File Size:'.ljust(30), f'{a0_filesize}')
#             print('  Threads:'.ljust(30), a0_threads)
#             print('  IO Depth:'.ljust(30), a0_iodepth)
#
#             print(' > Operation:'.ljust(40), a0_operation)
#             print('     IOP/s Result:'.ljust(40), a0_iops)
#             print('     MiB/s Result:'.ljust(40), a0_mib_per_sec)
#             print('     Latency Avg Result(us|ms):'.ljust(40), f'{a0_lat_us_avg} | {a0_lat_ms_avg}')
#
#             print(' > Operation:'.ljust(40), a1_operation)
#             print('     IOP/s Result:'.ljust(40), a1_iops)
#             print('     MiB/s Result:'.ljust(40), a1_mib_per_sec)
#             print('     Latency Avg Result(us|ms):'.ljust(40), f'{a1_lat_us_avg} | {a1_lat_ms_avg}')
#
#
#             print('')
#             print('Device Label B:'.ljust(30), b0_label)
#             print(' Test Options:')
#             print('  Block Size:'.ljust(30), f'{b0_blocksize}')
#             print('  File Size:'.ljust(30), f'{b0_filesize}')
#             print('  Threads:'.ljust(30), b0_threads)
#             print('  IO Depth:'.ljust(30), b0_iodepth)
#
#             print(' > Operation:'.ljust(40), b0_operation)
#             print('     IOP/s Result:'.ljust(40), b0_iops)
#             print('     MiB/s Result:'.ljust(40), b0_mib_per_sec)
#             print('     Latency Avg Result(us|ms):'.ljust(40), f'{b0_lat_us_avg} | {b0_lat_ms_avg}')
#
#             print(' > Operation:'.ljust(40), b1_operation)
#             print('     IOP/s Result:'.ljust(40), b1_iops)
#             print('     MiB/s Result:'.ljust(40), b1_mib_per_sec)
#             print('     Latency Avg Result(us|ms):'.ljust(40), f'{b1_lat_us_avg} | {b1_lat_ms_avg}')
#
#         k = {
#             "test_number": test_number,
#             "file_size": a0_filesize,
#             "block_size": a0_blocksize,
#             "threads": a0_threads,
#             "io_depth": a0_iodepth,
#             a0_operation: [
#                 {
#                     "device": a0_label,
#                     "iops": a0_iops,
#                     "mibs": a0_mib_per_sec,
#                     "lat": a0_lat_us_avg
#                 },
#                 {
#                     "device": b0_label,
#                     "iops": b0_iops,
#                     "mibs": b0_mib_per_sec,
#                     "lat": b0_lat_us_avg
#                 }
#             ],
#             a1_operation: [
#                 {
#                     "device": a0_label,
#                     "iops": a1_iops,
#                     "mibs": a1_mib_per_sec,
#                     "lat": a1_lat_us_avg
#                 },
#                 {
#                     "device": b0_label,
#                     "iops": b1_iops,
#                     "mibs": b1_mib_per_sec,
#                     "lat": b1_lat_us_avg
#                 }
#             ]
#         }
#         test_results_list.append(k)
#
#
# json_output = json.dumps(test_results_list, indent=4)
# final_output_json = os.path.join(log_folder, f'{a0_label}__{b0_label}.json')
# with open(final_output_json, 'w', encoding = 'utf-8') as json_file_handler:
#     json_file_handler.write(json_output)
# print(final_output_json)
