#!/bin/bash
service cron start
crontab -l > /tmp/mycron
echo "* * * * * root python3 /opt/app/script.py >> /opt/output.txt" >> /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron
