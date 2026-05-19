#!/usr/bin/env sh
set -eu

mkdir -p "${MEDIA_ROOT:-media}"

python manage.py check
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec daphne -b 0.0.0.0 -p "${PORT:-8000}" manage_ai.asgi:application
