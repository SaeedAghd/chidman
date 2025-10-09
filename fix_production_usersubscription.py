#!/usr/bin/env python
"""
Script to create UserSubscription table in production database
Run this on the production server
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.db import connection

def create_usersubscription_table_production():
    """Create UserSubscription table in production database"""
    cursor = connection.cursor()
    
    try:
        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='store_analysis_usersubscription';
        """)
        
        table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            print("Creating UserSubscription table in production...")
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
            print("✅ UserSubscription table created successfully in production!")
        else:
            print("✅ UserSubscription table already exists in production!")
            
        # Test the table
        cursor.execute("SELECT COUNT(*) FROM store_analysis_usersubscription;")
        count = cursor.fetchone()[0]
        print(f"✅ Table test successful! Count: {count}")
        
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = create_usersubscription_table_production()
    if success:
        print("🎉 UserSubscription table setup completed!")
    else:
        print("💥 Failed to setup UserSubscription table!")
        sys.exit(1)
