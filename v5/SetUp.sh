#!/bin/bash

nodes_list='/home/spillman/elcrapo/host_list.txt'
crd='/home/spillman/.config/generic.json'
ssh="sshpass -f ${crd} ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no -l"
host_count=`cat $nodes_list | egrep -v "^#|^$" | sort | uniq | wc -l`

function ping_svr() {
    local svr=$1
    text=`ping -c 1 -w 1 -W 1 $svr 2>&1`
    if [[ "$text" == *"1 received"* ]]; then
        return 0
    elif [[ "$text" == *"100% packet loss"* ]]; then
        return 1
    else
        return 1
    fi
}

function PingHosts() {
  counter=0
  max_loops=20
  y=0
  until [ $counter -eq 999 ]; do
    x=0
    online=0
    for tgt in `cat $nodes_list | egrep -v "^#|^$" | sort | uniq`; do
      x=$((x+1))
      
      (ping_svr $tgt) 
      result=$?
      if [[ $result == 0 ]]; then
        online=$((online+1))
      else
        echo "$tgt offline"
      fi
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

function MountPaths() {
    ssd_path="/mnt/elcrapo_ssd"   # /benchmark_tests/ssd
    hdd_path="/mnt/elcrapo_hdd"   # /mnt/Drives/12000a/benchmark_tests/hdd

    # mount -vvv -t nfs -o vers=3,rsize=131072,wsize=131072,hard,intr,timeo=600 beastserver.beastmode.local.net:/benchmark_tests/ssd /mnt/elcrapo_ssd
    # mount -vvv -t nfs -o vers=3,rsize=131072,wsize=131072,hard,intr,timeo=600 beastserver.beastmode.local.net:/mnt/Drives/12000a/benchmark_tests/hdd /mnt/elcrapo_hdd

    local_dns_suffix="beastmode.local.net"
    for tgt in `cat $nodes_list | egrep -v "^#|^$"| sort | uniq`; do
        echo
        echo
        echo
        echo "Checking : $tgt "
        ssd=false
        hdd=false
        while read -r line; do
            if [[ "$line" == *"$local_dns_suffix"* ]]; then
              echo $line
              if [[ "$line" == *"$ssd_path"* ]]; then
                  ssd=true
              elif [[ "$line" == *"$hdd_path"* ]]; then
                  hdd=true
              fi
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

function UnMountPaths() {
    ssd_path="/mnt/elcrapo_ssd"   # /benchmark_tests/ssd
    hdd_path="/mnt/elcrapo_hdd"   # /mnt/Drives/12000a/benchmark_tests/hdd

    for tgt in `cat $nodes_list | egrep -v "^#|^$"| sort | uniq`; do
        echo
        echo
        echo
        echo "Checking : $tgt "
        local_dns_suffix="beastmode.local.net"
        while read -r line; do
            if [[ "$line" == *"$local_dns_suffix"* ]]; then
                mount_point=`echo $line | awk '{print $NF}'`
                echo "Unmounting: $line"
                $ssh root $tgt "umount -vvfl $mount_point" 2>&1
            fi
        done < <( $ssh root $tgt "df -h" 2>&1 )
   done
}

function rebootHosts() {
    for tgt in `cat $nodes_list | egrep -v "^#|^$"| sort | uniq`; do  
        echo
        echo ">>> Rebooting $tgt"
        $ssh root $tgt "shutdown -r now" 2>&1
    done
}


function shutDownHosts() {
    for tgt in `cat $nodes_list | egrep -v "^#|^$"| sort | uniq`; do  
        echo
        echo ">>> Shutting down  $tgt"
        $ssh root $tgt "shutdown --poweroff"
    done
}

function startServices() {
    for tgt in `cat $nodes_list | egrep -v "^#|^$"| sort | uniq`; do
        echo
        echo ">>> start elbencho  $tgt"
        line=`$ssh spillman $tgt "/usr/bin/elbencho --service 2>&1"`
        if [[ "$line" == *"SysErr: Address in use"* ]]; then
          echo " >>>>>> service is running..."
        fi
    done
}

function stopServices() {
    for tgt in `cat $nodes_list | egrep -v "^#|^$"| sort | uniq`; do
        echo
        echo ">>> stop elbencho  $tgt"
        ret=`$ssh root $tgt "/usr/bin/elbencho --hosts $tgt --quit"`
        echo $ret
    done
}

function checkSSH() {
    for tgt in `cat $nodes_list | egrep -v "^#|^$"| sort | uniq`; do
        echo
        echo ">>> ssh check  $tgt"
        
        echo " user: spillman "
        $ssh spillman $tgt "uptime 2>&1"
        
        echo " user: root "
        $ssh root $tgt "uptime 2>&1"
    
    done

}

arg=$1
if [[ -z $arg ]]; then
    echo " ########## MENU ##########   "
    echo " Ping Hosts      :     1      "
    echo " Start Hosts     :     2      "
    echo " Start Services  :     3      "
    echo " Stop Services   :     4      "
    echo " Mount Paths     :     5      "
    echo " UnMount Paths   :     6      "
    echo " Reboot Hosts    :     7      "
    echo " Shutdown Hosts  :     8      "
    echo " ##########################   "
    exit 1
fi 

if [[ $arg == 1 ]]; then
    echo "PingHosts Selected...."
    PingHosts
elif [[ $arg == 2 ]]; then
    echo "startHosts Selected...."
    startHosts
elif [[ $arg == 3 ]]; then
    echo "startServices Selected...."
    startServices
elif [[ $arg == 4 ]]; then
    echo "stopServices Selected...."
    stopServices
elif [[ $arg == 5 ]]; then
    echo "MountPaths Selected...."
    MountPaths
elif [[ $arg == 6 ]]; then
    echo "UnMountPaths Selected...."
    UnMountPaths
elif [[ $arg == 7 ]]; then
    echo "rebootHosts Selected...."
    rebootHosts
elif [[ $arg == 8 ]]; then
    echo "shutDownHosts Selected...."
    shutDownHosts
elif [[ $arg == 9 ]]; then
     echo "checkSSH Selected...."
    checkSSH

else
    exit 2
fi    

exit 0