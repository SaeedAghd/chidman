#!/bin/bash
set -e

echo "🔄 Running Django migrations safely..."

# Pull latest code first
echo "📥 Pulling latest code..."
git pull origin main || echo "⚠️ Git pull failed, continuing..."

# Run migrations
echo "🔧 Running migrations..."
python manage.py migrate --noinput

if [ $? -eq 0 ]; then
    echo "✅ Django migrations completed successfully."
    
    # Check if there are any pending migrations
    echo "🔍 Checking for pending migrations..."
    python manage.py showmigrations --plan | grep "\[ \]" || echo "✅ All migrations are applied."
    
    exit 0
else
    echo "❌ Django migrations failed."
    exit 1
fi

