#!/bin/bash

# Start the cron service
service cron start

# Define the cron expression based on the FREQUENCY environment variable
case $FREQUENCY in
    H)
        CRON_EXPRESSION="0 * * * *"  # Every hour
        ;;
    *H)
        # Extract the number from the FREQUENCY variable (e.g., 4 from 4H)
        HOURS=${FREQUENCY%H}
        CRON_EXPRESSION="0 */$HOURS * * *"  # Every n hours
        ;;
    D)
        CRON_EXPRESSION="0 0 * * *"  # Every day at midnight
        ;;
    *D)
        # Extract the number from the FREQUENCY variable (e.g., 3 from 3D)
        DAYS=${FREQUENCY%D}
        CRON_EXPRESSION="0 0 */$DAYS * *"  # Every n days
        ;;
    W)
        CRON_EXPRESSION="0 0 * * 0"  # Every week (Sunday at midnight)
        ;;
    M)
        CRON_EXPRESSION="0 0 1 * *"  # Every month (1st of the month at midnight)
        ;;
    *)
        echo "Invalid FREQUENCY value. Please use H, nH, D, nD, W, or M."
        exit 1
        ;;
esac

# Backup the current cron jobs
crontab -l > /tmp/mycron

# Append the new cron job with the calculated CRON_EXPRESSION
echo "$CRON_EXPRESSION /usr/bin/python3 /opt/app/scanner.py" >> /tmp/mycron

# Install the new cron file
crontab /tmp/mycron

# Remove the temporary cron file
rm /tmp/mycron

# Append environment variables to /etc/environment
env >> /etc/environment
