#!/bin/bash

# Start script for Liara deployment
echo "🚀 Starting Chidmano application..."

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export DJANGO_SETTINGS_MODULE="chidmano.settings"

# Run migrations first
echo "📊 Running migrations..."
python manage.py migrate --noinput

# Do not collect static files at runtime on Liara; handled at build-time
echo "📁 Skipping collectstatic at runtime (handled during build)"

# Start the application with gunicorn
echo "🌐 Starting Gunicorn server..."
exec gunicorn chidmano.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
