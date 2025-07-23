import subprocess
import os
import datetime


def basic_jobs_setup(host_servers, remote_file_systems, cmd_server, elbencho_exe):
    script_folder = os.path.dirname(os.path.abspath(__file__))

    local_fs_paths = []
    for fs in remote_file_systems:
        local_path = fs["local_path"]
        if local_path not in local_fs_paths:
            local_fs_paths.append(local_path)

    nfs3_paths = ""
    nfs4_paths = ""
    nodes_string = ""
    for node in host_servers:
        nshort = node.split('.')[0]
        for fp in local_fs_paths:
            fpp = f'{fp}/{nshort}'
            if 'nfs3' in fpp:
                nfs3_paths += f'{fpp} '
            elif 'nfs4' in fpp:
                nfs4_paths += f'{fpp} '
        nodes_string += f'{node},'
    nodes_string = nodes_string.rstrip(',')
    nfs3_paths = nfs3_paths.rstrip(' ')
    nfs4_paths = nfs4_paths.rstrip(' ')

    # print(nodes_string)
    # print(nfs3_paths)
    # print(nfs4_paths)

    # ----- Ensure log directory exists -----
    LOGDIR = os.path.join(script_folder, "result-logs")
    os.makedirs(LOGDIR, exist_ok=True)


    # ----- Four Corners Test Matrix -----
    four_corners_tests = [
        ("--write", "1M", "512M", "seq_write_large"),
        ("--read", "1M", "512M", "seq_read_large"),
        ("--write", "4K", "256K", "rand_write_small"),
        ("--read", "4K", "256K", "rand_read_small"),
    ]
    timelimit = "0"
    threads = "1"
    dirs_i=1
    file_i=1
    iodepth=1
    other_params="--cpu --lat --mkdirs --nodelerr --trunctosize --direct --log 1"
    # --dirsharing --nodiocheck --nofdsharing --dryrun --deldirs --delfiles
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    job_commands = []
    job_commands.append('#!/bin/bash')

    def run_elbencho(mode_flag, blocksize, filesize, label):
        if 'rand' in label:
            mode_str = f"{mode_flag} --rand"
        else:
            mode_str = mode_flag

        # nfs3 job setup #
        label_str = f'NFS3_{label}'
        logfile = os.path.join(LOGDIR, f"{timestamp}_{label_str}.txt")
        gencsv = os.path.join(LOGDIR, f"{timestamp}_{label_str}.csv")
        livecsv = os.path.join(LOGDIR, f"{timestamp}_{label_str}-live.csv")
        
        nfs3_path = local_fs_paths[0]

        print()
        print('label_str:'.ljust(30), label_str)
        print('mode_str:'.ljust(30), mode_str)
        print('blocksize:'.ljust(30), blocksize)
        print('filesize:'.ljust(30), filesize)
        print('timelimit:'.ljust(30), timelimit)
        print('threads:'.ljust(30), threads)
        print('iodepth:'.ljust(30), iodepth)
        print('dirs_i:'.ljust(30), dirs_i)
        print('file_i:'.ljust(30), file_i)
        print('other_params:'.ljust(30), other_params)
        print('logfile:'.ljust(30), logfile)
        print('gencsv:'.ljust(30), gencsv)
        print('livecsv:'.ljust(30), livecsv)
        print('hosts:'.ljust(30), nodes_string)
        print('nfs3_path:'.ljust(30), nfs3_path)

        cmd3 = (f'{elbencho_exe} '
               f'--hosts {nodes_string} '
               f'--live1 --livecsv "{livecsv}" '
               f'--csvfile "{gencsv}" '
               f'--resfile "{logfile}" '
               f'{mode_str} '
               f'--threads=$(nproc) '
               f'--iodepth={iodepth} '
               f'--dirs={dirs_i} --files={file_i} '
               f'--block={blocksize} '
               f'--size={filesize} '
               f'{other_params} '
               f'--timelimit {timelimit}  '
               f'{nfs3_path}/')
        job_commands.append(f'')
        job_commands.append(f'#-----------------------------------------------------------------------------------')
        job_commands.append(f'')
        job_commands.append(f'echo "{label_str}"')
        job_commands.append(cmd3)
        job_commands.append(f'sleep 3')
        job_commands.append(f'#===================================================================================')
        cmd3 = ""


        # nfs4 job setup #
        label_str = f'NFS4_{label}'
        logfile = os.path.join(LOGDIR, f"{timestamp}_{label_str}.txt")
        gencsv = os.path.join(LOGDIR, f"{timestamp}_{label_str}.csv")
        livecsv = os.path.join(LOGDIR, f"{timestamp}_{label_str}-live.csv")
        
        nfs4_path = local_fs_paths[1]

        print()
        print('label_str:'.ljust(30), label_str)
        print('mode_str:'.ljust(30), mode_str)
        print('blocksize:'.ljust(30), blocksize)
        print('filesize:'.ljust(30), filesize)
        print('timelimit:'.ljust(30), timelimit)
        print('threads:'.ljust(30), threads)
        print('iodepth:'.ljust(30), iodepth)
        print('dirs_i:'.ljust(30), dirs_i)
        print('file_i:'.ljust(30), file_i)
        print('other_params:'.ljust(30), other_params)
        print('logfile:'.ljust(30), logfile)
        print('gencsv:'.ljust(30), gencsv)
        print('livecsv:'.ljust(30), livecsv)
        print('hosts:'.ljust(30), nodes_string)
        print('nfs4_path:'.ljust(30), nfs4_path)

        cmd4 = (f'{elbencho_exe} '
                f'--hosts {nodes_string} '
                f'--live1 --livecsv "{livecsv}" '
                f'--csvfile "{gencsv}" '
                f'--resfile "{logfile}" '
                f'{mode_str} '
                f'--threads=$(nproc) '
                f'--iodepth={iodepth} '
                f'--dirs={dirs_i} --files={file_i} '
                f'--block={blocksize} '
                f'--size={filesize} '
                f'{other_params} '
                f'--timelimit {timelimit}  '
                f'{nfs4_path}/')
        job_commands.append(f'')
        job_commands.append(f'#-----------------------------------------------------------------------------------')
        job_commands.append(f'')
        job_commands.append(f'echo "{label_str}"')
        job_commands.append(cmd4)
        job_commands.append(f'sleep 3')
        job_commands.append(f'#===================================================================================')
        cmd4 = ""

    # ----- create all tests -----
    for test in four_corners_tests:
        run_elbencho(*test)

    with open('launcher.sh', 'w', encoding='utf-8') as f_out:
        for job_command in job_commands:
            # print(job_command)
            f_out.write(f'{job_command}\n')

    os.chmod('launcher.sh', 0o764)  # u+x
    print()
    print()
    print('Created:  launcher.sh' )
   
    print()
    print('done')
    