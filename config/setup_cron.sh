#!/bin/bash

service cron start
crontab -l > /tmp/mycron

echo "10 * * * * root python3 /opt/app/scanner.py" >> /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron
