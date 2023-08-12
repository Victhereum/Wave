#!/bin/bash

# Activate the virtual environment

# Start Gunicorn
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers 4 \
  --timeout 120 \
  --log-level=info \
  --access-logfile - \
  --error-logfile -
