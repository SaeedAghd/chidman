"""
AI Consultant Service - مشاوره هوشمند بر اساس تحلیل فروشگاه
"""

import logging
import os
import time
import requests
from typing import Dict, Any, List
from django.conf import settings

logger = logging.getLogger(__name__)


class AIConsultantService:
    """سرویس مشاوره هوشمند با AI - پاسخ به سوالات کاربر بر اساس تحلیل فروشگاه"""
    
    def __init__(self):
        self.liara_api_key = os.getenv('LIARA_AI_API_KEY', '')
        self.api_url = "https://api.liara.ir/v1/chat/completions"
    
    def chat_with_analysis(
        self,
        user_message: str,
        store_analysis: Any,
        chat_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        چت هوشمند بر اساس تحلیل فروشگاه
        
        Args:
            user_message: پیام کاربر
            store_analysis: تحلیل فروشگاه
            chat_history: تاریخچه مکالمه
        
        Returns:
            {
                'response': str,
                'ai_model': str,
                'processing_time': float,
                'success': bool
            }
        """
        start_time = time.time()
        
        try:
            # آماده‌سازی context از تحلیل
            analysis_context = self._prepare_analysis_context(store_analysis)
            
            # آماده‌سازی پیام‌ها
            messages = self._prepare_messages(user_message, analysis_context, chat_history)
            
            # ارسال به Liara AI
            response = self._call_liara_ai(messages)
            
            processing_time = time.time() - start_time
            
            if response:
                return {
                    'response': response,
                    'ai_model': 'gpt-4.1',
                    'processing_time': processing_time,
                    'success': True
                }
            else:
                # Fallback: پاسخ ساده
                fallback_response = self._generate_fallback_response(user_message, analysis_context)
                return {
                    'response': fallback_response,
                    'ai_model': 'fallback',
                    'processing_time': processing_time,
                    'success': False
                }
        
        except Exception as e:
            logger.error(f"❌ خطا در AI consultant: {e}", exc_info=True)
            processing_time = time.time() - start_time
            return {
                'response': 'متأسفانه در حال حاضر مشکلی پیش آمده است. لطفاً بعداً امتحان کنید.',
                'ai_model': 'error',
                'processing_time': processing_time,
                'success': False,
                'error': str(e)
            }
    
    def _prepare_analysis_context(self, store_analysis: Any) -> str:
        """آماده‌سازی context از تحلیل فروشگاه"""
        try:
            results = store_analysis.results or {}
            analysis_data = store_analysis.analysis_data or {}
            
            context = f"""
## اطلاعات فروشگاه:
- نام: {store_analysis.store_name}
- نوع: {analysis_data.get('store_type', 'نامشخص')}
- مساحت: {analysis_data.get('store_size', 'نامشخص')} متر مربع
- موقعیت: {analysis_data.get('store_location', 'نامشخص')}

## نتایج تحلیل:
- امتیاز کلی: {results.get('scores', {}).get('overall_score', 'نامشخص')}/100
- امتیاز طراحی: {results.get('scores', {}).get('design_score', 'نامشخص')}/100
- کیفیت تحلیل: {results.get('scores', {}).get('quality_score', 'نامشخص')}%

## خلاصه تحلیل:
{results.get('analysis_text', 'تحلیل در دسترس نیست')[:1000]}

## پیشنهادات کلیدی:
"""
            
            # اضافه کردن پیشنهادات
            recommendations = results.get('recommendations', [])
            if recommendations:
                for i, rec in enumerate(recommendations[:5], 1):
                    if isinstance(rec, dict):
                        context += f"{i}. {rec.get('title', '')}: {rec.get('description', '')}\n"
                    else:
                        context += f"{i}. {rec}\n"
            else:
                context += "پیشنهادات در تحلیل جامع ارائه شده است.\n"
            
            return context
            
        except Exception as e:
            logger.error(f"خطا در آماده‌سازی context: {e}")
            return f"اطلاعات فروشگاه {store_analysis.store_name}"
    
    def _prepare_messages(
        self,
        user_message: str,
        analysis_context: str,
        chat_history: List[Dict[str, str]] = None
    ) -> List[Dict[str, str]]:
        """آماده‌سازی پیام‌ها برای AI"""
        
        system_prompt = f"""شما یک مشاور حرفه‌ای چیدمان فروشگاه هستید که به زبان فارسی روان و سلیس صحبت می‌کنید.

**وظیفه شما:**
- پاسخ‌های دقیق، کاربردی و عملی بدهید
- از اطلاعات تحلیل فروشگاه استفاده کنید
- پیشنهادات قابل اجرا ارائه دهید
- به زبان فارسی روان و حرفه‌ای پاسخ دهید
- از تجربه و دانش خود در زمینه چیدمان فروشگاه استفاده کنید

**اطلاعات فروشگاه و تحلیل:**
{analysis_context}

**قوانین پاسخ‌دهی:**
1. تمام پاسخ به زبان فارسی باشد
2. از جملات کامل و واضح استفاده کنید
3. پیشنهادات عملی و قابل اجرا ارائه دهید
4. از تخصص خود در چیدمان استفاده کنید
5. اگر سوال خارج از حوزه تخصص است، راهنمایی کلی بدهید
6. هرگز از کلمات انگلیسی مثل regards، Small، Kids_Clothing، Neutral، attractiveness، Design، functionality، example استفاده نکنید
"""
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # اضافه کردن تاریخچه چت
        if chat_history:
            for msg in chat_history[-10:]:  # آخرین 10 پیام
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
        
        # اضافه کردن پیام جدید کاربر
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages
    
    def _call_liara_ai(self, messages: List[Dict[str, str]]) -> str:
        """فراخوانی Liara AI"""
        try:
            if not self.liara_api_key:
                logger.warning("⚠️ Liara AI API key not found")
                return None
            
            headers = {
                "Authorization": f"Bearer {self.liara_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-4.1",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1500
            }
            
            logger.info("🚀 Calling Liara AI for consultation...")
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                logger.info("✅ Liara AI response received")
                return ai_response
            else:
                logger.error(f"❌ Liara AI error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ خطا در فراخوانی Liara AI: {e}")
            return None
    
    def _generate_fallback_response(self, user_message: str, analysis_context: str) -> str:
        """تولید پاسخ fallback ساده"""
        
        # پاسخ‌های از پیش تعریف شده برای سوالات متداول
        common_responses = {
            'امتیاز': f"بر اساس تحلیل انجام شده، فروشگاه شما امتیاز مناسبی دریافت کرده است. برای جزئیات بیشتر می‌توانید به بخش نتایج تحلیل مراجعه کنید.",
            'بهبود': "برای بهبود فروشگاه، پیشنهاد می‌کنم ابتدا پیشنهادات اولویت‌دار را اجرا کنید و سپس به سراغ بهبودهای دیگر بروید.",
            'چیدمان': "چیدمان مناسب فروشگاه باعث افزایش فروش و رضایت مشتریان می‌شود. بر اساس تحلیل، پیشنهادات خاصی برای بهبود چیدمان ارائه شده است.",
            'روشنایی': "روشنایی مناسب یکی از عوامل مهم در جذب مشتری است. توصیه می‌شود از ترکیب روشنایی عمومی و تأکیدی استفاده کنید.",
            'رنگ': "انتخاب رنگ مناسب می‌تواند تأثیر زیادی در روی مشتری داشته باشد. رنگ‌ها را متناسب با نوع محصولات خود انتخاب کنید."
        }
        
        # جستجوی کلمات کلیدی در سوال
        user_message_lower = user_message.lower()
        for keyword, response in common_responses.items():
            if keyword in user_message_lower:
                return response
        
        # پاسخ پیش‌فرض
        return f"""ممنون از سوال شما. بر اساس تحلیل فروشگاه، پیشنهادهای متعددی برای بهبود ارائه شده است. 

برای پاسخ دقیق‌تر به سوال شما، لطفاً جزئیات بیشتری ارائه دهید یا به بخش نتایج تحلیل مراجعه کنید.

در صورت نیاز به مشاوره تخصصی، می‌توانید با تیم پشتیبانی ما تماس بگیرید."""


    def suggest_questions(self, store_analysis: Any) -> List[str]:
        """پیشنهاد سوالات متداول بر اساس تحلیل"""
        
        suggestions = [
            "چطور می‌توانم امتیاز فروشگاهم را بهبود دهم؟",
            "مهم‌ترین نقاط ضعف فروشگاه من کدامند؟",
            "چگونه چیدمان فروشگاهم را بهینه کنم؟",
            "برای جذب مشتری بیشتر چه کارهایی انجام دهم؟",
            "اولویت اول من برای بهبود فروشگاه چیست؟"
        ]
        
        return suggestions

