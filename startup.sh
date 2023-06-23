#!/bin/sh

# Start the Gunicorn server
gunicorn --bind :5000 --workers 1 --threads 8 --timeout 0 api:app
