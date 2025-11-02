#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اضافه کردن فیلد address به UserProfile در Liara
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.db import connection

def add_address_field():
    """اضافه کردن فیلد address اگر وجود ندارد"""
    vendor = connection.vendor
    print(f"📊 Database Vendor: {vendor}")
    
    # بررسی وجود فیلد
    address_exists = False
    
    with connection.cursor() as cursor:
        if vendor == 'postgresql':
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='store_analysis_userprofile' 
                AND column_name='address'
            """)
            address_exists = cursor.fetchone() is not None
        elif vendor == 'sqlite':
            cursor.execute("PRAGMA table_info(store_analysis_userprofile)")
            columns = [row[1] for row in cursor.fetchall()]
            address_exists = 'address' in columns
    
    if address_exists:
        print("✅ فیلد address قبلاً وجود دارد")
        return True
    
    # اضافه کردن فیلد
    print("📊 اضافه کردن فیلد address...")
    try:
        with connection.cursor() as cursor:
            if vendor == 'postgresql':
                # PostgreSQL - استفاده از IF NOT EXISTS
                cursor.execute("""
                    ALTER TABLE store_analysis_userprofile 
                    ADD COLUMN IF NOT EXISTS address TEXT;
                """)
                connection.commit()
            elif vendor == 'sqlite':
                cursor.execute("""
                    ALTER TABLE store_analysis_userprofile 
                    ADD COLUMN address TEXT;
                """)
        print("✅ فیلد address با موفقیت اضافه شد")
        return True
    except Exception as e:
        if 'already exists' in str(e).lower() or 'duplicate column' in str(e).lower():
            print("✅ فیلد address قبلاً وجود دارد")
            return True
        print(f"❌ خطا در اضافه کردن فیلد: {e}")
        return False

if __name__ == '__main__':
    success = add_address_field()
    sys.exit(0 if success else 1)

