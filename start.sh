#!/bin/bash

# Start script for Liara deployment
echo "🚀 Starting Chidmano application..."

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export DJANGO_SETTINGS_MODULE="chidmano.settings"

# Setup production database
echo "🚀 Setting up production database..."
python manage.py setup_production --username saeed --email saeed@chidmano.ir --password Saeed33124 || {
    echo "❌ Setup failed, trying manual setup..."
    python manage.py makemigrations
    python manage.py migrate --noinput
    python manage.py create_superuser --username saeed --email saeed@chidmano.ir --password Saeed33124 || echo "⚠️ Superuser creation failed"
    python manage.py collectstatic --noinput
}

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
