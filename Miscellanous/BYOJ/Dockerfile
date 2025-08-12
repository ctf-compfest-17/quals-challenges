FROM ubuntu:24.04 AS base

RUN apt-get update
RUN apt-get install -y git
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y cmake
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y pkg-config
RUN mkdir /build
WORKDIR /build
RUN git clone -b v3.14.0rc1 --depth 1 https://github.com/python/cpython
WORKDIR /build/cpython
RUN ./configure
COPY ./src/bltinmodule.c /build/cpython/Python/bltinmodule.c
COPY ./src/freeze_modules.py /build/cpython/Tools/build/freeze_modules.py
COPY ./src/interpreters.py /build/cpython/Lib/concurrent/interpreters/__init__.py
RUN make -j 4
RUN make install; exit 0

RUN cd / && rm -rf /var/lib/apt/lists/* && rm -rf /build

FROM pwn.red/jail AS chall
COPY --from=base / /srv
COPY ./src/chall.py /srv/app/run
COPY ./src/flag.txt /srv/flag.txt
ENV JAIL_MEM=20M JAIL_TIME=30 JAIL_CPU=250
