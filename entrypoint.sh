#!/bin/sh

# Activate virtual environment
. /opt/venv/bin/activate

# Change to Django project directory
cd /app

# Apply Django migrations
python manage.py migrate

# Start Django application using gunicorn
exec /opt/venv/bin/gunicorn personal_portfolio.wsgi:application --bind 0.0.0.0:8000 --workers 4
