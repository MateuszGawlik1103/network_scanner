#!/bin/bash

service cron start
crontab -l > /tmp/mycron


echo echo "* * * * * date >> /opt/date.txt" >> /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron