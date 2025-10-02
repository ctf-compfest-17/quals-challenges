FROM python:3.11-slim


RUN apt-get update && \
    apt-get install -y socat

COPY /src/chall.py .
COPY /src/md5.py .
COPY /src/rand.py .

CMD socat TCP-LISTEN:8080,fork,reuseaddr EXEC:"python3 chall.py",stderr