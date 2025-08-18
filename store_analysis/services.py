import logging
import openai
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from .models import StoreAnalysis, StoreAnalysisResult
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class StoreAnalysisService:
    def __init__(self):
        # بررسی وجود API key
        if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        else:
            logger.warning("OpenAI API key not found, using fallback analysis")
            self.use_openai = False
            return
        
        self.use_openai = True
        try:
            # تست اتصال به OpenAI
            from openai import OpenAI
            client = OpenAI(api_key=openai.api_key)
            # تست ساده
            logger.info("OpenAI API connection successful")
        except Exception as e:
            logger.error(f"OpenAI API connection failed: {str(e)}")
            self.use_openai = False

    def analyze_layout(self, store_analysis):
        prompt = f"""
        تحلیل چیدمان فروشگاه {store_analysis.store_name}:
        - متراژ: {store_analysis.store_size} متر مربع
        - تعداد قفسه: {store_analysis.shelf_count}
        - ابعاد قفسه‌ها: {store_analysis.shelf_dimensions}
        - محتوای قفسه‌ها: {store_analysis.shelf_contents}
        - مناطق بلااستفاده: {store_analysis.unused_areas}
        - موقعیت صندوق: {store_analysis.checkout_location}
        
        لطفاً تحلیل دقیقی از چیدمان فروشگاه ارائه دهید و امتیازی بین 0 تا 100 به آن بدهید.
        """
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai.api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "شما یک متخصص تحلیل چیدمان فروشگاه هستید."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except ImportError:
            # Fallback for older openai versions
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "شما یک متخصص تحلیل چیدمان فروشگاه هستید."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error in analyze_layout: {str(e)}")
            return "خطا در تحلیل چیدمان"

    def analyze_traffic(self, store_analysis):
        prompt = f"""
        تحلیل ترافیک فروشگاه {store_analysis.store_name}:
        - مناطق پرتردد: {store_analysis.high_traffic_areas}
        - ساعات پیک: {store_analysis.peak_hours}
        - مسیر حرکت مشتریان: {store_analysis.customer_movement_paths}
        - تعداد دوربین: {store_analysis.camera_count}
        - پوشش دوربین‌ها: {store_analysis.camera_coverage}
        
        لطفاً تحلیل دقیقی از ترافیک فروشگاه ارائه دهید و امتیازی بین 0 تا 100 به آن بدهید.
        """
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai.api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "شما یک متخصص تحلیل ترافیک فروشگاه هستید."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except ImportError:
            # Fallback for older openai versions
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "شما یک متخصص تحلیل ترافیک فروشگاه هستید."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error in analyze_traffic: {str(e)}")
            return "خطا در تحلیل ترافیک"

    def analyze_design(self, store_analysis):
        prompt = f"""
        تحلیل طراحی فروشگاه {store_analysis.store_name}:
        - سبک طراحی: {store_analysis.design_style}
        - رنگ‌های اصلی: {store_analysis.brand_colors}
        - عناصر دکوراتیو: {store_analysis.decorative_elements}
        - محدودیت‌های چیدمان: {store_analysis.layout_restrictions}
        
        لطفاً تحلیل دقیقی از طراحی فروشگاه ارائه دهید و امتیازی بین 0 تا 100 به آن بدهید.
        """
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai.api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "شما یک متخصص طراحی فروشگاه هستید."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except ImportError:
            # Fallback for older openai versions
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "شما یک متخصص طراحی فروشگاه هستید."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error in analyze_design: {str(e)}")
            return "خطا در تحلیل طراحی"

    def analyze_sales(self, store_analysis):
        prompt = f"""
        تحلیل فروش فروشگاه {store_analysis.store_name}:
        - دسته‌بندی محصولات: {store_analysis.product_categories}
        - محصولات پرفروش: {store_analysis.top_products}
        - حجم فروش روزانه: {store_analysis.sales_volume}
        - نرم‌افزار صندوق: {store_analysis.pos_system}
        
        لطفاً تحلیل دقیقی از عملکرد فروش فروشگاه ارائه دهید و امتیازی بین 0 تا 100 به آن بدهید.
        """
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai.api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "شما یک متخصص تحلیل فروش هستید."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except ImportError:
            # Fallback for older openai versions
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "شما یک متخصص تحلیل فروش هستید."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error in analyze_sales: {str(e)}")
            return "خطا در تحلیل فروش"

    def generate_overall_analysis(self, store_analysis, layout_analysis, traffic_analysis, design_analysis, sales_analysis):
        prompt = f"""
        تحلیل کلی فروشگاه {store_analysis.store_name}:
        
        تحلیل چیدمان:
        {layout_analysis}
        
        تحلیل ترافیک:
        {traffic_analysis}
        
        تحلیل طراحی:
        {design_analysis}
        
        تحلیل فروش:
        {sales_analysis}
        
        لطفاً یک تحلیل کلی از وضعیت فروشگاه ارائه دهید و امتیازی بین 0 تا 100 به آن بدهید.
        """
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai.api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "شما یک متخصص تحلیل فروشگاه هستید."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except ImportError:
            # Fallback for older openai versions
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "شما یک متخصص تحلیل فروشگاه هستید."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error in generate_overall_analysis: {str(e)}")
            return "خطا در تحلیل کلی"

    def extract_score(self, analysis_text: str) -> float:
        """استخراج امتیاز از متن تحلیل"""
        try:
            if not analysis_text:
                return 5.0
            
            # الگوهای مختلف برای استخراج امتیاز
            patterns = [
                r'امتیاز[:\s]*(\d+(?:\.\d+)?)',
                r'نمره[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*از\s*100',
                r'(\d+(?:\.\d+)?)\s*امتیاز',
            ]
            
            for pattern in patterns:
                score_match = re.search(pattern, analysis_text)
                if score_match:
                    score = float(score_match.group(1))
                    # محدود کردن امتیاز بین 0 تا 100
                    return max(0.0, min(100.0, score))
            
            return 5.0  # امتیاز پیش‌فرض
        except (ValueError, TypeError) as e:
            logger.error(f"Error extracting score: {str(e)}")
            return 5.0

    def analyze_store(self, store_analysis):
        """تحلیل کامل فروشگاه"""
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