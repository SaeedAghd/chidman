import time
import hashlib
import json
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
import re
from user_agents import parse
from ipware import get_client_ip

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

class RateLimitMiddleware:
    """Middleware برای محدودیت نرخ درخواست"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}
    
    def __call__(self, request):
        # ساده‌سازی برای توسعه
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
    """
    میان‌افزار ثبت درخواست‌ها برای تحلیل و امنیت
    """
    
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.sensitive_paths = ['/admin/', '/api/', '/analysis/']
        self.suspicious_patterns = [
            r'<script', r'javascript:', r'vbscript:', r'onload=', r'onerror=',
            r'../', r'\.\./', r'%00', r'%0d', r'%0a', r'%0d%0a'
        ]

    def process_request(self, request):
        """ثبت درخواست ورودی"""
        try:
            # زمان شروع
            request.start_time = time.time()
            
            # بررسی درخواست‌های مشکوک
            if self._is_suspicious_request(request):
                logger.warning(f"Suspicious request detected: {request.path} from {request.META.get('REMOTE_ADDR')}")
            
            # ثبت درخواست‌های حساس
            if any(path in request.path for path in self.sensitive_paths):
                self._log_sensitive_request(request)
                
        except Exception as e:
            logger.error(f"Request logging middleware error: {str(e)}")

    def process_response(self, request, response):
        """ثبت پاسخ خروجی"""
        try:
            if hasattr(request, 'start_time'):
                duration = time.time() - request.start_time
                
                # ثبت درخواست‌های کند
                if duration > 5.0:  # بیش از 5 ثانیه
                    logger.warning(f"Slow request: {request.path} took {duration:.2f}s")
                
                # اضافه کردن هدر مدت زمان
                response['X-Request-Duration'] = f"{duration:.3f}"
            
            return response
            
        except Exception as e:
            logger.error(f"Response logging middleware error: {str(e)}")
            return response

    def _is_suspicious_request(self, request):
        """بررسی درخواست مشکوک"""
        try:
            # بررسی پارامترها
            for param_name, param_value in request.GET.items():
                if self._contains_suspicious_pattern(param_value):
                    return True
            
            # بررسی POST data
            if request.POST:
                for param_name, param_value in request.POST.items():
                    if self._contains_suspicious_pattern(param_value):
                        return True
            
            # بررسی User-Agent
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            if not user_agent or len(user_agent) > 500:
                return True

            return False
            
        except Exception as e:
            logger.error(f"Error checking suspicious request: {str(e)}")
            return False

    def _contains_suspicious_pattern(self, value):
        """بررسی وجود الگوهای مشکوک"""
        if not isinstance(value, str):
            return False
        
        for pattern in self.suspicious_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        return False

    def _log_sensitive_request(self, request):
        """ثبت درخواست حساس"""
        try:
            log_data = {
                'timestamp': timezone.now().isoformat(),
                'ip': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'method': request.method,
                'path': request.path,
                'user': request.user.username if request.user.is_authenticated else 'anonymous',
                'referer': request.META.get('HTTP_REFERER', ''),
            }
            
            logger.info(f"Sensitive request: {json.dumps(log_data)}")
            
        except Exception as e:
            logger.error(f"Error logging sensitive request: {str(e)}")

class PerformanceMiddleware(MiddlewareMixin):
    """
    میان‌افزار بهینه‌سازی عملکرد
    """
    
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.slow_threshold = 2.0  # 2 ثانیه
        self.db_query_threshold = 50  # 50 کوئری

    def process_request(self, request):
        """آماده‌سازی برای نظارت عملکرد"""
        try:
            request.start_time = time.time()
            
            # برای نظارت کوئری‌های دیتابیس
            if hasattr(settings, 'DEBUG') and settings.DEBUG:
                from django.db import connection
                connection.queries_log = True
                connection.queries = []
                
        except Exception as e:
            logger.error(f"Performance middleware error: {str(e)}")
    
    def process_response(self, request, response):
        """نظارت عملکرد پاسخ"""
        try:
            if hasattr(request, 'start_time'):
                duration = time.time() - request.start_time
                
                # بررسی عملکرد کند
                if duration > self.slow_threshold:
                    self._log_slow_request(request, duration)
                
                # بررسی کوئری‌های زیاد
                if hasattr(settings, 'DEBUG') and settings.DEBUG:
                    from django.db import connection
                    query_count = len(connection.queries)
                    if query_count > self.db_query_threshold:
                        self._log_heavy_queries(request, query_count)
                
                # اضافه کردن هدرهای عملکرد
                response['X-Response-Time'] = f"{duration:.3f}s"
                
            return response
            
        except Exception as e:
            logger.error(f"Performance middleware response error: {str(e)}")
            return response

    def _log_slow_request(self, request, duration):
        """ثبت درخواست کند"""
        logger.warning(
            f"Slow request detected: {request.method} {request.path} "
            f"took {duration:.2f}s from {request.META.get('REMOTE_ADDR')}"
        )

    def _log_heavy_queries(self, request, query_count):
        """ثبت کوئری‌های سنگین"""
        logger.warning(
            f"Heavy database usage: {request.method} {request.path} "
            f"executed {query_count} queries"
        )

class UserAgentMiddleware(MiddlewareMixin):
    """
    میان‌افزار تحلیل User-Agent
    """
    
    def process_request(self, request):
        """تحلیل User-Agent"""
        try:
            user_agent_string = request.META.get('HTTP_USER_AGENT', '')
            if user_agent_string:
                user_agent = parse(user_agent_string)
                
                # ذخیره اطلاعات User-Agent
                request.user_agent = {
                    'browser': user_agent.browser.family,
                    'browser_version': user_agent.browser.version_string,
                    'os': user_agent.os.family,
                    'os_version': user_agent.os.version_string,
                    'device': user_agent.device.family,
                    'is_mobile': user_agent.is_mobile,
                    'is_tablet': user_agent.is_tablet,
                    'is_pc': user_agent.is_pc,
                    'is_bot': user_agent.is_bot,
                }
                
                # ثبت bot ها
                if user_agent.is_bot:
                    logger.info(f"Bot detected: {user_agent_string}")
                    
        except Exception as e:
            logger.error(f"User agent middleware error: {str(e)}")

class MaintenanceMiddleware(MiddlewareMixin):
    """
    میان‌افزار حالت نگهداری
    """
    
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.maintenance_mode = getattr(settings, 'MAINTENANCE_MODE', False)
        self.maintenance_allowed_ips = getattr(settings, 'MAINTENANCE_ALLOWED_IPS', [])
        self.maintenance_exempt_paths = [
            '/admin/', '/static/', '/media/', '/health/', '/maintenance/'
        ]

    def process_request(self, request):
        """بررسی حالت نگهداری"""
        try:
            if not self.maintenance_mode:
                return None
            
            # بررسی IP مجاز
            client_ip, is_routable = get_client_ip(request)
            if client_ip in self.maintenance_allowed_ips:
                return None
            
            # بررسی مسیرهای معاف
            for exempt_path in self.maintenance_exempt_paths:
                if exempt_path in request.path:
                    return None
            
            # نمایش صفحه نگهداری
            return self._show_maintenance_page(request)
            
        except Exception as e:
            logger.error(f"Maintenance middleware error: {str(e)}")
            return None

    def _show_maintenance_page(self, request):
        """نمایش صفحه نگهداری"""
        from django.shortcuts import render
        return render(request, 'maintenance.html', status=503)

class CacheControlMiddleware(MiddlewareMixin):
    """
    میان‌افزار کنترل کش
    """
    
    def process_response(self, request, response):
        """تنظیم هدرهای کش"""
        try:
            # مسیرهای بدون کش
            no_cache_paths = ['/admin/', '/api/', '/analysis/']
            if any(path in request.path for path in no_cache_paths):
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
            else:
                # کش برای صفحات استاتیک
                if request.path.startswith('/static/') or request.path.startswith('/media/'):
                    response['Cache-Control'] = 'public, max-age=31536000'  # 1 سال
                else:
                    response['Cache-Control'] = 'public, max-age=300'  # 5 دقیقه
            
            return response
        
        except Exception as e:
            logger.error(f"Cache control middleware error: {str(e)}")
            return response 