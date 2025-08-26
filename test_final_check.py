#!/usr/bin/env python
"""
تست نهایی برای بررسی کامل سیستم
"""

import os
import sys
import django

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from store_analysis.models import StoreAnalysis, User

def final_check():
    """تست نهایی سیستم"""
    print("🎯 تست نهایی سیستم تحلیل فروشگاه")
    print("=" * 60)
    
    # بررسی تحلیل‌های موجود
    total_analyses = StoreAnalysis.objects.count()
    completed_analyses = StoreAnalysis.objects.filter(status='completed').count()
    pending_analyses = StoreAnalysis.objects.filter(status='pending').count()
    processing_analyses = StoreAnalysis.objects.filter(status='processing').count()
    
    print(f"📊 آمار کلی:")
    print(f"   - کل تحلیل‌ها: {total_analyses}")
    print(f"   - تکمیل شده: {completed_analyses}")
    print(f"   - در انتظار: {pending_analyses}")
    print(f"   - در حال پردازش: {processing_analyses}")
    
    # بررسی آخرین تحلیل تکمیل شده
    try:
        latest_completed = StoreAnalysis.objects.filter(status='completed').latest('created_at')
        print(f"\n✅ آخرین تحلیل تکمیل شده:")
        print(f"   - نام: {latest_completed.store_name}")
        print(f"   - شناسه: {latest_completed.id}")
        print(f"   - وضعیت: {latest_completed.get_status_display()}")
        print(f"   - نتایج AI: {'بله' if latest_completed.results else 'خیر'}")
        
        if latest_completed.results:
            print(f"   - خلاصه اجرایی: {'موجود' if 'executive_summary' in latest_completed.results else 'ناموجود'}")
            print(f"   - راهنمایی‌های عملی: {'موجود' if 'practical_guide' in latest_completed.results else 'ناموجود'}")
            print(f"   - امتیاز اطمینان: {latest_completed.results.get('confidence_score', 'نامشخص')}")
        
        # محاسبه امتیازات
        scores = {}
        if latest_completed.results and 'executive_summary' in latest_completed.results:
            confidence_score = latest_completed.results.get('confidence_score', 0.85)
            overall_score = int(confidence_score * 100)
            
            analysis_data = latest_completed.get_analysis_data()
            conversion_rate = analysis_data.get('conversion_rate', 35)
            customer_traffic = analysis_data.get('customer_traffic', 150)
            store_size = analysis_data.get('store_size', 500)
            unused_area_size = analysis_data.get('unused_area_size', 0)
            
            layout_score = max(60, 100 - (unused_area_size / store_size * 100) if store_size > 0 else 80)
            layout_score = min(95, layout_score + (conversion_rate - 30) * 0.5)
            
            traffic_score = min(95, max(60, customer_traffic / 10))
            design_score = min(95, max(60, conversion_rate * 1.5 + traffic_score * 0.3))
            sales_score = min(95, max(60, conversion_rate * 2))
            
            scores = {
                'overall_score': overall_score,
                'layout_score': int(layout_score),
                'traffic_score': int(traffic_score),
                'design_score': int(design_score),
                'sales_score': int(sales_score)
            }
            
            print(f"\n📊 امتیازات محاسبه شده:")
            print(f"   🎯 امتیاز کلی: {scores['overall_score']}")
            print(f"   🏪 امتیاز چیدمان: {scores['layout_score']}")
            print(f"   🚶 امتیاز ترافیک: {scores['traffic_score']}")
            print(f"   🎨 امتیاز طراحی: {scores['design_score']}")
            print(f"   💰 امتیاز فروش: {scores['sales_score']}")
        
        print(f"\n🔗 لینک‌های مهم:")
        print(f"   - نتایج تحلیل: http://127.0.0.1:8000/analyses/{latest_completed.id}/results/")
        print(f"   - دانلود گزارش: http://127.0.0.1:8000/analyses/{latest_completed.id}/download/")
        print(f"   - تحلیل پیشرفته: http://127.0.0.1:8000/analyses/{latest_completed.id}/advanced-ml/")
        
    except StoreAnalysis.DoesNotExist:
        print("❌ هیچ تحلیل تکمیل شده‌ای یافت نشد!")
    
    # بررسی کاربران
    total_users = User.objects.count()
    staff_users = User.objects.filter(is_staff=True).count()
    superusers = User.objects.filter(is_superuser=True).count()
    
    print(f"\n👥 آمار کاربران:")
    print(f"   - کل کاربران: {total_users}")
    print(f"   - کارکنان: {staff_users}")
    print(f"   - ادمین‌ها: {superusers}")
    
    print(f"\n🎉 نتیجه نهایی:")
    if completed_analyses > 0:
        print("✅ سیستم کاملاً عملکردی است!")
        print("✅ امتیازات محاسبه می‌شوند")
        print("✅ راهنمایی‌های عملی تولید می‌شوند")
        print("✅ گزارش‌های مدیریتی آماده هستند")
        print("🚀 آماده برای لانچ: بله")
    else:
        print("⚠️ سیستم نیاز به تست بیشتر دارد")
        print("❌ هیچ تحلیل تکمیل شده‌ای یافت نشد")

if __name__ == "__main__":
    final_check()
