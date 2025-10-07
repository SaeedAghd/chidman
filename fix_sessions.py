#!/usr/bin/env python
"""
اسکریپت حل مشکل django_session table
"""
import os
import sys
import django

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def fix_sessions_table():
    """حل مشکل جدول django_session"""
    print("🔧 در حال حل مشکل django_session table...")
    
    try:
        # بررسی وجود جدول
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='django_session'
            """)
            result = cursor.fetchone()
            
            if result:
                print("✅ جدول django_session موجود است")
                return True
            else:
                print("❌ جدول django_session موجود نیست")
                
                # ایجاد جدول django_session
                cursor.execute("""
                    CREATE TABLE django_session (
                        session_key varchar(40) NOT NULL PRIMARY KEY,
                        session_data text NOT NULL,
                        expire_date datetime NOT NULL
                    )
                """)
                
                # ایجاد ایندکس
                cursor.execute("""
                    CREATE INDEX django_session_expire_date 
                    ON django_session (expire_date)
                """)
                
                print("✅ جدول django_session ایجاد شد")
                return True
                
    except Exception as e:
        print(f"❌ خطا در ایجاد جدول: {e}")
        return False

def fix_static_files():
    """حل مشکل static files"""
    print("🔧 در حال حل مشکل static files...")
    
    try:
        # اجرای collectstatic
        call_command('collectstatic', '--noinput', '--clear')
        print("✅ collectstatic اجرا شد")
        return True
    except Exception as e:
        print(f"❌ خطا در collectstatic: {e}")
        return False

def main():
    """تابع اصلی"""
    print("🚀 شروع حل مشکلات سیستم...")
    
    # حل مشکل sessions
    sessions_ok = fix_sessions_table()
    
    # حل مشکل static files
    static_ok = fix_static_files()
    
    if sessions_ok and static_ok:
        print("✅ تمام مشکلات حل شدند!")
        return True
    else:
        print("❌ برخی مشکلات حل نشدند")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)