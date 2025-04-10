#!/bin/bash

db="${1:-data/database__2025-03-21__17:12:35.196730.pkl}"
docker run --rm -e DB_PATH=$db -p 5000:5000 -it aif-fep-db:latest
