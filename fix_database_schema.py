#!/usr/bin/env python
import os
import sys
import django
import sqlite3

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

def fix_database_schema():
    """اضافه کردن فیلدهای گمشده به دیتابیس"""
    print("🔧 اضافه کردن فیلدهای گمشده...")
    
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # بررسی وجود فیلد payment_method
        cursor.execute("PRAGMA table_info(store_analysis_order)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'payment_method' not in column_names:
            print("➕ اضافه کردن فیلد payment_method...")
            cursor.execute("ALTER TABLE store_analysis_order ADD COLUMN payment_method VARCHAR(50) DEFAULT 'online'")
            print("✅ فیلد payment_method اضافه شد")
        else:
            print("✅ فیلد payment_method موجود است")
        
        if 'transaction_id' not in column_names:
            print("➕ اضافه کردن فیلد transaction_id...")
            cursor.execute("ALTER TABLE store_analysis_order ADD COLUMN transaction_id VARCHAR(100)")
            print("✅ فیلد transaction_id اضافه شد")
        else:
            print("✅ فیلد transaction_id موجود است")
        
        conn.commit()
        
        # بررسی نهایی
        print("\n📊 بررسی نهایی schema:")
        cursor.execute("PRAGMA table_info(store_analysis_order)")
        columns = cursor.fetchall()
        
        for col in columns:
            print(f"   - {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'} - Default: {col[4]}")
        
    except Exception as e:
        print(f"❌ خطا در اضافه کردن فیلدها: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database_schema()