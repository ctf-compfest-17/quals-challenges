#!/bin/bash

set -e

(cd challenge-base && docker build  . -t gcr.io/paradigmxyz/ctf/base:latest)
(cd challenge && docker build . -f Dockerfile.eth -t dimasmaualana/eth:latest)