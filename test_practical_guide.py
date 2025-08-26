#!/usr/bin/env python
"""
تست کامل سیستم راهنمایی‌های عملی چیدمان
"""

import os
import sys
import django
from datetime import datetime

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from store_analysis.models import StoreAnalysis, User
from store_analysis.ai_analysis import StoreAnalysisAI

def test_practical_guide():
    """تست راهنمایی‌های عملی"""
    print("🔍 شروع تست راهنمایی‌های عملی چیدمان...")
    print("=" * 60)
    
    # ایجاد کاربر تست
    try:
        user = User.objects.create_user(
            username='test_user_practical',
            email='test_practical@example.com',
            password='testpass123'
        )
        print(f"✅ کاربر تست ایجاد شد: {user.username}")
    except:
        user = User.objects.get(username='test_user_practical')
        print(f"✅ کاربر تست موجود: {user.username}")
    
    # داده‌های تست واقعی‌تر
    test_data = {
        'store_name': 'فروشگاه مواد غذایی تازه',
        'store_type': 'grocery',
        'store_size': 350,  # متر مربع
        'entrance_count': 2,
        'checkout_count': 4,
        'shelf_count': 30,
        'conversion_rate': 38.5,
        'customer_traffic': 280,
        'customer_dwell_time': 35,
        'unused_area_size': 45,  # متر مربع فضای بلااستفاده
        'daily_sales_volume': 2500000,  # تومان
        'morning_sales_percent': 25,
        'noon_sales_percent': 45,
        'evening_sales_percent': 30,
        'product_categories': ['مواد غذایی', 'نوشیدنی', 'لبنیات', 'خشکبار', 'تنقلات'],
        'has_surveillance': True,
        'camera_count': 6,
        'main_lighting': 'LED',
        'lighting_intensity': '500 لوکس',
        'design_style': 'مدرن',
        'brand_colors': 'سبز و سفید',
        'store_location': 'تهران، منطقه 3',
        'city': 'تهران',
        'area': 'منطقه 3',
        'establishment_year': '2020',
        'shelf_dimensions': '2.1×0.6×0.4 متر',
        'shelf_contents': 'مواد غذایی و نوشیدنی',
        'unused_area_type': 'انبار قدیمی',
        'peak_hours': '10-14 و 17-21',
        'high_traffic_areas': 'ورودی، صندوق، بخش لبنیات',
        'top_products': 'شیر، نان، میوه، سبزیجات',
        'supplier_count': 15,
        'pos_system': 'نرم‌افزار صندوق پیشرفته',
        'inventory_system': 'سیستم موجودی هوشمند',
        'video_date': '2024-01-15',
        'video_duration': 300,
        'sales_improvement_target': 25,
        'optimization_timeline': 8,
        'historical_data_months': 18,
        'peak_days': ['جمعه', 'شنبه', 'یکشنبه']
    }
    
    # ایجاد تحلیل با فیلدهای صحیح
    analysis = StoreAnalysis.objects.create(
        user=user,
        store_name=test_data['store_name'],
        store_type=test_data['store_type'],
        store_size=str(test_data['store_size']),
        analysis_data=test_data
    )
    
    print(f"✅ تحلیل ایجاد شد: {analysis.store_name}")
    print(f"📊 اندازه فروشگاه: {analysis.store_size} متر مربع")
    print(f"👥 ترافیک روزانه: {test_data['customer_traffic']} مشتری")
    print(f"💰 نرخ تبدیل: {test_data['conversion_rate']}%")
    print(f"📦 فضای بلااستفاده: {test_data['unused_area_size']} متر مربع")
    
    # تست AI
    ai_analyzer = StoreAnalysisAI()
    
    print("\n🤖 شروع تحلیل AI...")
    analysis_result = ai_analyzer.generate_detailed_analysis(test_data)
    
    if 'error' in analysis_result:
        print(f"❌ خطا در تحلیل: {analysis_result['error']}")
        return
    
    print("✅ تحلیل AI تکمیل شد!")
    
    # نمایش راهنمایی‌های عملی
    print("\n" + "=" * 60)
    print("🎯 راهنمایی‌های عملی چیدمان")
    print("=" * 60)
    
    # بررسی وجود راهنمایی‌های عملی
    if 'practical_guide' in analysis_result:
        practical_guide = analysis_result['practical_guide']
        print("✅ راهنمایی‌های عملی تولید شد!")
        
        # ویترین
        if 'window_display' in practical_guide:
            window = practical_guide['window_display']
            print(f"\n🏪 راهنمای ویترین:")
            print(f"   ارتفاع: {window.get('height', 'نامشخص')}")
            print(f"   نورپردازی: {window.get('lighting', 'نامشخص')}")
            print(f"   قانون رنگی: {window.get('color_rule', 'نامشخص')}")
            print(f"   تعداد محصولات: {window.get('product_count', 'نامشخص')}")
            print(f"   تغییر محتوا: {window.get('rotation_frequency', 'نامشخص')}")
            print(f"   نکات: {', '.join(window.get('tips', []))}")
        
        # چیدمان قفسه‌ها
        if 'shelf_layout' in practical_guide:
            shelf = practical_guide['shelf_layout']
            print(f"\n📦 راهنمای چیدمان قفسه‌ها:")
            heights = shelf.get('shelf_heights', {})
            print(f"   ارتفاع قفسه پایین: {heights.get('bottom', 'نامشخص')}")
            print(f"   ارتفاع قفسه میانی: {heights.get('middle', 'نامشخص')}")
            print(f"   ارتفاع قفسه بالا: {heights.get('top', 'نامشخص')}")
            print(f"   عرض راهرو: {shelf.get('aisle_width', 'نامشخص')}")
            print(f"   ترتیب محصولات: {shelf.get('product_arrangement', 'نامشخص')}")
            print(f"   فاصله محصولات: {shelf.get('spacing', 'نامشخص')}")
            print(f"   نکات: {', '.join(shelf.get('tips', []))}")
        
        # طراحی مسیر
        if 'path_design' in practical_guide:
            path = practical_guide['path_design']
            print(f"\n🛤️ راهنمای طراحی مسیر:")
            main_path = path.get('main_path', {})
            print(f"   مسیر اصلی - عرض: {main_path.get('width', 'نامشخص')}")
            print(f"   مسیر اصلی - جهت: {main_path.get('direction', 'نامشخص')}")
            print(f"   مسیر اصلی - محصولات: {main_path.get('products', 'نامشخص')}")
            
            secondary = path.get('secondary_paths', {})
            print(f"   مسیر فرعی - عرض: {secondary.get('width', 'نامشخص')}")
            print(f"   مسیر فرعی - هدف: {secondary.get('purpose', 'نامشخص')}")
            
            stopping = path.get('stopping_points', {})
            print(f"   نقاط توقف - اندازه: {stopping.get('size', 'نامشخص')}")
            print(f"   نقاط توقف - هدف: {stopping.get('purpose', 'نامشخص')}")
            print(f"   نکات: {', '.join(path.get('tips', []))}")
        
        # نورپردازی
        if 'lighting' in practical_guide:
            lighting = practical_guide['lighting']
            print(f"\n💡 راهنمای نورپردازی:")
            general = lighting.get('general_lighting', {})
            print(f"   نور عمومی - شدت: {general.get('intensity', 'نامشخص')}")
            print(f"   نور عمومی - دمای رنگ: {general.get('color_temperature', 'نامشخص')}")
            print(f"   نور عمومی - نوع: {general.get('type', 'نامشخص')}")
            
            accent = lighting.get('accent_lighting', {})
            print(f"   نور تأکیدی - هدف: {accent.get('purpose', 'نامشخص')}")
            print(f"   نور تأکیدی - شدت: {accent.get('intensity', 'نامشخص')}")
            print(f"   نور تأکیدی - دمای رنگ: {accent.get('color_temperature', 'نامشخص')}")
            print(f"   نکات: {', '.join(lighting.get('tips', []))}")
        
        # ترکیب رنگی
        if 'color_scheme' in practical_guide:
            color = practical_guide['color_scheme']
            print(f"\n🎨 راهنمای ترکیب رنگی:")
            print(f"   طرح رنگی: {color.get('scheme', 'نامشخص')}")
            print(f"   رنگ‌های اصلی: {', '.join(color.get('primary_colors', []))}")
            print(f"   قانون رنگی: {color.get('rule', 'نامشخص')}")
            usage = color.get('usage', {})
            print(f"   استفاده 60%: {usage.get('60%', 'نامشخص')}")
            print(f"   استفاده 30%: {usage.get('30%', 'نامشخص')}")
            print(f"   استفاده 10%: {usage.get('10%', 'نامشخص')}")
        
        # قرارگیری محصولات
        if 'product_placement' in practical_guide:
            placement = practical_guide['product_placement']
            print(f"\n📦 راهنمای قرارگیری محصولات:")
            print(f"   مناطق پرتردد: {', '.join(placement.get('high_traffic_areas', []))}")
            
            arrangement = placement.get('product_arrangement', {})
            print(f"   سطح چشم: {arrangement.get('eye_level', 'نامشخص')}")
            print(f"   قفسه بالا: {arrangement.get('top_shelf', 'نامشخص')}")
            print(f"   قفسه پایین: {arrangement.get('bottom_shelf', 'نامشخص')}")
            
            cross = placement.get('cross_selling', {})
            print(f"   فروش متقابل - استراتژی: {cross.get('strategy', 'نامشخص')}")
            print(f"   فروش متقابل - مثال‌ها: {', '.join(cross.get('examples', []))}")
            
            seasonal = placement.get('seasonal_placement', {})
            print(f"   قرارگیری فصلی - جلو: {seasonal.get('front', 'نامشخص')}")
            print(f"   قرارگیری فصلی - عقب: {seasonal.get('back', 'نامشخص')}")
    
    else:
        print("❌ راهنمایی‌های عملی در نتیجه یافت نشد!")
    
    # نمایش تحلیل کلی
    print("\n" + "=" * 60)
    print("📋 خلاصه تحلیل")
    print("=" * 60)
    
    if 'executive_summary' in analysis_result:
        print(f"📝 خلاصه اجرایی:")
        print(f"   {analysis_result['executive_summary']}")
    
    if 'detailed_analysis' in analysis_result:
        detailed = analysis_result['detailed_analysis']
        print(f"\n✅ نقاط قوت ({len(detailed.get('strengths', []))} مورد):")
        for i, strength in enumerate(detailed.get('strengths', [])[:3], 1):
            print(f"   {i}. {strength}")
        
        print(f"\n❌ نقاط ضعف ({len(detailed.get('weaknesses', []))} مورد):")
        for i, weakness in enumerate(detailed.get('weaknesses', [])[:3], 1):
            print(f"   {i}. {weakness}")
    
    if 'recommendations' in analysis_result:
        recs = analysis_result['recommendations']
        print(f"\n🎯 پیشنهادات فوری ({len(recs.get('immediate', []))} مورد):")
        for i, rec in enumerate(recs.get('immediate', [])[:3], 1):
            print(f"   {i}. {rec}")
    
    if 'financial_projections' in analysis_result:
        financial = analysis_result['financial_projections']
        print(f"\n💰 پیش‌بینی مالی:")
        print(f"   فروش روزانه فعلی: {financial.get('current_daily_sales', 'نامشخص')}")
        print(f"   فروش روزانه جدید: {financial.get('new_daily_sales', 'نامشخص')}")
        print(f"   درصد افزایش فروش: {financial.get('sales_increase_percentage', 'نامشخص')}")
        print(f"   ROI: {financial.get('roi_percentage', 'نامشخص')}")
        print(f"   بازگشت سرمایه: {financial.get('payback_period_months', 'نامشخص')}")
    
    # ذخیره نتیجه
    analysis.results = analysis_result
    analysis.status = 'completed'
    analysis.save()
    
    print(f"\n✅ تحلیل در دیتابیس ذخیره شد!")
    print(f"🆔 شناسه تحلیل: {analysis.id}")
    
    return analysis

if __name__ == "__main__":
    test_practical_guide()
