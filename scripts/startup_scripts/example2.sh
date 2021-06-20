#!/bin/bash

function log() {
    TIME=$(date -u +'%Y-%m-%d %H:%M:%S %Z')
    LEVEL=$1
    case ${LEVEL} in
        ERROR)
            printf '%s | %s | %s\n' "$TIME" "$LEVEL" "$2" >&2
            ;;
        *)
            printf '%s | %s | %s\n' "$TIME" "$LEVEL" "$2" >&2
    esac
  }

function mountDisk() {
  if [[ $(lsblk | grep $1 | wc -l) -gt 0 ]] && [[ $(blkid | grep $1 | grep ext4 | wc -l) -eq 0 ]]; then
    cmdF="sudo mkfs.ext4 -m 0 -F -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/$1"
    eval ${cmdF}
  fi
  if [[ $(lsblk | grep $1 | wc -l) -gt 0 ]] && [[ $(mount | grep "disk$1" | wc -l) -eq 0 ]]; then
    cmdMD="mkdir -p /mnt/disks/disk$1"
    eval ${cmdMD}
    cmdM="mount -o discard,defaults /dev/$1 /mnt/disks/disk$1"
    eval ${cmdM}
    cmdCH="chmod -R 777 /mnt/disks/disk$1 2> /dev/null"
    eval ${cmdCH}
  fi
}

log INFO "Running startup script"

log INFO "Installing Docker and compose"
sudo apt-get -y remove docker docker-engine docker.io
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates wget software-properties-common rlwrap unzip strace lsof procps htop
sudo wget https://download.docker.com/linux/debian/gpg
sudo apt-key add gpg
echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee -a /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-cache policy docker-ce
sudo apt-get -y install docker-ce
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

log INFO "Authorising docker for container registry"
sudo gcloud -q auth configure-docker

log INFO "Setting up directories for code and logging"
sudo mkdir -p /opt/go
sudo chmod -R 777 /opt/go/
cd /opt/go

log INFO "Transfering the docker compose file from multi region storage"
sudo gsutil cp gs://... /opt/go/docker-compose.yml

disks=`lsblk | grep disk | grep -v sda | awk '{print $1}'`
for disk in $disks; do
  mountDisk $disk
done

log INFO "Run the docker containers"
sudo mkdir -p /mnt/disks/disksdb/kafka-logs
sudo mkdir -p /mnt/disks/disksdc/logs/zookeeper/data
sudo mkdir -p /mnt/disks/disksdc/logs/zookeeper/log
sudo docker-compose -f /opt/go/docker-compose.yml up > /mnt/disks/disksdc/logs/compose.log 2>&1 </dev/null &
