FROM dimasmaualana/eth:latest

# Install required packages for deployment only
RUN apt-get update && apt-get install -y \
    python3-pip \
    && pip3 install --upgrade \
    web3 


COPY deploy/ /home/ctf/
COPY contracts /tmp/contracts

RUN true \
    && cd /tmp \
    && forge build --out /home/ctf/compiled \
    && rm -rf /tmp/contracts \
    && true