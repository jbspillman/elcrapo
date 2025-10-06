from get_installers import get_releases
from install_elbencho import install_local_client, install_remote_client
from elbencho_jobs import create_job_files
from execute_tests import execute_setup
from execute_tests import launch_testing_environment


host_servers = [
    "mediaserver.beastmode.local.net",
    "centos01.beastmode.local.net",
    "centos02.beastmode.local.net",
    "centos03.beastmode.local.net",
    "centos04.beastmode.local.net"
]


def main():
    """
     Do the work to install and use elbencho ...
    """

    remote_file_systems = [
        {
            "server": "beastserver.beastmode.local.net",
            "path": "/mnt/Drives/02000a",
            "path_local": "/bench/nfs3_032k",
            "options": 'nfs rw,bg,hard,nointr,rsize=32768,wsize=32768,tcp,nfsvers=3,timeo=600,actimeo=0'
        },
        {
            "server": "beastserver.beastmode.local.net",
            "path": "/mnt/Drives/02000a",
            "path_local": "/bench/nfs3_064k",
            "options": 'nfs rw,bg,hard,nointr,rsize=65536,wsize=65536,tcp,nfsvers=3,timeo=600,actimeo=0'
        },
        {
            "server": "beastserver.beastmode.local.net",
            "path": "/mnt/Drives/02000a",
            "path_local": "/bench/nfs3_128k",
            "options": 'nfs rw,bg,hard,nointr,rsize=131072,wsize=131072,tcp,nfsvers=3,timeo=600,actimeo=0'
        },
        {
            "server": "beastserver.beastmode.local.net",
            "path": "/mnt/Drives/02000a",
            "path_local": "/bench/nfs4_032k",
            "options": 'nfs rw,bg,hard,nointr,rsize=32768,wsize=32768,tcp,nfsvers=4,timeo=600,actimeo=0'
        },
        {
            "server": "beastserver.beastmode.local.net",
            "path": "/mnt/Drives/02000a",
            "path_local": "/bench/nfs4_064k",
            "options": 'nfs rw,bg,hard,nointr,rsize=65536,wsize=65536,tcp,nfsvers=4,timeo=600,actimeo=0'
        },
        {
            "server": "beastserver.beastmode.local.net",
            "path": "/mnt/Drives/02000a",
            "path_local": "/bench/nfs4_128k",
            "options": 'nfs rw,bg,hard,nointr,rsize=131072,wsize=131072,tcp,nfsvers=4,timeo=600,actimeo=0'
        }
    ]

    ''' Download the latest clients for elbencho ... '''
    installers_list = get_releases()
    
    ''' Install the client locally. '''
    elbencho_local = install_local_client(installers_list)
    print('elbencho_local:'.ljust(30), elbencho_local)

    ''' Install the client remotes. '''
    elbencho_remotes = install_remote_client(installers_list, host_servers)
    print('remote_control_servers:'.ljust(30), len(elbencho_remotes))

    ''' Setup the basic folder and file testing jobs. '''
    performance_test_jobs = create_job_files()
    print('performance_test_jobs:'.ljust(30), len(performance_test_jobs))

    ''' Execute setup on target hosts servers. '''
    setup_valid = execute_setup(elbencho_remotes, remote_file_systems, performance_test_jobs)
    setup_valid = True
    if setup_valid:
        ''' Start the distributed load tests. '''
        launch_testing_environment(elbencho_local, elbencho_remotes, performance_test_jobs, remote_file_systems)


if __name__ == "__main__":
    main()


