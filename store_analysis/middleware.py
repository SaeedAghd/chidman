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

class RateLimitMiddleware(MiddlewareMixin):
    """
    میان‌افزار محدودیت نرخ درخواست با قابلیت‌های پیشرفته
    """
    
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.rate_limits = {
            'default': {'requests': 100, 'window': 60},  # 100 درخواست در دقیقه
            'api': {'requests': 50, 'window': 60},       # 50 درخواست API در دقیقه
            'analysis': {'requests': 10, 'window': 300}, # 10 تحلیل در 5 دقیقه
            'upload': {'requests': 5, 'window': 60},     # 5 آپلود در دقیقه
            'login': {'requests': 5, 'window': 300},     # 5 تلاش ورود در 5 دقیقه
        }
    
    def process_request(self, request):
        """پردازش درخواست و بررسی محدودیت نرخ"""
        try:
            # تشخیص نوع درخواست
            request_type = self._get_request_type(request)
            
            # دریافت IP کاربر
            client_ip, is_routable = get_client_ip(request)
            if not client_ip:
                client_ip = 'unknown'
            
            # ایجاد کلید کش
            cache_key = f"rate_limit:{client_ip}:{request_type}"
        
        # بررسی محدودیت نرخ
            if not self._check_rate_limit(request, request_type, client_ip, cache_key):
                return self._create_rate_limit_response(request_type)
            
            # ثبت درخواست
            self._record_request(cache_key, request_type)
            
        except Exception as e:
            logger.error(f"Rate limit middleware error: {str(e)}")
            # در صورت خطا، اجازه عبور می‌دهیم اما لاگ می‌کنیم
        return None
    
    def _get_request_type(self, request):
        """تشخیص نوع درخواست"""
        path = request.path.lower()
        
        if '/api/' in path:
            return 'api'
        elif '/analysis/' in path or 'start_analysis' in path:
            return 'analysis'
        elif '/upload/' in path or request.FILES:
            return 'upload'
        elif '/login/' in path or '/accounts/login/' in path:
            return 'login'
        else:
            return 'default'
    
    def _check_rate_limit(self, request, request_type, client_ip, cache_key):
        """بررسی محدودیت نرخ"""
        try:
            # دریافت تنظیمات محدودیت
            limit_config = self.rate_limits.get(request_type, self.rate_limits['default'])
            max_requests = limit_config['requests']
            window = limit_config['window']
            
            # دریافت تعداد درخواست‌های فعلی
            current_requests = cache.get(cache_key, 0)
            
            # بررسی محدودیت
            if current_requests >= max_requests:
                logger.warning(f"Rate limit exceeded for {client_ip} on {request_type}: {current_requests}/{max_requests}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {str(e)}")
            return True  # در صورت خطا اجازه عبور

    def _record_request(self, cache_key, request_type):
        """ثبت درخواست"""
        try:
            limit_config = self.rate_limits.get(request_type, self.rate_limits['default'])
            window = limit_config['window']
            
            # افزایش شمارنده
            current_requests = cache.get(cache_key, 0)
            cache.set(cache_key, current_requests + 1, window)
            
        except Exception as e:
            logger.error(f"Error recording request: {str(e)}")

    def _create_rate_limit_response(self, request_type):
        """ایجاد پاسخ محدودیت نرخ"""
        messages = {
            'default': 'تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً کمی صبر کنید.',
            'api': 'محدودیت نرخ API. لطفاً درخواست‌های خود را کاهش دهید.',
            'analysis': 'محدودیت تحلیل. لطفاً بین تحلیل‌ها فاصله زمانی قرار دهید.',
            'upload': 'محدودیت آپلود. لطفاً فایل‌های خود را در چندین مرحله آپلود کنید.',
            'login': 'تعداد تلاش‌های ورود بیش از حد مجاز است. لطفاً 5 دقیقه صبر کنید.',
        }
        
        return JsonResponse({
            'error': 'محدودیت نرخ درخواست',
            'message': messages.get(request_type, messages['default']),
            'retry_after': 60
        }, status=429)

class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    میان‌افزار هدرهای امنیتی پیشرفته
    """
    
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': self._get_csp_policy(),
        }

    def _get_csp_policy(self):
        """سیاست امنیت محتوا"""
        return (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://code.jquery.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https:; "
            "media-src 'self' https:; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none';"
        )

    def process_response(self, request, response):
        """اضافه کردن هدرهای امنیتی به پاسخ"""
        try:
            for header, value in self.security_headers.items():
                if header not in response:
                    response[header] = value
            
            # اضافه کردن هدرهای اضافی برای API
            if '/api/' in request.path:
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
            
            return response
            
        except Exception as e:
            logger.error(f"Security headers middleware error: {str(e)}")
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