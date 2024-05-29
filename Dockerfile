FROM immauss/openvas

# Setting up the environment
RUN cd /opt && mkdir reports && mkdir log && touch ./log/app.log
RUN mkdir app && cd ./app && mkdir config
RUN apt-get update -y && apt-get install -y python3-nmap cron

# Copying files
COPY ./src /opt/app
COPY ./config /opt/app/config

# Setting permissions for execution
RUN chmod +x /opt/app/scanner.py && chmod +x /opt/app/logger.py && chmod +x /opt/app/delete_task.py && chmod +x /opt/app/target_create.py && chmod +x /opt/app/host_disc.py
RUN chmod +x /opt/app/config/setup_cron.sh
