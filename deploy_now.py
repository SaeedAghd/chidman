#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اصلاح فوری database و دیپلوی
"""

import os
import sys
import django
import subprocess

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.db import connection

def fix_database_and_deploy():
    """اصلاح database و دیپلوی"""
    print("🔧 اصلاح فوری database...")
    
    try:
        cursor = connection.cursor()
        
        # اصلاح فیلد id
        cursor.execute("""
            CREATE TABLE store_analysis_storeanalysis_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_name varchar(200) NOT NULL,
                store_url varchar(200),
                analysis_type varchar(20) NOT NULL,
                status varchar(20) NOT NULL,
                priority varchar(10) DEFAULT 'medium',
                ai_insights TEXT,
                recommendations TEXT,
                analysis_files TEXT,
                price decimal,
                currency varchar(3),
                created_at datetime,
                updated_at datetime,
                completed_at datetime,
                user_id INTEGER,
                analysis_data TEXT,
                order_id char(32),
                preliminary_analysis TEXT,
                results TEXT,
                store_images TEXT
            )
        """)
        
        # کپی داده‌ها
        cursor.execute("""
            INSERT INTO store_analysis_storeanalysis_new 
            SELECT * FROM store_analysis_storeanalysis
        """)
        
        # حذف جدول قدیمی
        cursor.execute("DROP TABLE store_analysis_storeanalysis")
        
        # تغییر نام جدول جدید
        cursor.execute("ALTER TABLE store_analysis_storeanalysis_new RENAME TO store_analysis_storeanalysis")
        
        print("✅ Database اصلاح شد")
        return True
        
    except Exception as e:
        print(f"❌ خطا در اصلاح database: {e}")
        return False

def start_deployment():
    """شروع دیپلوی"""
    print("🚀 شروع دیپلوی...")
    
    try:
        # جمع‌آوری فایل‌های استاتیک
        print("📁 جمع‌آوری فایل‌های استاتیک...")
        result = subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ فایل‌های استاتیک جمع‌آوری شدند")
        else:
            print(f"⚠️ هشدار در collectstatic: {result.stderr}")
        
        # شروع سرور
        print("🌐 شروع سرور Django...")
        print("📝 سرور در آدرس http://127.0.0.1:8000/ در حال اجرا است")
        print("🎉 سیستم چیدمانو آماده برای استفاده است!")
        
        # اجرای سرور
        subprocess.run([sys.executable, 'manage.py', 'runserver', '8000'])
        
    except Exception as e:
        print(f"❌ خطا در دیپلوی: {e}")

if __name__ == "__main__":
    if fix_database_and_deploy():
        start_deployment()
    else:
        print("💥 دیپلوی ناموفق بود!")
