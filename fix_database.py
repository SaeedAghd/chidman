#!/usr/bin/env python3
"""
Fix missing database fields in production
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.db import connection

def fix_database():
    """Add missing fields to database tables"""
    cursor = connection.cursor()
    
    fixes = [
        ("ALTER TABLE store_analysis_payment ADD COLUMN IF NOT EXISTS order_id VARCHAR(100);", "order_id in payment table"),
        ("ALTER TABLE store_analysis_payment ADD COLUMN IF NOT EXISTS payment_id VARCHAR(100);", "payment_id in payment table"),
        ("ALTER TABLE store_analysis_payment ADD COLUMN IF NOT EXISTS gateway_response JSONB;", "gateway_response in payment table"),
        ("ALTER TABLE store_analysis_payment ADD COLUMN IF NOT EXISTS transaction_id VARCHAR(100);", "transaction_id in payment table"),
        ("ALTER TABLE store_analysis_payment ADD COLUMN IF NOT EXISTS is_test BOOLEAN DEFAULT FALSE;", "is_test in payment table"),
        ("ALTER TABLE store_analysis_wallet ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'IRR';", "currency in wallet table"),
        ("ALTER TABLE store_analysis_storeanalysis ADD COLUMN IF NOT EXISTS store_url VARCHAR(500);", "store_url in storeanalysis table"),
        ("ALTER TABLE store_analysis_supportticket ADD COLUMN IF NOT EXISTS resolved_at TIMESTAMP;", "resolved_at in supportticket table"),
        ("ALTER TABLE store_analysis_supportticket ADD COLUMN IF NOT EXISTS closed_at TIMESTAMP;", "closed_at in supportticket table"),
        ("ALTER TABLE store_analysis_supportticket ADD COLUMN IF NOT EXISTS last_reply_at TIMESTAMP;", "last_reply_at in supportticket table"),
    ]
    
    for sql, description in fixes:
        try:
            cursor.execute(sql)
            print(f"✅ {description}")
        except Exception as e:
            print(f"⚠️ {description}: {e}")
    
    print("🎉 Database fix completed!")

if __name__ == "__main__":
    fix_database()
