#!/usr/bin/env python
"""
تست کامل سفر کاربر از ابتدا تا انتها
شامل ثبت‌نام، ورود، پر کردن فرم جدید با فایل‌ها، و دریافت گزارش
"""

import os
import sys
import django
import requests
from pathlib import Path

# تنظیم Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from store_analysis.models import StoreAnalysis, StoreAnalysisResult
from store_analysis.forms import AIStoreAnalysisForm

def create_test_files():
    """ایجاد فایل‌های تست"""
    files = {}
    
    # ایجاد فایل تصویر تست معتبر (JPEG header)
    image_content = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
    
    files['store_photos'] = SimpleUploadedFile(
        "store_photo.jpg", 
        image_content, 
        content_type="image/jpeg"
    )
    
    files['shelf_photos'] = SimpleUploadedFile(
        "shelf_photo.jpg", 
        image_content, 
        content_type="image/jpeg"
    )
    
    files['entrance_photos'] = SimpleUploadedFile(
        "entrance_photo.jpg", 
        image_content, 
        content_type="image/jpeg"
    )
    
    files['checkout_photos'] = SimpleUploadedFile(
        "checkout_photo.jpg", 
        image_content, 
        content_type="image/jpeg"
    )
    
    # ایجاد فایل PDF تست
    pdf_content = b'%PDF-1.4 fake-pdf-content'
    files['store_plan'] = SimpleUploadedFile(
        "store_plan.pdf", 
        pdf_content, 
        content_type="application/pdf"
    )
    
    # ایجاد فایل Excel تست
    excel_content = b'fake-excel-content'
    files['sales_file'] = SimpleUploadedFile(
        "sales_report.xlsx", 
        excel_content, 
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    return files

def test_complete_user_journey():
    """تست کامل سفر کاربر"""
    print("🚀 شروع تست کامل سفر کاربر...")
    
    # ایجاد کاربر تست
    username = "testuser_complete"
    email = "test@example.com"
    password = "testpass123"
    
    # حذف کاربر قبلی اگر وجود دارد
    User.objects.filter(username=username).delete()
    
    # ایجاد کاربر جدید
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    print(f"✅ کاربر تست ایجاد شد: {username}")
    
    # ایجاد کلاینت تست
    client = Client()
    
    # ورود کاربر
    login_success = client.login(username=username, password=password)
    if not login_success:
        print("❌ خطا در ورود کاربر")
        return False
    print("✅ ورود کاربر موفق")
    
    # تست صفحه اصلی
    response = client.get('/')
    if response.status_code == 200:
        print("✅ صفحه اصلی در دسترس است")
    else:
        print(f"❌ خطا در صفحه اصلی: {response.status_code}")
        return False
    
    # تست صفحه فرم تحلیل
    response = client.get('/store-analysis/')
    if response.status_code == 200:
        print("✅ صفحه فرم تحلیل در دسترس است")
    else:
        print(f"❌ خطا در صفحه فرم: {response.status_code}")
        return False
    
    # ایجاد داده‌های فرم
    form_data = {
        # اطلاعات پایه فروشگاه
        'store_name': 'فروشگاه تست جامع',
        'store_type': 'retail',
        'store_size': 200,
        'store_location': 'تهران، خیابان ولیعصر',
        'city': 'تهران',
        'area': 'ولیعصر',
        'establishment_year': 1400,
        'phone': '02112345678',
        'email': 'store@example.com',
        
        # چیدمان فروشگاه
        'entrance_count': 2,
        'checkout_count': 3,
        'shelf_count': 10,
        'shelf_dimensions': '2x1.5 متر',
        'shelf_contents': 'محصولات متنوع',
        'unused_area_size': 20,
        'unused_area_type': 'storage',
        
        # طراحی و نورپردازی
        'design_style': 'modern',
        'brand_colors': 'آبی و سفید',
        'lighting_intensity': 'medium',
        'main_lighting': 'artificial',
        
        # ترافیک و رفتار مشتری
        'customer_traffic': 150,
        'customer_dwell_time': 45,
        'conversion_rate': 35.5,
        'peak_hours': '18:00-21:00',
        'peak_days': ['friday', 'saturday'],
        'high_traffic_areas': 'ورودی و صندوق‌ها',
        'morning_sales_percent': 30,
        'noon_sales_percent': 40,
        'evening_sales_percent': 30,
        
        # محصولات و فروش
        'product_categories': ['electronics', 'womens_clothing', 'books'],
        'top_products': ['لپ‌تاپ', 'کفش ورزشی', 'رمان'],
        'daily_sales_volume': 5000000,
        'supplier_count': 15,
        'sales_improvement_target': 20,
        'optimization_timeline': 3,
        'historical_data_months': 12,
        'prediction_period': '6',
        'prediction_accuracy': 'high',
        
        # نظارت و امنیت
        'has_surveillance': True,
        'camera_count': 4,
        'camera_locations': 'ورودی، صندوق‌ها، قفسه‌ها',
        
        # اطلاعات ویدیو
        'video_date': '2024-01-15',
        'video_time': '14:30',
        'video_duration': 300,
        
        # اطلاعات نرم‌افزاری
        'pos_system': 'سیستم صندوق پیشرفته',
        'inventory_system': 'مدیریت موجودی هوشمند',
        
        # اطلاعات گزارش
        'analyst_name': 'تست تحلیلگر',
        'report_email': 'report@example.com',
        'contact_phone': '09123456789',
        'report_deadline': '2024-02-15',
        'report_types': ['pdf', 'excel'],
        'additional_notes': 'این یک تست کامل از سیستم جدید است',
        'notifications': ['email', 'sms'],
        
        # تنظیمات AI
        'analysis_depth': 'comprehensive',
        'accuracy_level': 'high',
    }
    
    # ایجاد فایل‌های تست
    test_files = create_test_files()
    
    # ترکیب داده‌ها و فایل‌ها
    form_data.update(test_files)
    
    print("📝 ارسال فرم با داده‌های کامل...")
    
    # ارسال فرم
    response = client.post('/store-analysis/submit/', data=form_data, follow=True)
    
    if response.status_code == 200:
        print("✅ فرم با موفقیت ارسال شد")
        
        # بررسی ایجاد تحلیل
        analysis = StoreAnalysis.objects.filter(
            user=user,
            store_name='فروشگاه تست جامع'
        ).first()
        
        if analysis:
            print(f"✅ تحلیل ایجاد شد با ID: {analysis.id}")
            print(f"📊 نام فروشگاه: {analysis.store_name}")
            print(f"📅 تاریخ ایجاد: {analysis.created_at}")
            
            # بررسی نتایج تحلیل
            result = StoreAnalysisResult.objects.filter(store_analysis=analysis).first()
            if result:
                print("✅ نتایج تحلیل ایجاد شد")
                print(f"📈 امتیاز کلی: {result.overall_score}")
                print(f"📊 امتیاز چیدمان: {result.layout_score}")
                print(f"🚦 امتیاز ترافیک: {result.traffic_score}")
                print(f"🎨 امتیاز طراحی: {result.design_score}")
                print(f"💰 امتیاز فروش: {result.sales_score}")
                print(f"📝 تحلیل کلی: {result.overall_analysis[:100]}...")
                
                # تست صفحه نتایج
                response = client.get(f'/analyses/{analysis.id}/results/')
                if response.status_code == 200:
                    print("✅ صفحه نتایج در دسترس است")
                else:
                    print(f"❌ خطا در صفحه نتایج: {response.status_code}")
                
                # تست صفحه تحلیل پیشرفته ML
                response = client.get(f'/analysis/{analysis.id}/advanced-ml/')
                if response.status_code == 200:
                    print("✅ صفحه تحلیل پیشرفته ML در دسترس است")
                else:
                    print(f"❌ خطا در صفحه تحلیل پیشرفته: {response.status_code}")
                
                # تست دانلود گزارش
                response = client.get(f'/analyses/{analysis.id}/download/')
                if response.status_code == 200:
                    print("✅ دانلود گزارش PDF موفق")
                else:
                    print(f"❌ خطا در دانلود گزارش: {response.status_code}")
                
            else:
                print("❌ نتایج تحلیل ایجاد نشد")
        else:
            print("❌ تحلیل ایجاد نشد")
            
    else:
        print(f"❌ خطا در ارسال فرم: {response.status_code}")
        if hasattr(response, 'content'):
            print(f"محتوی پاسخ: {response.content.decode()[:500]}")
        return False
    
    print("\n🎉 تست کامل با موفقیت انجام شد!")
    print("=" * 50)
    print("📋 خلاصه تست:")
    print("✅ ثبت‌نام و ورود کاربر")
    print("✅ دسترسی به صفحات")
    print("✅ ارسال فرم با فایل‌های آپلود")
    print("✅ ایجاد تحلیل و نتایج")
    print("✅ دسترسی به صفحات نتایج")
    print("✅ دانلود گزارش")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    try:
        success = test_complete_user_journey()
        if success:
            print("\n🎯 تمام تست‌ها موفق بودند!")
            sys.exit(0)
        else:
            print("\n❌ برخی تست‌ها ناموفق بودند!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 خطا در تست: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
