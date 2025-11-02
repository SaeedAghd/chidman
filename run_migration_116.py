#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اسکریپت اجرای migration 0116 در Liara
این اسکریپت migration را اجرا می‌کند و فیلدهای store_address و package_type را اضافه می‌کند
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def check_migration_status():
    """بررسی وضعیت migration"""
    print("\n" + "="*60)
    print("🔍 بررسی وضعیت Migration 0116")
    print("="*60)
    
    vendor = connection.vendor
    print(f"📊 Database Vendor: {vendor}")
    
    # بررسی وجود فیلدها
    missing_fields = []
    
    with connection.cursor() as cursor:
        if vendor == 'postgresql':
            # بررسی store_address
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'store_analysis_storeanalysis' 
                AND column_name = 'store_address'
            """)
            if not cursor.fetchone():
                missing_fields.append('store_address')
            
            # بررسی package_type
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'store_analysis_storeanalysis' 
                AND column_name = 'package_type'
            """)
            if not cursor.fetchone():
                missing_fields.append('package_type')
        elif vendor == 'sqlite':
            cursor.execute("PRAGMA table_info(store_analysis_storeanalysis)")
            columns = {row[1] for row in cursor.fetchall()}
            if 'store_address' not in columns:
                missing_fields.append('store_address')
            if 'package_type' not in columns:
                missing_fields.append('package_type')
    
    if missing_fields:
        print(f"❌ فیلدهای missing: {', '.join(missing_fields)}")
        return False
    else:
        print("✅ تمام فیلدها موجود هستند")
        return True


def run_migration():
    """اجرای migration"""
    print("\n" + "="*60)
    print("🚀 اجرای Migration 0116")
    print("="*60)
    
    try:
        # اجرای migration
        call_command('migrate', 'store_analysis', '0116', verbosity=2)
        print("\n✅ Migration با موفقیت اجرا شد")
        return True
    except Exception as e:
        print(f"\n❌ خطا در اجرای migration: {e}")
        return False


def main():
    """اجرای اصلی"""
    print("\n" + "="*60)
    print("📦 Migration 0116 Runner for Liara")
    print("="*60)
    
    # بررسی وضعیت فعلی
    if check_migration_status():
        print("\n✅ Migration قبلاً اجرا شده است - نیازی به اجرای مجدد نیست")
        return 0
    
    # اجرای migration
    if run_migration():
        # بررسی مجدد
        if check_migration_status():
            print("\n✨ Migration با موفقیت انجام شد!")
            return 0
        else:
            print("\n⚠️ Migration اجرا شد اما فیلدها هنوز missing هستند")
            return 1
    else:
        print("\n❌ Migration ناموفق بود")
        return 1


if __name__ == '__main__':
    sys.exit(main())

