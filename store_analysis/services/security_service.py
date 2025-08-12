import re
import logging
from django.conf import settings
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

class SecurityService:
    """سرویس امنیتی برای اعتبارسنجی و پاکسازی ورودی‌ها"""
    
    def __init__(self):
        self.security_settings = getattr(settings, 'SECURITY_SETTINGS', {})
        self.input_validation = self.security_settings.get('input_validation', {})
        self.suspicious_patterns = self.input_validation.get('suspicious_patterns', [])
        self.max_length = self.input_validation.get('max_length', 1000)
    
    def validate_input(self, data):
        """اعتبارسنجی ورودی‌ها"""
        if not self.input_validation.get('enabled', True):
            return data
        
        validated_data = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # بررسی طول
                if len(value) > self.max_length:
                    raise ValidationError(f'طول فیلد {key} بیش از حد مجاز است.')
                
                # بررسی الگوهای مشکوک
                if self._contains_suspicious_pattern(value):
                    logger.warning(f"Suspicious pattern detected in field {key}")
                    raise ValidationError(f'محتوی مشکوک در فیلد {key} یافت شد.')
                
                # پاکسازی HTML
                value = self._sanitize_html(value)
            
            validated_data[key] = value
        
        return validated_data
    
    def _contains_suspicious_pattern(self, text):
        """بررسی وجود الگوهای مشکوک"""
        for pattern in self.suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _sanitize_html(self, text):
        """پاکسازی HTML"""
        # حذف تگ‌های خطرناک
        dangerous_tags = ['script', 'iframe', 'object', 'embed', 'form']
        for tag in dangerous_tags:
            text = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', text, flags=re.IGNORECASE | re.DOTALL)
            text = re.sub(f'<{tag}[^>]*>', '', text, flags=re.IGNORECASE)
        
        # حذف event handlers
        text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)
        
        return text
    
    def validate_file_upload(self, file):
        """اعتبارسنجی آپلود فایل"""
        file_settings = self.security_settings.get('file_upload', {})
        
        # بررسی اندازه فایل
        max_size = file_settings.get('max_size', 10 * 1024 * 1024)  # 10MB
        if file.size > max_size:
            raise ValidationError('حجم فایل بیش از حد مجاز است.')
        
        # بررسی پسوند فایل
        allowed_extensions = file_settings.get('allowed_extensions', [])
        if allowed_extensions:
            import os
            file_ext = os.path.splitext(file.name)[1].lower()
            if file_ext not in allowed_extensions:
                raise ValidationError('نوع فایل مجاز نیست.')
        
        return True
    
    def log_security_event(self, event_type, details):
        """ثبت رویدادهای امنیتی"""
        logger.warning(f"Security event: {event_type} - {details}")
    
    def check_session_security(self, request):
        """بررسی امنیت نشست"""
        session_settings = self.security_settings.get('session_security', {})
        
        # بررسی تعداد نشست‌های فعال
        max_sessions = session_settings.get('max_sessions_per_user', 5)
        if request.user.is_authenticated:
            active_sessions = request.session.get('active_sessions', 0)
            if active_sessions > max_sessions:
                self.log_security_event('session_limit_exceeded', f"User: {request.user.id}")
                return False
        
        return True 