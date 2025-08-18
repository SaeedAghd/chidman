import asyncio
import json
import logging
from typing import Dict, List, Optional, Callable
from django.core.cache import cache
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ..ai_models.advanced_analyzer import AdvancedStoreAnalyzer, AnalysisType

logger = logging.getLogger(__name__)

class RealTimeAnalyzer:
    """
    سیستم تحلیل Real-time با نمایش پیشرفت
    """
    
    def __init__(self):
        self.analyzer = AdvancedStoreAnalyzer()
        self.channel_layer = get_channel_layer()
        
    async def start_analysis(self, store_data: Dict, user_id: int, analysis_id: int):
        """
        شروع تحلیل با نمایش پیشرفت Real-time
        """
        # تنظیم وضعیت اولیه
        await self._update_status(analysis_id, "در حال شروع تحلیل...", 0)
        
        try:
            # مرحله 1: تحلیل چیدمان
            await self._update_status(analysis_id, "در حال تحلیل چیدمان...", 10)
            layout_result = await self.analyzer.analyze_layout_advanced(store_data)
            await self._send_analysis_update(analysis_id, "layout", layout_result)
            
            # مرحله 2: تحلیل ترافیک
            await self._update_status(analysis_id, "در حال تحلیل الگوهای ترافیک...", 30)
            traffic_result = await self.analyzer.analyze_traffic_patterns(store_data)
            await self._send_analysis_update(analysis_id, "traffic", traffic_result)
            
            # مرحله 3: تحلیل طراحی
            await self._update_status(analysis_id, "در حال تحلیل طراحی و دکوراسیون...", 50)
            design_result = await self.analyzer.analyze_design_elements(store_data)
            await self._send_analysis_update(analysis_id, "design", design_result)
            
            # مرحله 4: تحلیل فروش
            await self._update_status(analysis_id, "در حال تحلیل بهینه‌سازی فروش...", 70)
            sales_result = await self.analyzer.analyze_sales_optimization(store_data)
            await self._send_analysis_update(analysis_id, "sales", sales_result)
            
            # مرحله 5: تحلیل رفتار مشتری
            await self._update_status(analysis_id, "در حال تحلیل رفتار مشتری...", 85)
            behavior_result = await self.analyzer.analyze_customer_behavior(store_data)
            await self._send_analysis_update(analysis_id, "customer_behavior", behavior_result)
            
            # مرحله 6: تولید برنامه بهینه‌سازی
            await self._update_status(analysis_id, "در حال تولید برنامه بهینه‌سازی...", 95)
            optimization_result = await self.analyzer.generate_optimization_plan(store_data)
            await self._send_analysis_update(analysis_id, "optimization", optimization_result)
            
            # تکمیل تحلیل
            await self._update_status(analysis_id, "تحلیل تکمیل شد!", 100)
            await self._send_completion_notification(analysis_id, user_id)
            
            return {
                'layout': layout_result,
                'traffic': traffic_result,
                'design': design_result,
                'sales': sales_result,
                'customer_behavior': behavior_result,
                'optimization': optimization_result
            }
            
        except Exception as e:
            logger.error(f"Error in real-time analysis: {e}")
            await self._update_status(analysis_id, f"خطا در تحلیل: {str(e)}", -1)
            raise
    
    async def _update_status(self, analysis_id: int, message: str, progress: int):
        """به‌روزرسانی وضعیت تحلیل"""
        status_data = {
            'analysis_id': analysis_id,
            'message': message,
            'progress': progress,
            'timestamp': timezone.now().isoformat()
        }
        
        # ذخیره در cache
        cache_key = f'analysis_status_{analysis_id}'
        cache.set(cache_key, status_data, 3600)  # 1 ساعت
        
        # ارسال به WebSocket
        await self._send_status_update(analysis_id, status_data)
    
    async def _send_status_update(self, analysis_id: int, status_data: Dict):
        """ارسال به‌روزرسانی وضعیت به WebSocket"""
        try:
            await self.channel_layer.group_send(
                f'analysis_{analysis_id}',
                {
                    'type': 'analysis.status_update',
                    'data': status_data
                }
            )
        except Exception as e:
            logger.error(f"Error sending status update: {e}")
    
    async def _send_analysis_update(self, analysis_id: int, analysis_type: str, result):
        """ارسال نتیجه تحلیل به WebSocket"""
        try:
            update_data = {
                'analysis_id': analysis_id,
                'type': analysis_type,
                'score': result.score,
                'analysis': result.analysis,
                'recommendations': result.recommendations,
                'timestamp': timezone.now().isoformat()
            }
            
            await self.channel_layer.group_send(
                f'analysis_{analysis_id}',
                {
                    'type': 'analysis.result_update',
                    'data': update_data
                }
            )
        except Exception as e:
            logger.error(f"Error sending analysis update: {e}")
    
    async def _send_completion_notification(self, analysis_id: int, user_id: int):
        """ارسال اعلان تکمیل تحلیل"""
        try:
            notification_data = {
                'analysis_id': analysis_id,
                'user_id': user_id,
                'message': 'تحلیل فروشگاه شما تکمیل شد!',
                'timestamp': timezone.now().isoformat()
            }
            
            await self.channel_layer.group_send(
                f'user_{user_id}',
                {
                    'type': 'analysis.completion_notification',
                    'data': notification_data
                }
            )
        except Exception as e:
            logger.error(f"Error sending completion notification: {e}")
    
    def get_analysis_status(self, analysis_id: int) -> Optional[Dict]:
        """دریافت وضعیت تحلیل از cache"""
        cache_key = f'analysis_status_{analysis_id}'
        return cache.get(cache_key)
    
    def get_analysis_results(self, analysis_id: int) -> Optional[Dict]:
        """دریافت نتایج تحلیل از cache"""
        cache_key = f'analysis_results_{analysis_id}'
        return cache.get(cache_key)
    
    def save_analysis_results(self, analysis_id: int, results: Dict):
        """ذخیره نتایج تحلیل در cache"""
        cache_key = f'analysis_results_{analysis_id}'
        cache.set(cache_key, results, 86400)  # 24 ساعت
