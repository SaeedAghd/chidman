#!/usr/bin/env bash
# Build script for Render deployment

echo "🚀 Starting build process..."

# Set environment variables
export PYTHONPATH=/opt/render/project/src
export DJANGO_SETTINGS_MODULE=chidmano.settings

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# Create superuser if needed (optional)
echo "👤 Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@chidman.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
"

echo "✅ Build completed successfully!"
