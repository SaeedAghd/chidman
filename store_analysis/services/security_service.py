import re
import logging
import hashlib
import mimetypes
from typing import Optional, List
from django.conf import settings
from django.core.exceptions import ValidationError
from ..exceptions import SecurityError

logger = logging.getLogger(__name__)

class SecurityService:
    """سرویس امنیتی برای پاکسازی و اعتبارسنجی داده‌ها"""
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """پاکسازی ورودی از کدهای مخرب"""
        if not text:
            return text
            
        # حذف تگ‌های HTML
        text = re.sub(r'<[^>]*>', '', text)
        
        # حذف اسکریپت‌های مخرب
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        text = re.sub(r'vbscript:', '', text, flags=re.IGNORECASE)
        text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)
        
        # حذف کاراکترهای خطرناک
        text = text.replace('\\', '\\\\')
        text = text.replace('"', '\\"')
        text = text.replace("'", "\\'")
        
        return text.strip()
    
    @staticmethod
    def validate_file_upload(file, allowed_extensions: List[str], max_size: int) -> bool:
        """اعتبارسنجی فایل آپلود شده"""
        try:
            # بررسی اندازه فایل
            if file.size > max_size:
                raise SecurityError(f"حجم فایل نباید بیشتر از {max_size} بایت باشد")
            
            # بررسی پسوند فایل
            file_name = file.name.lower()
            if not any(file_name.endswith(ext) for ext in allowed_extensions):
                raise SecurityError(f"پسوند فایل مجاز نیست. پسوندهای مجاز: {', '.join(allowed_extensions)}")
            
            # بررسی نوع MIME
            mime_type, _ = mimetypes.guess_type(file_name)
            if mime_type and mime_type.startswith('text/'):
                # بررسی محتوای فایل‌های متنی
                content = file.read(1024).decode('utf-8', errors='ignore')
                if '<script' in content.lower():
                    raise SecurityError("فایل حاوی کد مخرب است")
                file.seek(0)  # بازگشت به ابتدای فایل
            
            return True
            
        except Exception as e:
            logger.error(f"File validation error: {str(e)}")
            raise SecurityError(f"خطا در اعتبارسنجی فایل: {str(e)}")
    
    @staticmethod
    def generate_secure_filename(filename: str) -> str:
        """تولید نام فایل امن"""
        import uuid
        import os
        
        # حذف کاراکترهای خطرناک
        safe_name = re.sub(r'[^\w\-_.]', '_', filename)
        
        # اضافه کردن UUID برای امنیت بیشتر
        name, ext = os.path.splitext(safe_name)
        return f"{name}_{uuid.uuid4().hex[:8]}{ext}"
    
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """اعتبارسنجی قدرت رمز عبور"""
        if len(password) < 8:
            return False
        
        # بررسی وجود حروف بزرگ و کوچک
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        
        # بررسی وجود اعداد
        if not re.search(r'\d', password):
            return False
        
        # بررسی وجود کاراکترهای خاص
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        
        return True

class FileSecurityValidator:
    """اعتبارسنج امنیتی فایل‌ها"""
    
    ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt']
    ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.wmv']
    
    @classmethod
    def validate_image(cls, file) -> bool:
        """اعتبارسنجی فایل تصویر"""
        return SecurityService.validate_file_upload(
            file, 
            cls.ALLOWED_IMAGE_EXTENSIONS, 
            5 * 1024 * 1024  # 5MB
        )
    
    @classmethod
    def validate_document(cls, file) -> bool:
        """اعتبارسنجی فایل مستند"""
        return SecurityService.validate_file_upload(
            file, 
            cls.ALLOWED_DOCUMENT_EXTENSIONS, 
            10 * 1024 * 1024  # 10MB
        )
    
    @classmethod
    def validate_video(cls, file) -> bool:
        """اعتبارسنجی فایل ویدیو"""
        return SecurityService.validate_file_upload(
            file, 
            cls.ALLOWED_VIDEO_EXTENSIONS, 
            50 * 1024 * 1024  # 50MB
        ) 