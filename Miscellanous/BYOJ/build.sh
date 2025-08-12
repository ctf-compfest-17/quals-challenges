#!/bin/bash

FILENAME="flag-$(tr -dc A-Za-z0-9 < /dev/urandom | head -c 20).txt"
echo "Filename is $FILENAME"
export FILENAME

docker compose down
docker compose up -d --build
