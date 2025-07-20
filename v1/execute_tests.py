from install_elbencho import execute_ssh_commands
import os


def execute_setup(remote_exe, remote_paths, jobs_list):

    def start_services():
        how_many_nodes = len(remote_exe)
        nodes_running = 0
        for k in remote_exe:
            remote_host = k["host"]
            remote_path = k["path"]

            start_listener_service = f'{remote_path} --service'
            start_text = execute_ssh_commands(remote_host, start_listener_service)
            for text in start_text:
                text = text.rstrip()
                if text:
                    if 'Daemonizing' in text:
                        print(f'{remote_host} service started into background.')
                    elif 'Unable to bind to desired port' in text:
                        nodes_running += 1
                    else:
                        print(f'{remote_host} : {text}')
                        break
        if how_many_nodes != nodes_running:
            print('Error: Service not found on all nodes!')
            exit(1)

    def mount_commands():
        local_mounts = []
        for item in remote_paths:
            local_path_string = f'{item["path_local"]}'
            local_mounts.append(local_path_string)

        mnt_errors = False
        how_many_paths = len(local_mounts)
        for k in remote_exe:
            remote_host = k["host"]
            how_many_found = 0
            list_mounts = execute_ssh_commands(remote_host, "df -h")
            for lcl_mount in local_mounts:
                for line in list_mounts:
                    if lcl_mount in line:
                        how_many_found += 1
            if how_many_paths != how_many_found:
                print(f'File System Path is missing: {remote_host}  Found {how_many_found} of {how_many_paths}')
                mnt_errors = True
            else:
                skip = True
                # print(f'File System Path all found:  {remote_host}  Found {how_many_found} of {how_many_paths}')

        if mnt_errors:
            mkdirs_text = "{\n"
            fstab_text = ""
            for item in remote_paths:
                # form mount commands for remote system.
                mount_string = f'{item["server"]}:{item["path"]}'
                local_path_string = f'{item["path_local"]}'
                mount_options = f'{item["options"]}'
                mkdirs_text += (f' sudo mkdir -p {local_path_string};\n'
                                f' sudo chmod -R 777 {local_path_string};\n'
                                f' sudo chown -R UNIXUSER:UNIXGROUP {local_path_string};\n')

                full_text = f'{mount_string}    {local_path_string}      {mount_options}'
                fstab_text += f'{full_text}\n'

            mkdirs_text += ' ls -la /bench/;\n}'
            mkdirs_text.rstrip('\n')

            print('create these:')
            print(mkdirs_text)
            print('mount these: sudo vim /etc/fstab ')
            print(fstab_text)

    def create_per_job_title_folders():
        make_folders = []
        for rp in remote_paths:
            host_local_path = rp["path_local"]
            for jb in jobs_list:
                job_title = str(os.path.basename(jb)).replace('.conf', '')
                new_local_path = host_local_path + "/" + f'{job_title}'
                if new_local_path not in make_folders:
                    make_folders.append(new_local_path)

        make_string = ""
        for dir_path in make_folders:
            mkdir_s = f'mkdir -p {dir_path}; '
            make_string += mkdir_s

        for k in remote_exe:
            remote_host = k["host"]
            mk_result = execute_ssh_commands(remote_host, make_string)
            if mk_result:
                print(remote_host, mk_result)
            break  # its already mounted, so you only need to do this once.


    ''' host configurations. '''
    mount_commands()  # create the mount point commands
    create_per_job_title_folders()  # create sub folders.
    start_services()  # start the processes.

    return True


def launch_testing_environment(elbencho_local, elbencho_remotes, test_jobs_list, remote_file_systems):

    the_commands = "@ECHO OFF\n"
    the_commands += "CLS\n"


    the_folder_path = os.path.dirname(os.path.abspath(__file__))
    results_folder = os.path.join(the_folder_path, 'results')
    os.makedirs(results_folder, exist_ok=True)

    elbencho_hosts = ""
    for x in elbencho_remotes:
        elbencho_hosts += f"{x['host']},"
    elbencho_hosts = elbencho_hosts.rstrip(',')

    local_mount_paths = []
    for rem_share in remote_file_systems:
        if rem_share["path_local"] not in local_mount_paths:
            local_mount_paths.append(rem_share["path_local"])
    local_mount_paths = set(local_mount_paths)

    config_00 = f'"{elbencho_local}" --hosts "{elbencho_hosts}" '
    for config_file in sorted(test_jobs_list, reverse=True):
        config_01 = f'--configfile "{config_file}" '

        # print('')
        # print('config_file:'.ljust(30), config_file)
        job_name = str(os.path.basename(config_file)).replace('.conf', '')

        for local_path in local_mount_paths:
            local_path_string = str(str(local_path).split('/')[-1]).upper()
            test_name = f'{job_name}__{local_path_string}'

            # print('test_name:'.ljust(30), test_name)

            live_csv_path = os.path.join(results_folder, f'{test_name}-live.csv')
            out_csv_path = os.path.join(results_folder, f'{test_name}.csv')
            results_file_path = os.path.join(results_folder,f'{test_name}.txt')
            json_file_path = os.path.join(results_folder,f'{test_name}.json')
            local_folder = f'{local_path}/{job_name}'

            config_02= f'--live1 --livecsv "{live_csv_path}" '
            config_03 = f'--csvfile "{out_csv_path}" '
            config_04 = f'--jsonfile "{json_file_path}" '
            config_05 = f'--resfile "{results_file_path}" '
            config_06 = f'--cpu --lat --direct '
            the_commands += "\n"
            the_commands += "ECHO.\n"
            the_commands += 'ECHO "' + test_name + f'" running at "{local_folder}"\n'

            # print(local_folder)

            cmd = config_00 + config_01 + config_02 + config_03 + config_04 + config_05 + config_06 + local_folder
            #print(cmd)

            the_commands += f"{cmd}\n"
            the_commands += f"timeout /t 5 /nobreak\n"
            the_commands += f"\n"

    with open("test.cmd", "w") as f:
        f.write(the_commands)
    print("test.cmd")





