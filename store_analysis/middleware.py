import time
import logging
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

class RateLimitMiddleware(MiddlewareMixin):
    """Middleware برای محدودیت نرخ درخواست"""
    
    def process_request(self, request):
        # بررسی اینکه آیا rate limiting فعال است
        if not hasattr(settings, 'SECURITY_SETTINGS') or not settings.SECURITY_SETTINGS.get('rate_limiting', {}).get('enabled', False):
            return None
        
        # جلوگیری از اجرای مجدد برای درخواست‌های static
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return None
            
        # شناسایی نوع درخواست
        request_type = self._get_request_type(request)
        rate_settings = settings.SECURITY_SETTINGS['rate_limiting']
        
        # تنظیمات محدودیت بر اساس نوع درخواست
        if request_type == 'login':
            max_requests = rate_settings.get('login_requests', 5)
            window = rate_settings.get('login_window', 300)
        elif request_type == 'api':
            max_requests = rate_settings.get('api_requests', 50)
            window = rate_settings.get('api_window', 60)
        elif request_type == 'upload':
            max_requests = rate_settings.get('upload_requests', 10)
            window = rate_settings.get('upload_window', 300)
        else:
            max_requests = rate_settings.get('default_requests', 100)
            window = rate_settings.get('default_window', 60)
        
        # بررسی محدودیت نرخ
        if not self._check_rate_limit(request, request_type, max_requests, window):
            user_info = getattr(request, 'user', 'anonymous')
            logger.warning(f"Rate limit exceeded for {user_info} on {request.path}")
            return JsonResponse({
                'error': 'محدودیت نرخ درخواست. لطفاً کمی صبر کنید.',
                'retry_after': window
            }, status=429)
        
        return None
    
    def _get_request_type(self, request):
        """تعیین نوع درخواست"""
        path = request.path.lower()
        
        if 'login' in path or 'auth' in path:
            return 'login'
        elif 'api' in path:
            return 'api'
        elif 'upload' in path or request.FILES:
            return 'upload'
        else:
            return 'default'
    
    def _check_rate_limit(self, request, request_type, max_requests, window):
        """بررسی محدودیت نرخ"""
        # شناسایی کلید محدودیت
        if hasattr(request, 'user') and request.user.is_authenticated:
            key = f"rate_limit:{request_type}:{request.user.id}"
        else:
            key = f"rate_limit:{request_type}:{request.META.get('REMOTE_ADDR', 'unknown')}"
        
        # بررسی تعداد درخواست‌ها
        current_requests = cache.get(key, 0)
        
        if current_requests >= max_requests:
            return False
        
        # افزایش شمارنده
        cache.set(key, current_requests + 1, window)
        return True


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Middleware برای اضافه کردن هدرهای امنیتی"""
    
    def process_response(self, request, response):
        # هدرهای امنیتی پایه
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # هدرهای اضافی برای HTTPS
        if not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # هدرهای محتوای امنیتی
        if hasattr(settings, 'SECURITY_SETTINGS'):
            csp_policy = self._get_csp_policy()
            if csp_policy:
                response['Content-Security-Policy'] = csp_policy
        
        return response
    
    def _get_csp_policy(self):
        """ایجاد سیاست CSP"""
        return "default-src 'self'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; img-src 'self' data:; font-src 'self' cdn.jsdelivr.net;" 