#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اسکریپت ایجاد یا به‌روزرسانی ادمین در Liara
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.contrib.auth.models import User

def create_or_update_admin():
    """ایجاد یا به‌روزرسانی ادمین"""
    
    print("\n" + "="*60)
    print("👤 مدیریت ادمین چیدمانو")
    print("="*60)
    
    # اطلاعات پیش‌فرض (می‌توانید تغییر دهید)
    username = os.getenv('ADMIN_USERNAME', 'admin')
    email = os.getenv('ADMIN_EMAIL', 'admin@chidmano.ir')
    password = os.getenv('ADMIN_PASSWORD', 'Chidmano2024!@#')
    
    # بررسی وجود کاربر
    try:
        user = User.objects.get(username=username)
        print(f"\n⚠️  کاربر '{username}' از قبل وجود دارد")
        print(f"📧 ایمیل: {user.email or 'ثبت نشده'}")
        print(f"🔑 Superuser: {user.is_superuser}")
        print(f"👔 Staff: {user.is_staff}")
        
        choice = input("\nآیا می‌خواهید رمز عبور را تغییر دهید؟ (y/n): ").lower()
        
        if choice == 'y':
            new_password = input("رمز عبور جدید را وارد کنید (یا Enter برای استفاده از رمز پیش‌فرض): ").strip()
            if not new_password:
                new_password = password
            
            user.set_password(new_password)
            user.is_superuser = True
            user.is_staff = True
            user.email = email if email else user.email
            user.save()
            
            print(f"\n✅ رمز ادمین '{username}' به‌روزرسانی شد")
            print(f"🔑 رمز جدید: {new_password}")
        else:
            print("\n✅ هیچ تغییری انجام نشد")
            
    except User.DoesNotExist:
        print(f"\n📝 ایجاد ادمین جدید '{username}'...")
        
        use_default = input(f"استفاده از رمز پیش‌فرض؟ (y/n): ").lower()
        
        if use_default != 'y':
            password = input("رمز عبور را وارد کنید: ").strip()
            if not password:
                print("❌ رمز عبور نمی‌تواند خالی باشد!")
                return False
        
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            print(f"\n✅ ادمین '{username}' با موفقیت ایجاد شد")
            print(f"📧 ایمیل: {email}")
            print(f"🔑 رمز عبور: {password}")
            
        except Exception as e:
            print(f"\n❌ خطا در ایجاد ادمین: {e}")
            return False
    
    # نمایش لیست ادمین‌ها
    print("\n" + "="*60)
    print("📋 لیست تمام ادمین‌ها:")
    print("="*60)
    
    admins = User.objects.filter(is_superuser=True)
    if admins:
        for admin in admins:
            print(f"\n👤 Username: {admin.username}")
            print(f"   📧 Email: {admin.email or 'ثبت نشده'}")
            print(f"   🔑 Superuser: {admin.is_superuser}")
            print(f"   👔 Staff: {admin.is_staff}")
            print(f"   🕐 Last Login: {admin.last_login or 'هرگز'}")
    else:
        print("\n⚠️  هیچ ادمینی پیدا نشد!")
    
    print("\n" + "="*60)
    return True

if __name__ == '__main__':
    try:
        success = create_or_update_admin()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  عملیات لغو شد")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

