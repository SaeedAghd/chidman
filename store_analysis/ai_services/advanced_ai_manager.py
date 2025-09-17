"""
مدیر پیشرفته هوش مصنوعی برای چیدمانو
ترکیب Ollama و لیارا AI برای بهترین عملکرد
"""

import logging
from typing import Dict, Any, Optional
from django.conf import settings
from django.core.cache import cache
import time

from .liara_ai_service import LiaraAIService
from ..ai_analysis import StoreAnalysisAI

logger = logging.getLogger(__name__)

class AdvancedAIManager:
    """مدیر پیشرفته هوش مصنوعی"""
    
    def __init__(self):
        self.liara_ai = LiaraAIService()
        self.ollama_ai = StoreAnalysisAI()
        self.use_liara = getattr(settings, 'USE_LIARA_AI', True)
        self.fallback_to_ollama = getattr(settings, 'FALLBACK_TO_OLLAMA', True)
    
    def analyze_store_advanced(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل پیشرفته فروشگاه با بهترین AI"""
        
        store_name = store_data.get('store_name', 'فروشگاه')
        logger.info(f"شروع تحلیل پیشرفته برای فروشگاه: {store_name}")
        
        # استراتژی تحلیل
        if self.use_liara:
            try:
                # اولویت با لیارا AI
                result = self._analyze_with_liara(store_data)
                if result and not result.get('error'):
                    logger.info(f"تحلیل موفق با لیارا AI برای: {store_name}")
                    return result
            except Exception as e:
                logger.warning(f"خطا در لیارا AI: {e}")
        
        # Fallback به Ollama
        if self.fallback_to_ollama:
            try:
                result = self._analyze_with_ollama(store_data)
                if result:
                    logger.info(f"تحلیل موفق با Ollama برای: {store_name}")
                    return result
            except Exception as e:
                logger.warning(f"خطا در Ollama: {e}")
        
        # Fallback نهایی
        return self._get_emergency_analysis(store_data)
    
    def _analyze_with_liara(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل با لیارا AI"""
        try:
            result = self.liara_ai.get_ai_insights(store_data)
            
            # اضافه کردن metadata
            result['ai_provider'] = 'liara'
            result['analysis_quality'] = 'premium'
            result['models_used'] = result.get('ai_models_used', [])
            
            return result
        except Exception as e:
            logger.error(f"خطا در تحلیل لیارا: {e}")
            return None
    
    def _analyze_with_ollama(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل با Ollama"""
        try:
            result = self.ollama_ai.generate_detailed_analysis(store_data)
            
            # تبدیل به فرمت یکسان
            formatted_result = {
                'final_report': result.get('analysis_text', 'تحلیل با Ollama انجام شد'),
                'detailed_analyses': {
                    'ollama_analysis': {
                        'type': 'ollama_analysis',
                        'content': result.get('analysis_text', ''),
                        'model': 'llama3.2'
                    }
                },
                'store_info': store_data,
                'analysis_timestamp': time.time(),
                'ai_provider': 'ollama',
                'analysis_quality': 'standard',
                'models_used': ['llama3.2']
            }
            
            return formatted_result
        except Exception as e:
            logger.error(f"خطا در تحلیل Ollama: {e}")
            return None
    
    def _get_emergency_analysis(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل اضطراری"""
        store_name = store_data.get('store_name', 'فروشگاه')
        
        return {
            'final_report': f"""
            ## 🎯 تحلیل فروشگاه {store_name}
            
            ### 📊 وضعیت کلی
            فروشگاه شما در حال تحلیل است. لطفاً چند دقیقه صبر کنید و مجدداً تلاش کنید.
            
            ### 💡 توصیه‌های کلی
            1. **نورپردازی مناسب**: از نور طبیعی و مصنوعی متعادل استفاده کنید
            2. **چیدمان منطقی**: محصولات را بر اساس منطق خرید چیدمان کنید
            3. **رنگ‌بندی هماهنگ**: از رنگ‌های هماهنگ و جذاب استفاده کنید
            4. **فضای کافی**: فضای کافی برای حرکت مشتریان فراهم کنید
            5. **نمایش محصولات**: محصولات را به صورت جذاب نمایش دهید
            
            ### 📈 پتانسیل افزایش فروش
            با بهینه‌سازی چیدمان، می‌توانید تا 30% افزایش فروش داشته باشید.
            """,
            'detailed_analyses': {},
            'store_info': store_data,
            'analysis_timestamp': time.time(),
            'ai_provider': 'emergency',
            'analysis_quality': 'basic',
            'models_used': ['emergency_fallback'],
            'error': 'خطا در سرویس‌های AI'
        }
    
    def get_analysis_status(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """بررسی وضعیت تحلیل"""
        
        # بررسی cache
        cache_key = f"analysis_status_{hash(str(store_data))}"
        status = cache.get(cache_key)
        
        if not status:
            status = {
                'status': 'pending',
                'progress': 0,
                'message': 'در حال آماده‌سازی تحلیل...'
            }
            cache.set(cache_key, status, 300)  # 5 دقیقه
        
        return status
    
    def start_advanced_analysis(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """شروع تحلیل پیشرفته"""
        
        store_name = store_data.get('store_name', 'فروشگاه')
        
        # تنظیم وضعیت
        cache_key = f"analysis_status_{hash(str(store_data))}"
        status = {
            'status': 'processing',
            'progress': 10,
            'message': f'شروع تحلیل پیشرفته برای {store_name}...'
        }
        cache.set(cache_key, status, 300)
        
        # شروع تحلیل
        try:
            result = self.analyze_store_advanced(store_data)
            
            # به‌روزرسانی وضعیت
            status.update({
                'status': 'completed',
                'progress': 100,
                'message': 'تحلیل با موفقیت تکمیل شد!',
                'result': result
            })
            cache.set(cache_key, status, 3600)  # 1 ساعت
            
            return result
            
        except Exception as e:
            logger.error(f"خطا در تحلیل پیشرفته: {e}")
            
            # به‌روزرسانی وضعیت خطا
            status.update({
                'status': 'failed',
                'progress': 0,
                'message': f'خطا در تحلیل: {str(e)}'
            })
            cache.set(cache_key, status, 300)
            
            return self._get_emergency_analysis(store_data)
    
    def get_ai_capabilities(self) -> Dict[str, Any]:
        """دریافت قابلیت‌های AI"""
        
        return {
            'liara_ai': {
                'available': self.use_liara,
                'models': [
                    'openai/gpt-4.1',  # جدیدترین و قدرتمندترین مدل
                    'openai/gpt-4-turbo',
                    'openai/gpt-4o',
                    'claude-3-opus',
                    'claude-3-sonnet'
                ],
                'capabilities': [
                    'تحلیل جامع فروشگاه با GPT-4.1',
                    'تحلیل طراحی حرفه‌ای پیشرفته',
                    'تحلیل روانشناسی مشتری عمیق',
                    'تحلیل بازاریابی استراتژیک',
                    'بهینه‌سازی عملکرد هوشمند',
                    'بینش‌های پیشرفته کسب‌وکار',
                    'توصیه‌های شخصی‌سازی شده'
                ]
            },
            'ollama_ai': {
                'available': self.fallback_to_ollama,
                'models': ['llama3.2'],
                'capabilities': [
                    'تحلیل پایه فروشگاه',
                    'توصیه‌های کلی'
                ]
            },
            'hybrid_mode': {
                'enabled': True,
                'strategy': 'liara_first_ollama_fallback',
                'benefits': [
                    'قابلیت اطمینان بالا',
                    'تحلیل‌های پیشرفته',
                    'پشتیبانی از چندین مدل',
                    'Fallback خودکار'
                ]
            }
        }
