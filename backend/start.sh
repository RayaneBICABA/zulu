#!/bin/sh
set -e

max_attempts=12
attempt=1

while true; do
	if flask --app run db upgrade; then
		break
	fi

	if [ "$attempt" -ge "$max_attempts" ]; then
		exit 1
	fi

	echo "Database not ready yet, retrying in 5 seconds... ($attempt/$max_attempts)"
	attempt=$((attempt + 1))
	sleep 5
done

exec gunicorn wsgi:app -c gunicorn.conf.py