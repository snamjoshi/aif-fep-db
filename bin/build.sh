#!/bin/bash

DOCKER_BUILDKIT=1 docker build -t aif-fep-db -f app/Dockerfile .
