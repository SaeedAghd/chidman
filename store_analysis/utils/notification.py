import logging
from typing import List, Optional
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import requests

logger = logging.getLogger(__name__)

class NotificationService:
    """سرویس اعلان‌ها برای ارسال پیام به کاربران"""
    
    @staticmethod
    def send_email_notification(
        to_email: str, 
        subject: str, 
        message: str, 
        html_template: Optional[str] = None,
        context: Optional[dict] = None
    ) -> bool:
        """ارسال اعلان ایمیل"""
        try:
            if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
                logger.warning("Email settings not configured")
                return False
            
            # استفاده از قالب HTML اگر موجود باشد
            if html_template and context:
                html_message = render_to_string(html_template, context)
            else:
                html_message = None
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Email notification sent to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False
    
    @staticmethod
    def send_whatsapp_notification(phone: str, message: str) -> bool:
        """ارسال اعلان واتساپ"""
        try:
            if not hasattr(settings, 'WHATSAPP_API_TOKEN') or not hasattr(settings, 'WHATSAPP_API_URL'):
                logger.warning("WhatsApp API settings not configured")
                return False
            
            headers = {
                'Authorization': f'Bearer {settings.WHATSAPP_API_TOKEN}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'to': phone,
                'message': message
            }
            
            response = requests.post(
                settings.WHATSAPP_API_URL,
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"WhatsApp notification sent to {phone}")
                return True
            else:
                logger.error(f"WhatsApp API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send WhatsApp notification: {e}")
            return False
    
    @staticmethod
    def send_sms_notification(phone: str, message: str) -> bool:
        """ارسال اعلان پیامک"""
        try:
            if not hasattr(settings, 'SMS_API_TOKEN') or not hasattr(settings, 'SMS_API_URL'):
                logger.warning("SMS API settings not configured")
                return False
            
            headers = {
                'Authorization': f'Bearer {settings.SMS_API_TOKEN}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'to': phone,
                'message': message
            }
            
            response = requests.post(
                settings.SMS_API_URL,
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"SMS notification sent to {phone}")
                return True
            else:
                logger.error(f"SMS API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send SMS notification: {e}")
            return False
    
    @staticmethod
    def send_analysis_completion_notification(user_email: str, store_name: str, analysis_id: int) -> bool:
        """ارسال اعلان تکمیل تحلیل"""
        subject = "تحلیل فروشگاه تکمیل شد"
        message = f"تحلیل فروشگاه {store_name} با موفقیت تکمیل شد. برای مشاهده نتایج به پنل کاربری مراجعه کنید."
        
        context = {
            'store_name': store_name,
            'analysis_id': analysis_id,
            'dashboard_url': f"{settings.SITE_URL}/analyses/{analysis_id}/results/" if hasattr(settings, 'SITE_URL') else None
        }
        
        return NotificationService.send_email_notification(
            to_email=user_email,
            subject=subject,
            message=message,
            html_template='store_analysis/emails/analysis_completed.html',
            context=context
        )
    
    @staticmethod
    def send_analysis_failed_notification(user_email: str, store_name: str, error_message: str) -> bool:
        """ارسال اعلان خطا در تحلیل"""
        subject = "خطا در تحلیل فروشگاه"
        message = f"متأسفانه در تحلیل فروشگاه {store_name} خطایی رخ داد: {error_message}"
        
        context = {
            'store_name': store_name,
            'error_message': error_message
        }
        
        return NotificationService.send_email_notification(
            to_email=user_email,
            subject=subject,
            message=message,
            html_template='store_analysis/emails/analysis_failed.html',
            context=context
        )
    
    @staticmethod
    def send_payment_success_notification(user_email: str, amount: float) -> bool:
        """ارسال اعلان موفقیت پرداخت"""
        subject = "پرداخت موفق"
        message = f"پرداخت شما به مبلغ {amount} تومان با موفقیت انجام شد."
        
        context = {
            'amount': amount
        }
        
        return NotificationService.send_email_notification(
            to_email=user_email,
            subject=subject,
            message=message,
            html_template='store_analysis/emails/payment_success.html',
            context=context
        )

# توابع قدیمی برای سازگاری
def send_email_notification(to_email: str, subject: str, message: str) -> bool:
    """تابع قدیمی برای ارسال ایمیل"""
    return NotificationService.send_email_notification(to_email, subject, message)

def send_whatsapp_notification(phone: str, message: str) -> bool:
    """تابع قدیمی برای ارسال واتساپ"""
    return NotificationService.send_whatsapp_notification(phone, message) 