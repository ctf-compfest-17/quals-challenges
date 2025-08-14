FROM ubuntu:22.04

RUN apt-get -y -q update \
    && apt-get -y -q install sudo nano git curl wget build-essential python3-pip socat

RUN pip3 install py-ecc pycryptodome

RUN mkdir -p /app/
WORKDIR /app/

COPY src/* .

CMD ["socat", "TCP-LISTEN:8080,fork,reuseaddr", "EXEC:sage chall.py,stderr"]