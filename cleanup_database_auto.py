#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اسکریپت پاک کردن دیتابیس (به جز ادمین‌ها)
این اسکریپت تمام تحلیل‌ها، کاربران غیرادمین، سفارشات و تیکت‌ها را پاک می‌کند
"""

import os
import sys
import django

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection
from store_analysis.models import (
    Order, Payment, SupportTicket, TicketMessage,
    UserProfile, FreeUsageTracking, ChatSession, ChatMessage
)

def cleanup_database():
    """پاک کردن دیتابیس به جز ادمین‌ها"""
    
    print("=" * 60)
    print("🧹 شروع پاک کردن دیتابیس...")
    print("=" * 60)
    
    # شمارش قبل از پاک کردن - استفاده از raw SQL برای جلوگیری از خطای فیلدهای missing
    from django.db import connection
    
    admin_count = User.objects.filter(is_superuser=True).count()
    total_users = User.objects.count()
    
    # شمارش با raw SQL برای جلوگیری از خطای فیلدهای missing
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM store_analysis_storeanalysis")
        total_analyses = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM store_analysis_order")
        total_orders = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM store_analysis_payment")
        total_payments = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM store_analysis_supportticket")
        total_tickets = cursor.fetchone()[0]
    
    print(f"\n📊 آمار قبل از پاک کردن:")
    print(f"   - کاربران ادمین: {admin_count}")
    print(f"   - کل کاربران: {total_users}")
    print(f"   - کل تحلیل‌ها: {total_analyses}")
    print(f"   - کل سفارشات: {total_orders}")
    print(f"   - کل پرداخت‌ها: {total_payments}")
    print(f"   - کل تیکت‌ها: {total_tickets}")
    
    # پاک کردن تحلیل‌ها - استفاده از raw SQL برای جلوگیری از خطای فیلدهای missing
    print("\n🗑️  در حال پاک کردن تحلیل‌ها...")
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM store_analysis_storeanalysis")
        count_before = cursor.fetchone()[0]
        cursor.execute("DELETE FROM store_analysis_storeanalysis")
        analyses_deleted = count_before
    print(f"   ✅ {analyses_deleted} تحلیل پاک شد")
    
    # پاک کردن سفارشات
    print("\n🗑️  در حال پاک کردن سفارشات...")
    orders_deleted = Order.objects.all().delete()[0]
    print(f"   ✅ {orders_deleted} سفارش پاک شد")
    
    # پاک کردن پرداخت‌ها
    print("\n🗑️  در حال پاک کردن پرداخت‌ها...")
    payments_deleted = Payment.objects.all().delete()[0]
    print(f"   ✅ {payments_deleted} پرداخت پاک شد")
    
    # پاک کردن تیکت‌ها
    print("\n🗑️  در حال پاک کردن تیکت‌ها...")
    tickets_deleted = SupportTicket.objects.all().delete()[0]
    print(f"   ✅ {tickets_deleted} تیکت پاک شد")
    
    # پاک کردن پیام‌های تیکت
    print("\n🗑️  در حال پاک کردن پیام‌های تیکت...")
    messages_deleted = TicketMessage.objects.all().delete()[0]
    print(f"   ✅ {messages_deleted} پیام تیکت پاک شد")
    
    # پاک کردن Chat Sessions
    print("\n🗑️  در حال پاک کردن Chat Sessions...")
    chat_sessions_deleted = ChatSession.objects.all().delete()[0]
    print(f"   ✅ {chat_sessions_deleted} Chat Session پاک شد")
    
    # پاک کردن Chat Messages
    print("\n🗑️  در حال پاک کردن Chat Messages...")
    chat_messages_deleted = ChatMessage.objects.all().delete()[0]
    print(f"   ✅ {chat_messages_deleted} Chat Message پاک شد")
    
    # پاک کردن Free Usage Tracking
    print("\n🗑️  در حال پاک کردن Free Usage Tracking...")
    free_usage_deleted = FreeUsageTracking.objects.all().delete()[0]
    print(f"   ✅ {free_usage_deleted} Free Usage Tracking پاک شد")
    
    # پاک کردن User Profiles (به جز ادمین‌ها)
    print("\n🗑️  در حال پاک کردن User Profiles...")
    admin_user_ids = User.objects.filter(is_superuser=True).values_list('id', flat=True)
    profiles_deleted = UserProfile.objects.exclude(user_id__in=admin_user_ids).delete()[0]
    print(f"   ✅ {profiles_deleted} User Profile پاک شد")
    
    # پاک کردن کاربران غیرادمین
    print("\n🗑️  در حال پاک کردن کاربران غیرادمین...")
    non_admin_users = User.objects.filter(is_superuser=False)
    non_admin_count = non_admin_users.count()
    non_admin_users.delete()
    print(f"   ✅ {non_admin_count} کاربر غیرادمین پاک شد")
    
    # شمارش بعد از پاک کردن
    admin_count_after = User.objects.filter(is_superuser=True).count()
    total_users_after = User.objects.count()
    
    print("\n" + "=" * 60)
    print("✅ پاک کردن دیتابیس با موفقیت انجام شد!")
    print("=" * 60)
    print(f"\n📊 آمار بعد از پاک کردن:")
    print(f"   - کاربران ادمین: {admin_count_after} (حفظ شده)")
    print(f"   - کل کاربران: {total_users_after}")
    print(f"   - تحلیل‌ها: 0")
    print(f"   - سفارشات: 0")
    print(f"   - پرداخت‌ها: 0")
    print(f"   - تیکت‌ها: 0")
    print("\n✨ دیتابیس پاک شد و فقط ادمین‌ها باقی ماندند!")

if __name__ == '__main__':
    try:
        cleanup_database()
    except Exception as e:
        print(f"\n❌ خطا در پاک کردن دیتابیس: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

