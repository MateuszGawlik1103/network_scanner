#!/bin/bash

service cron start
crontab -l > /tmp/mycron

echo "*/11 * * * * root python3 /opt/app/scanner.py >> /opt/output.txt" >> /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron
