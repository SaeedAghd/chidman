import openai
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from store_analysis.models import StoreAnalysis, StoreAnalysisResult
import logging

logger = logging.getLogger(__name__)

class StoreAnalysisService:
    """سرویس تحلیل فروشگاه"""
    
    def __init__(self):
        self.openai_api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def analyze_store(self, store_analysis):
        """تحلیل فروشگاه"""
        try:
            # تحلیل بخش‌های مختلف
            layout_analysis = self.analyze_layout(store_analysis)
            traffic_analysis = self.analyze_traffic(store_analysis)
            design_analysis = self.analyze_design(store_analysis)
            sales_analysis = self.analyze_sales(store_analysis)
            
            # استخراج امتیازها
            layout_score = self.extract_score(layout_analysis)
            traffic_score = self.extract_score(traffic_analysis)
            design_score = self.extract_score(design_analysis)
            sales_score = self.extract_score(sales_analysis)
            
            # تولید تحلیل کلی
            overall_analysis = self.generate_overall_analysis(
                store_analysis,
                layout_analysis,
                traffic_analysis,
                design_analysis,
                sales_analysis
            )
            
            # محاسبه امتیاز کلی
            overall_score = (layout_score + traffic_score + design_score + sales_score) / 4
            
            # ذخیره نتایج
            try:
                result = StoreAnalysisResult.objects.create(
                    store_analysis=store_analysis,
                    overall_score=overall_score,
                    layout_score=layout_score,
                    traffic_score=traffic_score,
                    design_score=design_score,
                    sales_score=sales_score,
                    layout_analysis=layout_analysis,
                    traffic_analysis=traffic_analysis,
                    design_analysis=design_analysis,
                    sales_analysis=sales_analysis,
                    overall_analysis=overall_analysis
                )
                
                # به‌روزرسانی وضعیت تحلیل
                store_analysis.status = 'completed'
                store_analysis.save()
                
                logger.info(f"Analysis completed successfully for {store_analysis.id}")
                return result
                
            except DatabaseError as e:
                logger.error(f"Database error in analyze_store: {str(e)}")
                store_analysis.status = 'failed'
                store_analysis.error_message = f'خطا در ذخیره‌سازی: {str(e)}'
                store_analysis.save()
                raise ValidationError('خطا در ذخیره‌سازی نتایج تحلیل')
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in analyze_store: {str(e)}")
            store_analysis.status = 'failed'
            store_analysis.error_message = f'خطای غیرمنتظره: {str(e)}'
            store_analysis.save()
            raise ValidationError('خطای غیرمنتظره در تحلیل')
    
    def analyze_layout(self, store_analysis):
        """تحلیل چیدمان فروشگاه"""
        prompt = f"""
        تحلیل چیدمان فروشگاه {store_analysis.store_name}:
        - نوع فروشگاه: {store_analysis.get_store_type_display()}
        - متراژ: {store_analysis.store_size} متر مربع
        - ابعاد: {store_analysis.store_dimensions}
        - موقعیت: {store_analysis.store_location}
        
        لطفاً تحلیل جامعی از چیدمان این فروشگاه ارائه دهید و امتیاز 1-10 بدهید.
        """
        
        return self._call_openai(prompt)
    
    def analyze_traffic(self, store_analysis):
        """تحلیل ترافیک فروشگاه"""
        prompt = f"""
        تحلیل ترافیک فروشگاه {store_analysis.store_name}:
        - موقعیت: {store_analysis.store_location}
        - شهر: {store_analysis.city}
        - منطقه: {store_analysis.area}
        
        لطفاً تحلیل جامعی از ترافیک این فروشگاه ارائه دهید و امتیاز 1-10 بدهید.
        """
        
        return self._call_openai(prompt)
    
    def analyze_design(self, store_analysis):
        """تحلیل طراحی فروشگاه"""
        prompt = f"""
        تحلیل طراحی فروشگاه {store_analysis.store_name}:
        - نوع فروشگاه: {store_analysis.get_store_type_display()}
        - متراژ: {store_analysis.store_size} متر مربع
        - دوربین نظارتی: {'دارد' if store_analysis.has_surveillance else 'ندارد'}
        
        لطفاً تحلیل جامعی از طراحی این فروشگاه ارائه دهید و امتیاز 1-10 بدهید.
        """
        
        return self._call_openai(prompt)
    
    def analyze_sales(self, store_analysis):
        """تحلیل فروش فروشگاه"""
        prompt = f"""
        تحلیل فروش فروشگاه {store_analysis.store_name}:
        - درصد فروش صبح: {store_analysis.morning_sales_percent}%
        - درصد فروش ظهر: {store_analysis.noon_sales_percent}%
        - درصد فروش عصر: {store_analysis.evening_sales_percent}%
        - درصد فروش شب: {store_analysis.night_sales_percent}%
        
        لطفاً تحلیل جامعی از فروش این فروشگاه ارائه دهید و امتیاز 1-10 بدهید.
        """
        
        return self._call_openai(prompt)
    
    def generate_overall_analysis(self, store_analysis, layout_analysis, traffic_analysis, design_analysis, sales_analysis):
        """تولید تحلیل کلی"""
        prompt = f"""
        تحلیل کلی فروشگاه {store_analysis.store_name}:
        
        تحلیل چیدمان: {layout_analysis}
        تحلیل ترافیک: {traffic_analysis}
        تحلیل طراحی: {design_analysis}
        تحلیل فروش: {sales_analysis}
        
        لطفاً تحلیل کلی و پیشنهادات بهبود ارائه دهید.
        """
        
        return self._call_openai(prompt)
    
    def extract_score(self, analysis_text):
        """استخراج امتیاز از متن تحلیل"""
        try:
            # جستجوی الگوی امتیاز در متن
            import re
            score_match = re.search(r'امتیاز[:\s]*(\d+)', analysis_text)
            if score_match:
                return int(score_match.group(1))
            else:
                return 5  # امتیاز پیش‌فرض
        except:
            return 5
    
    def _call_openai(self, prompt):
        """فراخوانی OpenAI API"""
        if not self.openai_api_key:
            return "تحلیل با استفاده از هوش مصنوعی در دسترس نیست."
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "شما یک متخصص تحلیل فروشگاه هستید."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return "خطا در تحلیل هوش مصنوعی" 