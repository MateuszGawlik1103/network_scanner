#!/bin/bash

service cron start
crontab -l > /tmp/mycron

echo "*11 * * * * root python3 /opt/app/scanner.py >> /var/log/scanner.log 2>&1" >> /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron
