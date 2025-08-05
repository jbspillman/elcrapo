from configuration_tools import define_benchmark_env
from configure_jobs import basic_jobs_setup


def main():


    host_servers, remote_file_systems, cmd_server, elbencho_exe, is_ready = define_benchmark_env()
    print()
    print('host_servers:'.ljust(30), len(host_servers))
    print('remote_file_systems:'.ljust(30),len(remote_file_systems))
    print('cmd_server:'.ljust(30), cmd_server)
    print('elbencho_exe:'.ljust(30), elbencho_exe)
    print('is_ready:'.ljust(30), is_ready)
    print()
    if is_ready:
        basic_jobs_setup(host_servers, remote_file_systems, cmd_server, elbencho_exe)




if __name__ == "__main__":
    main()