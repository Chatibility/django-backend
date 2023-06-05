#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python3 -m uvicorn chatibility.asgi:application --host 0.0.0.0 --port 5050