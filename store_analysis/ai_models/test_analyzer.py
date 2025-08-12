from store_analysis.ai_models.layout_analyzer import LayoutAnalyzer
import os
from django.conf import settings

def test_analysis():
    # ایجاد نمونه LayoutAnalyzer
    analyzer = LayoutAnalyzer()
    
    # مسیر تصویر نمونه
    sample_image_path = os.path.join(settings.MEDIA_ROOT, 'store_analysis', 'sample', 'layout.jpg')
    
    # اطمینان از وجود پوشه
    os.makedirs(os.path.dirname(sample_image_path), exist_ok=True)
    
    # تحلیل تصویر
    try:
        analysis_result = analyzer.analyze_layout(sample_image_path)
        print("\nخروجی خام تحلیل:")
        print(analysis_result)
        
        if not analysis_result:
            print("خطا در تحلیل تصویر یا خروجی None بود.")
            return
        
        # بررسی وجود کلیدها
        if 'detections' in analysis_result:
            print("\nاشیاء تشخیص داده شده:")
            for det in analysis_result['detections']:
                print(f"- {det['class']} (اطمینان: {det['confidence']:.2f})")
        else:
            print("کلید 'detections' در خروجی وجود ندارد.")
        
        if 'summary' in analysis_result and 'flow_score' in analysis_result['summary']:
            print("\nتحلیل جریان ترافیک:")
            print(f"- امتیاز جریان: {analysis_result['summary']['flow_score']}")
        else:
            print("کلید 'summary' یا 'flow_score' وجود ندارد.")
        
        if 'traffic_flow' in analysis_result and 'blind_spots' in analysis_result['traffic_flow']:
            print(f"- تعداد نقاط کور: {len(analysis_result['traffic_flow']['blind_spots'])}")
        else:
            print("کلید 'traffic_flow' یا 'blind_spots' وجود ندارد.")
        
        if 'shelf_analysis' in analysis_result:
            print("\nتحلیل چیدمان قفسه‌ها:")
            print(f"- تعداد قفسه‌ها: {analysis_result['shelf_analysis'].get('total_shelves', 'نامشخص')}")
            print(f"- فاصله متوسط: {analysis_result['shelf_analysis'].get('average_distance', 0):.2f}")
        else:
            print("کلید 'shelf_analysis' وجود ندارد.")
        
        if 'empty_space' in analysis_result:
            print("\nتحلیل فضای خالی:")
            print(f"- درصد استفاده از فضا: {analysis_result['empty_space'].get('utilization_percentage', 0):.2f}%")
        else:
            print("کلید 'empty_space' وجود ندارد.")
        
        if 'suggestions' in analysis_result:
            print("\nپیشنهادات بهبود:")
            for suggestion in analysis_result['suggestions']:
                print(f"- {suggestion['suggestion']} (اولویت: {suggestion['priority']})")
        else:
            print("کلید 'suggestions' وجود ندارد.")
        
    except Exception as e:
        print(f"خطا در اجرای تست: {str(e)}")

if __name__ == "__main__":
    test_analysis() 