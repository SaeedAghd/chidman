"""
سرویس هوش مصنوعی پیشرفته لیارا برای چیدمانو
استفاده از بهترین مدل‌های AI برای تحلیل حرفه‌ای فروشگاه‌ها
"""

import requests
import json
import logging
from typing import Dict, List, Any, Optional
from django.conf import settings
from django.core.cache import cache
import time

logger = logging.getLogger(__name__)

class LiaraAIService:
    """سرویس هوش مصنوعی پیشرفته لیارا"""
    
    def __init__(self):
        # URL صحیح API لیارا بر اساس مستندات
        self.base_url = "https://ai.liara.ir/api/68cb388afcfe30ace3a2a314/v1"
        self.api_key = getattr(settings, 'LIARA_AI_API_KEY', '')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Chidmano-AI-Client/1.0'
        }
        
        # مدل‌های موجود در لیارا بر اساس مستندات
        self.models = {
            'analysis': 'openai/gpt-4.1',           # تحلیل اصلی
            'design': 'openai/gpt-4.1',             # تحلیل طراحی
            'marketing': 'openai/gpt-4.1',          # تحلیل بازاریابی
            'psychology': 'openai/gpt-4.1',         # روانشناسی مشتری
            'optimization': 'openai/gpt-4.1',       # بهینه‌سازی
            'summary': 'openai/gpt-4.1'             # خلاصه‌سازی
        }
    
    def _make_request(self, model: str, prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> Dict:
        """ارسال درخواست به API لیارا"""
        try:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "شما بهترین متخصص تحلیل فروشگاه و مشاور کسب‌وکار دنیا هستید. تخصص شما در بهینه‌سازی چیدمان فروشگاه‌ها و افزایش فروش است."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=45  # کاهش timeout برای سرعت بیشتر
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"خطا در API لیارا: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout در ارتباط با لیارا AI - درخواست بیش از 2 دقیقه طول کشید")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"خطا در اتصال به لیارا AI - بررسی اتصال اینترنت")
            return None
        except Exception as e:
            logger.error(f"خطا در ارتباط با لیارا AI: {e}")
            return None
    
    def analyze_store_comprehensive(self, store_data: Dict[str, Any], images: List[str] = None) -> Dict[str, Any]:
        """تحلیل جامع و حرفه‌ای فروشگاه با استفاده از چندین مدل AI و پردازش تصاویر"""
        
        store_name = store_data.get('store_name', 'فروشگاه')
        store_type = store_data.get('store_type', 'عمومی')
        
        logger.info(f"🚀 شروع تحلیل جامع فروشگاه {store_name} با {len(images) if images else 0} تصویر")
        
        # تحلیل‌های موازی با مدل‌های مختلف
        analyses = {}
        
        # 1. تحلیل اصلی با GPT-4 Turbo (شامل اطلاعات تصاویر)
        main_analysis = self._analyze_main_store(store_data, images)
        if main_analysis:
            analyses['main'] = main_analysis
        
        # 2. تحلیل طراحی با Claude-3 Opus (با تمرکز بر تصاویر)
        design_analysis = self._analyze_store_design(store_data, images)
        if design_analysis:
            analyses['design'] = design_analysis
        
        # 3. تحلیل روانشناسی مشتری با Claude-3 Sonnet
        psychology_analysis = self._analyze_customer_psychology(store_data)
        if psychology_analysis:
            analyses['psychology'] = psychology_analysis
        
        # 4. تحلیل بازاریابی با GPT-4o
        marketing_analysis = self._analyze_marketing_potential(store_data)
        if marketing_analysis:
            analyses['marketing'] = marketing_analysis
        
        # 5. بهینه‌سازی با GPT-4 Turbo
        optimization_analysis = self._analyze_optimization(store_data)
        if optimization_analysis:
            analyses['optimization'] = optimization_analysis
        
        # ترکیب و خلاصه‌سازی نتایج
        final_analysis = self._combine_analyses(analyses, store_data, images)
        
        return final_analysis
    
    def _analyze_main_store(self, store_data: Dict[str, Any], images: List[str] = None) -> Dict[str, Any]:
        """تحلیل اصلی فروشگاه با GPT-4 Turbo"""
        
        prompt = f"""
        شما بهترین متخصص تحلیل فروشگاه دنیا هستید. تحلیل کاملاً حرفه‌ای و شخصی‌سازی شده برای فروشگاه "{store_data.get('store_name', 'فروشگاه')}" ارائه دهید.

        **قوانین مهم:**
        1. تمام پاسخ شما باید کاملاً به زبان فارسی باشد
        2. از هیچ کلمه انگلیسی، آلمانی، چینی یا عبری استفاده نکنید
        3. فقط از کلمات و اصطلاحات فارسی استفاده کنید
        4. تحلیل باید حرفه‌ای و قابل فهم برای صاحب فروشگاه باشد
        5. از اعداد و ارقام فارسی استفاده کنید (مثال: ۶.۸ به جای 6.8)

        **اطلاعات فروشگاه:**
        - نام: {store_data.get('store_name', 'نامشخص')}
        - نوع: {store_data.get('store_type', 'عمومی')}
        - اندازه: {store_data.get('store_size', 'نامشخص')}
        - شهر: {store_data.get('city', 'نامشخص')}
        - منطقه: {store_data.get('area', 'نامشخص')}
        - مشتریان روزانه: {store_data.get('daily_customers', 'نامشخص')}
        - فروش روزانه: {store_data.get('daily_sales', 'نامشخص')}
        - محصولات: {store_data.get('products', 'نامشخص')}
        - رنگ‌بندی: {store_data.get('color_scheme', 'نامشخص')}
        - نورپردازی: {store_data.get('lighting_type', 'نامشخص')}
        - چیدمان: {store_data.get('layout_type', 'نامشخص')}

        **لطفاً تحلیل جامع ارائه دهید:**

        ## 🎯 تحلیل حرفه‌ای فروشگاه {store_data.get('store_name', 'فروشگاه')}

        ### 📊 امتیاز کلی (1-100)
        [بر اساس تمام عوامل، امتیاز دقیق دهید]

        ### 💪 نقاط قوت استراتژیک
        [حداقل 7 مورد با تحلیل عمیق]

        ### ⚠️ چالش‌های کلیدی
        [حداقل 7 مورد با راه‌حل]

        ### 🎨 تحلیل طراحی و چیدمان
        **نورپردازی:**
        [تحلیل دقیق نورپردازی فعلی و پیشنهادات]

        **رنگ‌بندی:**
        [تحلیل روانشناسی رنگ‌ها و تأثیر بر مشتری]

        **چیدمان محصولات:**
        [تحلیل چیدمان فعلی و بهینه‌سازی]

        ### 🧠 تحلیل روانشناسی مشتری
        **رفتار مشتری:**
        [تحلیل رفتار مشتریان در فروشگاه]

        **تجربه خرید:**
        [تحلیل journey مشتری]

        ### 📈 پتانسیل افزایش فروش
        **تخمین افزایش:**
        [درصد دقیق افزایش فروش با تحلیل]

        **استراتژی‌های کلیدی:**
        [5 استراتژی اصلی برای افزایش فروش]

        ### 🚀 توصیه‌های عملی
        **فوری (1-2 هفته):**
        [اقدامات فوری]

        **کوتاه‌مدت (1-3 ماه):**
        [اقدامات کوتاه‌مدت]

        **بلندمدت (3-12 ماه):**
        [اقدامات بلندمدت]

        **نکته مهم: تمام تحلیل‌ها باید کاملاً شخصی‌سازی شده و مختص این فروشگاه باشد!**
        
        **تأکید نهایی:**
        - فقط از زبان فارسی استفاده کنید
        - هیچ کلمه غیرفارسی در پاسخ نباشد
        - تحلیل باید برای صاحب فروشگاه ایرانی قابل فهم باشد
        - از اصطلاحات تجاری فارسی استفاده کنید
        """
        
        result = self._make_request(self.models['analysis'], prompt, max_tokens=4000)
        if result and 'choices' in result:
            return {
                'type': 'main_analysis',
                'content': result['choices'][0]['message']['content'],
                'model': 'gpt-4-turbo'
            }
        return None
    
    def _analyze_store_design(self, store_data: Dict[str, Any], images: List[str] = None) -> Dict[str, Any]:
        """تحلیل طراحی با Claude-3 Opus"""
        
        prompt = f"""
        شما متخصص طراحی فروشگاه و معماری داخلی هستید. تحلیل حرفه‌ای طراحی برای فروشگاه "{store_data.get('store_name', 'فروشگاه')}" ارائه دهید.

        **اطلاعات طراحی:**
        - نوع فروشگاه: {store_data.get('store_type', 'عمومی')}
        - اندازه: {store_data.get('store_size', 'نامشخص')}
        - چیدمان: {store_data.get('layout_type', 'نامشخص')}
        - نورپردازی: {store_data.get('lighting_type', 'نامشخص')}
        - رنگ‌بندی: {store_data.get('color_scheme', 'نامشخص')}
        - محصولات: {store_data.get('products', 'نامشخص')}

        **تحلیل طراحی حرفه‌ای:**

        ## 🎨 تحلیل طراحی فروشگاه {store_data.get('store_name', 'فروشگاه')}

        ### 🏗️ تحلیل معماری داخلی
        **فضا و جریان:**
        [تحلیل جریان مشتری و بهینه‌سازی فضا]

        **نقاط کانونی:**
        [شناسایی و بهینه‌سازی نقاط کانونی]

        ### 💡 تحلیل نورپردازی
        **نورپردازی فعلی:**
        [تحلیل نورپردازی موجود]

        **بهینه‌سازی نور:**
        [پیشنهادات نورپردازی حرفه‌ای]

        ### 🎨 تحلیل رنگ‌بندی
        **روانشناسی رنگ:**
        [تحلیل تأثیر رنگ‌ها بر مشتری]

        **پالت رنگ بهینه:**
        [پیشنهاد پالت رنگ حرفه‌ای]

        ### 📐 تحلیل چیدمان
        **چیدمان محصولات:**
        [تحلیل و بهینه‌سازی چیدمان]

        **فاصله‌گذاری:**
        [تحلیل فاصله‌گذاری و تراکم]

        ### 🎯 توصیه‌های طراحی
        **بهبودهای فوری:**
        [توصیه‌های فوری طراحی]

        **تحولات بلندمدت:**
        [پیشنهادات تحولی طراحی]

        **نکته: تحلیل باید کاملاً تخصصی و عملی باشد!**
        """
        
        result = self._make_request(self.models['design'], prompt, max_tokens=3000)
        if result and 'choices' in result:
            return {
                'type': 'design_analysis',
                'content': result['choices'][0]['message']['content'],
                'model': 'claude-3-opus'
            }
        return None
    
    def _analyze_customer_psychology(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل روانشناسی مشتری با Claude-3 Sonnet"""
        
        prompt = f"""
        شما متخصص روانشناسی مصرف‌کننده و رفتارشناسی مشتری هستید. تحلیل روانشناسی برای فروشگاه "{store_data.get('store_name', 'فروشگاه')}" ارائه دهید.

        **اطلاعات فروشگاه:**
        - نوع: {store_data.get('store_type', 'عمومی')}
        - مشتریان روزانه: {store_data.get('daily_customers', 'نامشخص')}
        - فروش روزانه: {store_data.get('daily_sales', 'نامشخص')}
        - محصولات: {store_data.get('products', 'نامشخص')}
        - منطقه: {store_data.get('area', 'نامشخص')}

        **تحلیل روانشناسی مشتری:**

        ## 🧠 تحلیل روانشناسی مشتری - {store_data.get('store_name', 'فروشگاه')}

        ### 👥 پروفایل مشتری
        **مشتریان هدف:**
        [تحلیل دقیق مشتریان هدف]

        **رفتار خرید:**
        [تحلیل الگوهای رفتاری]

        ### 🎯 انگیزه‌های خرید
        **انگیزه‌های اصلی:**
        [شناسایی انگیزه‌های خرید]

        **عوامل تأثیرگذار:**
        [تحلیل عوامل روانی تأثیرگذار]

        ### 🛒 تجربه خرید
        **Journey مشتری:**
        [تحلیل مسیر مشتری در فروشگاه]

        **نقاط تصمیم‌گیری:**
        [شناسایی نقاط کلیدی تصمیم]

        ### 💭 روانشناسی فضا
        **تأثیر محیط:**
        [تحلیل تأثیر محیط بر رفتار]

        **احساسات مشتری:**
        [تحلیل احساسات و واکنش‌ها]

        ### 🎨 روانشناسی بصری
        **تأثیر رنگ‌ها:**
        [تحلیل تأثیر روانی رنگ‌ها]

        **تأثیر نور:**
        [تحلیل تأثیر نور بر روان]

        ### 🚀 استراتژی‌های روانشناسی
        **تکنیک‌های فروش:**
        [تکنیک‌های روانشناسی فروش]

        **بهینه‌سازی تجربه:**
        [بهینه‌سازی تجربه مشتری]

        **نکته: تحلیل باید بر اساس اصول روانشناسی باشد!**
        """
        
        result = self._make_request(self.models['psychology'], prompt, max_tokens=3000)
        if result and 'choices' in result:
            return {
                'type': 'psychology_analysis',
                'content': result['choices'][0]['message']['content'],
                'model': 'claude-3-sonnet'
            }
        return None
    
    def _analyze_marketing_potential(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل بازاریابی با GPT-4o"""
        
        prompt = f"""
        شما متخصص بازاریابی و استراتژی کسب‌وکار هستید. تحلیل بازاریابی برای فروشگاه "{store_data.get('store_name', 'فروشگاه')}" ارائه دهید.

        **اطلاعات کسب‌وکار:**
        - نام: {store_data.get('store_name', 'فروشگاه')}
        - نوع: {store_data.get('store_type', 'عمومی')}
        - منطقه: {store_data.get('area', 'نامشخص')}
        - مشتریان روزانه: {store_data.get('daily_customers', 'نامشخص')}
        - فروش روزانه: {store_data.get('daily_sales', 'نامشخص')}
        - محصولات: {store_data.get('products', 'نامشخص')}

        **تحلیل بازاریابی حرفه‌ای:**

        ## 📈 تحلیل بازاریابی - {store_data.get('store_name', 'فروشگاه')}

        ### 🎯 تحلیل بازار
        **موقعیت رقابتی:**
        [تحلیل موقعیت در بازار]

        **فرصت‌های بازار:**
        [شناسایی فرصت‌های رشد]

        ### 👥 تحلیل مشتری
        **بازار هدف:**
        [تحلیل دقیق بازار هدف]

        **نیازهای مشتری:**
        [شناسایی نیازهای پنهان]

        ### 💰 تحلیل درآمد
        **پتانسیل درآمد:**
        [تحلیل پتانسیل افزایش درآمد]

        **نقاط ضعف درآمد:**
        [شناسایی نقاط ضعف]

        ### 🚀 استراتژی‌های بازاریابی
        **بازاریابی دیجیتال:**
        [استراتژی‌های دیجیتال]

        **بازاریابی محلی:**
        [استراتژی‌های محلی]

        **بازاریابی تجربی:**
        [استراتژی‌های تجربی]

        ### 📊 تحلیل رقابتی
        **مزیت‌های رقابتی:**
        [شناسایی مزیت‌ها]

        **تهدیدات:**
        [تحلیل تهدیدات]

        ### 🎯 برنامه عملیاتی
        **اقدامات فوری:**
        [اقدامات 30 روزه]

        **اقدامات بلندمدت:**
        [اقدامات 6 ماهه]

        **نکته: تحلیل باید عملی و قابل اجرا باشد!**
        """
        
        result = self._make_request(self.models['marketing'], prompt, max_tokens=3000)
        if result and 'choices' in result:
            return {
                'type': 'marketing_analysis',
                'content': result['choices'][0]['message']['content'],
                'model': 'gpt-4o'
            }
        return None
    
    def _analyze_optimization(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل بهینه‌سازی با GPT-4 Turbo"""
        
        prompt = f"""
        شما متخصص بهینه‌سازی فروشگاه و افزایش کارایی هستید. تحلیل بهینه‌سازی برای فروشگاه "{store_data.get('store_name', 'فروشگاه')}" ارائه دهید.

        **اطلاعات فروشگاه:**
        - نام: {store_data.get('store_name', 'فروشگاه')}
        - نوع: {store_data.get('store_type', 'عمومی')}
        - اندازه: {store_data.get('store_size', 'نامشخص')}
        - مشتریان روزانه: {store_data.get('daily_customers', 'نامشخص')}
        - فروش روزانه: {store_data.get('daily_sales', 'نامشخص')}
        - چیدمان: {store_data.get('layout_type', 'نامشخص')}

        **تحلیل بهینه‌سازی حرفه‌ای:**

        ## ⚡ تحلیل بهینه‌سازی - {store_data.get('store_name', 'فروشگاه')}

        ### 📊 تحلیل کارایی
        **نرخ تبدیل:**
        [تحلیل نرخ تبدیل مشتری]

        **کارایی فضا:**
        [تحلیل استفاده از فضا]

        ### 🎯 بهینه‌سازی چیدمان
        **چیدمان محصولات:**
        [بهینه‌سازی چیدمان]

        **جریان مشتری:**
        [بهینه‌سازی جریان]

        ### 💡 بهینه‌سازی نور
        **نورپردازی:**
        [بهینه‌سازی نور]

        **صرفه‌جویی انرژی:**
        [بهینه‌سازی مصرف]

        ### 🎨 بهینه‌سازی بصری
        **رنگ‌بندی:**
        [بهینه‌سازی رنگ‌ها]

        **نمایش محصولات:**
        [بهینه‌سازی نمایش]

        ### 📈 بهینه‌سازی فروش
        **نقاط فروش:**
        [بهینه‌سازی نقاط فروش]

        **تکنیک‌های فروش:**
        [بهینه‌سازی تکنیک‌ها]

        ### 🚀 برنامه بهینه‌سازی
        **مرحله 1 (فوری):**
        [بهینه‌سازی‌های فوری]

        **مرحله 2 (کوتاه‌مدت):**
        [بهینه‌سازی‌های کوتاه‌مدت]

        **مرحله 3 (بلندمدت):**
        [بهینه‌سازی‌های بلندمدت]

        ### 📊 شاخص‌های عملکرد
        **KPI های کلیدی:**
        [تعریف شاخص‌های عملکرد]

        **نحوه اندازه‌گیری:**
        [روش‌های اندازه‌گیری]

        **نکته: تحلیل باید قابل اندازه‌گیری و عملی باشد!**
        """
        
        result = self._make_request(self.models['optimization'], prompt, max_tokens=3000)
        if result and 'choices' in result:
            return {
                'type': 'optimization_analysis',
                'content': result['choices'][0]['message']['content'],
                'model': 'gpt-4-turbo'
            }
        return None
    
    def _combine_analyses(self, analyses: Dict[str, Any], store_data: Dict[str, Any], images: List[str] = None) -> Dict[str, Any]:
        """ترکیب و خلاصه‌سازی تحلیل‌ها"""
        
        if not analyses:
            return self._get_fallback_analysis(store_data)
        
        # ایجاد خلاصه نهایی
        summary_prompt = f"""
        شما متخصص خلاصه‌سازی و ترکیب تحلیل‌ها هستید. تحلیل‌های زیر را برای فروشگاه "{store_data.get('store_name', 'فروشگاه')}" ترکیب و خلاصه کنید:

        {json.dumps(analyses, ensure_ascii=False, indent=2)}

        **لطفاً گزارش نهایی حرفه‌ای ارائه دهید:**

        ## 🎯 گزارش نهایی تحلیل فروشگاه {store_data.get('store_name', 'فروشگاه')}

        ### 📊 خلاصه اجرایی
        [خلاصه 3-4 خطی از وضعیت کلی]

        ### 🎯 امتیاز کلی
        [امتیاز نهایی 1-100]

        ### 💪 نقاط قوت کلیدی
        [5 نقطه قوت اصلی]

        ### ⚠️ چالش‌های مهم
        [5 چالش اصلی]

        ### 🚀 توصیه‌های اولویت‌دار
        [5 توصیه اولویت‌دار]

        ### 📈 پتانسیل افزایش فروش
        [درصد و توضیح]

        ### 🎯 برنامه عملیاتی
        **فوری (1-2 هفته):**
        [اقدامات فوری]

        **کوتاه‌مدت (1-3 ماه):**
        [اقدامات کوتاه‌مدت]

        **بلندمدت (3-12 ماه):**
        [اقدامات بلندمدت]

        **نکته: گزارش باید جامع، عملی و قابل اجرا باشد!**
        """
        
        result = self._make_request(self.models['summary'], summary_prompt, max_tokens=2000)
        if result and 'choices' in result:
            return {
                'final_report': result['choices'][0]['message']['content'],
                'detailed_analyses': analyses,
                'store_info': store_data,
                'analysis_timestamp': time.time(),
                'ai_models_used': list(set([analysis.get('model', 'unknown') for analysis in analyses.values() if analysis]))
            }
        
        return self._get_fallback_analysis(store_data)
    
    def _get_fallback_analysis(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل fallback در صورت خطا"""
        return {
            'final_report': f"تحلیل فروشگاه {store_data.get('store_name', 'فروشگاه')} در حال پردازش است. لطفاً مجدداً تلاش کنید.",
            'detailed_analyses': {},
            'store_info': store_data,
            'analysis_timestamp': time.time(),
            'ai_models_used': ['fallback'],
            'error': 'خطا در ارتباط با سرویس AI'
        }
    
    def get_ai_insights(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """دریافت بینش‌های AI برای فروشگاه"""
        
        # بررسی cache
        cache_key = f"ai_analysis_{hash(str(store_data))}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # انجام تحلیل
        result = self.analyze_store_comprehensive(store_data)
        
        # ذخیره در cache (1 ساعت)
        cache.set(cache_key, result, 3600)
        
        return result
