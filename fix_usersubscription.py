#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.db import connection

def create_usersubscription_table():
    """Create UserSubscription table if it doesn't exist"""
    cursor = connection.cursor()
    
    # Check if table exists (SQLite syntax)
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='store_analysis_usersubscription';
    """)
    
    table_exists = cursor.fetchone() is not None
    
    if not table_exists:
        print("Creating UserSubscription table...")
        cursor.execute("""
            CREATE TABLE store_analysis_usersubscription (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                service_package_id INTEGER NOT NULL,
                start_date DATETIME NOT NULL,
                end_date DATETIME NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✅ UserSubscription table created successfully!")
    else:
        print("✅ UserSubscription table already exists!")

if __name__ == "__main__":
    create_usersubscription_table()
