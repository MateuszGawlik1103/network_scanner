#!/bin/bash
service cron start
crontab -l > /tmp/mycron
echo "* * * * * date >> /opt/date" >> /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron
