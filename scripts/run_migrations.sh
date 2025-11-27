#!/bin/bash
# Script to run Django migrations automatically
# This script should be run on the server after git pull

set -e  # Exit on error

echo "🔄 Running Django migrations..."

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run migrations
python manage.py migrate --noinput

echo "✅ Migrations completed successfully!"

# Verify migration for client_ip
python manage.py shell << EOF
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='store_analysis_payment' AND column_name='client_ip';")
result = cursor.fetchone()
if result:
    print("✅ client_ip column exists in Payment table")
else:
    print("❌ client_ip column NOT found - migration may have failed")
EOF

echo "✅ Migration verification completed!"

