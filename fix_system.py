#!/usr/bin/env python
"""
اسکریپت جامع حل مشکلات سیستم
"""
import os
import sys
import django
import subprocess
import sqlite3
from pathlib import Path

def setup_django():
    """تنظیم Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
    django.setup()

def check_database():
    """بررسی وضعیت دیتابیس"""
    print("🔍 بررسی وضعیت دیتابیس...")
    
    db_path = Path('db.sqlite3')
    if not db_path.exists():
        print("❌ فایل دیتابیس وجود ندارد")
        return False
    
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # بررسی جداول اصلی
        tables = ['django_session', 'django_migrations', 'django_content_type', 'auth_user']
        
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                print(f"❌ جدول {table} وجود ندارد")
                conn.close()
                return False
            else:
                print(f"✅ جدول {table} موجود است")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطا در بررسی دیتابیس: {e}")
        return False

def fix_database():
    """حل مشکلات دیتابیس"""
    print("🔧 حل مشکلات دیتابیس...")
    
    try:
        # اجرای migration
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate', '--verbosity=2'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Migration ها اجرا شدند")
            return True
        else:
            print(f"❌ خطا در migration: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Migration timeout شد")
        return False
    except Exception as e:
        print(f"❌ خطا در اجرای migration: {e}")
        return False

def fix_static_files():
    """حل مشکلات static files"""
    print("🔧 حل مشکلات static files...")
    
    try:
        # اجرای collectstatic
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput', '--clear'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ collectstatic اجرا شد")
            return True
        else:
            print(f"❌ خطا در collectstatic: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ collectstatic timeout شد")
        return False
    except Exception as e:
        print(f"❌ خطا در اجرای collectstatic: {e}")
        return False

def test_system():
    """تست سیستم"""
    print("🧪 تست سیستم...")
    
    try:
        # تست Django
        result = subprocess.run([
            sys.executable, 'manage.py', 'check'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Django check موفق بود")
            return True
        else:
            print(f"❌ خطا در Django check: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ خطا در تست سیستم: {e}")
        return False

def main():
    """تابع اصلی"""
    print("🚀 شروع حل مشکلات سیستم...")
    print("=" * 50)
    
    # تنظیم Django
    setup_django()
    
    # بررسی دیتابیس
    db_ok = check_database()
    
    if not db_ok:
        print("🔧 تلاش برای حل مشکلات دیتابیس...")
        db_ok = fix_database()
    
    # حل مشکلات static files
    static_ok = fix_static_files()
    
    # تست سیستم
    test_ok = test_system()
    
    print("=" * 50)
    
    if db_ok and static_ok and test_ok:
        print("✅ تمام مشکلات حل شدند!")
        return True
    else:
        print("❌ برخی مشکلات حل نشدند")
        print(f"Database: {'✅' if db_ok else '❌'}")
        print(f"Static Files: {'✅' if static_ok else '❌'}")
        print(f"System Test: {'✅' if test_ok else '❌'}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)