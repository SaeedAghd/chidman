"""
سرویس ارسال ایمیل برای تاییدیه ثبت نام
"""

import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import random
from datetime import datetime, timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)

class EmailVerificationService:
    """سرویس تاییدیه ایمیل"""
    
    def __init__(self):
        self.from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@chidmano.com')
        self.site_name = 'چیدمانو'
        self.site_url = getattr(settings, 'SITE_URL', 'https://chidmano.liara.app')
    
    def generate_verification_code(self) -> str:
        """تولید کد تایید 6 رقمی"""
        return str(random.randint(100000, 999999))
    
    def send_verification_email(self, user, email: str, verification_code: str) -> bool:
        """ارسال ایمیل تاییدیه"""
        try:
            # محتوای ایمیل
            subject = f'تایید ایمیل - {self.site_name}'
            
            # متن ایمیل
            html_message = f"""
            <!DOCTYPE html>
            <html lang="fa" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>تایید ایمیل</title>
                <style>
                    body {{
                        font-family: 'Vazirmatn', Arial, sans-serif;
                        direction: rtl;
                        background-color: #f8f9fa;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 15px;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                        overflow: hidden;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 30px;
                        text-align: center;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 2rem;
                        font-weight: bold;
                    }}
                    .content {{
                        padding: 40px 30px;
                        text-align: center;
                    }}
                    .verification-code {{
                        background: linear-gradient(135deg, #4a90e2 0%, #50e3c2 100%);
                        color: white;
                        font-size: 2.5rem;
                        font-weight: bold;
                        padding: 20px;
                        border-radius: 15px;
                        margin: 30px 0;
                        letter-spacing: 5px;
                        font-family: 'Courier New', monospace;
                    }}
                    .message {{
                        font-size: 1.1rem;
                        line-height: 1.6;
                        color: #333;
                        margin-bottom: 30px;
                    }}
                    .warning {{
                        background: #fff3cd;
                        border: 1px solid #ffeaa7;
                        border-radius: 10px;
                        padding: 15px;
                        margin: 20px 0;
                        color: #856404;
                    }}
                    .footer {{
                        background: #f8f9fa;
                        padding: 20px;
                        text-align: center;
                        color: #666;
                        font-size: 0.9rem;
                    }}
                    .btn {{
                        display: inline-block;
                        background: linear-gradient(135deg, #4a90e2 0%, #50e3c2 100%);
                        color: white;
                        padding: 15px 30px;
                        text-decoration: none;
                        border-radius: 25px;
                        font-weight: bold;
                        margin: 20px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 خوش آمدید به {self.site_name}</h1>
                    </div>
                    
                    <div class="content">
                        <p class="message">
                            سلام <strong>{user.username}</strong> عزیز،<br><br>
                            از ثبت نام شما در {self.site_name} متشکریم! برای تکمیل فرآیند ثبت نام، 
                            لطفاً کد تایید زیر را در سایت وارد کنید:
                        </p>
                        
                        <div class="verification-code">
                            {verification_code}
                        </div>
                        
                        <p class="message">
                            این کد تا <strong>10 دقیقه</strong> معتبر است.
                        </p>
                        
                        <div class="warning">
                            ⚠️ <strong>نکته مهم:</strong> این کد را با هیچکس به اشتراک نگذارید. 
                            تیم {self.site_name} هیچ‌گاه از شما کد تایید نخواهد خواست.
                        </div>
                        
                        <a href="{self.site_url}/accounts/verify-email/" class="btn">
                            🔗 تایید ایمیل
                        </a>
                    </div>
                    
                    <div class="footer">
                        <p>
                            اگر این ایمیل را درخواست نکرده‌اید، لطفاً آن را نادیده بگیرید.<br>
                            © 2024 {self.site_name} - تمامی حقوق محفوظ است
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # ارسال ایمیل
            send_mail(
                subject=subject,
                message=strip_tags(html_message),
                from_email=self.from_email,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"ایمیل تاییدیه برای {email} ارسال شد")
            return True
            
        except Exception as e:
            logger.error(f"خطا در ارسال ایمیل تاییدیه: {e}")
            return False
    
    def send_welcome_email(self, user, email: str) -> bool:
        """ارسال ایمیل خوش‌آمدگویی"""
        try:
            subject = f'خوش آمدید به {self.site_name} - حساب کاربری شما فعال شد!'
            
            html_message = f"""
            <!DOCTYPE html>
            <html lang="fa" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>خوش آمدید</title>
                <style>
                    body {{
                        font-family: 'Vazirmatn', Arial, sans-serif;
                        direction: rtl;
                        background-color: #f8f9fa;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 15px;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                        overflow: hidden;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #50e3c2 0%, #4a90e2 100%);
                        color: white;
                        padding: 30px;
                        text-align: center;
                    }}
                    .content {{
                        padding: 40px 30px;
                        text-align: center;
                    }}
                    .success-icon {{
                        font-size: 4rem;
                        margin-bottom: 20px;
                    }}
                    .btn {{
                        display: inline-block;
                        background: linear-gradient(135deg, #4a90e2 0%, #50e3c2 100%);
                        color: white;
                        padding: 15px 30px;
                        text-decoration: none;
                        border-radius: 25px;
                        font-weight: bold;
                        margin: 20px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 تبریک!</h1>
                    </div>
                    
                    <div class="content">
                        <div class="success-icon">✅</div>
                        <h2>حساب کاربری شما فعال شد!</h2>
                        <p>
                            سلام <strong>{user.username}</strong> عزیز،<br><br>
                            ایمیل شما با موفقیت تایید شد و حساب کاربری شما در {self.site_name} فعال گردید.
                        </p>
                        
                        <p>
                            حالا می‌توانید از تمامی امکانات سایت استفاده کنید:
                        </p>
                        
                        <ul style="text-align: right; margin: 20px 0;">
                            <li>🎯 تحلیل هوشمند فروشگاه</li>
                            <li>📊 گزارش‌های تفصیلی</li>
                            <li>🤖 مشاوره هوش مصنوعی</li>
                            <li>📈 بهینه‌سازی فروش</li>
                        </ul>
                        
                        <a href="{self.site_url}/store/dashboard/" class="btn">
                            🚀 شروع تحلیل فروشگاه
                        </a>
                    </div>
                </div>
            </body>
            </html>
            """
            
            send_mail(
                subject=subject,
                message=strip_tags(html_message),
                from_email=self.from_email,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"ایمیل خوش‌آمدگویی برای {email} ارسال شد")
            return True
            
        except Exception as e:
            logger.error(f"خطا در ارسال ایمیل خوش‌آمدگویی: {e}")
            return False
