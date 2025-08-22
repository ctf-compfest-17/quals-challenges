FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y socat && \
    pip install py-ecc pycryptodome

COPY src/chall.py .
COPY src/secret.py .
COPY src/flag.txt .

CMD socat TCP-LISTEN:8080,fork,reuseaddr EXEC:"python3 chall.py",stderr
