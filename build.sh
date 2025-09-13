#!/usr/bin/env bash
# Build script for Render deployment

echo "Starting build process..."

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:/opt/render/project/src"
export DJANGO_SETTINGS_MODULE="chidmano.settings"

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
EOF

# Test the application
echo "Testing application..."
python manage.py check --deploy

# Create a simple test user if it doesn't exist
echo "Creating test user if needed..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='saeed').exists():
    User.objects.create_user('saeed', 'saeed@example.com', 'saeed123')
    print('Test user created: saeed/saeed123')
else:
    print('Test user already exists')
EOF

echo "Build process completed successfully!"