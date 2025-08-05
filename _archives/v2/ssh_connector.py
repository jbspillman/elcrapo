import paramiko
from paramiko.client import AutoAddPolicy


def parse_ssh_returns(stdout_t, stderr_t):
    decoded_std_out = stdout_t.read().decode("utf8")
    decoded_std_err = stderr_t.read().decode("utf8")
    content_as_list = []
    if len(decoded_std_err) > 0:
        for err_line in decoded_std_err.split('\n'):
            content_as_list.append(err_line)
    if len(decoded_std_out) > 0:
        for out_line in decoded_std_out.split('\n'):
            content_as_list.append(out_line)
    return content_as_list


def execute_ssh_commands(target_server, remote_command):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AutoAddPolicy())
    output_list = []
    client.connect(target_server, username='XXXXXXXXX', password='XXXXXXXXX')
    stdin, stdout, stderr = client.exec_command(remote_command)
    output_list = parse_ssh_returns(stdout, stderr)
    stdin.close()
    stdout.close()
    stderr.close()
    client.close()
    return output_list

