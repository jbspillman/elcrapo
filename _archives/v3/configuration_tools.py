from connection_tools import execute_ssh_commands, external_creds
from download_elbencho import get_releases
from install_elbencho import install_remote_client
from datetime import datetime
import json


def define_benchmark_env():
    host_servers = [
        "centos01.beastmode.local.net",
        "centos02.beastmode.local.net",
        "centos03.beastmode.local.net",
        "centos04.beastmode.local.net",
        "centos05.beastmode.local.net",
        "centos06.beastmode.local.net",
    ]

    nfs_server = "beastserver.beastmode.local.net"
    cmd_server = "mediaserver.beastmode.local.net"
    elbencho_exe = '/usr/bin/elbencho'
    remote_file_systems = [
        {
            "nfs_server": nfs_server,
            "mount_path": "/mnt/Drives/02000c/elbencho",
            "local_path": "/bench/nfs3_data",
        },
        {
            "nfs_server": nfs_server,
            "mount_path": "/mnt/Drives/02000c/elbencho",
            "local_path": "/bench/nfs4_data",
        }
    ]

    mount_nfs_paths(host_servers, remote_file_systems)

    installers = get_releases()
    is_ready = start_benchmark_services(host_servers, installers)

    return host_servers, remote_file_systems, cmd_server, elbencho_exe, is_ready


def mount_nfs_paths(nfs_clients, file_systems):
    nfs_mounts_ready = True
    for client in nfs_clients:
        # print('CHECKING: ##################################################################')
        # print('client:', client)

        for z in file_systems:
            nfs_server = z["nfs_server"]
            nfs_mount = z["mount_path"]
            nfs_path = f"{nfs_server}:{nfs_mount}"
            local_path = z["local_path"]
            # print(f'check for :       {local_path}')
            mnt_d = execute_ssh_commands(client, f"df -h | grep {local_path}", False)
            if len(mnt_d) > 0:
                skip = True
                # print(f'is mounted.....   {local_path}')
                # for line in mnt_d.split("\n"):
                #     print(line)
            else:
                print(f'{client} not mounted.....  {local_path}')
                current_timestamp = datetime.now().timestamp()
                print(f"current_timestamp: {current_timestamp}")
                print()
                if 'nfs3' in local_path:
                    nfs_mount_options = "mount -vvv -t nfs -o vers=3,rsize=131072,wsize=131072,hard,intr,timeo=600"
                else:
                    nfs_mount_options = "mount -vvv -t nfs -o vers=4,rsize=131072,wsize=131072,hard,intr,timeo=600"
                full_cmd = f'{nfs_mount_options} {nfs_path} {local_path} '
                print(full_cmd)
                m_results = execute_ssh_commands(client, full_cmd , False)
                print(m_results)
    return nfs_mounts_ready


def start_benchmark_services(nodes_list, install_files):
    auth_str = external_creds()
    is_connected = True

    nodes_list2 = sorted(set(nodes_list))
    how_many_nodes = len(nodes_list2)
    is_started = 0
    for node in nodes_list2:
        node = node.rstrip()
        if node:
            # print(f'check services on - [{node}]')
            check_exe = execute_ssh_commands(node, 'which elbencho', False)
            if ' no elbencho in ' in check_exe:
                print()
                print(f'Install Check Failed for : {node} : NOT INSTALLED.')
                install_remote_client(node, install_files)
            else:
                if len(check_exe) > 0:
                    remote_path = str(check_exe).split('\n')[0]
                    start_listener_service = f'{remote_path} --service'
                    start_svc = execute_ssh_commands(node, start_listener_service, False)
                    if 'Daemonizing' in start_svc:
                        is_started += 1
                        print(f'{node} service started into background.')
                    elif 'Unable to bind to desired port' in start_svc:
                        is_started += 1
                        # print(f'{node} service already running in background.')
                    else:
                        print(f'{node} : {start_svc}')
                        exit(1)
            check_exe = None

    # print(f'how_many_nodes: {how_many_nodes}   is_started: {is_started} ')
    if how_many_nodes == is_started:
        return is_connected
    else:
        exit(999)  #     setup_ssh_keys(nodes_list)


def setup_ssh_keys(tgt_svrs):
    for tgt in tgt_svrs:
        cppy_key = f"sshpass -p {auth_str} ssh-copy-id -o ConnectTimeout=10 -o StrictHostKeyChecking=no {tgt};"
        std_user = execute_ssh_commands(node, f'{cppy_key}', False)
        for li in std_user:
            print(f'user key install: {li}')

        god_user = execute_ssh_commands(node, f'{cppy_key}', True)
        for li in god_user:
            print(f'root key install:S {li}')

