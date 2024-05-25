#!/bin/bash
service cron start
crontab -l > /tmp/mycron
echo "*/2 * * * * . $HOME/.bashrc; /usr/bin/python3 /opt/app/send.py" >> /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron
