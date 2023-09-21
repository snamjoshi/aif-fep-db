#!/bin/sh

docker build -t aif-fep-db .
docker run --name aif-fep-db -p 5000:5000 -it aif-fep-db:latest