#!/bin/bash


if ! command -v docker &> /dev/null; then
    echo "[!] Docker is not installed."
    echo "[!] Warning: Script supports installing Docker on Ubuntu and Debian systems only!"
    echo "[*] Updating package lists..."
    sudo apt-get update -y
    echo "[*] Installing Docker..."
    sudo apt install docker.io -y
    echo "[+] Docker has been installed and started successfully."
else
    echo "[*] Docker is installed."
fi

sudo service docker start


if [ -z "$EMAIL" ]; then
    echo "[!] EMAIL is not set."
    echo "[!] Please set the EMAIL environment variable."
    exit 1
fi


if [ -z "$EMAIL_PASS" ]; then
    echo "[!] SENDER_PASS is not set."
    echo "[!] Please set the SENDER_PASS environment variable."
    exit 1
fi



echo "[*] Pulling ghcr.io/adi7312/net-scanner-ghcr:latest..."
sudo docker pull ghcr.io/mateusz_gawlik1103/net-scanner-ghcr:latest
# if --audit flag is passed perform below operation

echo "[*] Running the container in detached mode..."
sudo docker run --detach --publish 8090:9392 -e SKIPSYNC=true -e EMAIL_PASS="$EMAIL_PASS" -e EMAIL=$EMAIL --name avs ghcr.io/mateusz_gawlik1103/net-scanner-ghcr:latest
sudo docker exec avs /bin/bash /opt/setup_cron.sh