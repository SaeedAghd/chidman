import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache

logger = logging.getLogger(__name__)

class AnalysisConsumer(AsyncWebsocketConsumer):
    """
    WebSocket Consumer برای نمایش Real-time updates تحلیل
    """
    
    async def connect(self):
        """اتصال WebSocket"""
        self.analysis_id = self.scope['url_route']['kwargs']['analysis_id']
        self.user = self.scope['user']
        
        # بررسی احراز هویت
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return
        
        # بررسی دسترسی به تحلیل
        if not await self._can_access_analysis(self.analysis_id):
            await self.close()
            return
        
        # عضویت در گروه تحلیل
        await self.channel_layer.group_add(
            f'analysis_{self.analysis_id}',
            self.channel_name
        )
        
        # عضویت در گروه کاربر
        await self.channel_layer.group_add(
            f'user_{self.user.id}',
            self.channel_name
        )
        
        await self.accept()
        
        # ارسال وضعیت فعلی
        await self._send_current_status()
    
    async def disconnect(self, close_code):
        """قطع اتصال WebSocket"""
        # خروج از گروه‌ها
        await self.channel_layer.group_discard(
            f'analysis_{self.analysis_id}',
            self.channel_name
        )
        await self.channel_layer.group_discard(
            f'user_{self.user.id}',
            self.channel_name
        )
    
    async def receive(self, text_data):
        """دریافت پیام از کلاینت"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'get_status':
                await self._send_current_status()
            elif message_type == 'get_results':
                await self._send_current_results()
            elif message_type == 'cancel_analysis':
                await self._cancel_analysis()
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    async def analysis_status_update(self, event):
        """دریافت به‌روزرسانی وضعیت تحلیل"""
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'data': event['data']
        }))
    
    async def analysis_result_update(self, event):
        """دریافت به‌روزرسانی نتیجه تحلیل"""
        await self.send(text_data=json.dumps({
            'type': 'result_update',
            'data': event['data']
        }))
    
    async def analysis_completion_notification(self, event):
        """دریافت اعلان تکمیل تحلیل"""
        await self.send(text_data=json.dumps({
            'type': 'completion_notification',
            'data': event['data']
        }))
    
    async def _send_current_status(self):
        """ارسال وضعیت فعلی تحلیل"""
        from .services.real_time_analyzer import RealTimeAnalyzer
        
        analyzer = RealTimeAnalyzer()
        status = analyzer.get_analysis_status(self.analysis_id)
        
        if status:
            await self.send(text_data=json.dumps({
                'type': 'current_status',
                'data': status
            }))
    
    async def _send_current_results(self):
        """ارسال نتایج فعلی تحلیل"""
        from .services.real_time_analyzer import RealTimeAnalyzer
        
        analyzer = RealTimeAnalyzer()
        results = analyzer.get_analysis_results(self.analysis_id)
        
        if results:
            await self.send(text_data=json.dumps({
                'type': 'current_results',
                'data': results
            }))
    
    async def _cancel_analysis(self):
        """لغو تحلیل"""
        # در نسخه کامل، این تابع تحلیل را لغو می‌کند
        await self.send(text_data=json.dumps({
            'type': 'analysis_cancelled',
            'message': 'تحلیل لغو شد'
        }))
    
    @database_sync_to_async
    def _can_access_analysis(self, analysis_id):
        """بررسی دسترسی کاربر به تحلیل"""
        from .models import StoreAnalysis
        
        try:
            analysis = StoreAnalysis.objects.get(
                id=analysis_id,
                user=self.user
            )
            return True
        except StoreAnalysis.DoesNotExist:
            return False

class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket Consumer برای اعلان‌های عمومی
    """
    
    async def connect(self):
        """اتصال WebSocket"""
        self.user = self.scope['user']
        
        # بررسی احراز هویت
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return
        
        # عضویت در گروه کاربر
        await self.channel_layer.group_add(
            f'user_{self.user.id}',
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """قطع اتصال WebSocket"""
        await self.channel_layer.group_discard(
            f'user_{self.user.id}',
            self.channel_name
        )
    
    async def receive(self, text_data):
        """دریافت پیام از کلاینت"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'mark_read':
                notification_id = data.get('notification_id')
                await self._mark_notification_read(notification_id)
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    async def notification_message(self, event):
        """دریافت پیام اعلان"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'data': event['data']
        }))
    
    async def _mark_notification_read(self, notification_id):
        """علامت‌گذاری اعلان به عنوان خوانده شده"""
        # در نسخه کامل، این تابع اعلان را علامت‌گذاری می‌کند
        await self.send(text_data=json.dumps({
            'type': 'notification_marked_read',
            'notification_id': notification_id
        }))

