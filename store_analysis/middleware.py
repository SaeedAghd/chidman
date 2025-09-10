import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.conf import settings
import re

logger = logging.getLogger(__name__)

class SecurityMiddleware:
    """Middleware برای بهبود امنیت سایت"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # مسیرهایی که نیاز به احراز هویت دارند
        self.protected_paths = [
            r'^/store/store-analysis/',
            r'^/store/dashboard/',
            r'^/store/analyses/',
            r'^/store/professional-dashboard/',
        ]
        
        # مسیرهایی که همیشه در دسترس هستند
        self.public_paths = [
            r'^/$',
            r'^/accounts/',
            r'^/admin/',
            r'^/health/',
            r'^/static/',
            r'^/media/',
        ]
    
    def __call__(self, request):
        # بررسی مسیر درخواست
        path = request.path_info
        
        # بررسی مسیرهای عمومی
        for pattern in self.public_paths:
            if re.match(pattern, path):
                return self.get_response(request)
        
        # بررسی مسیرهای محافظت شده
        for pattern in self.protected_paths:
            if re.match(pattern, path):
                if not request.user.is_authenticated:
                    return HttpResponseForbidden("دسترسی غیرمجاز")
                break
        
        return self.get_response(request)

class SecurityHeadersMiddleware:
    """Middleware برای اضافه کردن هدرهای امنیتی"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # اضافه کردن هدرهای امنیتی
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response

class RequestLoggingMiddleware(MiddlewareMixin):
    """میان‌افزار ثبت درخواست‌ها"""

    def process_request(self, request):
        """ثبت درخواست ورودی"""
        try:
            request.start_time = time.time()
        except Exception as e:
            logger.error(f"Request logging middleware error: {str(e)}")

    def process_response(self, request, response):
        """ثبت پاسخ خروجی"""
        try:
            if hasattr(request, 'start_time'):
                duration = time.time() - request.start_time
                response['X-Request-Duration'] = f"{duration:.3f}"
            return response
        except Exception as e:
            logger.error(f"Response logging middleware error: {str(e)}")
            return response
