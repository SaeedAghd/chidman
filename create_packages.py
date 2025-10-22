#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from store_analysis.models import ServicePackage

# Create ServicePackage objects
packages = [
    {
        'name': 'پکیج پایه',
        'package_type': 'basic',
        'price': 0,
        'description': 'تحلیل اولیه رایگان فروشگاه',
        'features': ['تحلیل اولیه', 'گزارش ساده', 'توصیه‌های پایه']
    },
    {
        'name': 'پکیج حرفه‌ای',
        'package_type': 'professional',
        'price': 750000,
        'description': 'تحلیل کامل فروشگاه با 50% تخفیف',
        'features': ['تحلیل کامل', 'گزارش تفصیلی', 'توصیه‌های پیشرفته', 'پشتیبانی']
    },
    {
        'name': 'پکیج پیشرفته',
        'package_type': 'enterprise',
        'price': 1500000,
        'description': 'تحلیل پیشرفته فروشگاه با 50% تخفیف',
        'features': ['تحلیل پیشرفته', 'گزارش کامل', 'توصیه‌های تخصصی', 'پشتیبانی VIP']
    }
]

# Clear existing packages
ServicePackage.objects.all().delete()
print("✅ پکیج‌های قبلی حذف شدند")

# Create new packages
for pkg_data in packages:
    package, created = ServicePackage.objects.get_or_create(
        package_type=pkg_data['package_type'],
        defaults=pkg_data
    )
    if created:
        print(f"✅ پکیج {pkg_data['name']} ایجاد شد")
    else:
        print(f"⚠️ پکیج {pkg_data['name']} قبلاً وجود داشت")

print(f"\n📊 تعداد کل پکیج‌ها: {ServicePackage.objects.count()}")
print("🎉 تمام پکیج‌ها آماده شدند!")
