#!/usr/bin/env python
"""
Setup script for testing the store analysis system
Creates a test user and 100% discount code for testing
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.contrib.auth.models import User
from store_analysis.models import DiscountCode, PricingPlan
from django.utils import timezone

def setup_test_environment():
    """Setup test environment with user and discount code"""
    
    print("🔧 Setting up test environment...")
    
    # Create test user if not exists
    username = "testuser"
    email = "test@example.com"
    password = "testpass123"
    
    try:
        user = User.objects.get(username=username)
        print(f"✅ Test user '{username}' already exists")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name="کاربر",
            last_name="تست"
        )
        print(f"✅ Created test user: {username} / {password}")
    
    # Create 100% discount code if not exists
    discount_code = "TEST100"
    try:
        existing_code = DiscountCode.objects.get(code=discount_code)
        print(f"✅ Discount code '{discount_code}' already exists")
    except DiscountCode.DoesNotExist:
        # Create admin user for discount code
        admin_username = "admin"
        try:
            admin_user = User.objects.get(username=admin_username)
        except User.DoesNotExist:
            admin_user = User.objects.create_superuser(
                username=admin_username,
                email="admin@example.com",
                password="admin123"
            )
            print(f"✅ Created admin user: {admin_username} / admin123")
        
        # Create 100% discount code
        DiscountCode.objects.create(
            code=discount_code,
            discount_percentage=100,
            max_uses=999,
            valid_from=timezone.now(),
            valid_until=timezone.now() + timedelta(days=30),
            created_by=admin_user
        )
        print(f"✅ Created 100% discount code: {discount_code}")
    
    # Ensure pricing plans exist
    plans_data = [
        {
            'name': 'تحلیل یکباره',
            'plan_type': 'one_time',
            'price': 500000,  # 500,000 تومان
            'original_price': 500000,
            'discount_percentage': 0,
            'features': ['تحلیل کامل', 'گزارش PDF', 'پشتیبانی 7 روزه']
        },
        {
            'name': 'اشتراک ماهانه',
            'plan_type': 'monthly',
            'price': 1500000,  # 1,500,000 تومان
            'original_price': 1500000,
            'discount_percentage': 0,
            'features': ['تحلیل ماهانه', 'گزارش PDF', 'پشتیبانی 30 روزه', 'بروزرسانی مداوم']
        },
        {
            'name': 'اشتراک سالانه',
            'plan_type': 'yearly',
            'price': 15000000,  # 15,000,000 تومان
            'original_price': 15000000,
            'discount_percentage': 0,
            'features': ['تحلیل سالانه', 'گزارش PDF', 'پشتیبانی 365 روزه', 'تخفیف 17%', 'بروزرسانی مداوم']
        }
    ]
    
    for plan_data in plans_data:
        plan, created = PricingPlan.objects.get_or_create(
            name=plan_data['name'],
            defaults=plan_data
        )
        if created:
            print(f"✅ Created pricing plan: {plan_data['name']}")
        else:
            print(f"✅ Pricing plan '{plan_data['name']}' already exists")
    
    print("\n🎯 Test Environment Setup Complete!")
    print("=" * 50)
    print(f"👤 Test User: {username} / {password}")
    print(f"🎫 100% Discount Code: {discount_code}")
    print(f"👨‍💼 Admin User: admin / admin123")
    print("=" * 50)
    print("\n🚀 Ready for user flow testing!")

if __name__ == "__main__":
    setup_test_environment()
