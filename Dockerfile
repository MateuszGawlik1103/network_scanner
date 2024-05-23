FROM immauss/openvas

# Ustawienie środowiska
RUN cd /opt && mkdir reports && mkdir log; touch ./log/app.log
RUN mkdir app; cd ./app; mkdir config;
RUN apt-get update -y && apt-get install -y python3-nmap python3-netifaces cron

# Skopiowanie plików
COPY ./src /opt/app
COPY ./config /opt/app/config

# Ustawianie uprawnień do uruchamiania
RUN chmod +x /opt/app/scanner.py; chmod +x /opt/app/logger.py; chmod +x /opt/app/delete_task.py; chmod +x /opt/app/target_create.py; chmod +x /opt/app/host_disc.py
RUN chmod +x /opt/app/config/setup_cron.sh
