#!/bin/bash
service cron start
crontab -l > /tmp/mycron
echo "" >> /tmp/mycron
echo "*/2 * * * * env EMAIL=$EMAIL EMAIL_PASS=$EMAIL_PASS /usr/bin/python3 /opt/app/send.py" >> /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron
