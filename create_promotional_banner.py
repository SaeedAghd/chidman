#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from store_analysis.models import PromotionalBanner
from django.utils import timezone

def create_sample_banner():
    """ایجاد تبلیغ نمونه"""
    
    # حذف تبلیغات قبلی
    PromotionalBanner.objects.all().delete()
    
    # ایجاد تبلیغ جدید
    banner = PromotionalBanner.objects.create(
        title="🎉 تخفیف ویژه شروع سال جدید!",
        subtitle="با استفاده از کد تخفیف WELCOME10، 10% تخفیف از تمام پلن‌ها دریافت کنید",
        discount_percentage=10,
        discount_text="تخفیف ویژه",
        background_color="#FF6B6B",
        text_color="#FFFFFF",
        is_active=True,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=30)
    )
    
    print(f"✅ تبلیغ نمونه ایجاد شد:")
    print(f"   عنوان: {banner.title}")
    print(f"   درصد تخفیف: {banner.discount_percentage}%")
    print(f"   تاریخ شروع: {banner.start_date}")
    print(f"   تاریخ پایان: {banner.end_date}")
    print(f"   فعال: {banner.is_active}")

if __name__ == "__main__":
    create_sample_banner()
