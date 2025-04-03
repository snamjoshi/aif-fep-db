#!/bin/bash

DOCKER_BUILDKIT=1 docker build -t aif-fep-db -f app/Dockerfile .
docker run --rm -p 5000:5000 -it aif-fep-db:latest
