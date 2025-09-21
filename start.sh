#!/bin/bash

# Start script for Liara deployment
echo "🚀 Starting Chidmano application..."

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export DJANGO_SETTINGS_MODULE="chidmano.settings"

# Create database tables
echo "📊 Creating database tables..."
python manage.py migrate --noinput || echo "Migration failed, continuing..."

# Create superuser
echo "👤 Creating superuser..."
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('saeed', 'saeed@chidmano.ir', 'Saeed33124') if not User.objects.filter(username='saeed').exists() else print('Superuser exists')" || echo "Superuser creation failed, continuing..."

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput || echo "Collectstatic failed, continuing..."

# Start the application with gunicorn
echo "🌐 Starting Gunicorn server..."
exec gunicorn chidmano.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
