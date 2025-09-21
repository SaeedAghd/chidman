#!/bin/bash

# Start script for Liara deployment
echo "🚀 Starting Chidmano application..."

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export DJANGO_SETTINGS_MODULE="chidmano.settings"

# Wait for database to be ready
echo "⏳ Waiting for database..."
python manage.py shell -c "
import time
from django.db import connection
from django.core.exceptions import ImproperlyConfigured

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        print('✅ Database connection successful')
        break
    except Exception as e:
        retry_count += 1
        print(f'⏳ Database not ready, retry {retry_count}/{max_retries}: {e}')
        time.sleep(2)

if retry_count >= max_retries:
    print('❌ Database connection failed after maximum retries')
    exit(1)
"

# Create database tables
echo "📊 Creating database tables..."
python manage.py migrate --noinput

# Create superuser
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='saeed').exists():
    User.objects.create_superuser('saeed', 'saeed@chidmano.ir', 'Saeed33124')
    print('✅ Superuser created')
else:
    print('⚠️ Superuser already exists')
"

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
