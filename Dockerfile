FROM immauss/openvas

# Ustawienie środowiska
RUN cd /opt && mkdir reports && mkdir app
RUN apt-get update -y && apt-get install -y python3-nmap python3-netifaces cron

# Skopiowanie plików
COPY ./src /opt/app
COPY crontab.txt /etc/cron.d/crontab.txt

# Uprawnienia i uruchomienie cron
RUN chmod 0644 /etc/cron.d/crontab.txt
RUN crontab /etc/cron.d/crontab.txt
RUN touch /var/log/cron.log

# Uruchomienie cron
CMD ["cron", "-f"]
