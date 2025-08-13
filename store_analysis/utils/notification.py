from django.core.mail import send_mail
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

def send_email_notification(email, subject, message):
    """ارسال ایمیل"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
            html_message=message.replace('\n', '<br>')
        )
        return True
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return False

def send_whatsapp_notification(phone, message):
    """ارسال پیام واتساپ"""
    try:
        # حذف صفر ابتدایی شماره تلفن
        if phone.startswith('0'):
            phone = phone[1:]
        
        # اضافه کردن کد کشور
        if not phone.startswith('98'):
            phone = '98' + phone
        
        # Check if WhatsApp settings are configured
        whatsapp_url = getattr(settings, 'WHATSAPP_API_URL', None)
        whatsapp_token = getattr(settings, 'WHATSAPP_API_TOKEN', None)
        
        if not whatsapp_url or not whatsapp_token:
            logger.warning("WhatsApp API not configured")
            return False
        
        response = requests.post(
            whatsapp_url,
            json={
                'phone': phone,
                'message': message
            },
            headers={
                'Authorization': f'Bearer {whatsapp_token}',
                'Content-Type': 'application/json'
            }
        )
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {str(e)}")
        return False 