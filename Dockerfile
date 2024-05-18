FROM immauss/openvas
RUN cd /opt; mkdir reports;
RUN mkdir app;
RUN apt-get update -y; apt-get install python3-nmap -y; apt-get install python3-netifaces -y
COPY ./src /opt/app