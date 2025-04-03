#!/bin/bash
gunicorn --timeout 520 --threads 3 -b 0.0.0.0:5000 wsgi:app