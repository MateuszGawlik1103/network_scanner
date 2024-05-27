#!/bin/bash


if ! command -v docker &> /dev/null; then
    echo -e "\e[0;31m[!]\e[m Docker is not installed."
    echo -e "\e[0;31m[!]\e[m Warning: Script supports installing Docker on Ubuntu and Debian systems only!"
    echo -e "\e[0;36m[*]\e[m Updating package lists..."
    sudo apt-get update -y
    echo -e "\e[0;36m[*]\e[m Installing Docker..."
    sudo apt install docker.io -y
    echo -e "\e[0;31m\e[0;32m[*]\e[m\e[m Docker has been installed and started successfully."
else
    echo -e "\e[0;36m[*]\e[m Docker is installed."
fi

sudo service docker start

if [ -z "$FREQUENCY" ]; then
    echo -e "\e[0;31m[!]\e[m FREQUENCY is not set."
    echo -e "\e[0;31m[!]\e[m Please set the FREQUENCY environment variable."
    exit 1
fi

if [ -z "$EMAIL" ]; then
    echo -e "\e[0;31m[!]\e[m EMAIL is not set."
    echo -e "\e[0;31m[!]\e[m Please set the EMAIL environment variable."
    exit 1
fi

if [ -z "$EMAIL_PASS" ]; then
    echo -e "\e[0;31m[!]\e[m EMAIL_PASS is not set."
    echo -e "\e[0;31m[!]\e[m Please set the EMAIL_PASS environment variable."
    exit 1
fi

IP=$(ip addr show eth0 | grep -oP 'inet \K[\d.]+/\d{2}')

echo -e "\e[0;36m[*]\e[m Pulling ghcr.io/mateuszgawlik1103/net-scanner-ghcr:latest..."
docker pull ghcr.io/mateuszgawlik1103/net-scanner-ghcr:latest

echo -e "Host ip address: {$IP}"
echo -e "\e[0;36m[*]\e[m Running the container in detached mode..."
docker run --detach --publish 8090:9392 -e SKIPSYNC=true -e IP=$IP -e FREQUENCY=$FREQUENCY -e EMAIL_PASS="$EMAIL_PASS" -e EMAIL=$EMAIL --name scanner ghcr.io/mateuszgawlik1103/net-scanner-ghcr:latest
docker exec scanner /bin/bash /opt/app/config/setup_cron.sh
docker exec -it scanner python3 /opt/app/scanner.py