#!/bin/bash
service cron start
crontab -l > /tmp/mycron
echo "*/11 * * * * . $HOME/.profile; /usr/bin/python3 /opt/app/send.py" >> /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron
