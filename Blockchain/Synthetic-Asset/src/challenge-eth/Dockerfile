FROM dimasmaualana/eth:latest

COPY deploy/ /home/ctf/
COPY contracts /tmp/contracts

RUN true \
    && cd /tmp \
    && mkdir -p lib \
    && cd lib \
    && curl -L https://github.com/OpenZeppelin/openzeppelin-contracts/archive/v4.9.3.tar.gz | tar xz \
    && mv openzeppelin-contracts-4.9.3 openzeppelin-contracts \
    && cd /tmp \
    && echo "@openzeppelin/=lib/openzeppelin-contracts/" > remappings.txt \
    && forge build --out /home/ctf/compiled \
    && rm -rf /tmp/contracts /tmp/lib \
    && true