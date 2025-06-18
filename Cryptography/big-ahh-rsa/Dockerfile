FROM python:3.9-slim

WORKDIR /app

# Install required packages
RUN apt-get update && \
    apt-get install -y socat && \
    pip install pycryptodome

# Copy challenge files
COPY src/src.py .

# Run with socat
CMD socat TCP-LISTEN:1337,fork,reuseaddr EXEC:"python3 src.py",stderr