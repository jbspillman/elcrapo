#!/bin/bash

nodes_list='host_list.txt'
crd='generic.json'
ssh="sshpass -f ${crd} ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no -l"
host_count=`cat $nodes_list | grep -v ^$ | sort | uniq | wc -l`

function PingHosts() {
  counter=0
  until [ $counter -eq 999 ]; do
    x=0
    online=0
    for tgt in `cat $nodes_list | sort | uniq`; do
      x=$((x+1))
      while read -r line; do
        if [[ "$line" == *"1 received"* ]]; then
          online=$((online+1))
          break
        elif [[ "$line" == *"100% packet loss"* ]]; then
          echo "$tgt offline"
          break
        fi
      done < <( ping -c 1 -w 1 -W 1 $tgt )
    done

    echo "PingHosts: online count: $online of $host_count"
    if [[ $host_count == $online ]]; then
        counter=999
    else
        sleep 3  #  Pause for 3 second.
    fi
  done
}



function CheckPaths() {
    echo "> Check Main FileSystem Done."
    $ssh root beastserver.beastmode.local.net 'df -h /mnt/Drives/02000c/elbencho'
    # $ssh root beastserver.beastmode.local.net 'ls -la /mnt/Drives/02000c/elbencho'
    
    # for tgt in `cat $nodes_list | sort | uniq`; do
        # lcl_host=`echo $tgt | awk -F "." '{print $1}'`
        # $ssh root beastserver.beastmode.local.net "mkdir -p /mnt/Drives/02000c/elbencho/"
    # done
    $ssh root beastserver.beastmode.local.net 'chown -R spillman:spillman /mnt/Drives/02000c/elbencho'
    $ssh root beastserver.beastmode.local.net 'chmod -R 777 /mnt/Drives/02000c/elbencho'
    $ssh root beastserver.beastmode.local.net 'ls -la /mnt/Drives/02000c/elbencho'
    echo "> Main FileSystem Done."
    echo
    
    for tgt in `cat $nodes_list | sort | uniq`; do
        echo
        echo ">>> Check for NFS3 Folder Path on $tgt"
        n3_path="/bench/nfs3_data"
        
        ismnt=`$ssh root $tgt "df -h 2>&1 | grep $n3_path"`
        if [[ "$ismnt" == *"beastserver.beastmode.local.net"* ]]; then
            echo " PASS: $tgt [$ismnt]"
        else
            echo " FAIL: $tgt [$ismnt]"
            if [[ "$ismnt" == *"Stale file handle"* ]]; then
                $ssh root $tgt "umount -fl $n3_path 2>&1"
            fi
            echo "remove the path."
            $ssh root $tgt "rm -Rf $n3_path 2>&1"
            echo "create the path."
            $ssh root $tgt "mkdir -p $n3_path 2>&1"
            echo "chmod the path."
            $ssh root $tgt "chmod -R 777 $n3_path 2>&1"
            echo "chown the path."
            $ssh root $tgt "chown -R spillman:spillman $n3_path 2>&1"
            echo "ls the path."
            $ssh root $tgt "ls -la $n3_path 2>&1"
            echo "mount the path."
            $ssh root $tgt "mount -vvv -t nfs -o vers=3,rsize=131072,wsize=131072,hard,intr,timeo=600 beastserver.beastmode.local.net:/mnt/Drives/02000c/elbencho /bench/nfs3_data 2>&1"
            echo "df -h the path."
            $ssh root $tgt "df -h $n3_path 2>&1"
        fi

        echo
        echo ">>> Check for NFS4 Folder Path on $tgt"
        n4_path="/bench/nfs4_data"
        ismnt=`$ssh root $tgt "df -h 2>&1 | grep $n4_path"`
        if [[ "$ismnt" == *"beastserver.beastmode.local.net"* ]]; then
            echo " PASS: $tgt [$ismnt]"
        else
            echo " FAIL: $tgt [$ismnt]"
            if [[ "$ismnt" == *"Stale file handle"* ]]; then
                $ssh root $tgt "umount -fl $n4_path 2>&1"
            fi
            echo "remove the path."
            $ssh root $tgt "rm -Rf $n4_path 2>&1"
            echo "create the path."
            $ssh root $tgt "mkdir -p $n4_path 2>&1"
            echo "chmod the path."
            $ssh root $tgt "chmod -R 777 $n4_path 2>&1"
            echo "chown the path."
            $ssh root $tgt "chown -R spillman:spillman $n4_path 2>&1"
            echo "ls the path."
            $ssh root $tgt "ls -la $n4_path 2>&1"
            echo "mount the path."
            $ssh root $tgt "mount -vvv -t nfs -o vers=4,rsize=131072,wsize=131072,hard,intr,timeo=600 beastserver.beastmode.local.net:/mnt/Drives/02000c/elbencho /bench/nfs4_data 2>&1"
            echo "df -h the path."
            $ssh root $tgt "df -h $n4_path 2>&1"
        fi
       
    done

}

PingHosts
CheckPaths


exit 0
