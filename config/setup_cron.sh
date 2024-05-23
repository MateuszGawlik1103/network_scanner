#!/bin/bash
service cron start
crontab -l > /tmp/mycron
echo "* * * * * /usr/bin/python3 /opt/app/scanner.py" >> /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron
