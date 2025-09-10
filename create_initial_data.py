#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ایجاد داده‌های اولیه برای سیستم پرداخت
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from store_analysis.models import PricingPlan, DiscountCode
from django.contrib.auth.models import User

def create_initial_data():
    print("🚀 ایجاد داده‌های اولیه سیستم پرداخت...")
    
    # ایجاد پلن‌های قیمت‌گذاری
    print("\n📋 ایجاد پلن‌های قیمت‌گذاری...")
    
    # پلن یکباره
    one_time_plan, created = PricingPlan.objects.get_or_create(
        plan_type='one_time',
        defaults={
            'name': 'تحلیل یکباره',
            'price': Decimal('500000'),
            'original_price': Decimal('500000'),
            'discount_percentage': 0,
            'features': [
                'تحلیل کامل فروشگاه',
                'گزارش تفصیلی 50 صفحه‌ای',
                'پیشنهادات بهینه‌سازی',
                'نقشه چیدمان جدید',
                'تحلیل رقبا',
                'پشتیبانی 7 روزه'
            ]
        }
    )
    if created:
        print("✅ پلن یکباره ایجاد شد")
    else:
        print("ℹ️ پلن یکباره از قبل موجود است")
    
    # پلن ماهیانه
    monthly_plan, created = PricingPlan.objects.get_or_create(
        plan_type='monthly',
        defaults={
            'name': 'پلن ماهیانه',
            'price': Decimal('1200000'),
            'original_price': Decimal('1500000'),
            'discount_percentage': 20,
            'features': [
                'همه ویژگی‌های پلن یکباره',
                'تحلیل ماهانه فروشگاه',
                'گزارش‌های دوره‌ای',
                'به‌روزرسانی نقشه چیدمان',
                'مشاوره تخصصی',
                'پشتیبانی 24/7',
                'دسترسی به ابزارهای پیشرفته'
            ]
        }
    )
    if created:
        print("✅ پلن ماهیانه ایجاد شد")
    else:
        print("ℹ️ پلن ماهیانه از قبل موجود است")
    
    # پلن سالیانه
    yearly_plan, created = PricingPlan.objects.get_or_create(
        plan_type='yearly',
        defaults={
            'name': 'پلن سالیانه',
            'price': Decimal('12000000'),
            'original_price': Decimal('20000000'),
            'discount_percentage': 40,
            'features': [
                'همه ویژگی‌های پلن ماهیانه',
                'تحلیل سالانه کامل',
                'گزارش‌های فصلی',
                'مشاوره اختصاصی',
                'دسترسی به API',
                'پشتیبانی VIP',
                'کارگاه‌های آموزشی رایگان',
                'گزارش ROI'
            ]
        }
    )
    if created:
        print("✅ پلن سالیانه ایجاد شد")
    else:
        print("ℹ️ پلن سالیانه از قبل موجود است")
    
    # ایجاد کدهای تخفیف نمونه
    print("\n🎁 ایجاد کدهای تخفیف نمونه...")
    
    # کد تخفیف 10%
    discount_10, created = DiscountCode.objects.get_or_create(
        code='WELCOME10',
        defaults={
            'discount_percentage': 10,
            'max_uses': 100,
            'valid_from': datetime.now(),
            'valid_until': datetime.now() + timedelta(days=30),
            'created_by': User.objects.first() or User.objects.create_user('admin', 'admin@example.com', 'admin123456')
        }
    )
    if created:
        print("✅ کد تخفیف WELCOME10 ایجاد شد")
    else:
        print("ℹ️ کد تخفیف WELCOME10 از قبل موجود است")
    
    # کد تخفیف 20%
    discount_20, created = DiscountCode.objects.get_or_create(
        code='SPECIAL20',
        defaults={
            'discount_percentage': 20,
            'max_uses': 50,
            'valid_from': datetime.now(),
            'valid_until': datetime.now() + timedelta(days=15),
            'created_by': User.objects.first()
        }
    )
    if created:
        print("✅ کد تخفیف SPECIAL20 ایجاد شد")
    else:
        print("ℹ️ کد تخفیف SPECIAL20 از قبل موجود است")
    
    print("\n" + "=" * 50)
    print("✅ تمام داده‌های اولیه با موفقیت ایجاد شدند!")
    print("\n📊 خلاصه:")
    print(f"   • پلن‌های قیمت‌گذاری: {PricingPlan.objects.count()}")
    print(f"   • کدهای تخفیف: {DiscountCode.objects.count()}")
    print("\n🎯 کدهای تخفیف موجود:")
    for discount in DiscountCode.objects.all():
        print(f"   • {discount.code}: {discount.discount_percentage}% تخفیف")

if __name__ == "__main__":
    create_initial_data()
