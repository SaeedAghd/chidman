#!/bin/bash

# Start script for Liara deployment
echo "🚀 Starting Chidmano application..."

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export DJANGO_SETTINGS_MODULE="chidmano.settings"

# Create database tables
echo "📊 Creating database tables..."
python manage.py migrate --noinput

# Create superuser
echo "👤 Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='saeed').exists():
    User.objects.create_superuser('saeed', 'saeed@chidmano.ir', 'Saeed33124')
    print('✅ Superuser created')
else:
    print('⚠️ Superuser already exists')
EOF

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
