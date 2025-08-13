from store_analysis.ai_models.layout_analyzer import LayoutAnalyzer
import os
from django.conf import settings

def test_analysis():
    """تست تحلیل چیدمان فروشگاه"""
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
        if 'identified_objects' in analysis_result:
            print("\nاشیاء تشخیص داده شده:")
            for obj in analysis_result['identified_objects']:
                print(f"- {obj}")
        else:
            print("کلید 'identified_objects' در خروجی وجود ندارد.")
        
        if 'layout_score' in analysis_result:
            print(f"\nامتیاز چیدمان: {analysis_result['layout_score']}")
        else:
            print("کلید 'layout_score' وجود ندارد.")
        
        if 'empty_spaces' in analysis_result:
            print(f"\nفضاهای خالی: {len(analysis_result['empty_spaces'])}")
        else:
            print("کلید 'empty_spaces' وجود ندارد.")
        
        if 'suggestions' in analysis_result:
            print("\nپیشنهادات بهبود:")
            for suggestion in analysis_result['suggestions']:
                print(f"- {suggestion}")
        else:
            print("کلید 'suggestions' وجود ندارد.")
        
    except Exception as e:
        print(f"خطا در اجرای تست: {str(e)}")

if __name__ == "__main__":
    test_analysis() 