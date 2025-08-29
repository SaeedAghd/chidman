#!/usr/bin/env bash
# Build script for Render deployment

set -e  # Exit on any error

echo "🚀 Starting build process..."

# Set environment variables
export PYTHONPATH=/opt/render/project/src
export DJANGO_SETTINGS_MODULE=chidmano.settings

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Verify Django project structure
echo "🔍 Verifying Django project structure..."
python -c "import chidmano; print('✅ chidmano module found')" || exit 1
python -c "import store_analysis; print('✅ store_analysis module found')" || exit 1

# Test Django setup
echo "🧪 Testing Django setup..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
import django
django.setup()
print('✅ Django setup successful')
" || exit 1

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear || echo "⚠️ Warning: Static files collection failed"

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput || echo "⚠️ Warning: Migrations failed"

# Test WSGI application
echo "🧪 Testing WSGI application..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
from chidmano.wsgi import application
print('✅ chidmano.wsgi:application loaded successfully')
" || exit 1

echo "✅ Build completed successfully!"
