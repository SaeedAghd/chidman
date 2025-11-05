"""
SEO Middleware پیشرفته
Advanced SEO Middleware
"""

import logging
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class SEOMiddleware(MiddlewareMixin):
    """Middleware پایه برای SEO"""
    
    def process_response(self, request, response):
        """پردازش پاسخ برای SEO"""
        # اضافه کردن headers پایه
        if 'X-Robots-Tag' not in response:
            if request.path.startswith('/admin/'):
                response['X-Robots-Tag'] = 'noindex, nofollow'
            else:
                response['X-Robots-Tag'] = 'index, follow'
        
        return response

class AdvancedSEOMiddleware(MiddlewareMixin):
    """Middleware برای بهینه‌سازی SEO"""
    
    def process_request(self, request):
        """پردازش درخواست برای SEO"""
        # اضافه کردن اطلاعات SEO به request
        request.seo_data = {
            'canonical_url': self._get_canonical_url(request),
            'page_type': self._detect_page_type(request),
            'is_ajax': request.headers.get('X-Requested-With') == 'XMLHttpRequest',
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referer': request.META.get('HTTP_REFERER', ''),
        }
        
        # تشخیص bot ها (شامل AI bots)
        request.is_bot = self._is_bot(request)
        request.is_ai_bot = self._is_ai_bot(request)
        
        return None
    
    def process_response(self, request, response):
        """پردازش پاسخ برای SEO"""
        # اضافه کردن headers برای SEO
        if hasattr(request, 'seo_data'):
            self._add_seo_headers(request, response)
        
        # اضافه کردن cache headers
        self._add_cache_headers(request, response)
        
        # اضافه کردن security headers
        self._add_security_headers(request, response)
        
        return response
    
    def _get_canonical_url(self, request):
        """تولید canonical URL"""
        if hasattr(settings, 'BASE_DOMAIN'):
            return f"https://{settings.BASE_DOMAIN}{request.path}"
        return request.build_absolute_uri(request.path)
    
    def _detect_page_type(self, request):
        """تشخیص نوع صفحه"""
        path = request.path
        
        if path == '/':
            return 'home'
        elif path.startswith('/store/analysis/'):
            return 'analysis'
        elif path.startswith('/store/features/'):
            return 'features'
        elif path.startswith('/store/forms/'):
            return 'forms'
        elif path.startswith('/guide/'):
            return 'guide'
        elif path.startswith('/about/'):
            return 'about'
        elif path.startswith('/contact/'):
            return 'contact'
        else:
            return 'other'
    
    def _is_bot(self, request):
        """تشخیص bot ها (شامل AI bots)"""
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        bot_keywords = [
            # Search Engine Bots
            'googlebot', 'bingbot', 'slurp', 'duckduckbot', 'baiduspider',
            'yandexbot', 'facebookexternalhit', 'twitterbot', 'linkedinbot',
            'whatsapp', 'telegram', 'skype', 'discord', 'slack',
            # AI Bots
            'gptbot', 'chatgpt', 'claudebot', 'anthropic', 'perplexity',
            'google-extended', 'ccbot', 'applebot-extended', 'bingpreview'
        ]
        
        return any(keyword in user_agent for keyword in bot_keywords)
    
    def _is_ai_bot(self, request):
        """تشخیص AI bot ها"""
        from .ai_seo_optimizer import AIBotDetector
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        return AIBotDetector.is_ai_bot(user_agent)
    
    def _add_seo_headers(self, request, response):
        """اضافه کردن headers برای SEO"""
        # Canonical URL
        if hasattr(request, 'seo_data'):
            response['Link'] = f'<{request.seo_data["canonical_url"]}>; rel="canonical"'
        
        # Language
        response['Content-Language'] = 'fa-IR'
        
        # Content Type
        if response.get('Content-Type', '').startswith('text/html'):
            response['Content-Type'] = 'text/html; charset=utf-8'
        
        # X-Robots-Tag
        if request.path.startswith('/admin/'):
            response['X-Robots-Tag'] = 'noindex, nofollow'
        else:
            response['X-Robots-Tag'] = 'index, follow'
    
    def _add_cache_headers(self, request, response):
        """اضافه کردن cache headers"""
        path = request.path
        
        # Static files
        if path.startswith('/static/') or path.startswith('/media/'):
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
            return
        
        # API endpoints
        if path.startswith('/api/'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return
        
        # Admin pages
        if path.startswith('/admin/'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return
        
        # HTML pages
        if response.get('Content-Type', '').startswith('text/html'):
            if hasattr(request, 'is_ai_bot') and request.is_ai_bot:
                # AI bots: cache بیشتر برای دسترسی سریع
                response['Cache-Control'] = 'public, max-age=7200'  # 2 hours
                # اضافه کردن header برای AI bots
                response['X-AI-Friendly'] = 'true'
            elif request.is_bot:
                # سایر Bot ها می‌توانند cache کنند
                response['Cache-Control'] = 'public, max-age=3600'
            else:
                # کاربران عادی cache کمتری دارند
                response['Cache-Control'] = 'public, max-age=300'
    
    def _add_security_headers(self, request, response):
        """اضافه کردن security headers"""
        # X-Content-Type-Options
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options
        response['X-Frame-Options'] = 'DENY'
        
        # X-XSS-Protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Content Security Policy (enhanced) - with Edge compatibility
        import time
        csp_timestamp = int(time.time())
        
        # Get user agent for browser-specific handling
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        is_edge = 'edge' in user_agent or 'edg/' in user_agent
        
        if is_edge:
            # Edge-specific CSP (more permissive for compatibility)
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://www.googletagmanager.com https://www.google-analytics.com https://ssl.google-analytics.com https://connect.facebook.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/; "
                "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
                "img-src 'self' data: https: https://www.google-analytics.com https://ssl.google-analytics.com https://trustseal.enamad.ir; "
                "connect-src 'self' https://www.google-analytics.com https://ssl.google-analytics.com https://www.googletagmanager.com https://region1.google-analytics.com https://*.google-analytics.com; "
                "frame-src 'self' https:;"  # Allow self and https for Edge compatibility
            )
        else:
            # Standard CSP for other browsers
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://www.googletagmanager.com https://www.google-analytics.com https://ssl.google-analytics.com https://connect.facebook.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/; "
                "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
                "img-src 'self' data: blob: https: https://www.google-analytics.com https://ssl.google-analytics.com https://trustseal.enamad.ir; "
                "media-src 'self' blob: data: https:; "  # Allow blob URLs for video preview
                "connect-src 'self' https://www.google-analytics.com https://ssl.google-analytics.com https://www.googletagmanager.com https://region1.google-analytics.com https://*.google-analytics.com; "
                "frame-src 'none';"
            )
        
        response['Content-Security-Policy'] = csp
        response['X-CSP-Timestamp'] = str(csp_timestamp)  # Cache busting header

class SEOLoggingMiddleware(MiddlewareMixin):
    """Middleware برای لاگ کردن اطلاعات SEO"""
    
    def process_request(self, request):
        """لاگ کردن درخواست‌های مهم"""
        if self._should_log_request(request):
            logger.info(f"SEO Request: {request.method} {request.path} - User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}")
        
        return None
    
    def process_response(self, request, response):
        """لاگ کردن پاسخ‌های مهم"""
        if self._should_log_response(request, response):
            logger.info(f"SEO Response: {response.status_code} {request.path} - Content-Type: {response.get('Content-Type', 'Unknown')}")
        
        return response

    def _should_log_request(self, request):
        """تشخیص درخواست‌های مهم برای لاگ"""
        important_paths = [
            '/', '/store/', '/guide/', '/features/', '/about/', '/contact/'
        ]
        
        return (
            any(request.path.startswith(path) for path in important_paths) or
            request.is_bot or
            request.META.get('HTTP_USER_AGENT', '').startswith('Mozilla')
        )
    
    def _should_log_response(self, request, response):
        """تشخیص پاسخ‌های مهم برای لاگ"""
        return (
            response.status_code >= 400 or
            request.is_bot or
            response.get('Content-Type', '').startswith('text/html')
        )