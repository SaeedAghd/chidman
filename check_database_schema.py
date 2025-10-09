#!/usr/bin/env python
import os
import sys
import django
import sqlite3

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

def check_database_schema():
    """بررسی کامل schema دیتابیس"""
    print("🔍 بررسی Schema دیتابیس...")
    
    # اتصال مستقیم به دیتابیس
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # بررسی جدول store_analysis_order
        print("\n📊 بررسی جدول store_analysis_order:")
        cursor.execute("PRAGMA table_info(store_analysis_order)")
        columns = cursor.fetchall()
        
        if columns:
            print("✅ جدول موجود است:")
            for col in columns:
                print(f"   - {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'} - Default: {col[4]}")
        else:
            print("❌ جدول store_analysis_order وجود ندارد!")
        
        # بررسی migration ها
        print("\n📋 بررسی migration ها:")
        cursor.execute("SELECT * FROM django_migrations WHERE app='store_analysis' ORDER BY id DESC LIMIT 10")
        migrations = cursor.fetchall()
        
        for migration in migrations:
            print(f"   - {migration[2]} ({migration[3]})")
        
        # بررسی تعداد رکوردها
        print("\n📈 آمار رکوردها:")
        tables = ['store_analysis_order', 'store_analysis_storeanalysis', 'store_analysis_payment']
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   - {table}: {count} رکورد")
            except sqlite3.OperationalError as e:
                print(f"   - {table}: خطا - {e}")
        
    except Exception as e:
        print(f"❌ خطا در بررسی schema: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    check_database_schema()
