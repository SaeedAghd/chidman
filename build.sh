#!/bin/bash

# Build script for Liara deployment
echo "🚀 Starting build process for Liara..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser if not exists
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@chidmano.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Run system checks
echo "🔍 Running system checks..."
python manage.py check --deploy

echo "✅ Build completed successfully!"
echo "🌐 Your app is ready for deployment on Liara!"
