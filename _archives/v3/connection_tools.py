import paramiko
from paramiko.client import AutoAddPolicy
import json


def external_creds():
    generic_creds = r"generic.json"
    s_usr = None
    s_psw = None
    with open(generic_creds, 'r') as file:
        s_psw = file.read()
    return s_psw


def parse_ssh_returns(stdout_t, stderr_t):
    decoded_std_out = stdout_t.read().decode("utf8")
    decoded_std_err = stderr_t.read().decode("utf8")
    content_as_str = ""
    if len(decoded_std_err) > 0:
        for err_line in decoded_std_err.split('\n'):
            content_as_str += f"{err_line}\n"
    if len(decoded_std_out) > 0:
        for out_line in decoded_std_out.split('\n'):
            content_as_str += f"{out_line}\n"
    return content_as_str


def execute_ssh_commands(target_server, remote_command, account_default):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AutoAddPolicy())

    authorize = external_creds()
    if account_default:
        account = 'spillman'
    else:
        account = 'root'

    client.connect(target_server, username=account, password=authorize)
    stdin, stdout, stderr = client.exec_command(remote_command)
    output_list = parse_ssh_returns(stdout, stderr)
    stdin.close()
    stdout.close()
    stderr.close()
    client.close()
    return output_list


