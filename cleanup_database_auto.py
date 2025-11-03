#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اسکریپت پاک‌سازی دیتابیس - نسخه خودکار (بدون نیاز به تأیید)
- حذف تمام تحلیل‌ها (StoreAnalysis)
- حذف تمام کاربران غیر admin
- حذف سفارشات مرتبط
- حذف تیکت‌های مرتبط

⚠️ هشدار: این اسکریپت داده‌ها را به صورت دائمی حذف می‌کند!
"""

import os
import sys
import django

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from store_analysis.models import (
    StoreAnalysis, Order, SupportTicket, TicketMessage,
    Payment, UserProfile, AnalysisRequest
)
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

def cleanup_database(auto_confirm=False):
    """پاک‌سازی کامل دیتابیس"""
    
    print("=" * 60)
    print("⚠️  هشدار: این عملیات تمام تحلیل‌ها و کاربران غیر admin را حذف می‌کند!")
    print("=" * 60)
    
    # تأیید کاربر (اگر auto_confirm نباشد)
    if not auto_confirm:
        confirm = input("\nآیا مطمئن هستید؟ (بله/خیر): ").strip().lower()
        if confirm not in ['بله', 'yes', 'y', '1']:
            print("❌ عملیات لغو شد.")
            return
        
        confirm2 = input("دوباره تأیید کنید - تمام داده‌ها حذف می‌شوند! (بله/خیر): ").strip().lower()
        if confirm2 not in ['بله', 'yes', 'y', '1']:
            print("❌ عملیات لغو شد.")
            return
    else:
        print("\n✅ حالت خودکار - بدون نیاز به تأیید")
    
    with transaction.atomic():
        try:
            # شمارش داده‌ها قبل از حذف
            analyses_count = StoreAnalysis.objects.count()
            non_admin_users = User.objects.filter(is_staff=False, is_superuser=False).count()
            orders_count = Order.objects.count()
            tickets_count = SupportTicket.objects.count()
            
            print(f"\n📊 آمار قبل از حذف:")
            print(f"  - تعداد تحلیل‌ها: {analyses_count}")
            print(f"  - تعداد کاربران غیر admin: {non_admin_users}")
            print(f"  - تعداد سفارشات: {orders_count}")
            print(f"  - تعداد تیکت‌ها: {tickets_count}")
            
            # 1. حذف تمام تحلیل‌ها
            print("\n🗑️  حذف تحلیل‌ها...")
            deleted_analyses = StoreAnalysis.objects.all().delete()
            print(f"✅ {deleted_analyses[0]} تحلیل حذف شد.")
            
            # 2. حذف سفارشات
            print("\n🗑️  حذف سفارشات...")
            deleted_orders = Order.objects.all().delete()
            print(f"✅ {deleted_orders[0]} سفارش حذف شد.")
            
            # 3. حذف تیکت‌ها و پیام‌های مرتبط
            print("\n🗑️  حذف تیکت‌ها...")
            deleted_tickets = SupportTicket.objects.all().delete()
            print(f"✅ {deleted_tickets[0]} تیکت حذف شد.")
            
            # 4. حذف پیام‌های تیکت
            print("\n🗑️  حذف پیام‌های تیکت...")
            deleted_messages = TicketMessage.objects.all().delete()
            print(f"✅ {deleted_messages[0]} پیام حذف شد.")
            
            # 5. حذف پرداخت‌ها
            print("\n🗑️  حذف پرداخت‌ها...")
            deleted_payments = Payment.objects.all().delete()
            print(f"✅ {deleted_payments[0]} پرداخت حذف شد.")
            
            # 6. حذف AnalysisRequest ها
            print("\n🗑️  حذف درخواست‌های تحلیل...")
            try:
                deleted_requests = AnalysisRequest.objects.all().delete()
                print(f"✅ {deleted_requests[0]} درخواست حذف شد.")
            except Exception as e:
                print(f"⚠️  خطا در حذف AnalysisRequest (ممکن است مدل وجود نداشته باشد): {e}")
            
            # 7. حذف کاربران غیر admin
            print("\n🗑️  حذف کاربران غیر admin...")
            non_admin_users_query = User.objects.filter(is_staff=False, is_superuser=False)
            non_admin_count = non_admin_users_query.count()
            
            # حذف UserProfile های مرتبط
            for user in non_admin_users_query:
                try:
                    profile = UserProfile.objects.filter(user=user).first()
                    if profile:
                        profile.delete()
                except:
                    pass
            
            deleted_users = non_admin_users_query.delete()
            print(f"✅ {deleted_users[0]} کاربر غیر admin حذف شد.")
            
            # 8. نمایش کاربران باقی‌مانده
            print("\n👥 کاربران باقی‌مانده (admin ها):")
            admin_users = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
            for user in admin_users.distinct():
                print(f"  - {user.username} (staff: {user.is_staff}, superuser: {user.is_superuser})")
            
            print("\n" + "=" * 60)
            print("✅ پاک‌سازی با موفقیت انجام شد!")
            print("=" * 60)
            
        except Exception as e:
            logger.error(f"❌ خطا در پاک‌سازی: {e}", exc_info=True)
            print(f"\n❌ خطا در پاک‌سازی: {e}")
            raise

if __name__ == '__main__':
    import sys
    # اگر --auto یا --yes پاس داده شد، auto_confirm=True
    auto_confirm = '--auto' in sys.argv or '--yes' in sys.argv or '-y' in sys.argv
    cleanup_database(auto_confirm=auto_confirm)

