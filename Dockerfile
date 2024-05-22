FROM immauss/openvas

# Ustawienie środowiska
RUN cd /opt && mkdir reports && mkdir log; touch ./log/app.log
RUN mkdir app; cd ./app; mkdir config;
RUN apt-get update -y && apt-get install -y python3-nmap python3-netifaces cron

# Skopiowanie plików
COPY ./src /opt/app
COPY ./config /opt/app/config
