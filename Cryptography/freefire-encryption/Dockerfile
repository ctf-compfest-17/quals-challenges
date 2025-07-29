# FROM ubuntu:22.04
# ENV DEBIAN_FRONTEND=noninteractive
# ENV TZ=UTC

# RUN apt-get -y -q update \
#     && apt-get -y -q install sudo nano git curl wget build-essential python3-pip socat

# RUN apt-get -y -q install sagemath

# RUN pip3 install py-ecc pycryptodome

# RUN mkdir -p /app/
# WORKDIR /app/

# # Copy your challenge file
# COPY src/* .

# CMD ["socat", "TCP-LISTEN:8080,fork,reuseaddr", "EXEC:sage chall.py,stderr"]


FROM sagemath/sagemath:10.4

USER root
# Update package list and install socat
RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /home/sage

# Copy your Python scripts or other necessary files
COPY src/* /home/sage
COPY requirements.txt /home/sage/
COPY run.sh /home/sage/

# Install Python dependencies
ENV PATH=$PATH:/home/sage/sage/local/var/lib/sage/venv-python3.12.4/bin/
RUN pip3 install -r requirements.txt

RUN chmod +x ./run.sh

# Command to run when the container starts
CMD ["./run.sh"]
