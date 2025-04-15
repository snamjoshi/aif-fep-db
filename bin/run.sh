#!/bin/bash

db="${1:-data/database__2025-04-15__16:45:04.248461.pkl}"
docker run --rm -e DB_PATH=$db -p 5000:5000 -it aif-fep-db:latest
