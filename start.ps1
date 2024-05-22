
if (-not $env:EMAIL) {
    Write-Host "[!] EMAIL is not set."
    Write-Host "[!] Please set the EMAIL environment variable."
    exit 1
}


if (-not $env:EMAIL_PASS) {
    Write-Host "[!] EMAIL_PASS is not set."
    Write-Host "[!] Please set the SENDER_PASS environment variable."
    exit 1
}


Write-Host "[*] Pulling ghcr.io/mateuszgawlik1103/net-scanner-ghcr:latest..."
docker pull ghcr.io/mateuszgawlik1103/net-scanner-ghcr:latest
Write-Host "[*] Running the container in detached mode..."
docker run --detach --publish 8090:9392 -e SKIPSYNC=true -e EMAIL_PASS="$env:EMAIL_PASS" -e EMAIL=$env:EMAIL --name avs ghcr.io/mateuszgawlik1103/net-scanner-ghcr:latest
docker exec avs /bin/bash /opt/app/config/setup_cron.sh