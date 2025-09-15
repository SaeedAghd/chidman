#!/usr/bin/env python
"""
سیستم تحلیل هوشمند فروشگاه
تولید تحلیل تفصیلی و راهنمایی‌های عملی با استفاده از AI
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import requests
from django.conf import settings
from django.core.cache import cache

# Import Ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

# Import ML libraries
try:
    import numpy as np
    ML_AVAILABLE = True
    PANDAS_AVAILABLE = False
    SKLEARN_AVAILABLE = False
    TENSORFLOW_AVAILABLE = False
    
    # Skip problematic libraries for now
    try:
        # Skip pandas due to compatibility issues
        # import pandas as pd
        # PANDAS_AVAILABLE = True
        pass
    except Exception:
        pass
        
    try:
        # Skip sklearn for now
        # from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
        # SKLEARN_AVAILABLE = True
        pass
    except Exception:
        pass
        
    try:
        # Skip tensorflow for now
        # import tensorflow as tf
        # TENSORFLOW_AVAILABLE = True
        pass
    except Exception:
        pass
        
except ImportError:
    # Create a dummy numpy for when it's not available
    class DummyNumpy:
        def array(self, data):
            return data
        def ndarray(self, *args, **kwargs):
            return []
    
    np = DummyNumpy()
    ML_AVAILABLE = False
    PANDAS_AVAILABLE = False
    SKLEARN_AVAILABLE = False
    TENSORFLOW_AVAILABLE = False
    logging.warning("ML libraries not available. Advanced analysis will be disabled.")

logger = logging.getLogger(__name__)

class StoreAnalysisAI:
    """کلاس تحلیل هوشمند فروشگاه با استفاده از Ollama (رایگان و محلی)"""
    
    def __init__(self):
        # تنظیمات Ollama
        self.model_name = "llama3.2"  # مدل پیش‌فرض Ollama
        
        # بررسی دسترسی به Ollama
        self.ollama_available = self._check_ollama_availability()
        
        if not self.ollama_available:
            logger.warning("Ollama not available, using local analysis")
    
    def _check_ollama_availability(self):
        """بررسی دسترسی به Ollama"""
        if not OLLAMA_AVAILABLE:
            return False
        
        try:
            # بررسی دسترسی به Ollama با کتابخانه ollama
            ollama.list()
            return True
        except:
            try:
                # Fallback به API request
                response = requests.get("http://localhost:11434/api/tags", timeout=5)
                return response.status_code == 200
            except:
                return False
    
    def call_ollama_api(self, prompt: str, max_tokens: int = 2000) -> str:
        """فراخوانی API Ollama (رایگان و محلی)"""
        try:
            if not self.ollama_available:
                logger.warning("Ollama not available, using local analysis")
                return self._get_local_analysis(prompt)
            
            # تنظیم prompt شخصی‌سازی شده برای Ollama
            system_prompt = """شما یک متخصص طراحی فروشگاه و مشاور تجاری با تجربه 20 ساله هستید. شما باید مانند یک دوست صمیمی و مشاور قابل اعتماد با مالک فروشگاه صحبت کنید.

مهم: در تمام پاسخ خود باید:
1. از نام فروشگاه و جزئیات خاص آن استفاده کنید
2. به محصولات، رنگ‌بندی، چیدمان و نورپردازی موجود اشاره کنید
3. بازار هدف و مشتریان را در نظر بگیرید
4. مانند یک دوست صمیمی و حرفه‌ای صحبت کنید
5. تحلیل کاملاً شخصی‌سازی شده و منحصر به فرد ارائه دهید

پاسخ‌های خود را به فارسی و به صورت جامع، عملی و شخصی‌سازی شده ارائه دهید."""
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": max_tokens
                }
            }
            
            # استفاده از کتابخانه ollama
            if OLLAMA_AVAILABLE:
                try:
                    response = ollama.generate(
                        model=self.model_name,
                        prompt=full_prompt,
                        options={
                            'temperature': 0.7,
                            'top_p': 0.9,
                            'num_predict': max_tokens
                        }
                    )
                    return response['response']
                except Exception as e:
                    logger.error(f"Ollama library error: {str(e)}")
                    # Fallback به API request
                    pass
            
            # Fallback به API request
            response = requests.post(
                "http://localhost:11434/api/generate",
                json=payload,
                timeout=60  # Ollama ممکن است کمی کندتر باشد
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return self._get_local_analysis(prompt)
                
        except Exception as e:
            logger.error(f"Error calling Ollama API: {e}")
            return self._get_local_analysis(prompt)
    
    def call_deepseek_api(self, prompt: str, max_tokens: int = 2000) -> str:
        """متد سازگاری - فراخوانی Ollama"""
        return self.call_ollama_api(prompt, max_tokens)
    
    def _get_local_analysis(self, prompt: str) -> str:
        """تحلیل محلی بر اساس الگوهای از پیش تعریف شده"""
        # استخراج اطلاعات کلیدی از prompt
        store_name = self._extract_from_prompt(prompt, "نام فروشگاه:")
        store_type = self._extract_from_prompt(prompt, "نوع فروشگاه:")
        store_size = self._extract_from_prompt(prompt, "اندازه فروشگاه:")
        daily_customers = self._extract_from_prompt(prompt, "تعداد مشتری روزانه:")
        daily_sales = self._extract_from_prompt(prompt, "فروش روزانه:")
        
        # تحلیل بر اساس الگوها
        analysis = self._generate_pattern_based_analysis(
            store_name, store_type, store_size, daily_customers, daily_sales
        )
        
        return analysis
    
    def _extract_from_prompt(self, prompt: str, keyword: str) -> str:
        """استخراج مقدار از prompt بر اساس کلیدواژه"""
        try:
            start_idx = prompt.find(keyword)
            if start_idx != -1:
                start_idx += len(keyword)
                end_idx = prompt.find('\n', start_idx)
                if end_idx == -1:
                    end_idx = start_idx + 50
                return prompt[start_idx:end_idx].strip()
        except:
            pass
        return "نامشخص"
    
    def _generate_pattern_based_analysis(self, store_name, store_type, store_size, daily_customers, daily_sales):
        """تولید تحلیل شخصی‌سازی شده بر اساس الگوهای از پیش تعریف شده"""
        
        # محاسبه امتیاز بر اساس الگوها
        score = 5.0
        
        # امتیاز بر اساس اندازه فروشگاه
        try:
            size = int(store_size.replace('متر مربع', '').strip())
            if size > 200:
                score += 2.0
            elif size > 100:
                score += 1.5
            elif size > 50:
                score += 1.0
        except:
            pass
        
        # امتیاز بر اساس تعداد مشتری
        try:
            customers = int(daily_customers)
            if customers > 500:
                score += 2.0
            elif customers > 200:
                score += 1.5
            elif customers > 100:
                score += 1.0
        except:
            pass
        
        # امتیاز بر اساس فروش
        try:
            sales = int(daily_sales.replace('تومان', '').replace(',', '').strip())
            if sales > 10000000:
                score += 1.5
            elif sales > 5000000:
                score += 1.0
            elif sales > 1000000:
                score += 0.5
        except:
            pass
        
        score = min(score, 10.0)
        
        # تولید تحلیل شخصی‌سازی شده بر اساس امتیاز
        if score >= 8:
            analysis_level = "عالی"
            strengths = [
                f"فروشگاه {store_name} شما دارای پتانسیل بسیار بالایی است",
                f"ساختار و موقعیت جغرافیایی {store_name} مناسب است",
                f"ترافیک {daily_customers} مشتری روزانه در سطح مطلوب است",
                f"فروش روزانه {daily_sales} تومان نشان‌دهنده عملکرد خوب است"
            ]
            weaknesses = [
                f"نیاز به بهینه‌سازی جزئی در چیدمان {store_name}",
                f"امکان بهبود در نورپردازی فروشگاه {store_name}",
                f"بهبود نمایش محصولات در {store_name}"
            ]
        elif score >= 6:
            analysis_level = "خوب"
            strengths = [
                f"فروشگاه {store_name} شما دارای پتانسیل خوبی است",
                f"ساختار کلی {store_name} مناسب است",
                f"موقعیت جغرافیایی {store_name} قابل قبول است",
                f"فروش {daily_sales} تومان روزانه نشان‌دهنده پتانسیل است"
            ]
            weaknesses = [
                f"نیاز به بهبود چیدمان قفسه‌های {store_name}",
                f"بهینه‌سازی سیستم نورپردازی {store_name}",
                f"افزایش کارایی ترافیک {daily_customers} مشتری روزانه",
                f"بهبود نمایش محصولات در {store_name}"
            ]
        else:
            analysis_level = "نیاز به بهبود"
            strengths = [
                f"فروشگاه {store_name} شما دارای پتانسیل رشد است",
                f"امکان بهبود قابل توجه در {store_name} وجود دارد",
                f"فروش {daily_sales} تومان پایه خوبی برای رشد است"
            ]
            weaknesses = [
                f"نیاز به بازطراحی کامل چیدمان {store_name}",
                f"بهبود سیستم نورپردازی {store_name}",
                f"بهینه‌سازی جریان {daily_customers} مشتری روزانه",
                f"افزایش کارایی صندوق‌های پرداخت {store_name}",
                f"بهبود نمایش محصولات در {store_name}"
            ]
        
        # تولید تحلیل کامل و شخصی‌سازی شده
        analysis = f"""
# 🎯 تحلیل شخصی‌سازی شده فروشگاه {store_name}

سلام! من به عنوان یک متخصص طراحی فروشگاه، تحلیل کاملی از فروشگاه {store_name} شما انجام داده‌ام. بیایید ببینیم چطور می‌توانیم فروشگاه شما را به یک فروشگاه خاص و موفق تبدیل کنیم.

## 📊 امتیاز کلی {store_name}: {score:.1f}/10 ({analysis_level})

### 💪 نقاط قوت فروشگاه {store_name}:
"""
        for strength in strengths:
            analysis += f"- {strength}\n"
        
        analysis += f"\n### ⚠️ نقاط ضعف و چالش‌های {store_name}:\n"
        for weakness in weaknesses:
            analysis += f"- {weakness}\n"
        
        analysis += f"""
### 🎨 تحلیل طراحی و چیدمان {store_name}:

**نورپردازی فروشگاه {store_name}:**
فروشگاه {store_name} شما نیاز به بررسی دقیق‌تر سیستم نورپردازی دارد. نور مناسب می‌تواند تأثیر مستقیمی بر فروش {daily_sales} تومان روزانه شما داشته باشد.

**رنگ‌بندی و فضای {store_name}:**
رنگ‌بندی مناسب برای فروشگاه {store_type} شما بسیار مهم است. باید با بازار هدف شما هماهنگ باشد.

**چیدمان قفسه‌های {store_name}:**
چیدمان فعلی قفسه‌ها در {store_name} نیاز به بهینه‌سازی دارد تا جریان {daily_customers} مشتری روزانه شما بهبود یابد.

### 🛍️ تحلیل محصولات و بازار {store_name}:

**محصولات فروشگاه {store_name}:**
محصولات شما در فروشگاه {store_name} نیاز به نمایش بهتر و جذاب‌تری دارند تا فروش {daily_sales} تومان روزانه افزایش یابد.

**بازار هدف {store_name}:**
مشتریان {daily_customers} نفری روزانه شما نیاز به تجربه بهتری در {store_name} دارند.

        ### 💡 توصیه‌های عملی و شخصی‌سازی شده برای {store_name}:
        1. **بهبود نورپردازی {store_name}:** استفاده از نور طبیعی و مصنوعی ترکیبی
        2. **بهینه‌سازی چیدمان {store_name}:** ایجاد مسیر حرکت منطقی برای مشتریان
        3. **بهبود نمایش محصولات {store_name}:** استفاده از تکنیک‌های نمایش جذاب
        4. **افزایش کارایی صندوق‌ها در {store_name}:** کاهش زمان انتظار مشتریان
        5. **بهبود فضای {store_name}:** ایجاد محیطی دوستانه و جذاب
        6. **استفاده از رنگ‌های مناسب در {store_name}:** هماهنگ با نوع کسب‌وکار
        7. **بهینه‌سازی قفسه‌بندی {store_name}:** دسترسی آسان به محصولات
        8. **ایجاد نقاط کانونی در {store_name}:** جلب توجه به محصولات خاص
        9. **بهبود تهویه {store_name}:** ایجاد محیطی راحت برای مشتریان
        10. **استفاده از موسیقی مناسب در {store_name}:** ایجاد فضای مثبت
        11. **بهبود نقشه حرکتی {store_name}:** ایجاد مسیر روان از ورودی تا نقطه فروش
        12. **بهینه‌سازی منطقه داغ {store_name}:** قرارگیری محصولات مهم در نقاط پرتردد
        13. **قفسه‌بندی هوشمند {store_name}:** ارتفاع مناسب و دسترسی آسان
        14. **نورپردازی تأکیدی {store_name}:** تمرکز نور روی محصولات خاص
        15. **نورپردازی احساسی {store_name}:** ایجاد فضای گرم و صمیمی
        16. **رنگ سازمانی {store_name}:** پالت رنگی هماهنگ با برند
        17. **متریال و بافت {store_name}:** انتقال حس برند از طریق متریال
        18. **نشانه‌گذاری {store_name}:** تابلوها و علائم راهنما واضح
        19. **تجربه پنج‌گانه {store_name}:** بهبود حس دیداری، شنیداری، بویایی، لامسه و چشایی
        20. **راحتی و آرامش {store_name}:** فضای نشستن و اتاق پرو مناسب
        21. **تعامل دیجیتال {store_name}:** نمایشگرها و QR کدها
        22. **ویترین جذاب {store_name}:** داستان‌سرایی بصری
        23. **ترکیب‌بندی محصولات {store_name}:** چینش بر اساس تم رنگی و فصل
        24. **صندوق و خروجی {store_name}:** تجربه نهایی خرید و بسته‌بندی
        25. **ارگونومی {store_name}:** دسترسی آسان و راحتی مشتری
        26. **راهنمایی روان {store_name}:** علائم واضح و جلوگیری از گم‌گشتگی
        27. **خدمات انسانی {store_name}:** جایگاه مشاوره و پرسنل

        ### 🌈 توصیه‌های تخصصی رنگ‌بندی و چیدمان محصولات {store_name}:

        **رنگ‌بندی محصولات بر اساس نوع کسب‌وکار {store_type}:**
        - استفاده از رنگ‌های گرم (قرمز، نارنجی، زرد) برای محصولات پرفروش
        - قرار دادن محصولات با رنگ‌های متضاد کنار هم برای جلب توجه
        - استفاده از رنگ‌های سرد (آبی، سبز) برای محصولات آرامش‌بخش
        - ایجاد گرادیان رنگی از تیره به روشن در قفسه‌ها

        **چیدمان محصولات برای جلب توجه:**
        - قرار دادن محصولات پرفروش در ارتفاع چشم (120-160 سانتی‌متر)
        - استفاده از قانون "قدرت سه" در چیدمان محصولات
        - ایجاد مثلث طلایی برای محصولات مهم
        - استفاده از فاصله‌گذاری مناسب بین محصولات

        **استراتژی‌های جلب توجه مشتری:**
        - استفاده از نور تاکیدی روی محصولات خاص
        - ایجاد نقاط کانونی با رنگ‌های متضاد
        - استفاده از آینه‌ها برای ایجاد عمق بصری
        - قرار دادن محصولات جدید در مسیر اصلی حرکت مشتری

### 📈 برنامه بهبود مرحله‌ای {store_name}:

**مرحله 1 (هفته 1-2):** اقدامات فوری
- بررسی و بهبود نورپردازی {store_name}
- بهینه‌سازی چیدمان قفسه‌های {store_name}
- بهبود نمایش محصولات در {store_name}

**مرحله 2 (هفته 3-4):** بهبودهای کوتاه‌مدت
- بهینه‌سازی مسیر حرکت مشتریان در {store_name}
- بهبود سیستم صندوق‌های پرداخت {store_name}
- ایجاد نقاط کانونی در {store_name}

**مرحله 3 (ماه 2-3):** بهبودهای بلندمدت
- بازطراحی کامل فضای {store_name}
- پیاده‌سازی سیستم‌های پیشرفته در {store_name}
- آموزش کارکنان {store_name} برای ارائه خدمات بهتر

### 🎯 پیش‌بینی نتایج برای {store_name}:
با اجرای این توصیه‌ها، فروشگاه {store_name} شما می‌تواند:
- فروش روزانه را از {daily_sales} تومان به 30-50% افزایش دهد
- تعداد مشتریان روزانه را از {daily_customers} نفر بهبود بخشد
- تجربه مشتریان در {store_name} را به طور قابل توجهی ارتقا دهد
- {store_name} را به یک فروشگاه خاص و متمایز تبدیل کند

### 💰 تأثیر بر فروش {store_name}:
این تغییرات می‌تواند فروش روزانه {store_name} شما را از {daily_sales} تومان به میزان قابل توجهی افزایش دهد و {store_name} را به یک فروشگاه موفق و خاص تبدیل کند.

**نکته مهم:** تمام این توصیه‌ها مخصوص فروشگاه {store_name} شما طراحی شده‌اند و با در نظر گیری نوع کسب‌وکار {store_type}، اندازه {store_size} متر مربع، و {daily_customers} مشتری روزانه شما ارائه شده‌اند.

موفق باشید! 🚀
**مرحله 2:** طراحی چیدمان جدید (2 هفته)
**مرحله 3:** اجرای تغییرات (3-4 هفته)
**مرحله 4:** نظارت و ارزیابی (2 هفته)

### 🎯 پیش‌بینی نتایج:
با اجرای توصیه‌های ارائه شده، انتظار می‌رود:
- افزایش 15-25% در فروش
- بهبود 20-30% در رضایت مشتریان
- کاهش 10-15% در زمان انتظار در صندوق‌ها
- افزایش 20% در کارایی فضای فروشگاه

### 📋 خلاصه:
فروشگاه شما دارای پتانسیل خوبی برای رشد و بهبود است. با اجرای توصیه‌های ارائه شده، می‌توانید به نتایج قابل توجهی دست یابید.
"""
        
        return analysis
    
    def _get_fallback_analysis(self) -> str:
        """تحلیل پیش‌فرض در صورت عدم دسترسی به API"""
        return """
        تحلیل فروشگاه شما با موفقیت انجام شد. بر اساس اطلاعات ارائه شده:
        
        **نقاط قوت:**
        - فروشگاه شما دارای پتانسیل خوبی برای بهبود است
        - ساختار کلی مناسب است
        
        **نقاط ضعف:**
        - نیاز به بهینه‌سازی چیدمان
        - بهبود سیستم نورپردازی
        - افزایش کارایی ترافیک مشتریان
        
        **توصیه‌ها:**
        1. بازچینی قفسه‌ها برای بهبود جریان مشتری
        2. بهبود نورپردازی برای جذابیت بیشتر
        3. بهینه‌سازی محل صندوق‌های پرداخت
        
        برای دریافت تحلیل کامل‌تر، لطفاً با تیم پشتیبانی تماس بگیرید.
        """
    
    def analyze_store(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل کامل فروشگاه"""
        try:
            # ایجاد prompt برای تحلیل
            prompt = self._create_analysis_prompt(store_data)
            
            # فراخوانی API
            analysis_result = self.call_deepseek_api(prompt, max_tokens=3000)
            
            # پردازش نتیجه
            return self._process_analysis_result(analysis_result, store_data)
            
        except Exception as e:
            logger.error(f"Error in store analysis: {e}")
            return self._get_default_analysis_result(store_data)
    
    def _extract_real_store_data(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """استخراج اطلاعات واقعی فروشگاه از داده‌های ورودی"""
        try:
            # استخراج اطلاعات از کلیدهای مختلف
            extracted_data = {}
            
            # اطلاعات پایه
            extracted_data.update({
                'city': store_data.get('city') or store_data.get('store_city'),
                'area': store_data.get('area') or store_data.get('store_area'),
                'entrance_count': store_data.get('entrance_count') or store_data.get('entrances'),
                'checkout_count': store_data.get('checkout_count') or store_data.get('checkout_location'),
                'shelf_count': store_data.get('shelf_count'),
                'shelf_dimensions': store_data.get('shelf_dimensions'),
                'shelf_contents': store_data.get('shelf_contents'),
                'design_style': store_data.get('design_style'),
                'primary_brand_color': store_data.get('primary_brand_color') or store_data.get('brand_colors'),
                'brand_colors': store_data.get('brand_colors'),
                'lighting_type': store_data.get('lighting_type') or store_data.get('main_lighting'),
                'lighting_intensity': store_data.get('lighting_intensity'),
                'decorative_elements': store_data.get('decorative_elements'),
                'customer_time': store_data.get('customer_time') or store_data.get('customer_dwell_time'),
                'customer_flow': store_data.get('customer_flow'),
                'customer_movement_paths': store_data.get('customer_movement_paths'),
                'stopping_points': store_data.get('stopping_points'),
                'high_traffic_areas': store_data.get('high_traffic_areas'),
                'peak_hours': store_data.get('peak_hours'),
                'top_products': store_data.get('top_products'),
                'monthly_sales': store_data.get('monthly_sales'),
                'product_count': store_data.get('product_count'),
                'product_categories': store_data.get('product_categories'),
                'has_cameras': store_data.get('has_cameras') or store_data.get('has_surveillance'),
                'camera_count': store_data.get('camera_count'),
                'camera_locations': store_data.get('camera_locations'),
                'camera_coverage': store_data.get('camera_coverage'),
                'optimization_goals': store_data.get('optimization_goals'),
                'priority_goal': store_data.get('priority_goal')
            })
            
            # حذف مقادیر None و خالی
            cleaned_data = {k: v for k, v in extracted_data.items() if v is not None and v != ''}
            
            return cleaned_data
            
        except Exception as e:
            logger.error(f"خطا در استخراج داده‌های فروشگاه: {e}")
            return {}
    
    def _create_analysis_prompt(self, store_data: Dict[str, Any]) -> str:
        """ایجاد prompt شخصی‌سازی شده برای تحلیل فروشگاه"""
        store_name = store_data.get('store_name', 'فروشگاه')
        store_type = store_data.get('store_type', 'عمومی')
        store_size = store_data.get('store_size', 'نامشخص')
        daily_customers = store_data.get('daily_customers', 'نامشخص')
        daily_sales = store_data.get('daily_sales', 'نامشخص')
        
        # استخراج اطلاعات واقعی از store_data
        actual_data = self._extract_real_store_data(store_data)
        
        prompt = f"""
شما بهترین متخصص تحلیل فروشگاه و مشاور کسب‌وکار دنیا هستید. شما با نام "چیدمانو" شناخته می‌شوید و تخصص شما در بهینه‌سازی چیدمان فروشگاه‌ها است.

**مهم: شما باید تحلیل کاملاً شخصی‌سازی شده و منحصر به فرد برای فروشگاه "{store_name}" ارائه دهید، نه آموزش عمومی!**

**اطلاعات واقعی فروشگاه "{store_name}":**

📍 **اطلاعات کلی:**
- نام: {store_name}
- نوع کسب‌وکار: {store_type}
- اندازه: {store_size}
- شهر: {actual_data.get('city', 'نامشخص')}
- منطقه: {actual_data.get('area', 'نامشخص')}

🏗️ **ساختار واقعی فروشگاه {store_name}:**
- تعداد ورودی: {actual_data.get('entrance_count', 'نامشخص')}
- تعداد صندوق: {actual_data.get('checkout_count', 'نامشخص')}
- تعداد قفسه: {actual_data.get('shelf_count', 'نامشخص')}
- ابعاد قفسه‌ها: {actual_data.get('shelf_dimensions', 'نامشخص')}
- محتویات قفسه‌ها: {actual_data.get('shelf_contents', 'نامشخص')}

🎨 **طراحی و دکوراسیون واقعی {store_name}:**
- سبک طراحی: {actual_data.get('design_style', 'نامشخص')}
- رنگ اصلی: {actual_data.get('primary_brand_color', 'نامشخص')}
- رنگ‌های برند: {actual_data.get('brand_colors', 'نامشخص')}
- نوع نورپردازی: {actual_data.get('lighting_type', 'نامشخص')}
- شدت نور: {actual_data.get('lighting_intensity', 'نامشخص')}
- عناصر تزئینی: {actual_data.get('decorative_elements', 'نامشخص')}

👥 **رفتار واقعی مشتریان {store_name}:**
- تعداد مشتری روزانه: {daily_customers}
- زمان حضور مشتری: {actual_data.get('customer_time', 'نامشخص')}
- جریان مشتری: {actual_data.get('customer_flow', 'نامشخص')}
- مسیرهای حرکت مشتری: {actual_data.get('customer_movement_paths', 'نامشخص')}
- نقاط توقف: {actual_data.get('stopping_points', 'نامشخص')}
- مناطق پرتردد: {actual_data.get('high_traffic_areas', 'نامشخص')}
- ساعات پیک: {actual_data.get('peak_hours', 'نامشخص')}

🛍️ **فروش و محصولات واقعی {store_name}:**
- محصولات پرفروش: {actual_data.get('top_products', 'نامشخص')}
- فروش روزانه: {daily_sales}
- فروش ماهانه: {actual_data.get('monthly_sales', 'نامشخص')}
- تعداد محصولات: {actual_data.get('product_count', 'نامشخص')}
- دسته‌بندی محصولات: {actual_data.get('product_categories', 'نامشخص')}

🔒 **امنیت واقعی {store_name}:**
- دوربین نظارتی: {actual_data.get('has_cameras', 'نامشخص')}
- تعداد دوربین: {actual_data.get('camera_count', 'نامشخص')}
- موقعیت دوربین‌ها: {actual_data.get('camera_locations', 'نامشخص')}
- پوشش دوربین‌ها: {actual_data.get('camera_coverage', 'نامشخص')}

🎯 **اهداف بهینه‌سازی {store_name}:**
- اهداف: {actual_data.get('optimization_goals', 'نامشخص')}
- هدف اولویت: {actual_data.get('priority_goal', 'نامشخص')}

**لطفاً تحلیل جامع و شخصی‌سازی شده ارائه دهید:**

## 🎯 تحلیل شخصی‌سازی شده فروشگاه {store_name}

### 📊 امتیاز کلی (1-10)
[بر اساس تمام جزئیات فوق، امتیاز دقیق دهید]

### 💪 نقاط قوت {store_name}
[حداقل 5 مورد با اشاره به جزئیات خاص فروشگاه]

### ⚠️ نقاط ضعف و چالش‌ها
[حداقل 5 مورد با اشاره به مشکلات خاص]

### 🎨 تحلیل طراحی و چیدمان
**نورپردازی {actual_data.get('lighting_type', 'نامشخص')}:**
[تحلیل دقیق نورپردازی فعلی {store_name}]

**رنگ‌بندی {actual_data.get('primary_brand_color', 'نامشخص')}:**
[تحلیل رنگ‌بندی و تأثیر آن بر مشتریان {store_name}]

**چیدمان قفسه‌های {actual_data.get('shelf_count', 'نامشخص')}:**
[تحلیل چیدمان و پیشنهادات بهبود {store_name}]

**سبک طراحی {actual_data.get('design_style', 'نامشخص')}:**
[تحلیل سبک طراحی و تطبیق با نوع کسب‌وکار {store_type}]

### 🌈 تحلیل رنگ‌بندی و چیدمان محصولات
**رنگ‌بندی محصولات {store_name}:**
[تحلیل رنگ‌بندی محصولات و نحوه چیدمان آن‌ها برای جلب توجه بیشتر]

**چیدمان محصولات بر اساس رنگ:**
[توصیه‌های خاص برای چیدمان محصولات بر اساس رنگ‌بندی]

**استراتژی جلب توجه:**
[راهکارهای عملی برای جلب توجه مشتریان در {store_name}]

### 🏗️ تحلیل معماری فضایی و جریان مشتری
**نقشه حرکتی مشتری {store_name}:**
[تحلیل مسیر حرکت مشتری از ورودی تا نقطه فروش]

**منطقه داغ (Hot Zone) {store_name}:**
[شناسایی نقاط پرتردد و پیشنهادات برای قرارگیری محصولات مهم]

**قفسه‌بندی هوشمند {store_name}:**
[تحلیل چیدمان قفسه‌ها و پیشنهادات بهبود]

### 🎯 توصیه‌های عملی و قابل اجرا
**اقدامات فوری (1-2 هفته):**
[حداقل 5 اقدام فوری برای {store_name}]

**اقدامات کوتاه‌مدت (1-3 ماه):**
[حداقل 5 اقدام کوتاه‌مدت برای {store_name}]

**اقدامات بلندمدت (3-12 ماه):**
[حداقل 5 اقدام بلندمدت برای {store_name}]

### 📈 پیش‌بینی نتایج
**افزایش فروش پیش‌بینی شده:**
[درصد افزایش فروش برای {store_name}]

**بهبود تجربه مشتری:**
[نحوه بهبود تجربه مشتری در {store_name}]

**بازگشت سرمایه:**
[زمان بازگشت سرمایه برای {store_name}]

**نکته مهم: تمام تحلیل‌ها باید کاملاً شخصی‌سازی شده و مختص فروشگاه "{store_name}" باشد، نه آموزش عمومی!**
        """
        
        return prompt
    
    def _process_analysis_result(self, analysis_text: str, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """پردازش نتیجه تحلیل"""
        try:
            # محاسبه امتیاز کلی (ساده)
            overall_score = self._calculate_overall_score(store_data)
            
            # تقسیم‌بندی تحلیل
            sections = self._parse_analysis_sections(analysis_text)
            
            return {
                'overall_score': overall_score,
                'analysis_text': analysis_text,
                'sections': sections,
                'recommendations': self._extract_recommendations(analysis_text),
                'strengths': self._extract_strengths(analysis_text),
                'weaknesses': self._extract_weaknesses(analysis_text),
                'improvement_plan': self._extract_improvement_plan(analysis_text),
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing analysis result: {e}")
            return self._get_default_analysis_result(store_data)
    
    def _calculate_overall_score(self, store_data: Dict[str, Any]) -> float:
        """محاسبه امتیاز کلی فروشگاه"""
        score = 5.0  # امتیاز پایه
        
        # امتیاز بر اساس اندازه فروشگاه
        store_size = store_data.get('store_size', '0')
        try:
            size = int(store_size)
            if size > 100:
                score += 1.0
            elif size > 50:
                score += 0.5
        except:
            pass
        
        # امتیاز بر اساس تعداد مشتری
        daily_customers = store_data.get('daily_customers', '0')
        try:
            customers = int(daily_customers)
            if customers > 200:
                score += 1.0
            elif customers > 100:
                score += 0.5
        except:
            pass
        
        # امتیاز بر اساس سیستم امنیتی
        if store_data.get('has_cameras') == 'on':
            score += 0.5
        
        # امتیاز بر اساس نورپردازی
        if store_data.get('lighting_type') == 'mixed':
            score += 0.5
        
        return min(score, 10.0)  # حداکثر 10
    
    def _parse_analysis_sections(self, analysis_text: str) -> Dict[str, str]:
        """تقسیم‌بندی تحلیل به بخش‌های مختلف"""
        sections = {}
        
        # جستجوی بخش‌های مختلف
        section_patterns = {
            'overall': ['تحلیل کلی', 'امتیاز کلی', 'نتیجه کلی'],
            'strengths': ['نقاط قوت', 'مزایا', 'قوت‌ها'],
            'weaknesses': ['نقاط ضعف', 'مشکلات', 'ضعف‌ها'],
            'recommendations': ['توصیه‌ها', 'پیشنهادات', 'راهکارها'],
            'improvement': ['برنامه بهبود', 'مراحل اجرا', 'بهبود']
        }
        
        for section_name, patterns in section_patterns.items():
            for pattern in patterns:
                if pattern in analysis_text:
                    # استخراج متن مربوط به این بخش
                    start_idx = analysis_text.find(pattern)
                    if start_idx != -1:
                        # پیدا کردن پایان بخش
                        end_idx = start_idx + 500  # حداکثر 500 کاراکتر
                        sections[section_name] = analysis_text[start_idx:end_idx]
                        break
        
        return sections
    
    def _extract_recommendations(self, analysis_text: str) -> List[str]:
        """استخراج توصیه‌ها از متن تحلیل"""
        recommendations = []
        
        # جستجوی شماره‌گذاری‌ها
        import re
        numbered_items = re.findall(r'\d+\.\s*([^\n]+)', analysis_text)
        recommendations.extend(numbered_items[:5])  # حداکثر 5 مورد
        
        return recommendations
    
    def _extract_strengths(self, analysis_text: str) -> List[str]:
        """استخراج نقاط قوت"""
        strengths = []
        
        # جستجوی کلمات کلیدی
        strength_keywords = ['قوت', 'مزیت', 'خوب', 'مناسب', 'عالی']
        
        sentences = analysis_text.split('.')
        for sentence in sentences:
            for keyword in strength_keywords:
                if keyword in sentence and len(sentence.strip()) > 10:
                    strengths.append(sentence.strip())
                    break
        
        return strengths[:3]  # حداکثر 3 مورد
    
    def _extract_weaknesses(self, analysis_text: str) -> List[str]:
        """استخراج نقاط ضعف"""
        weaknesses = []
        
        # جستجوی کلمات کلیدی
        weakness_keywords = ['ضعف', 'مشکل', 'نیاز', 'بهبود', 'کمبود']
        
        sentences = analysis_text.split('.')
        for sentence in sentences:
            for keyword in weakness_keywords:
                if keyword in sentence and len(sentence.strip()) > 10:
                    weaknesses.append(sentence.strip())
                    break
        
        return weaknesses[:3]  # حداکثر 3 مورد
    
    def _extract_improvement_plan(self, analysis_text: str) -> List[str]:
        """استخراج برنامه بهبود"""
        plan = []
        
        # جستجوی مراحل
        import re
        steps = re.findall(r'(مرحله|گام|قدم)\s*\d*[:\-]?\s*([^\n]+)', analysis_text)
        for step in steps:
            plan.append(step[1].strip())
        
        return plan[:5]  # حداکثر 5 مرحله
    
    def _get_default_analysis_result(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """نتیجه پیش‌فرض در صورت خطا"""
        return {
            'overall_score': 6.0,
            'analysis_text': self._get_fallback_analysis(),
            'sections': {
                'overall': 'تحلیل کلی فروشگاه',
                'strengths': 'نقاط قوت فروشگاه',
                'weaknesses': 'نقاط ضعف فروشگاه',
                'recommendations': 'توصیه‌های بهبود'
            },
            'recommendations': [
                'بهبود چیدمان قفسه‌ها',
                'بهینه‌سازی نورپردازی',
                'افزایش کارایی صندوق‌ها',
                'بهبود جریان مشتری',
                'بهینه‌سازی محصولات'
            ],
            'strengths': [
                'ساختار کلی مناسب',
                'پتانسیل رشد خوب',
                'موقعیت جغرافیایی مناسب'
            ],
            'weaknesses': [
                'نیاز به بهبود چیدمان',
                'بهینه‌سازی نورپردازی',
                'افزایش کارایی'
            ],
            'improvement_plan': [
                'مرحله 1: تحلیل وضعیت فعلی',
                'مرحله 2: برنامه‌ریزی بهبود',
                'مرحله 3: اجرای تغییرات',
                'مرحله 4: نظارت و ارزیابی'
            ],
            'created_at': datetime.now().isoformat()
        }
    
    def _initialize_ml_models(self):
        """راه‌اندازی مدل‌های ML"""
        try:
            if SKLEARN_AVAILABLE:
                from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
                
                # Sales prediction model
                self.ml_models['sales_predictor'] = RandomForestRegressor(
                    n_estimators=100,
                    random_state=42
                )
                
                # Conversion rate predictor
                self.ml_models['conversion_predictor'] = RandomForestRegressor(
                    n_estimators=100,
                    random_state=42
                )
                
                # Customer behavior classifier
                self.ml_models['behavior_classifier'] = RandomForestClassifier(
                    n_estimators=100,
                    random_state=42
                )
            
            # Neural network for complex patterns
            self.ml_models['neural_network'] = self._create_neural_network()
            
            logger.info("ML models initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing ML models: {e}")
            global ML_AVAILABLE
            ML_AVAILABLE = False
    
    def _create_neural_network(self):
        """ایجاد شبکه عصبی برای تحلیل پیچیده"""
        if not TENSORFLOW_AVAILABLE:
            return None
            
        try:
            from tensorflow import keras
            
            model = keras.Sequential([
                keras.layers.Dense(64, activation='relu', input_shape=(20,)),
                keras.layers.Dropout(0.2),
                keras.layers.Dense(32, activation='relu'),
                keras.layers.Dropout(0.2),
                keras.layers.Dense(16, activation='relu'),
                keras.layers.Dense(1, activation='linear')
            ])
            
            model.compile(
                optimizer='adam',
                loss='mse',
                metrics=['mae']
            )
            
            return model
            
        except Exception as e:
            logger.error(f"Error creating neural network: {e}")
            return None
    
    def generate_detailed_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """تولید تحلیل تفصیلی شخصی‌سازی شده با استفاده از Ollama"""
        try:
            # استفاده از Ollama برای تحلیل شخصی‌سازی شده
            prompt = self._create_analysis_prompt(analysis_data)
            analysis_text = self.call_ollama_api(prompt, max_tokens=3000)
            
            # پردازش نتیجه تحلیل
            result = self._process_analysis_result(analysis_text, analysis_data)
            
            # اضافه کردن جزئیات شخصی‌سازی شده
            result['personalized'] = True
            result['store_name'] = analysis_data.get('store_name', 'فروشگاه')
            result['analysis_type'] = 'detailed_personalized'
            
            # اضافه کردن توصیه‌های تخصصی رنگ‌بندی و چیدمان
            store_name = analysis_data.get('store_name', 'فروشگاه')
            store_type = analysis_data.get('store_type', 'عمومی')
            product_categories = analysis_data.get('product_categories', [])
            
            result['color_layout_recommendations'] = self._generate_color_and_layout_recommendations(
                store_name, store_type, product_categories
            )
            
            return result
            
        except Exception as e:
            logger.error(f"خطا در تولید تحلیل AI: {e}")
            return self._generate_local_analysis(analysis_data)
    
    def generate_advanced_ml_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """تولید تحلیل پیشرفته با استفاده از ML"""
        if not ML_AVAILABLE:
            return {"error": "ML libraries not available"}
        
        try:
            # تبدیل داده‌ها به فرمت مناسب برای ML
            features = self._extract_ml_features(analysis_data)
            
            # پیش‌بینی‌های مختلف
            predictions = {
                "sales_prediction": self._predict_sales(features),
                "conversion_optimization": self._predict_conversion_improvement(features),
                "customer_behavior": self._analyze_customer_behavior(features),
                "optimization_priority": self._get_optimization_priority(features),
                "roi_prediction": self._predict_roi(features)
            }
            
            # تحلیل الگوها
            pattern_analysis = self._analyze_patterns(features)
            
            # پیشنهادات مبتنی بر ML
            ml_recommendations = self._generate_ml_recommendations(features, predictions)
            
            return {
                "ml_predictions": predictions,
                "pattern_analysis": pattern_analysis,
                "ml_recommendations": ml_recommendations,
                "confidence_scores": self._calculate_confidence_scores(features),
                "generated_at": datetime.now().isoformat(),
                "analysis_type": "advanced_ml"
            }
            
        except Exception as e:
            logger.error(f"Error in ML analysis: {e}")
            return {"error": f"ML analysis failed: {str(e)}"}
    
    def _extract_ml_features(self, analysis_data: Dict[str, Any]):
        """استخراج ویژگی‌های ML از داده‌ها"""
        features = []
        
        # تبدیل داده‌ها به اعداد
        def safe_float(value, default=0.0):
            try:
                if isinstance(value, str):
                    return float(value)
                return float(value) if value is not None else default
            except (ValueError, TypeError):
                return default
        
        # ویژگی‌های عددی
        features.extend([
            safe_float(analysis_data.get('store_size', 500)),
            safe_float(analysis_data.get('entrance_count', 2)),
            safe_float(analysis_data.get('checkout_count', 3)),
            safe_float(analysis_data.get('shelf_count', 25)),
            safe_float(analysis_data.get('conversion_rate', 35.5)),
            safe_float(analysis_data.get('customer_traffic', 150)),
            safe_float(analysis_data.get('customer_dwell_time', 45)),
            safe_float(analysis_data.get('unused_area_size', 0)),
            safe_float(analysis_data.get('daily_sales_volume', 0)),
            safe_float(analysis_data.get('supplier_count', 0)),
            safe_float(analysis_data.get('camera_count', 0)),
            safe_float(analysis_data.get('morning_sales_percent', 30)),
            safe_float(analysis_data.get('noon_sales_percent', 40)),
            safe_float(analysis_data.get('evening_sales_percent', 30)),
            safe_float(analysis_data.get('sales_improvement_target', 20)),
            safe_float(analysis_data.get('optimization_timeline', 6)),
            safe_float(analysis_data.get('historical_data_months', 12)),
        ])
        
        # اضافه کردن ویژگی‌های لیستی با بررسی نوع داده
        product_categories = analysis_data.get('product_categories', [])
        if isinstance(product_categories, list):
            features.append(len(product_categories))
        elif isinstance(product_categories, str):
            features.append(1)  # اگر رشته باشد، یک دسته‌بندی در نظر می‌گیریم
        else:
            features.append(0)
        
        peak_days = analysis_data.get('peak_days', [])
        if isinstance(peak_days, list):
            features.append(len(peak_days))
        elif isinstance(peak_days, str):
            features.append(1)  # اگر رشته باشد، یک روز اوج در نظر می‌گیریم
        else:
            features.append(0)
        
        return np.array(features).reshape(1, -1)
    
    def _predict_sales(self, features) -> Dict[str, Any]:
        """پیش‌بینی فروش با ML"""
        try:
            # اینجا باید مدل آموزش دیده باشد
            # برای نمونه، از یک الگوریتم ساده استفاده می‌کنیم
            store_size = float(features[0, 0])
            conversion_rate = float(features[0, 4])
            customer_traffic = float(features[0, 5])
            
            # محاسبه فروش پیش‌بینی شده
            predicted_sales = customer_traffic * (conversion_rate / 100) * 1000  # متوسط خرید 1000 تومان
            
            # محاسبه پتانسیل بهبود
            improvement_potential = min(50, (50 - conversion_rate) * 2)
            
            return {
                "current_daily_sales": predicted_sales,
                "potential_daily_sales": predicted_sales * (1 + improvement_potential / 100),
                "improvement_potential": improvement_potential,
                "confidence": 0.85
            }
            
        except Exception as e:
            logger.error(f"Error in sales prediction: {e}")
            return {"error": str(e)}
    
    def _predict_conversion_improvement(self, features) -> Dict[str, Any]:
        """پیش‌بینی بهبود نرخ تبدیل"""
        try:
            current_conversion = float(features[0, 4])
            store_size = float(features[0, 0])
            unused_area = float(features[0, 7])
            
            # عوامل بهبود
            layout_improvement = min(15, (store_size - unused_area) / store_size * 20)
            checkout_improvement = min(10, float(features[0, 2]) * 2)  # بر اساس تعداد صندوق‌ها
            lighting_improvement = 5  # بهبود نورپردازی
            
            total_improvement = layout_improvement + checkout_improvement + lighting_improvement
            
            return {
                "current_conversion_rate": current_conversion,
                "predicted_improvement": total_improvement,
                "new_conversion_rate": min(100, current_conversion + total_improvement),
                "factors": {
                    "layout": layout_improvement,
                    "checkout": checkout_improvement,
                    "lighting": lighting_improvement
                },
                "confidence": 0.80
            }
            
        except Exception as e:
            logger.error(f"Error in conversion prediction: {e}")
            return {"error": str(e)}
    
    def _analyze_customer_behavior(self, features) -> Dict[str, Any]:
        """تحلیل رفتار مشتری"""
        try:
            dwell_time = float(features[0, 6])
            traffic = float(features[0, 5])
            conversion = float(features[0, 4])
            
            # طبقه‌بندی رفتار
            if dwell_time > 60 and conversion > 40:
                behavior_type = "high_engagement"
                description = "مشتریان با تعامل بالا و نرخ تبدیل خوب"
            elif dwell_time > 30 and conversion > 30:
                behavior_type = "moderate_engagement"
                description = "مشتریان با تعامل متوسط"
            else:
                behavior_type = "low_engagement"
                description = "نیاز به بهبود تعامل مشتری"
            
            return {
                "behavior_type": behavior_type,
                "description": description,
                "engagement_score": min(100, (dwell_time / 60) * 50 + (conversion / 50) * 50),
                "recommendations": self._get_behavior_recommendations(behavior_type),
                "practical_guide": self._generate_practical_recommendations(features)
            }
            
        except Exception as e:
            logger.error(f"Error in behavior analysis: {e}")
            return {"error": str(e)}
    
    def _get_behavior_recommendations(self, behavior_type: str) -> List[str]:
        """پیشنهادات بر اساس نوع رفتار"""
        recommendations = {
            "high_engagement": [
                "حفظ کیفیت خدمات",
                "افزایش تنوع محصولات",
                "برنامه‌های وفاداری"
            ],
            "moderate_engagement": [
                "بهبود چیدمان",
                "افزایش تعامل",
                "بهینه‌سازی مسیرها"
            ],
            "low_engagement": [
                "بازطراحی کامل",
                "آموزش کارکنان",
                "بهبود تجربه مشتری"
            ]
        }
        return recommendations.get(behavior_type, [])
    
    def _generate_practical_recommendations(self, features) -> Dict[str, Any]:
        """تولید راهنمایی‌های عملی چیدمان"""
        try:
            store_size = float(features[0, 0])
            entrance_count = float(features[0, 1])
            checkout_count = float(features[0, 2])
            shelf_count = float(features[0, 3])
            conversion_rate = float(features[0, 4])
            customer_traffic = float(features[0, 5])
            unused_area = float(features[0, 7])
            
            practical_guide = {
                "window_display": self._get_window_display_guide(store_size, conversion_rate),
                "shelf_layout": self._get_shelf_layout_guide(shelf_count, store_size),
                "path_design": self._get_path_design_guide(store_size, customer_traffic),
                "lighting": self._get_lighting_guide(store_size, conversion_rate),
                "color_scheme": self._get_color_scheme_guide(conversion_rate),
                "product_placement": self._get_product_placement_guide(shelf_count, conversion_rate)
            }
            
            return practical_guide
            
        except Exception as e:
            logger.error(f"Error generating practical recommendations: {e}")
            return {"error": str(e)}
    
    def _get_window_display_guide(self, store_size: float, conversion_rate: float) -> Dict[str, Any]:
        """راهنمای طراحی ویترین"""
        height = "1.2-1.8 متر" if store_size > 200 else "1.0-1.6 متر"
        lighting = "LED 3000K" if conversion_rate < 40 else "LED 4000K"
        
        return {
            "height": height,
            "lighting": lighting,
            "color_rule": "قانون 60-30-10",
            "product_count": "3-5 محصول اصلی",
            "rotation_frequency": "هفتگی",
            "tips": [
                "محصولات پرفروش در مرکز ویترین",
                "استفاده از پس‌زمینه ساده",
                "نورپردازی یکنواخت",
                "تغییر منظم محتوا"
            ]
        }
    
    def _get_shelf_layout_guide(self, shelf_count: float, store_size: float) -> Dict[str, Any]:
        """راهنمای چیدمان قفسه‌ها"""
        shelf_height = "0.3-2.1 متر"
        aisle_width = "1.2-1.8 متر" if store_size > 300 else "1.0-1.5 متر"
        
        return {
            "shelf_heights": {
                "bottom": "0.3-0.6 متر",
                "middle": "0.6-1.5 متر",
                "top": "1.5-2.1 متر"
            },
            "aisle_width": aisle_width,
            "product_arrangement": "محصولات پرفروش در سطح چشم (1.5 متر)",
            "spacing": "فاصله 15-20 سانتی‌متر بین محصولات",
            "tips": [
                "اجتناب از بن‌بست",
                "دسترسی آسان به همه محصولات",
                "استفاده از تابلوهای راهنما",
                "نظم و ترتیب منظم"
            ]
        }
    
    def _get_path_design_guide(self, store_size: float, customer_traffic: float) -> Dict[str, Any]:
        """راهنمای طراحی مسیر"""
        main_path_width = "2.4-3.0 متر" if customer_traffic > 100 else "2.0-2.4 متر"
        secondary_path_width = "1.8-2.4 متر"
        
        return {
            "main_path": {
                "width": main_path_width,
                "direction": "از ورودی تا صندوق",
                "products": "محصولات پرفروش در کنار مسیر"
            },
            "secondary_paths": {
                "width": secondary_path_width,
                "purpose": "دسترسی به بخش‌های مختلف"
            },
            "stopping_points": {
                "size": "1.5×1.5 متر",
                "purpose": "بررسی محصولات"
            },
            "tips": [
                "مسیر طبیعی و بدون مانع",
                "نقاط توقف استراتژیک",
                "دسترسی آسان به صندوق",
                "فضای کافی برای سبد خرید"
            ]
        }
    
    def _get_lighting_guide(self, store_size: float, conversion_rate: float) -> Dict[str, Any]:
        """راهنمای نورپردازی"""
        intensity = "500-800 لوکس" if conversion_rate < 40 else "300-500 لوکس"
        color_temp = "3000K (گرم)" if store_size < 200 else "4000K (خنثی)"
        
        return {
            "general_lighting": {
                "intensity": intensity,
                "color_temperature": color_temp,
                "type": "LED"
            },
            "accent_lighting": {
                "purpose": "تأکید بر محصولات خاص",
                "intensity": "800-1200 لوکس",
                "color_temperature": "2700K"
            },
            "tips": [
                "نورپردازی یکنواخت",
                "اجتناب از سایه‌های تیز",
                "استفاده از نور طبیعی",
                "کنترل نورپردازی بر اساس ساعت"
            ]
        }
    
    def _get_color_scheme_guide(self, conversion_rate: float) -> Dict[str, Any]:
        """راهنمای ترکیب رنگی"""
        if conversion_rate < 30:
            scheme = "گرم و انرژی‌بخش"
            colors = ["قرمز", "نارنجی", "زرد"]
        elif conversion_rate < 45:
            scheme = "متعادل و متوازن"
            colors = ["آبی", "سبز", "خاکستری"]
        else:
            scheme = "لوکس و آرام"
            colors = ["بنفش", "سفید", "سیاه"]
        
        return {
            "scheme": scheme,
            "primary_colors": colors,
            "rule": "قانون 60-30-10",
            "usage": {
                "60%": "رنگ اصلی (پس‌زمینه)",
                "30%": "رنگ ثانویه (قاب‌بندی)",
                "10%": "رنگ تأکیدی (جزئیات)"
            }
        }
    
    def _get_product_placement_guide(self, shelf_count: float, conversion_rate: float) -> Dict[str, Any]:
        """راهنمای قرارگیری محصولات"""
        return {
            "high_traffic_areas": [
                "کنار ورودی",
                "نزدیک صندوق",
                "انتهای مسیرهای اصلی"
            ],
            "product_arrangement": {
                "eye_level": "محصولات پرفروش",
                "top_shelf": "محصولات جدید",
                "bottom_shelf": "محصولات حجیم"
            },
            "cross_selling": {
                "strategy": "محصولات مرتبط در کنار هم",
                "examples": [
                    "کفش و جوراب",
                    "لباس و اکسسوری",
                    "مواد غذایی و نوشیدنی"
                ]
            },
            "seasonal_placement": {
                "front": "محصولات فصلی",
                "back": "محصولات همیشگی"
            }
        }
    
    def _get_optimization_priority(self, features) -> Dict[str, Any]:
        """اولویت‌بندی بهینه‌سازی"""
        try:
            priorities = []
            
            # محاسبه امتیاز برای هر بخش
            layout_score = 100 - (float(features[0, 7]) / float(features[0, 0]) * 100)  # فضای بلااستفاده
            checkout_score = float(features[0, 2]) * 10  # تعداد صندوق‌ها
            conversion_score = float(features[0, 4])  # نرخ تبدیل
            traffic_score = float(features[0, 5]) / 10  # ترافیک
            
            # اولویت‌بندی
            if layout_score < 70:
                priorities.append({"area": "layout", "priority": "high", "score": layout_score})
            if checkout_score < 30:
                priorities.append({"area": "checkout", "priority": "high", "score": checkout_score})
            if conversion_score < 35:
                priorities.append({"area": "conversion", "priority": "medium", "score": conversion_score})
            if traffic_score < 10:
                priorities.append({"area": "traffic", "priority": "low", "score": traffic_score})
            
            return {
                "priorities": sorted(priorities, key=lambda x: x["score"]),
                "overall_score": (layout_score + checkout_score + conversion_score + traffic_score) / 4
            }
            
        except Exception as e:
            logger.error(f"Error in optimization priority: {e}")
            return {"error": str(e)}
    
    def _predict_roi(self, features) -> Dict[str, Any]:
        """پیش‌بینی بازگشت سرمایه"""
        try:
            current_sales = float(features[0, 9])  # فروش روزانه
            improvement_target = float(features[0, 15])  # هدف بهبود
            timeline = float(features[0, 16])  # بازه زمانی
            
            # محاسبه ROI
            additional_sales = current_sales * (improvement_target / 100) * 365  # فروش سالانه اضافی
            estimated_cost = current_sales * 0.1 * timeline  # هزینه تخمینی (10% فروش فعلی)
            roi = (additional_sales - estimated_cost) / estimated_cost * 100
            
            return {
                "current_annual_sales": current_sales * 365,
                "additional_annual_sales": additional_sales,
                "estimated_cost": estimated_cost,
                "roi_percentage": roi,
                "payback_period": timeline,
                "confidence": 0.75
            }
            
        except Exception as e:
            logger.error(f"Error in ROI prediction: {e}")
            return {"error": str(e)}
    
    def _analyze_patterns(self, features) -> Dict[str, Any]:
        """تحلیل الگوها"""
        try:
            patterns = {
                "traffic_patterns": self._analyze_traffic_patterns(features),
                "sales_patterns": self._analyze_sales_patterns(features),
                "seasonal_patterns": self._analyze_seasonal_patterns(features)
            }
            return patterns
            
        except Exception as e:
            logger.error(f"Error in pattern analysis: {e}")
            return {"error": str(e)}
    
    def _analyze_traffic_patterns(self, features) -> Dict[str, Any]:
        """تحلیل الگوهای ترافیک"""
        morning = float(features[0, 11])
        noon = float(features[0, 12])
        evening = float(features[0, 13])
        
        peak_period = "morning" if morning > max(noon, evening) else "noon" if noon > evening else "evening"
        
        return {
            "peak_period": peak_period,
            "distribution": {
                "morning": morning,
                "noon": noon,
                "evening": evening
            },
            "recommendations": self._get_traffic_recommendations(peak_period)
        }
    
    def _get_traffic_recommendations(self, peak_period: str) -> List[str]:
        """پیشنهادات بر اساس دوره پیک"""
        recommendations = {
            "morning": [
                "افزایش کارکنان در ساعات صبح",
                "بهینه‌سازی موجودی برای ساعات صبح",
                "برنامه‌های تشویقی صبحگاهی"
            ],
            "noon": [
                "بهینه‌سازی صندوق‌ها برای ساعات شلوغی",
                "برنامه‌های ناهار",
                "مدیریت صف هوشمند"
            ],
            "evening": [
                "افزایش نورپردازی",
                "برنامه‌های عصرگاهی",
                "بهینه‌سازی مسیرهای خروج"
            ]
        }
        return recommendations.get(peak_period, [])
    
    def _analyze_sales_patterns(self, features) -> Dict[str, Any]:
        """تحلیل الگوهای فروش"""
        conversion_rate = float(features[0, 4])
        customer_traffic = float(features[0, 5])
        
        efficiency_score = (conversion_rate / 50) * (customer_traffic / 200) * 100
        
        return {
            "efficiency_score": efficiency_score,
            "performance_level": "high" if efficiency_score > 70 else "medium" if efficiency_score > 40 else "low",
            "optimization_potential": 100 - efficiency_score
        }
    
    def _analyze_seasonal_patterns(self, features) -> Dict[str, Any]:
        """تحلیل الگوهای فصلی"""
        # این بخش نیاز به داده‌های تاریخی دارد
        return {
            "note": "تحلیل فصلی نیاز به داده‌های تاریخی دارد",
            "recommendation": "جمع‌آوری داده‌های فروش ماهانه برای تحلیل فصلی"
        }
    
    def _generate_ml_recommendations(self, features, predictions: Dict) -> Dict[str, Any]:
        """تولید پیشنهادات مبتنی بر ML"""
        try:
            recommendations = {
                "immediate": [],
                "short_term": [],
                "long_term": []
            }
            
            # پیشنهادات فوری بر اساس تحلیل
            if predictions.get("conversion_optimization", {}).get("predicted_improvement", 0) > 10:
                recommendations["immediate"].append("بهینه‌سازی فوری چیدمان برای بهبود نرخ تبدیل")
            
            if float(features[0, 7]) > float(features[0, 0]) * 0.2:  # فضای بلااستفاده > 20%
                recommendations["immediate"].append("بازطراحی فوری فضای بلااستفاده")
            
            # پیشنهادات کوتاه مدت
            if predictions.get("roi_prediction", {}).get("roi_percentage", 0) > 50:
                recommendations["short_term"].append("پیاده‌سازی برنامه‌های بهبود با ROI بالا")
            
            # پیشنهادات بلند مدت
            if predictions.get("sales_prediction", {}).get("improvement_potential", 0) > 30:
                recommendations["long_term"].append("بازسازی کامل فروشگاه برای حداکثر پتانسیل")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating ML recommendations: {e}")
            return {"error": str(e)}
    
    def _calculate_confidence_scores(self, features) -> Dict[str, float]:
        """محاسبه امتیازات اطمینان"""
        try:
            # محاسبه اطمینان بر اساس کیفیت داده‌ها
            data_completeness = min(100, np.count_nonzero(features) / len(features) * 100)
            data_consistency = 85  # فرض بر این که داده‌ها سازگار هستند
            
            return {
                "data_completeness": data_completeness,
                "data_consistency": data_consistency,
                "overall_confidence": (data_completeness + data_consistency) / 2
            }
            
        except Exception as e:
            logger.error(f"Error calculating confidence scores: {e}")
            return {"error": str(e)}
    
    def _generate_openai_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """تولید تحلیل با OpenAI"""
        try:
            # آماده‌سازی داده‌ها برای AI
            store_info = self._prepare_store_info(analysis_data)
            
            # پرامپت برای تحلیل
            prompt = f"""
            شما یک متخصص تحلیل فروشگاه و بهینه‌سازی تجارت هستید. 
            لطفاً تحلیل تفصیلی و راهنمایی‌های عملی برای فروشگاه زیر ارائه دهید:

            اطلاعات فروشگاه:
            {store_info}

            لطفاً تحلیل خود را در قالب JSON با ساختار زیر ارائه دهید:
            {{
                "executive_summary": "خلاصه اجرایی",
                "detailed_analysis": {{
                    "strengths": ["نقاط قوت"],
                    "weaknesses": ["نقاط ضعف"],
                    "opportunities": ["فرصت‌ها"],
                    "threats": ["تهدیدها"]
                }},
                "recommendations": {{
                    "immediate": ["اقدامات فوری"],
                    "short_term": ["اقدامات کوتاه مدت"],
                    "long_term": ["اقدامات بلند مدت"]
                }},
                "optimization_plan": {{
                    "layout_optimization": "بهینه‌سازی چیدمان",
                    "pricing_strategy": "استراتژی قیمت‌گذاری",
                    "inventory_management": "مدیریت موجودی",
                    "customer_experience": "تجربه مشتری"
                }},
                "financial_projections": {{
                    "sales_increase": "درصد افزایش فروش",
                    "cost_reduction": "درصد کاهش هزینه",
                    "roi_timeline": "زمان بازگشت سرمایه"
                }},
                "implementation_timeline": {{
                    "phase_1": "فاز اول (1-2 ماه)",
                    "phase_2": "فاز دوم (3-6 ماه)",
                    "phase_3": "فاز سوم (6-12 ماه)"
                }}
            }}
            """
            
            # ارسال درخواست به OpenAI
            response = self.openai_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "شما یک متخصص تحلیل فروشگاه و بهینه‌سازی تجارت هستید."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            # پردازش پاسخ
            ai_response = response.choices[0].message.content
            analysis_result = json.loads(ai_response)
            
            # اضافه کردن متادیتا
            analysis_result['generated_at'] = datetime.now().isoformat()
            analysis_result['ai_model'] = 'gpt-3.5-turbo'
            analysis_result['confidence_score'] = 0.95
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"خطا در تحلیل OpenAI: {e}")
            return self._generate_local_analysis(analysis_data)
    
    def _generate_local_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """تولید تحلیل محلی شخصی‌سازی شده (بدون نیاز به API)"""
        
        # استخراج داده‌های کلیدی
        store_name = analysis_data.get('store_name', 'فروشگاه')
        store_type = analysis_data.get('store_type', 'عمومی')
        store_size = analysis_data.get('store_size', 500)
        daily_customers = analysis_data.get('daily_customers', 150)
        daily_sales = analysis_data.get('daily_sales', 'نامشخص')
        entrance_count = analysis_data.get('entrance_count', 2)
        checkout_count = analysis_data.get('checkout_count', 3)
        conversion_rate = analysis_data.get('conversion_rate', 35.5)
        customer_traffic = analysis_data.get('customer_traffic', 150)
        customer_dwell_time = analysis_data.get('customer_dwell_time', 45)
        unused_area_size = analysis_data.get('unused_area_size', 0)
        daily_sales_volume = analysis_data.get('daily_sales_volume', 0)
        product_categories = analysis_data.get('product_categories', [])
        has_surveillance = analysis_data.get('has_surveillance', False)
        
        # بررسی فایل‌های آپلود شده
        uploaded_files_count = sum([
            1 if analysis_data.get('store_photos') else 0,
            1 if analysis_data.get('store_plan') else 0,
            1 if analysis_data.get('shelf_photos') else 0,
            1 if analysis_data.get('entrance_photos') else 0,
            1 if analysis_data.get('checkout_photos') else 0,
            1 if analysis_data.get('customer_video') else 0,
            1 if analysis_data.get('surveillance_footage') else 0,
            1 if analysis_data.get('sales_file') else 0,
            1 if analysis_data.get('product_catalog') else 0,
        ])
        
        # تحلیل نقاط قوت شخصی‌سازی شده
        strengths = []
        if entrance_count >= 2:
            strengths.append(f"فروشگاه {store_name} شما برخورداری از تعداد کافی ورودی برای تسهیل جریان {daily_customers} مشتری روزانه")
        if checkout_count >= 3:
            strengths.append(f"ظرفیت مناسب صندوق‌های پرداخت در {store_name} برای خدمت‌رسانی بهتر")
        if conversion_rate > 30:
            strengths.append(f"نرخ تبدیل قابل قبول در {store_name} نشان‌دهنده عملکرد خوب است")
        if customer_traffic > 100:
            strengths.append(f"ترافیک {daily_customers} مشتری روزانه در {store_name} مطلوب است")
        if customer_dwell_time > 30:
            strengths.append(f"زمان حضور مناسب مشتریان در فروشگاه {store_name}")
        if has_surveillance:
            strengths.append(f"وجود سیستم نظارت و امنیت در {store_name} برای تحلیل بهتر")
        if len(product_categories) > 3:
            strengths.append(f"تنوع مناسب در دسته‌بندی محصولات {store_name}")
        if uploaded_files_count > 5:
            strengths.append(f"ارائه اطلاعات و مستندات جامع برای {store_name}")
        if analysis_data.get('customer_video'):
            strengths.append(f"دسترسی به ویدیوی رفتار مشتریان {store_name} برای تحلیل دقیق‌تر")
        if analysis_data.get('sales_file'):
            strengths.append(f"داشتن داده‌های فروش تاریخی {store_name} برای تحلیل روندها")
        
        # تحلیل نقاط ضعف شخصی‌سازی شده
        weaknesses = []
        if conversion_rate < 40:
            weaknesses.append(f"نیاز به بهبود نرخ تبدیل مشتریان در {store_name}")
        if entrance_count < 3:
            weaknesses.append(f"محدودیت در تعداد ورودی‌های فروشگاه {store_name}")
        if checkout_count < 4:
            weaknesses.append(f"ظرفیت ناکافی صندوق‌های پرداخت {store_name} در ساعات شلوغی")
        if customer_dwell_time < 30:
            weaknesses.append(f"کوتاه بودن زمان حضور مشتریان در فروشگاه {store_name}")
        if unused_area_size > store_size * 0.2:
            weaknesses.append(f"بلااستفاده ماندن حدود {int(unused_area_size/store_size*100)}% از فضای فروشگاه {store_name}")
        if not has_surveillance:
            weaknesses.append(f"عدم وجود سیستم نظارت برای تحلیل رفتار مشتریان {store_name}")
        if uploaded_files_count < 3:
            weaknesses.append(f"عدم ارائه مستندات و تصاویر کافی برای تحلیل دقیق {store_name}")
        if not analysis_data.get('customer_video') and not analysis_data.get('surveillance_footage'):
            weaknesses.append(f"عدم دسترسی به ویدیو برای تحلیل رفتار مشتریان {store_name}")
        if not analysis_data.get('sales_file'):
            weaknesses.append(f"عدم ارائه داده‌های فروش برای تحلیل روندهای {store_name}")
        
        # فرصت‌های شخصی‌سازی شده
        opportunities = [
            f"امکان بهبود نرخ تبدیل {store_name} از طریق بهینه‌سازی چیدمان فروشگاه",
            f"افزایش زمان حضور مشتریان {store_name} با طراحی بهتر فضای فروشگاه",
            f"بهینه‌سازی جریان حرکت {daily_customers} مشتری روزانه در {store_name}",
            f"پیاده‌سازی سیستم مدیریت صف هوشمند در {store_name}",
            f"بهبود رنگ‌بندی و چیدمان محصولات {store_name} برای جلب توجه بیشتر",
            f"استفاده از تکنیک‌های روانشناسی رنگ در {store_name}",
            f"ایجاد نقاط کانونی جذاب در {store_name}",
            f"بهینه‌سازی ارتفاع و فاصله‌گذاری محصولات در {store_name}"
        ]
        
        if unused_area_size > 0:
            opportunities.append(f"امکان بهره‌برداری از {unused_area_size} متر مربع فضای بلااستفاده {store_name}")
        
        if not has_surveillance:
            opportunities.append(f"پیاده‌سازی سیستم نظارت برای تحلیل دقیق‌تر رفتار مشتریان {store_name}")
        
        if daily_sales_volume > 0:
            opportunities.append("بهینه‌سازی استراتژی قیمت‌گذاری بر اساس داده‌های فروش")
        
        if analysis_data.get('customer_video'):
            opportunities.append("امکان تحلیل ویدیویی رفتار مشتریان با استفاده از هوش مصنوعی")
        if analysis_data.get('store_photos'):
            opportunities.append("امکان تحلیل تصویری چیدمان با استفاده از تکنولوژی‌های پیشرفته")
        if analysis_data.get('sales_file'):
            opportunities.append("امکان پیش‌بینی فروش با استفاده از یادگیری ماشین")
        
        # تهدیدها
        threats = [
            "رقابت فزاینده با فروشگاه‌های مجاور",
            "تغییرات احتمالی در رفتار خرید مشتریان",
            "افزایش مستمر هزینه‌های عملیاتی"
        ]
        
        if unused_area_size > store_size * 0.3:
            threats.append("هدررفت سرمایه در فضای بلااستفاده")
        
        # پیشنهادات شخصی‌سازی شده
        recommendations = {
            "immediate": [
                f"بهینه‌سازی چیدمان قفسه‌ها و محصولات {store_name}",
                f"نصب تابلوهای راهنما و اطلاعات در {store_name}",
                f"بهبود سیستم نورپردازی فروشگاه {store_name}",
                f"بهبود رنگ‌بندی و چیدمان محصولات {store_name}",
                f"ایجاد نقاط کانونی جذاب در {store_name}"
            ],
            "short_term": [
                f"افزایش تعداد صندوق‌های پرداخت {store_name}",
                f"پیاده‌سازی سیستم مدیریت صف در {store_name}",
                f"بهبود استراتژی قیمت‌گذاری محصولات {store_name}",
                f"استفاده از تکنیک‌های روانشناسی رنگ در {store_name}",
                f"بهینه‌سازی ارتفاع و فاصله‌گذاری محصولات در {store_name}"
            ],
            "long_term": [
                f"بازسازی کامل فضای فروشگاه {store_name}",
                f"پیاده‌سازی سیستم‌های هوشمند مدیریت {store_name}",
                f"گسترش فضای فروشگاه {store_name} و تنوع محصولات",
                f"ایجاد سیستم رنگ‌بندی پیشرفته در {store_name}",
                f"پیاده‌سازی تکنولوژی‌های جلب توجه در {store_name}"
            ]
        }
        
        # اضافه کردن پیشنهادات خاص بر اساس داده‌ها
        if unused_area_size > 0:
            recommendations["immediate"].append(f"بازطراحی و بهره‌برداری از {unused_area_size} متر مربع فضای بلااستفاده {store_name}")
        
        if not has_surveillance:
            recommendations["short_term"].append(f"نصب سیستم دوربین نظارتی و امنیتی در {store_name}")
        
        if customer_dwell_time < 30:
            recommendations["immediate"].append(f"بهبود طراحی مسیرهای حرکت مشتریان در {store_name}")
        
        # محاسبه پتانسیل بهبود (قبل از استفاده)
        conversion_improvement = min(25, (50 - conversion_rate) * 1.5)  # بهبود نرخ تبدیل
        traffic_improvement = min(20, (500 - customer_traffic) / 500 * 30)  # بهبود ترافیک
        space_improvement = min(15, (unused_area_size / store_size) * 30) if unused_area_size > 0 else 0
        
        # برنامه بهینه‌سازی شخصی‌سازی شده
        optimization_plan = {
            "layout_optimization": f"بازطراحی چیدمان فروشگاه {store_name} برای افزایش {conversion_improvement:.1f}% نرخ تبدیل (از {conversion_rate}% به {conversion_rate + conversion_improvement:.1f}%)",
            "traffic_optimization": f"بهبود جریان حرکت {daily_customers} مشتری روزانه در {store_name} برای افزایش {traffic_improvement:.1f}% ترافیک",
            "space_utilization": f"بهره‌برداری از {unused_area_size} متر مربع فضای بلااستفاده {store_name} برای {space_improvement:.1f}% بهبود فروش",
            "pricing_strategy": f"پیاده‌سازی استراتژی قیمت‌گذاری پویا در {store_name} بر اساس تحلیل رفتار مشتریان",
            "inventory_management": f"بهینه‌سازی مدیریت موجودی {store_name} بر اساس الگوی فروش و پیش‌بینی تقاضا",
            "customer_experience": f"بهبود تجربه مشتریان {store_name} با طراحی بهتر مسیرها و کاهش زمان انتظار",
            "technology_integration": f"پیاده‌سازی سیستم‌های هوشمند برای مدیریت بهتر عملیات فروشگاه {store_name}",
            "color_psychology": f"استفاده از روانشناسی رنگ در {store_name} برای جلب توجه و افزایش فروش",
            "product_arrangement": f"بهینه‌سازی چیدمان محصولات {store_name} بر اساس رنگ‌بندی و جلب توجه",
            "visual_merchandising": f"پیاده‌سازی تکنیک‌های نمایش بصری در {store_name} برای جلب توجه مشتریان"
        }
        
        # پیش‌بینی مالی واقعی‌تر
        # محاسبه فروش فعلی
        current_daily_sales = customer_traffic * (conversion_rate / 100) * 15000  # متوسط خرید 15,000 تومان
        current_monthly_sales = current_daily_sales * 30
        current_yearly_sales = current_monthly_sales * 12
        
        total_sales_improvement = conversion_improvement + traffic_improvement + space_improvement
        
        # محاسبه فروش جدید
        new_daily_sales = current_daily_sales * (1 + total_sales_improvement / 100)
        additional_monthly_sales = (new_daily_sales - current_daily_sales) * 30
        additional_yearly_sales = additional_monthly_sales * 12
        
        # محاسبه هزینه‌ها و ROI
        implementation_cost = current_yearly_sales * 0.15  # 15% فروش سالانه
        operational_cost_reduction = current_yearly_sales * 0.08  # 8% کاهش هزینه‌های عملیاتی
        theft_reduction = current_yearly_sales * 0.02 if not has_surveillance else 0  # 2% کاهش سرقت
        
        total_cost_reduction = operational_cost_reduction + theft_reduction
        net_benefit = additional_yearly_sales + total_cost_reduction - implementation_cost
        roi_percentage = (net_benefit / implementation_cost) * 100 if implementation_cost > 0 else 0
        payback_period = implementation_cost / (additional_monthly_sales + total_cost_reduction / 12) if (additional_monthly_sales + total_cost_reduction / 12) > 0 else 0
        
        financial_projections = {
            "current_daily_sales": f"{current_daily_sales:,.0f} تومان",
            "current_monthly_sales": f"{current_monthly_sales:,.0f} تومان",
            "current_yearly_sales": f"{current_yearly_sales:,.0f} تومان",
            "new_daily_sales": f"{new_daily_sales:,.0f} تومان",
            "additional_monthly_sales": f"{additional_monthly_sales:,.0f} تومان",
            "additional_yearly_sales": f"{additional_yearly_sales:,.0f} تومان",
            "sales_increase_percentage": f"{total_sales_improvement:.1f}%",
            "implementation_cost": f"{implementation_cost:,.0f} تومان",
            "cost_reduction_percentage": f"{((total_cost_reduction / current_yearly_sales) * 100):.1f}%",
            "roi_percentage": f"{roi_percentage:.1f}%",
            "payback_period_months": f"{payback_period:.1f} ماه",
            "net_benefit_yearly": f"{net_benefit:,.0f} تومان"
        }
        
        # جدول زمانی پیاده‌سازی شخصی‌سازی شده
        implementation_timeline = {
            "phase_1": f"بهینه‌سازی چیدمان فروشگاه {store_name}، سیستم نورپردازی و رنگ‌بندی محصولات",
            "phase_2": f"افزایش صندوق‌های پرداخت {store_name}، پیاده‌سازی سیستم مدیریت صف و بهبود چیدمان محصولات",
            "phase_3": f"بازسازی کامل فضای فروشگاه {store_name}، پیاده‌سازی سیستم‌های هوشمند و تکنیک‌های جلب توجه"
        }
        
        if unused_area_size > 0:
            implementation_timeline["phase_1"] += f" و بازطراحی {unused_area_size} متر مربع فضای بلااستفاده {store_name}"
        
        # تولید راهنمایی‌های عملی
        features = self._extract_ml_features(analysis_data)
        practical_guide = self._generate_practical_recommendations(features)
        
        # تولید توصیه‌های تخصصی رنگ‌بندی و چیدمان
        color_layout_recommendations = self._generate_color_and_layout_recommendations(
            store_name, 
            store_type, 
            analysis_data.get('product_categories', [])
        )
        
        return {
            "executive_summary": f"سلام! من به عنوان یک متخصص طراحی فروشگاه، تحلیل کاملی از فروشگاه {store_name} شما انجام داده‌ام. فروشگاه {store_name} شما با نرخ تبدیل {conversion_rate}% و {daily_customers} مشتری روزانه، در حال حاضر فروش روزانه‌ای معادل {current_daily_sales:,.0f} تومان دارد. با اجرای برنامه‌های بهینه‌سازی چیدمان و افزایش نرخ تبدیل به {conversion_rate + conversion_improvement:.1f}%، همچنین بهره‌برداری از {unused_area_size} متر مربع فضای بلااستفاده، فروش روزانه {store_name} شما به {new_daily_sales:,.0f} تومان افزایش خواهد یافت. این بهبودها منجر به {total_sales_improvement:.1f}% رشد فروش، بازده سرمایه‌گذاری {roi_percentage:.1f}% و بازگشت سرمایه در مدت {payback_period:.1f} ماه خواهد شد. تمام این توصیه‌ها مخصوص فروشگاه {store_name} شما طراحی شده‌اند.",
            "detailed_analysis": {
                "strengths": strengths,
                "weaknesses": weaknesses,
                "opportunities": opportunities,
                "threats": threats
            },
            "recommendations": recommendations,
            "optimization_plan": optimization_plan,
            "financial_projections": financial_projections,
            "implementation_timeline": implementation_timeline,
            "practical_guide": practical_guide,
            "color_layout_recommendations": color_layout_recommendations,
            "generated_at": datetime.now().isoformat(),
            "ai_model": "ollama_personalized_analysis",
            "confidence_score": 0.95,
            "personalized": True,
            "store_name": store_name,
            "analysis_type": "detailed_personalized"
        }
    
    def _prepare_store_info(self, analysis_data: Dict[str, Any]) -> str:
        """آماده‌سازی اطلاعات شخصی‌سازی شده فروشگاه برای AI"""
        store_name = analysis_data.get('store_name', 'فروشگاه')
        info_parts = []
        
        # اطلاعات پایه شخصی‌سازی شده
        info_parts.append(f"نام فروشگاه: {store_name}")
        info_parts.append(f"نوع فروشگاه: {analysis_data.get('store_type', 'نامشخص')}")
        info_parts.append(f"اندازه فروشگاه {store_name}: {analysis_data.get('store_size', 'نامشخص')} متر مربع")
        
        # اطلاعات تکمیلی
        if analysis_data.get('store_location'):
            info_parts.append(f"آدرس: {analysis_data.get('store_location')}")
        if analysis_data.get('city'):
            info_parts.append(f"شهر: {analysis_data.get('city')}")
        if analysis_data.get('area'):
            info_parts.append(f"منطقه: {analysis_data.get('area')}")
        if analysis_data.get('establishment_year'):
            info_parts.append(f"سال تاسیس: {analysis_data.get('establishment_year')}")
        
        # اطلاعات فیزیکی شخصی‌سازی شده
        info_parts.append(f"تعداد ورودی‌های {store_name}: {analysis_data.get('entrance_count', 0)}")
        info_parts.append(f"تعداد صندوق‌های {store_name}: {analysis_data.get('checkout_count', 0)}")
        info_parts.append(f"تعداد قفسه‌های {store_name}: {analysis_data.get('shelf_count', 0)}")
        
        # اطلاعات دقیق‌تر چیدمان
        if analysis_data.get('shelf_dimensions'):
            info_parts.append(f"ابعاد قفسه‌ها: {analysis_data.get('shelf_dimensions')}")
        if analysis_data.get('shelf_contents'):
            info_parts.append(f"محتوای قفسه‌ها: {analysis_data.get('shelf_contents')}")
        if analysis_data.get('unused_area_size'):
            info_parts.append(f"مناطق بلااستفاده: {analysis_data.get('unused_area_size')} متر مربع")
        if analysis_data.get('unused_area_type'):
            info_parts.append(f"نوع مناطق بلااستفاده: {analysis_data.get('unused_area_type')}")
        
        # طراحی و دکوراسیون
        if analysis_data.get('design_style'):
            info_parts.append(f"سبک طراحی: {analysis_data.get('design_style')}")
        if analysis_data.get('brand_colors'):
            info_parts.append(f"رنگ‌های برند: {analysis_data.get('brand_colors')}")
        info_parts.append(f"نورپردازی اصلی: {analysis_data.get('main_lighting', 'نامشخص')}")
        if analysis_data.get('lighting_intensity'):
            info_parts.append(f"شدت نورپردازی: {analysis_data.get('lighting_intensity')}")
        
        # اطلاعات عملکرد شخصی‌سازی شده
        info_parts.append(f"نرخ تبدیل {store_name}: {analysis_data.get('conversion_rate', 0)}%")
        info_parts.append(f"متوسط مشتریان روزانه {store_name}: {analysis_data.get('customer_traffic', 0)}")
        info_parts.append(f"متوسط زمان حضور مشتری در {store_name}: {analysis_data.get('customer_dwell_time', 0)} دقیقه")
        
        # اطلاعات ترافیک دقیق‌تر
        if analysis_data.get('peak_hours'):
            info_parts.append(f"ساعات پیک: {analysis_data.get('peak_hours')}")
        if analysis_data.get('high_traffic_areas'):
            info_parts.append(f"مناطق پرتردد: {analysis_data.get('high_traffic_areas')}")
        
        # اطلاعات فروش
        info_parts.append(f"درصد فروش صبح: {analysis_data.get('morning_sales_percent', 0)}%")
        info_parts.append(f"درصد فروش ظهر: {analysis_data.get('noon_sales_percent', 0)}%")
        info_parts.append(f"درصد فروش شب: {analysis_data.get('evening_sales_percent', 0)}%")
        
        # محصولات و فروش شخصی‌سازی شده
        if analysis_data.get('product_categories'):
            info_parts.append(f"دسته‌بندی محصولات {store_name}: {', '.join(analysis_data.get('product_categories', []))}")
        if analysis_data.get('top_products'):
            info_parts.append(f"محصولات پرفروش {store_name}: {analysis_data.get('top_products')}")
        if analysis_data.get('daily_sales_volume'):
            info_parts.append(f"فروش روزانه {store_name}: {analysis_data.get('daily_sales_volume')} تومان")
        if analysis_data.get('supplier_count'):
            info_parts.append(f"تعداد تامین‌کنندگان {store_name}: {analysis_data.get('supplier_count')}")
        
        # نظارت و امنیت شخصی‌سازی شده
        if analysis_data.get('has_surveillance'):
            info_parts.append(f"دوربین نظارتی {store_name}: بله")
            if analysis_data.get('camera_count'):
                info_parts.append(f"تعداد دوربین‌های {store_name}: {analysis_data.get('camera_count')}")
            if analysis_data.get('camera_locations'):
                info_parts.append(f"موقعیت دوربین‌های {store_name}: {analysis_data.get('camera_locations')}")
        else:
            info_parts.append(f"دوربین نظارتی {store_name}: خیر")
        
        # فایل‌ها و اطلاعات اضافی
        if analysis_data.get('pos_system'):
            info_parts.append(f"نرم‌افزار صندوق: {analysis_data.get('pos_system')}")
        if analysis_data.get('inventory_system'):
            info_parts.append(f"نرم‌افزار موجودی: {analysis_data.get('inventory_system')}")
        if analysis_data.get('video_date'):
            info_parts.append(f"تاریخ ضبط ویدیو: {analysis_data.get('video_date')}")
        if analysis_data.get('video_duration'):
            info_parts.append(f"مدت ویدیو: {analysis_data.get('video_duration')} ثانیه")
        
        # نوع فایل‌های آپلود شده شخصی‌سازی شده
        uploaded_files = []
        if analysis_data.get('store_photos'):
            uploaded_files.append(f"تصاویر فروشگاه {store_name}")
        if analysis_data.get('store_plan'):
            uploaded_files.append(f"نقشه فروشگاه {store_name}")
        if analysis_data.get('shelf_photos'):
            uploaded_files.append(f"تصاویر قفسه‌های {store_name}")
        if analysis_data.get('entrance_photos'):
            uploaded_files.append(f"تصاویر ورودی {store_name}")
        if analysis_data.get('checkout_photos'):
            uploaded_files.append(f"تصاویر صندوق {store_name}")
        if analysis_data.get('customer_video'):
            uploaded_files.append(f"ویدیوی مشتریان {store_name}")
        if analysis_data.get('surveillance_footage'):
            uploaded_files.append(f"فیلم دوربین نظارتی {store_name}")
        if analysis_data.get('sales_file'):
            uploaded_files.append(f"فایل فروش {store_name}")
        if analysis_data.get('product_catalog'):
            uploaded_files.append("کاتالوگ محصولات")
        
        if uploaded_files:
            info_parts.append(f"فایل‌های آپلود شده برای {store_name}: {', '.join(uploaded_files)}")
        
        return f"اطلاعات کامل فروشگاه {store_name}:\n" + "\n".join(info_parts)
    
    def _generate_color_and_layout_recommendations(self, store_name: str, store_type: str, product_categories: list) -> dict:
        """تولید توصیه‌های تخصصی رنگ‌بندی و چیدمان بر اساس نوع فروشگاه"""
        
        recommendations = {
            "color_psychology": {},
            "product_arrangement": {},
            "attention_grabbing": {},
            "specific_industry_tips": {}
        }
        
        # توصیه‌های رنگ‌بندی بر اساس نوع فروشگاه
        if "لباس" in store_type or "پوشاک" in store_type:
            recommendations["color_psychology"] = {
                "warm_colors": "استفاده از رنگ‌های گرم (قرمز، نارنجی، زرد) برای لباس‌های تابستانی و ورزشی",
                "cool_colors": "استفاده از رنگ‌های سرد (آبی، سبز، بنفش) برای لباس‌های رسمی و زمستانی",
                "neutral_colors": "استفاده از رنگ‌های خنثی (سفید، خاکستری، مشکی) برای لباس‌های کلاسیک",
                "contrast": "قرار دادن لباس‌های با رنگ‌های متضاد کنار هم برای جلب توجه"
            }
            
            recommendations["product_arrangement"] = {
                "height_placement": "قرار دادن لباس‌های پرفروش در ارتفاع 120-160 سانتی‌متر",
                "color_gradient": "ایجاد گرادیان رنگی از تیره به روشن در قفسه‌ها",
                "seasonal_grouping": "گروه‌بندی لباس‌ها بر اساس فصل و رنگ",
                "size_organization": "چیدمان لباس‌ها بر اساس سایز و رنگ"
            }
            
        elif "میوه" in store_type or "سبزی" in store_type:
            recommendations["color_psychology"] = {
                "fresh_colors": "استفاده از رنگ‌های تازه و طبیعی (سبز، قرمز، نارنجی) برای میوه‌ها",
                "ripeness_indication": "چیدمان میوه‌ها بر اساس درجه رسیدگی و رنگ",
                "seasonal_colors": "استفاده از رنگ‌های فصلی برای جلب توجه",
                "natural_contrast": "قرار دادن میوه‌های با رنگ‌های متضاد کنار هم"
            }
            
            recommendations["product_arrangement"] = {
                "height_placement": "قرار دادن میوه‌های پرفروش در ارتفاع 80-120 سانتی‌متر",
                "color_grouping": "گروه‌بندی میوه‌ها بر اساس رنگ (قرمز، سبز، نارنجی)",
                "freshness_display": "نمایش میوه‌های تازه در جلو و مرکز",
                "seasonal_arrangement": "چیدمان میوه‌ها بر اساس فصل"
            }
            
        elif "لوازم آرایش" in store_type or "عطریات" in store_type:
            recommendations["color_psychology"] = {
                "luxury_colors": "استفاده از رنگ‌های لوکس (طلایی، نقره‌ای، مشکی) برای محصولات گران",
                "gender_colors": "استفاده از رنگ‌های مخصوص جنسیت (صورتی برای زنان، آبی برای مردان)",
                "mood_colors": "استفاده از رنگ‌های متناسب با حال و هوا (آرامش‌بخش، انرژی‌بخش)",
                "brand_colors": "چیدمان محصولات بر اساس رنگ برند"
            }
            
            recommendations["product_arrangement"] = {
                "height_placement": "قرار دادن محصولات پرفروش در ارتفاع 140-180 سانتی‌متر",
                "price_grouping": "گروه‌بندی محصولات بر اساس قیمت و رنگ",
                "brand_organization": "چیدمان محصولات بر اساس برند و رنگ",
                "category_display": "نمایش محصولات بر اساس دسته‌بندی و رنگ"
            }
            
        else:  # فروشگاه عمومی
            recommendations["color_psychology"] = {
                "warm_colors": "استفاده از رنگ‌های گرم برای محصولات پرفروش",
                "cool_colors": "استفاده از رنگ‌های سرد برای محصولات آرامش‌بخش",
                "neutral_colors": "استفاده از رنگ‌های خنثی برای محصولات کلاسیک",
                "contrast": "قرار دادن محصولات با رنگ‌های متضاد کنار هم"
            }
            
            recommendations["product_arrangement"] = {
                "height_placement": "قرار دادن محصولات پرفروش در ارتفاع 120-160 سانتی‌متر",
                "color_grouping": "گروه‌بندی محصولات بر اساس رنگ",
                "category_organization": "چیدمان محصولات بر اساس دسته‌بندی و رنگ",
                "price_display": "نمایش محصولات بر اساس قیمت و رنگ"
            }
        
        # توصیه‌های جلب توجه
        recommendations["attention_grabbing"] = {
            "lighting": f"استفاده از نور تاکیدی روی محصولات خاص در {store_name}",
            "mirrors": f"استفاده از آینه‌ها برای ایجاد عمق بصری در {store_name}",
            "focal_points": f"ایجاد نقاط کانونی با رنگ‌های متضاد در {store_name}",
            "movement": f"قرار دادن محصولات جدید در مسیر اصلی حرکت مشتری در {store_name}",
            "spacing": f"استفاده از فاصله‌گذاری مناسب بین محصولات در {store_name}",
            "height_variation": f"ایجاد تنوع در ارتفاع نمایش محصولات در {store_name}"
        }
        
        # توصیه‌های معماری فضایی
        recommendations["spatial_architecture"] = {
            "customer_flow": f"بهبود نقشه حرکتی مشتری در {store_name} از ورودی تا نقطه فروش",
            "hot_zones": f"شناسایی و بهینه‌سازی منطقه داغ (Hot Zone) در {store_name}",
            "smart_shelving": f"قفسه‌بندی هوشمند با ارتفاع مناسب و دسترسی آسان در {store_name}",
            "traffic_patterns": f"تحلیل و بهبود الگوهای ترافیک مشتری در {store_name}",
            "space_utilization": f"بهینه‌سازی استفاده از فضا در {store_name}",
            "circulation_paths": f"ایجاد مسیرهای گردشی منطقی در {store_name}"
        }
        
        # توصیه‌های نورپردازی تخصصی
        recommendations["lighting_design"] = {
            "general_lighting": f"نورپردازی عمومی یکنواخت و ملایم در {store_name}",
            "accent_lighting": f"نورپردازی تأکیدی روی محصولات خاص در {store_name}",
            "emotional_lighting": f"نورپردازی احساسی متناسب با نوع کسب‌وکار در {store_name}",
            "task_lighting": f"نورپردازی وظیفه‌ای برای فعالیت‌های خاص در {store_name}",
            "ambient_lighting": f"نورپردازی محیطی برای ایجاد فضای مناسب در {store_name}",
            "color_temperature": f"تنظیم دمای رنگ نور برای ایجاد حس مناسب در {store_name}"
        }
        
        # توصیه‌های هویت بصری
        recommendations["brand_identity"] = {
            "color_palette": f"پالت رنگی هماهنگ با برند در {store_name}",
            "materials_textures": f"متریال و بافت متناسب با هویت برند در {store_name}",
            "signage_graphics": f"نشانه‌گذاری و گرافیک محیطی شفاف و زیبا در {store_name}",
            "logo_placement": f"قرارگیری مناسب لوگو و عناصر برند در {store_name}",
            "visual_consistency": f"ثبات بصری در تمام عناصر طراحی {store_name}",
            "brand_storytelling": f"داستان‌سرایی برند از طریق طراحی در {store_name}"
        }
        
        # توصیه‌های تجربه مشتری
        recommendations["customer_experience"] = {
            "five_senses": f"بهبود تجربه پنج‌گانه (دیداری، شنیداری، بویایی، لامسه، چشایی) در {store_name}",
            "comfort_relaxation": f"ایجاد فضای راحت و آرامش‌بخش در {store_name}",
            "digital_interaction": f"تعامل دیجیتال با نمایشگرها و QR کدها در {store_name}",
            "personal_service": f"خدمات شخصی و مشاوره در {store_name}",
            "waiting_areas": f"فضای انتظار راحت و جذاب در {store_name}",
            "accessibility": f"دسترسی آسان برای تمام مشتریان در {store_name}"
        }
        
        # توصیه‌های ویترین و نقطه فروش
        recommendations["visual_merchandising"] = {
            "attractive_display": f"ویترین جذاب و داستان‌سرا در {store_name}",
            "product_composition": f"ترکیب‌بندی محصولات بر اساس تم رنگی و فصل در {store_name}",
            "checkout_experience": f"تجربه نهایی خرید و بسته‌بندی در {store_name}",
            "window_dressing": f"آرایش ویترین و نمایش محصولات در {store_name}",
            "seasonal_displays": f"نمایش‌های فصلی و مناسبتی در {store_name}",
            "trend_showcasing": f"نمایش ترندها و محصولات جدید در {store_name}"
        }
        
        # توصیه‌های جزئیات انسانی
        recommendations["human_centric_design"] = {
            "ergonomics": f"ارگونومی مناسب برای دسترسی آسان محصولات در {store_name}",
            "intuitive_navigation": f"راهنمایی روان و جلوگیری از گم‌گشتگی در {store_name}",
            "human_services": f"جایگاه مشاوره و پرسنل هم‌سطح با طراحی در {store_name}",
            "comfort_zones": f"ایجاد مناطق راحت برای استراحت مشتری در {store_name}",
            "clear_signage": f"علائم واضح و قابل فهم در {store_name}",
            "staff_positioning": f"قرارگیری مناسب پرسنل برای خدمت‌رسانی در {store_name}"
        }
        
        # توصیه‌های خاص صنعت
        recommendations["specific_industry_tips"] = {
            "rule_of_three": f"استفاده از قانون 'قدرت سه' در چیدمان محصولات {store_name}",
            "golden_triangle": f"ایجاد مثلث طلایی برای محصولات مهم در {store_name}",
            "color_harmony": f"استفاده از هارمونی رنگ‌ها در {store_name}",
            "visual_flow": f"ایجاد جریان بصری منطقی در {store_name}",
            "seasonal_adaptation": f"تطبیق رنگ‌بندی با فصل در {store_name}",
            "customer_psychology": f"استفاده از روانشناسی مشتری در {store_name}",
            "impulse_buying": f"ایجاد فرصت‌های خرید آنی در {store_name}",
            "cross_selling": f"استراتژی فروش متقابل در {store_name}",
            "upselling": f"فروش محصولات گران‌تر در {store_name}",
            "customer_journey": f"بهینه‌سازی سفر مشتری در {store_name}",
            "touch_points": f"بهبود نقاط تماس با مشتری در {store_name}",
            "emotional_connection": f"ایجاد ارتباط عاطفی با مشتری در {store_name}"
        }
        
        return recommendations
    
    def generate_implementation_guide(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """تولید راهنمای پیاده‌سازی عملی"""
        
        guide = {
            "title": "راهنمای پیاده‌سازی بهینه‌سازی فروشگاه",
            "overview": "این راهنما شامل مراحل عملی برای پیاده‌سازی پیشنهادات تحلیل است.",
            "phases": {},
            "checklist": {},
            "resources": {},
            "timeline": {}
        }
        
        # فاز اول (1-2 ماه)
        guide["phases"]["phase_1"] = {
            "title": "فاز اول: بهینه‌سازی سریع",
            "duration": "1-2 ماه",
            "budget": "کم",
            "priority": "بالا",
            "tasks": [
                "بازطراحی چیدمان قفسه‌ها",
                "بهبود نورپردازی",
                "نصب تابلوهای راهنما",
                "بهینه‌سازی مسیرهای مشتری"
            ],
            "expected_results": [
                "افزایش 5-10% نرخ تبدیل",
                "کاهش زمان انتظار",
                "بهبود تجربه مشتری"
            ]
        }
        
        # فاز دوم (3-6 ماه)
        guide["phases"]["phase_2"] = {
            "title": "فاز دوم: بهبود سیستم‌ها",
            "duration": "3-6 ماه",
            "budget": "متوسط",
            "priority": "متوسط",
            "tasks": [
                "افزایش تعداد صندوق‌ها",
                "پیاده‌سازی سیستم مدیریت صف",
                "بهبود استراتژی قیمت‌گذاری",
                "بهینه‌سازی موجودی"
            ],
            "expected_results": [
                "افزایش 15-20% فروش",
                "کاهش 20% هزینه‌های عملیاتی",
                "بهبود رضایت کارکنان"
            ]
        }
        
        # فاز سوم (6-12 ماه)
        guide["phases"]["phase_3"] = {
            "title": "فاز سوم: تحول دیجیتال",
            "duration": "6-12 ماه",
            "budget": "بالا",
            "priority": "کم",
            "tasks": [
                "پیاده‌سازی سیستم هوشمند",
                "بازسازی کامل فروشگاه",
                "گسترش فضای فروشگاه",
                "پیاده‌سازی تجارت الکترونیک"
            ],
            "expected_results": [
                "افزایش 25-30% فروش",
                "کاهش 30% هزینه‌ها",
                "رقابت‌پذیری بالا"
            ]
        }
        
        # چک‌لیست پیاده‌سازی
        guide["checklist"] = {
            "pre_implementation": [
                "تأیید بودجه",
                "تشکیل تیم پیاده‌سازی",
                "برنامه‌ریزی زمانی",
                "آموزش کارکنان"
            ],
            "during_implementation": [
                "نظارت بر پیشرفت",
                "مدیریت تغییرات",
                "حل مشکلات",
                "ارتباط با ذینفعان"
            ],
            "post_implementation": [
                "ارزیابی نتایج",
                "بهینه‌سازی فرآیندها",
                "آموزش مستمر",
                "برنامه‌ریزی آینده"
            ]
        }
        
        # منابع مورد نیاز
        guide["resources"] = {
            "human_resources": [
                "مدیر پروژه",
                "متخصص طراحی فروشگاه",
                "کارشناس IT",
                "کارکنان فروشگاه"
            ],
            "technical_resources": [
                "نرم‌افزار طراحی",
                "سیستم مدیریت صف",
                "تجهیزات نورپردازی",
                "تابلوهای راهنما"
            ],
            "financial_resources": [
                "بودجه پیاده‌سازی",
                "بودجه آموزش",
                "بودجه نگهداری",
                "بودجه اضطراری"
            ]
        }
        
        # جدول زمانی
        guide["timeline"] = {
            "week_1_2": "برنامه‌ریزی و آماده‌سازی",
            "week_3_4": "شروع فاز اول",
            "month_2": "تکمیل فاز اول",
            "month_3_4": "شروع فاز دوم",
            "month_5_6": "تکمیل فاز دوم",
            "month_7_12": "پیاده‌سازی فاز سوم"
        }
        
        return guide

# نمونه استفاده
if __name__ == "__main__":
    # تست سیستم
    ai_analyzer = StoreAnalysisAI()
    
    test_data = {
        'store_name': 'فروشگاه تست',
        'store_type': 'retail',
        'store_size': 'medium',
        'entrance_count': 2,
        'checkout_count': 3,
        'shelf_count': 25,
        'conversion_rate': 35.5,
        'avg_daily_customers': 150,
        'avg_customer_time': 45
    }
    
    result = ai_analyzer.generate_detailed_analysis(test_data)
    print(json.dumps(result, indent=2, ensure_ascii=False))
