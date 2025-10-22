"""
Browser Compatibility Middleware
حل مشکلات سازگاری با مرورگرهای مختلف
"""

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class BrowserCompatibilityMiddleware(MiddlewareMixin):
    """Middleware برای حل مشکلات سازگاری با مرورگرها"""
    
    def process_request(self, request):
        """پردازش درخواست برای سازگاری با مرورگرها"""
        # تنظیم headers برای سازگاری
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # تشخیص مرورگر
        if 'Edge' in user_agent or 'Edg/' in user_agent:
            request.browser = 'edge'
        elif 'Chrome' in user_agent and 'Edg' not in user_agent:
            request.browser = 'chrome'
        elif 'Firefox' in user_agent:
            request.browser = 'firefox'
        elif 'Safari' in user_agent and 'Chrome' not in user_agent:
            request.browser = 'safari'
        else:
            request.browser = 'unknown'
        
        # تنظیمات خاص برای هر مرورگر
        if request.browser == 'edge':
            # Edge نیاز به تنظیمات خاص دارد - کاهش محدودیت‌ها
            request.edge_compatibility = True
        elif request.browser == 'chrome':
            # Chrome تنظیمات خاص
            pass
        
        return None
    
    def process_response(self, request, response):
        """پردازش پاسخ برای سازگاری با مرورگرها"""
        # تنظیم headers برای سازگاری
        if hasattr(request, 'browser'):
            if request.browser == 'edge':
                # Edge نیاز به headers خاص دارد - کاهش محدودیت‌ها
                response['X-Content-Type-Options'] = 'nosniff'
                response['X-Frame-Options'] = 'SAMEORIGIN'  # کمتر محدودکننده
                response['X-XSS-Protection'] = '1; mode=block'
                # حذف CSP سخت‌گیرانه برای Edge
                if 'Content-Security-Policy' in response:
                    # CSP را برای Edge کمتر محدودکننده می‌کنیم
                    pass
            elif request.browser == 'chrome':
                # Chrome تنظیمات خاص
                response['X-Content-Type-Options'] = 'nosniff'
            elif request.browser == 'firefox':
                # Firefox تنظیمات خاص
                response['X-Content-Type-Options'] = 'nosniff'
        
        # تنظیمات عمومی برای همه مرورگرها (کمتر محدودکننده برای Edge)
        if hasattr(request, 'browser') and request.browser == 'edge':
            # Edge نیاز به cache کمتری دارد
            response['Cache-Control'] = 'no-cache, must-revalidate'
            response['Pragma'] = 'no-cache'
        else:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response

class SEOEnhancementMiddleware(MiddlewareMixin):
    """Middleware برای بهبود SEO"""
    
    def process_response(self, request, response):
        """اضافه کردن headers برای SEO"""
        
        # تنظیم headers برای SEO
        if hasattr(response, 'headers'):
            # تنظیم Content-Type
            if not response.get('Content-Type'):
                response['Content-Type'] = 'text/html; charset=utf-8'
            
            # تنظیم Cache-Control برای صفحات مختلف
            if request.path.startswith('/static/') or request.path.startswith('/media/'):
                response['Cache-Control'] = 'public, max-age=31536000'  # 1 year
            elif request.path.startswith('/admin/'):
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            else:
                response['Cache-Control'] = 'public, max-age=3600'  # 1 hour
            
            # تنظیم ETag برای caching
            if not response.get('ETag'):
                import hashlib
                content_hash = hashlib.md5(response.content).hexdigest()
                response['ETag'] = f'"{content_hash}"'
            
            # تنظیم Last-Modified
            if not response.get('Last-Modified'):
                from django.utils.http import http_date
                from datetime import datetime
                response['Last-Modified'] = http_date(datetime.now().timestamp())
            
            # تنظیم Vary header
            vary_headers = ['Accept-Encoding', 'User-Agent']
            if response.get('Vary'):
                vary_headers.extend(response['Vary'].split(','))
            response['Vary'] = ', '.join(set(vary_headers))
        
        return response

class SearchEngineOptimizationMiddleware(MiddlewareMixin):
    """Middleware برای بهینه‌سازی موتورهای جستجو"""
    
    def process_request(self, request):
        """پردازش درخواست برای SEO"""
        
        # تشخیص bot های موتورهای جستجو
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        if any(bot in user_agent for bot in ['googlebot', 'bingbot', 'slurp', 'duckduckbot', 'baiduspider', 'yandexbot']):
            request.is_search_engine_bot = True
        else:
            request.is_search_engine_bot = False
        
        return None
    
    def process_response(self, request, response):
        """پردازش پاسخ برای SEO"""
        
        # تنظیمات خاص برای bot های موتورهای جستجو
        if hasattr(request, 'is_search_engine_bot') and request.is_search_engine_bot:
            # اضافه کردن headers خاص برای bot ها
            response['X-Robots-Tag'] = 'index, follow'
            
            # تنظیم Content-Type برای bot ها
            if response.get('Content-Type') and 'text/html' in response.get('Content-Type'):
                response['Content-Type'] = 'text/html; charset=utf-8'
        
        return response

class ConcurrencyLimitMiddleware(MiddlewareMixin):
    """Middleware برای مدیریت محدودیت concurrency"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.active_requests = {}
        super().__init__(get_response)
    
    def process_request(self, request):
        """بررسی محدودیت concurrency"""
        user_id = request.user.id if request.user.is_authenticated else request.META.get('REMOTE_ADDR')
        
        if user_id:
            # بررسی تعداد درخواست‌های فعال
            if user_id in self.active_requests:
                if self.active_requests[user_id] >= 3:  # حداکثر 3 درخواست همزمان
                    logger.warning(f"Concurrency limit exceeded for user {user_id}")
                    return JsonResponse({
                        'error': 'تعداد درخواست‌های همزمان بیش از حد مجاز است. لطفاً کمی صبر کنید.',
                        'code': 'CONCURRENCY_LIMIT_EXCEEDED'
                    }, status=429)
                else:
                    self.active_requests[user_id] += 1
            else:
                self.active_requests[user_id] = 1
        
        return None
    
    def process_response(self, request, response):
        """کاهش تعداد درخواست‌های فعال"""
        user_id = request.user.id if request.user.is_authenticated else request.META.get('REMOTE_ADDR')
        
        if user_id and user_id in self.active_requests:
            self.active_requests[user_id] -= 1
            if self.active_requests[user_id] <= 0:
                del self.active_requests[user_id]
        
        return response

class SEOEnhancementMiddleware(MiddlewareMixin):
    """Middleware برای بهبود SEO"""
    
    def process_response(self, request, response):
        """اضافه کردن headers برای SEO"""
        
        # تنظیم headers برای SEO
        if hasattr(response, 'headers'):
            # تنظیم Content-Type
            if not response.get('Content-Type'):
                response['Content-Type'] = 'text/html; charset=utf-8'
            
            # تنظیم Cache-Control برای صفحات مختلف
            if request.path.startswith('/static/') or request.path.startswith('/media/'):
                response['Cache-Control'] = 'public, max-age=31536000'  # 1 year
            elif request.path.startswith('/admin/'):
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            else:
                response['Cache-Control'] = 'public, max-age=3600'  # 1 hour
            
            # تنظیم ETag برای caching
            if not response.get('ETag'):
                import hashlib
                content_hash = hashlib.md5(response.content).hexdigest()
                response['ETag'] = f'"{content_hash}"'
            
            # تنظیم Last-Modified
            if not response.get('Last-Modified'):
                from django.utils.http import http_date
                from datetime import datetime
                response['Last-Modified'] = http_date(datetime.now().timestamp())
            
            # تنظیم Vary header
            vary_headers = ['Accept-Encoding', 'User-Agent']
            if response.get('Vary'):
                vary_headers.extend(response['Vary'].split(','))
            response['Vary'] = ', '.join(set(vary_headers))
        
        return response

class SearchEngineOptimizationMiddleware(MiddlewareMixin):
    """Middleware برای بهینه‌سازی موتورهای جستجو"""
    
    def process_request(self, request):
        """پردازش درخواست برای SEO"""
        
        # تشخیص bot های موتورهای جستجو
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        if any(bot in user_agent for bot in ['googlebot', 'bingbot', 'slurp', 'duckduckbot', 'baiduspider', 'yandexbot']):
            request.is_search_engine_bot = True
        else:
            request.is_search_engine_bot = False
        
        return None
    
    def process_response(self, request, response):
        """پردازش پاسخ برای SEO"""
        
        # تنظیمات خاص برای bot های موتورهای جستجو
        if hasattr(request, 'is_search_engine_bot') and request.is_search_engine_bot:
            # اضافه کردن headers خاص برای bot ها
            response['X-Robots-Tag'] = 'index, follow'
            
            # تنظیم Content-Type برای bot ها
            if response.get('Content-Type') and 'text/html' in response.get('Content-Type'):
                response['Content-Type'] = 'text/html; charset=utf-8'
        
        return response

class SessionFixMiddleware(MiddlewareMixin):
    """Middleware برای حل مشکلات session"""
    
    def process_request(self, request):
        """بررسی و تنظیم session"""
        # بررسی وجود session
        if not request.session.session_key:
            request.session.create()
        
        # تنظیم session برای مرورگرهای مختلف
        if hasattr(request, 'browser'):
            if request.browser == 'edge':
                # Edge نیاز به تنظیمات خاص session دارد
                request.session.set_expiry(3600)  # 1 ساعت
            elif request.browser == 'chrome':
                # Chrome تنظیمات خاص
                request.session.set_expiry(3600)
        
        return None
    
    def process_response(self, request, response):
        """تنظیم cookies برای سازگاری"""
        # تنظیم SameSite برای cookies
        if hasattr(request, 'browser'):
            if request.browser in ['edge', 'chrome']:
                # تنظیم SameSite=Lax برای مرورگرهای مدرن
                if hasattr(response, 'cookies'):
                    for cookie in response.cookies.values():
                        cookie['samesite'] = 'Lax'
        
        return response

class SEOEnhancementMiddleware(MiddlewareMixin):
    """Middleware برای بهبود SEO"""
    
    def process_response(self, request, response):
        """اضافه کردن headers برای SEO"""
        
        # تنظیم headers برای SEO
        if hasattr(response, 'headers'):
            # تنظیم Content-Type
            if not response.get('Content-Type'):
                response['Content-Type'] = 'text/html; charset=utf-8'
            
            # تنظیم Cache-Control برای صفحات مختلف
            if request.path.startswith('/static/') or request.path.startswith('/media/'):
                response['Cache-Control'] = 'public, max-age=31536000'  # 1 year
            elif request.path.startswith('/admin/'):
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            else:
                response['Cache-Control'] = 'public, max-age=3600'  # 1 hour
            
            # تنظیم ETag برای caching
            if not response.get('ETag'):
                import hashlib
                content_hash = hashlib.md5(response.content).hexdigest()
                response['ETag'] = f'"{content_hash}"'
            
            # تنظیم Last-Modified
            if not response.get('Last-Modified'):
                from django.utils.http import http_date
                from datetime import datetime
                response['Last-Modified'] = http_date(datetime.now().timestamp())
            
            # تنظیم Vary header
            vary_headers = ['Accept-Encoding', 'User-Agent']
            if response.get('Vary'):
                vary_headers.extend(response['Vary'].split(','))
            response['Vary'] = ', '.join(set(vary_headers))
        
        return response

class SearchEngineOptimizationMiddleware(MiddlewareMixin):
    """Middleware برای بهینه‌سازی موتورهای جستجو"""
    
    def process_request(self, request):
        """پردازش درخواست برای SEO"""
        
        # تشخیص bot های موتورهای جستجو
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        if any(bot in user_agent for bot in ['googlebot', 'bingbot', 'slurp', 'duckduckbot', 'baiduspider', 'yandexbot']):
            request.is_search_engine_bot = True
        else:
            request.is_search_engine_bot = False
        
        return None
    
    def process_response(self, request, response):
        """پردازش پاسخ برای SEO"""
        
        # تنظیمات خاص برای bot های موتورهای جستجو
        if hasattr(request, 'is_search_engine_bot') and request.is_search_engine_bot:
            # اضافه کردن headers خاص برای bot ها
            response['X-Robots-Tag'] = 'index, follow'
            
            # تنظیم Content-Type برای bot ها
            if response.get('Content-Type') and 'text/html' in response.get('Content-Type'):
                response['Content-Type'] = 'text/html; charset=utf-8'
        
        return response
