import zipfile
import shutil
import os
import paramiko
from paramiko.client import AutoAddPolicy
"""
Some of this is hard coded to keep from repeating things..

"""

def parse_ssh_returns(stdout_t, stderr_t):

    decoded_std_out = stdout_t.read().decode("utf8")
    decoded_std_err = stderr_t.read().decode("utf8")
    content_as_list = []
    if len(decoded_std_err) > 0:
        for err_line in decoded_std_err.split('\n'):
            # print(err_line)
            content_as_list.append(err_line)
    if len(decoded_std_out) > 0:
        for out_line in decoded_std_out.split('\n'):
            # print(out_line)
            content_as_list.append(out_line)
    return content_as_list


def execute_ssh_commands(target_server, remote_command):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AutoAddPolicy())
    output_list = []
    client.connect(target_server, username='XXXXXXX', password='XXXXXXX')
    stdin, stdout, stderr = client.exec_command(remote_command)
    output_list = parse_ssh_returns(stdout, stderr)
    stdin.close()
    stdout.close()
    stderr.close()
    client.close()
    return output_list


def install_local_client(install_files_list):
    script_folder = os.path.dirname(os.path.abspath(__file__))
    def unzip_file_path(zip_file_path, extract_to_directory):
        os.makedirs(extract_to_directory, exist_ok=True)
        try:
            # Open the zip file in read mode
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                # Extract all contents to the specified directory
                zip_ref.extractall(extract_to_directory)
            print(f"Successfully extracted '{zip_file_path}' to '{extract_to_directory}'.")
        except zipfile.BadZipFile:
            print(f"Error: '{zip_file_path}' is not a valid zip file.")
        except FileNotFoundError:
            print(f"Error: Zip file '{zip_file_path}' not found.")
        except Exception as zip_extract_error:
            print(f"An unexpected error occurred: {zip_extract_error}")

    if os.name == 'nt':
        elbencho_client = os.path.join(script_folder, 'elbencho_client')
        windows_exe = os.path.join(elbencho_client, 'elbencho.exe')

        if not os.path.exists(windows_exe):
            if os.path.exists(elbencho_client):
                try:
                    shutil.rmtree(elbencho_client)
                    print(f"Directory '{elbencho_client}' and its contents deleted successfully.")
                except OSError as e:
                    print(f"Error: {elbencho_client} : {e.strerror}")

            print('WINDOWS CLIENT')
            for install_file in install_files_list:
                if '.zip' in install_file:
                    unzip_file_path(install_file, elbencho_client)
                    print(f'Installed: {windows_exe}')
        return windows_exe
    else:
        print(os.name)
        return None


def upload_client_file(target_server, local_file_path, remote_file_path):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Be cautious with AutoAddPolicy in production

    # Connect to the SFTP server
    ssh_client.connect(hostname=target_server, port=22, username='XXXXXXX', password='XXXXXXX')
    # Open an SFTP client
    sftp_client = ssh_client.open_sftp()
    # Upload the file
    sftp_client.put(local_file_path, remote_file_path)
    print(f"File '{local_file_path}' uploaded successfully to '{remote_file_path}' on SFTP server.")


def install_remote_client(install_files_list, host_servers):
    remote_clients = []
    for server in host_servers:
        # print(' ')
        # print(f'checking server: {server}')
        text_data = execute_ssh_commands(server, 'which elbencho')
        is_found = False
        installed_at = ""
        for sentence in text_data:
            sentence = sentence.rstrip()
            if sentence:
                if 'which' in str(sentence).lower():
                    is_found = False
                    break
                elif str(sentence).startswith('/'):
                    is_found = True
                    installed_at = sentence
                    break
        if is_found:
            text_data = execute_ssh_commands(server, 'elbencho --version')
            for txt in text_data:
                if 'Version: ' in txt:
                    # print(f'{installed_at} {txt}')
                    break
            k = {
                'host': server,
                'path': installed_at
            }
            remote_clients.append(k)

        else:
            rpm_data = execute_ssh_commands(server, 'rpm -qa 2>&1')
            if len(rpm_data) > 5:
                script_folder = os.path.dirname(os.path.abspath(__file__))
                install_src = os.path.join(script_folder, '00_installers', 'elbencho-static.x86_64.rpm')
                install_tgt = '/home/spillman/elbencho-static.x86_64.rpm'
                upload_client_file(server, install_src, install_tgt)
                print(f'Please install with command: ssh -l spillman@{server} "sudo -S rpm -ivh {install_tgt}" ')

            else:
                deb_data = execute_ssh_commands(server, 'dpkg -l 2>&1')
                for dline in deb_data:
                    print(dline)

    return remote_clients
