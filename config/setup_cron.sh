#!/bin/bash
service cron start
crontab -l > /tmp/mycron
env >> /etc/environment
echo "*/11 * * * * /usr/bin/python3 /opt/app/scanner.py" >> /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron
