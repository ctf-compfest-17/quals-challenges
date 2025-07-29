FROM sagemath/sagemath:latest

USER root

WORKDIR /app

RUN apt-get update && \
    apt-get install -y socat && \
    pip install py-ecc pycryptodome && \
    rm -rf /var/lib/apt/lists/*

COPY src/* .

USER sage

CMD socat TCP-LISTEN:8080,fork,reuseaddr EXEC:"python3 chall.py",stderr