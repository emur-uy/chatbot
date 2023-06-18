#!/bin/sh

# Start the Gunicorn server
gunicorn --bind :80 --workers 1 --threads 8 --timeout 0 server:app