#!/bin/bash

socat TCP-LISTEN:8080,reuseaddr,fork EXEC:"python3 -B chall.py"