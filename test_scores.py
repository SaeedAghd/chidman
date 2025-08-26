#!/usr/bin/env python
"""
تست سریع برای بررسی نمایش امتیازات
"""

import os
import sys
import django

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from store_analysis.models import StoreAnalysis, User

def test_scores():
    """تست نمایش امتیازات"""
    print("🔍 تست نمایش امتیازات...")
    print("=" * 50)
    
    # پیدا کردن آخرین تحلیل
    try:
        analysis = StoreAnalysis.objects.latest('created_at')
        print(f"✅ تحلیل یافت شد: {analysis.store_name}")
        print(f"📊 وضعیت: {analysis.get_status_display()}")
        print(f"🤖 نتایج AI: {'بله' if analysis.results else 'خیر'}")
        
        if analysis.results:
            print(f"📝 خلاصه اجرایی: {'موجود' if 'executive_summary' in analysis.results else 'ناموجود'}")
            print(f"🎯 امتیاز اطمینان: {analysis.results.get('confidence_score', 'نامشخص')}")
        
        # محاسبه امتیازات
        scores = {}
        if analysis.results and 'executive_summary' in analysis.results:
            # محاسبه امتیاز کلی بر اساس confidence_score
            confidence_score = analysis.results.get('confidence_score', 0.85)
            overall_score = int(confidence_score * 100)
            
            # محاسبه امتیازات جزئی بر اساس داده‌های تحلیل
            analysis_data = analysis.get_analysis_data()
            conversion_rate = analysis_data.get('conversion_rate', 35)
            customer_traffic = analysis_data.get('customer_traffic', 150)
            store_size = analysis_data.get('store_size', 500)
            unused_area_size = analysis_data.get('unused_area_size', 0)
            
            # امتیاز چیدمان (بر اساس فضای بلااستفاده و نرخ تبدیل)
            layout_score = max(60, 100 - (unused_area_size / store_size * 100) if store_size > 0 else 80)
            layout_score = min(95, layout_score + (conversion_rate - 30) * 0.5)
            
            # امتیاز ترافیک (بر اساس تعداد مشتریان)
            traffic_score = min(95, max(60, customer_traffic / 10))
            
            # امتیاز طراحی (بر اساس نرخ تبدیل و ترافیک)
            design_score = min(95, max(60, conversion_rate * 1.5 + traffic_score * 0.3))
            
            # امتیاز فروش (بر اساس نرخ تبدیل)
            sales_score = min(95, max(60, conversion_rate * 2))
            
            scores = {
                'overall_score': overall_score,
                'layout_score': int(layout_score),
                'traffic_score': int(traffic_score),
                'design_score': int(design_score),
                'sales_score': int(sales_score)
            }
        else:
            # امتیازات پیش‌فرض
            scores = {
                'overall_score': 75,
                'layout_score': 70,
                'traffic_score': 75,
                'design_score': 80,
                'sales_score': 72
            }
        
        print(f"\n📊 امتیازات محاسبه شده:")
        print(f"   🎯 امتیاز کلی: {scores['overall_score']}")
        print(f"   🏪 امتیاز چیدمان: {scores['layout_score']}")
        print(f"   🚶 امتیاز ترافیک: {scores['traffic_score']}")
        print(f"   🎨 امتیاز طراحی: {scores['design_score']}")
        print(f"   💰 امتیاز فروش: {scores['sales_score']}")
        
        print(f"\n🔗 لینک نتایج:")
        print(f"   http://127.0.0.1:8000/analyses/{analysis.id}/results/")
        
    except StoreAnalysis.DoesNotExist:
        print("❌ هیچ تحلیلی یافت نشد!")
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    test_scores()
