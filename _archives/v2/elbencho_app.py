from ssh_connector import execute_ssh_commands
import os


def launch_storage_tests(elbencho_client, servers_list, file_systems):
    standard_tests = [
        {
            "TestName": "Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1",
            "TestLabel": "SWLF__T4.[D2xF8].B1M.S1G.D1.S1",
            "TestOptions": " --write --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --sync --timelimit 60"
        },
        {
            "TestName": "Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0",
            "TestLabel": "SRLF__T4.[D2xF8].B1M.S1G.D1.S0",
            "TestOptions": "--read --trunctosize --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --timelimit 60"
        },
        {
            "TestName": "Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0",
            "TestLabel": "RWSB__T8.[D4xF16].B4K.S512M.D1.S0",
            "TestOptions": "--write --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 60"
        },
        {
            "TestName": "Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0",
            "TestLabel": "RRSB__T8.[D4xF16].B4K.S512M.D1.S0",
            "TestOptions": "--read --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 60"
        },
        {
            "TestName": "Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0",
            "TestLabel": "MR70W30__T6.[D3xF12].B64K.S256M.D1.S0",
            "TestOptions": "--write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=70 --direct --timelimit 60"
        },
        {
            "TestName": "Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0",
            "TestLabel": "MR30W70__T6.[D3xF12].B64K.S256M.D1.S0",
            "TestOptions": "--write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=30 --direct --timelimit 60"
        }
    ]

    # lists_of_folders_to_create = []
    # for server_name in servers_list:
    #     server_short = server_name.split('.')[0]
    #     for f_system in file_systems:
    #         node_local_path = f_system["path_local"]
    #         for standard_test in standard_tests:
    #             test_label = standard_test["TestLabel"]
    #             long_path = node_local_path + '/' + server_short + '/' + test_label
    #             if long_path not in lists_of_folders_to_create:
    #                 lists_of_folders_to_create.append(long_path)
    #                 # print('long_path:'.ljust(30), long_path)
    #
    # host_owner = servers_list[0]
    # cmds = ''
    # for folder in lists_of_folders_to_create:
    #     cmds += f'mkdir -p {folder} ;\n'
    # output = execute_ssh_commands(host_owner, cmds)
    # if len(output) > 0:
    #     print(output)


    the_folder_path = os.path.dirname(os.path.abspath(__file__))
    results_folder = os.path.join(the_folder_path, 'elbencho_results')
    os.makedirs(results_folder, exist_ok=True)

    elbencho_x1 = str(servers_list[0])
    elbencho_x2 = f'{elbencho_x1},{str(servers_list[1])}'
    elbencho_x3 = f'{elbencho_x2},{str(servers_list[2])}'
    elbencho_x4 = f'{elbencho_x3},{str(servers_list[3])}'
    elbencho_x5 = f'{elbencho_x4},{str(servers_list[4])}'

    elbencho_nodes_lists = [
        elbencho_x1,
        elbencho_x2,
        elbencho_x3,
        elbencho_x4,
        elbencho_x5,
    ]

    all_commands = '@ECHO OFF\n'
    all_commands += 'ECHO.\n'
    all_commands += 'ECHO.\n'
    x = 0
    for elbencho_nodes in elbencho_nodes_lists:
        x += 1
        for fs in file_systems:
            short_path_local = fs["path_local"]
            for std in standard_tests:
                test_name = str(std["TestName"]) + f'_NODES{x}'
                test_label = str(std["TestLabel"]) + f'_NODES{x}'
                test_options = std["TestOptions"]

                host_targets = f'--hosts "{elbencho_nodes}"'
                add_options = '--mkdirs --deldirs --delfiles --cpu --lat --lathisto'
                if 'Read' in test_name:
                    add_options = '--mkdirs --nodelerr --cpu --lat --lathisto'

                label_option = f'--label {test_label}'

                csv_live_path = os.path.join(results_folder, f'{test_name}_LIVE.csv')
                csv_file_path = os.path.join(results_folder, f'{test_name}.csv')
                json_file_path = os.path.join(results_folder, f'{test_name}.json')
                results_file_path = os.path.join(results_folder, f'{test_name}.txt')
                ops_log_path = f'{short_path_local}/io_logs/{test_name}_iops.json'
                ops_options = f'--opslog "{ops_log_path}"'

                csv_options = f'--live1 --livecsv "{csv_live_path}" --csvfile "{csv_file_path}" '
                json_options = f'--jsonfile "{json_file_path}" '
                txt_options = f'--resfile "{results_file_path}"'

                testing_folder = f'{short_path_local}/io_data'

                form_command = f'"{elbencho_client}" {host_targets} {csv_options} {json_options} {txt_options} '
                form_command += f'{test_options} {add_options} {label_option} {testing_folder}'   #  --dryrun

                all_commands += f'ECHO "{test_name} : {testing_folder}" \n'
                all_commands += f'{form_command}\n'
                all_commands += f'timeout /t 3 /nobreak \n'
                all_commands += 'ECHO.\n'
                all_commands += 'ECHO.\n'
                all_commands += '\n'
                all_commands += '\n'

    with open("test.cmd", "w") as f:
        f.write(all_commands)



def start_services(remote_nodes):
    how_many_nodes = len(remote_nodes)
    nodes_running = 0
    for k in remote_nodes:
        remote_host = k
        remote_path = '/usr/bin/elbencho'

        start_listener_service = f'{remote_path} --service'
        start_text = execute_ssh_commands(remote_host, start_listener_service)
        for text in start_text:
            text = text.rstrip()
            if text:
                if 'Daemonizing' in text:
                    nodes_running += 1
                    print(f'{remote_host} service started into background.')
                elif 'Unable to bind to desired port' in text:
                    nodes_running += 1
                    # print(f'{remote_host} already running > {text}')
                else:
                    print(f'{remote_host} Error > {text}')
                    break
    if how_many_nodes != nodes_running:
        print('Error: Service not found on all nodes!')
        return False

    return True