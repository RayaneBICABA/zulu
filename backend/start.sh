#!/bin/sh
set -e

flask --app run db upgrade
exec gunicorn wsgi:app -c gunicorn.conf.py