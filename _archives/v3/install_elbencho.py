from connection_tools import execute_ssh_commands, external_creds
import paramiko
import os


def upload_client_file(target_server, local_file_path, remote_file_path, account_default):

    authorize = external_creds()
    if account_default:
        account = 'spillman'
    else:
        account = 'root'

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Be cautious with AutoAddPolicy in production

    # Connect to the SFTP server
    ssh_client.connect(hostname=target_server, port=22, username=account, password=authorize)
    # Open an SFTP client
    sftp_client = ssh_client.open_sftp()
    # Upload the file
    sftp_client.put(local_file_path, remote_file_path)
    print(f"File '{local_file_path}' uploaded successfully to '{remote_file_path}' on SFTP server.")

    if '.rpm' in local_file_path:
        install_rpm = execute_ssh_commands(target_server, f'sudo -S rpm -ivh {remote_file_path} 2>&1', False)
        print(install_rpm)


def install_remote_client(server_name, install_files_list):
    rpm_data = execute_ssh_commands(server_name, 'rpm -qa 2>&1', False)
    if len(rpm_data) > 5:
        for f in install_files_list:
            if f.endswith('.rpm'):
                install_src = f
                tgt_file = os.path.basename(install_src)
                install_tgt = '/home/spillman/' + tgt_file
                upload_client_file(server_name, install_src, install_tgt, False)
                break
    else:
        deb_data = execute_ssh_commands(server_name, 'dpkg -l 2>&1', False)
        if len(deb_data) > 5:
            print('Is Deb Based!')
        else:
            print('unknown!')
            return False
    return True
