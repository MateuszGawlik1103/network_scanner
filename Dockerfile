FROM immauss/openvas

# Ustawienie środowiska
RUN cd /opt && mkdir reports && mkdir app
RUN apt-get update -y && apt-get install -y python3-nmap python3-netifaces cron

# Skopiowanie plików
COPY ./src /opt/app
COPY setup_cron.sh /opt/setup_cron.sh