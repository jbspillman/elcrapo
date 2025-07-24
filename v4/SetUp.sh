#!/bin/bash

nodes_list='/home/spillman/elcrapo/host_list.txt'
crd='/home/spillman/.config/generic.json'
ssh="sshpass -f ${crd} ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no -l"

host_count=`cat $nodes_list | grep -v ^$ | sort | uniq | wc -l`


function PingHosts() {
  counter=0
  max_loops=20
  y=0
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
        y=$((y+1))
        if [[ $y == $max_loops ]]; then
            counter=999
        fi
    fi  
  done
}


function CheckPaths() {
    echo "> Check Main FileSystem Start."
    
    ssd_path="/mnt/elcrapo_ssd"
    hdd_path="/mnt/elcrapo_hdd"
    
    # /benchmark_tests/ssd                   
    # /mnt/Drives/12000a/benchmark_tests/hdd
    
    # mount -vvv -t nfs -o vers=3,rsize=131072,wsize=131072,hard,intr,timeo=600 beastserver.beastmode.local.net:/benchmark_tests/ssd /mnt/elcrapo_ssd
    # mount -vvv -t nfs -o vers=3,rsize=131072,wsize=131072,hard,intr,timeo=600 beastserver.beastmode.local.net:/mnt/Drives/12000a/benchmark_tests/hdd /mnt/elcrapo_hdd

    
    for tgt in `cat $nodes_list | sort | uniq`; do
        echo
        echo
        echo
        echo "Checking : $tgt "
        ssd=false
        hdd=false
        while read -r line; do
            echo $line
            if [[ "$line" == *"$ssd_path"* ]]; then               
                ssd=true
            elif [[ "$line" == *"$hdd_path"* ]]; then
                hdd=true
            fi
        done < <( $ssh root $tgt "df -h" 2>&1 )
        
       
        if [[ $hdd == "false" ]]; then
            echo "hdd:  $hdd"
            echo "# create the path."
            $ssh root $tgt "mkdir -p $hdd_path 2>&1"
            echo "# chmod the path."
            $ssh root $tgt "chmod -Rv 777 $hdd_path 2>&1"
            echo "# chown the path."
            $ssh root $tgt "chown -Rv spillman:spillman $hdd_path 2>&1"
            echo "# ls the path."
            $ssh root $tgt "ls -la $hdd_path 2>&1"
            echo "# mount the path."
            $ssh root $tgt "mount -vvv -t nfs -o vers=3,rsize=131072,wsize=131072,hard,intr,timeo=600 beastserver.beastmode.local.net:/mnt/Drives/12000a/benchmark_tests/hdd $hdd_path 2>&1"
            echo "# df -h the path."
            $ssh root $tgt "df -h $hdd_path 2>&1"   
            echo            

        fi
        
        if [[ $ssd == "false" ]]; then
            echo "ssd:  $ssd"
            echo "# create the path."
            $ssh root $tgt "mkdir -p $ssd_path 2>&1"
            echo "# chmod the path."
            $ssh root $tgt "chmod -Rv 777 $ssd_path 2>&1"
            echo "# chown the path."
            $ssh root $tgt "chown -Rv spillman:spillman $ssd_path 2>&1"
            echo "# ls the path."
            $ssh root $tgt "ls -la $ssd_path 2>&1"
            echo "# mount the path."
            $ssh root $tgt "mount -vvv -t nfs -o vers=3,rsize=131072,wsize=131072,hard,intr,timeo=600 beastserver.beastmode.local.net:/benchmark_tests/ssd $ssd_path 2>&1"
            echo "# df -h the path."
            $ssh root $tgt "df -h $ssd_path 2>&1"   
            echo            

        fi
             
        
   done
    
 
}


function shutDownHosts() {
    for tgt in `cat $nodes_list | sort | uniq`; do  
        echo
        echo ">>> Shutting down  $tgt"
        $ssh root $tgt "shutdown --poweroff"
    done

}

function startServices() {

    for tgt in `cat $nodes_list | sort | uniq`; do  
        echo
        echo ">>> start elbencho  $tgt"
        $ssh spillman $tgt "/usr/bin/elbencho --service"
    done

}

function stopServices() {

    for tgt in `cat $nodes_list | sort | uniq`; do  
        echo
        echo ">>> stop elbencho  $tgt"
        $ssh root $tgt "/usr/bin/elbencho --hosts $tgt --quit"
    done

}


# PingHosts
# CheckPaths
# shutDownHosts

# stopServices
# startServices



exit 0


# /bench/nfs3_data
# /bench/nfs4_data
