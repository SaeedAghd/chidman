#!/bin/bash

# Start script for Liara deployment
echo "🚀 Starting Chidmano application..."

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export DJANGO_SETTINGS_MODULE="chidmano.settings"

# Run migrations
echo "📊 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start the application with gunicorn
echo "🌐 Starting Gunicorn server..."
exec gunicorn chidmano.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --timeout 120 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile - \
    --error-logfile -
