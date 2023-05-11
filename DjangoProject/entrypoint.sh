#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn MushroomDjango.wsgi:application --bind 0.0.0.0:8098