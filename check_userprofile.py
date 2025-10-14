#!/usr/bin/env python
"""
بررسی جدول UserProfile و ستون‌های آن
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.db import connection
from store_analysis.models import UserProfile

def check_userprofile_table():
    """بررسی جدول UserProfile"""
    try:
        cursor = connection.cursor()
        
        # بررسی وجود جدول (برای SQLite)
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='store_analysis_userprofile'
        """)
        
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ جدول UserProfile وجود دارد")
            
            # بررسی ستون‌ها (SQLite)
            cursor.execute("PRAGMA table_info(store_analysis_userprofile)")
            
            columns = cursor.fetchall()
            print("\n📋 ستون‌های جدول:")
            print("-" * 80)
            print(f"{'نام ستون':<30} {'نوع':<20} {'Nullable':<10} {'Default':<15}")
            print("-" * 80)
            
            has_phone = False
            for col in columns:
                # SQLite PRAGMA returns: (cid, name, type, notnull, default_value, pk)
                cid, col_name, data_type, notnull, default_val, pk = col
                nullable = "NO" if notnull else "YES"
                default_str = str(default_val) if default_val else '-'
                print(f"{col_name:<30} {data_type:<20} {nullable:<10} {default_str:<15}")
                
                if col_name == 'phone':
                    has_phone = True
            
            # بررسی تعداد رکوردها
            cursor.execute("SELECT COUNT(*) FROM store_analysis_userprofile")
            count = cursor.fetchone()[0]
            print(f"\n📊 تعداد رکوردها: {count}")
            
            # بررسی ستون phone
            if has_phone:
                print("✅ ستون 'phone' وجود دارد")
            else:
                print("❌ ستون 'phone' وجود ندارد!")
                
        else:
            print("❌ جدول UserProfile وجود ندارد!")
            print("\n🔧 لطفاً Migration ها را اجرا کنید:")
            print("   python manage.py makemigrations")
            print("   python manage.py migrate")
            
    except Exception as e:
        print(f"❌ خطا در بررسی: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cursor.close()

if __name__ == '__main__':
    check_userprofile_table()

