

def configuration_details():
    """ Default Listings of Things. """
    host_servers = [
        "mediaserver.beastmode.local.net",
        "centos01.beastmode.local.net",
        "centos02.beastmode.local.net",
        "centos03.beastmode.local.net",
        "centos04.beastmode.local.net"
    ]

    remote_file_systems = [
        {
            "server": "beastserver.beastmode.local.net",
            "path": "/mnt/Drives/02000c/elbencho",
            "path_local": "/bench/nfs3_032k",
            "options": 'nfs rw,bg,hard,nointr,rsize=32768,wsize=32768,tcp,nfsvers=3,timeo=600,actimeo=0'
        },
        {
            "server": "beastserver.beastmode.local.net",
            "path": "/mnt/Drives/02000c/elbencho",
            "path_local": "/bench/nfs3_064k",
            "options": 'nfs rw,bg,hard,nointr,rsize=65536,wsize=65536,tcp,nfsvers=3,timeo=600,actimeo=0'
        },
        {
            "server": "beastserver.beastmode.local.net",
            "path": "/mnt/Drives/02000c/elbencho",
            "path_local": "/bench/nfs3_128k",
            "options": 'nfs rw,bg,hard,nointr,rsize=131072,wsize=131072,tcp,nfsvers=3,timeo=600,actimeo=0'
        },
        {
            "server": "beastserver.beastmode.local.net",
            "path": "/mnt/Drives/02000c/elbencho",
            "path_local": "/bench/nfs4_032k",
            "options": 'nfs rw,bg,hard,nointr,rsize=32768,wsize=32768,tcp,nfsvers=4,timeo=600,actimeo=0'
        },
        {
            "server": "beastserver.beastmode.local.net",
            "path": "/mnt/Drives/02000c/elbencho",
            "path_local": "/bench/nfs4_064k",
            "options": 'nfs rw,bg,hard,nointr,rsize=65536,wsize=65536,tcp,nfsvers=4,timeo=600,actimeo=0'
        },
        {
            "server": "beastserver.beastmode.local.net",
            "path": "/mnt/Drives/02000c/elbencho",
            "path_local": "/bench/nfs4_128k",
            "options": 'nfs rw,bg,hard,nointr,rsize=131072,wsize=131072,tcp,nfsvers=4,timeo=600,actimeo=0'
        }
    ]

    elbencho_local = r'C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe'
    return host_servers, remote_file_systems, elbencho_local
