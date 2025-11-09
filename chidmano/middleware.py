"""
Security Headers Middleware for enhanced security
"""

import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.utils import timezone
import time
import json

logger = logging.getLogger(__name__)

class UltraLightHealthMiddleware(MiddlewareMixin):
    """Ultra-light health check middleware"""
    
    def process_request(self, request):
        if request.path == '/health/':
            return HttpResponse('OK', content_type='text/plain')
        return None

class CanonicalHostRedirectMiddleware(MiddlewareMixin):
    """Redirect to canonical host"""
    
    def process_request(self, request):
        if not request.is_secure() and not settings.DEBUG:
            return HttpResponseRedirect(f"https://{request.get_host()}{request.get_full_path()}")
        return None

class NoIndexPrivatePathsMiddleware(MiddlewareMixin):
    """Add noindex to private paths"""
    
    def process_response(self, request, response):
        private_paths = ['/admin/', '/api/', '/store/admin/']
        if any(request.path.startswith(path) for path in private_paths):
            response['X-Robots-Tag'] = 'noindex, nofollow'
        return response

class CSPMiddleware(MiddlewareMixin):
    """Content Security Policy middleware"""
    
    def process_response(self, request, response):
        # CSP header is already handled by SecurityHeadersMiddleware
        return response

class CacheAndTimingMiddleware(MiddlewareMixin):
    """Cache and timing middleware"""
    
    def process_response(self, request, response):
        # Add cache headers for static content
        if request.path.startswith('/static/'):
            response['Cache-Control'] = 'public, max-age=31536000'
        elif request.path.startswith('/media/'):
            response['Cache-Control'] = 'public, max-age=86400'
        else:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        
        # Add timing header
        response['X-Response-Time'] = str(time.time())
        return response

class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware to add security headers and block suspicious requests
    """
    
    # Suspicious patterns to block
    SUSPICIOUS_PATTERNS = [
        '/payment/index.php',
        '/admin.php',
        '/config.php',
        '/wp-admin/',
        '/wp-login.php',
        '/phpmyadmin/',
        '/.env',
        '/.git/',
        '/.gitignore',
        '/.gitattributes',
        '/.gitconfig',
        '/.gitmodules',
        '/backup/',
        '/test/',
        '/debug/',
        '/api/v1/admin',
        # do not include '/admin/' or '/store/admin/' here to avoid blocking legitimate admin dashboards
        '/login.php',
        '/index.php',
        '/shell.php',
        '/cmd.php',
        '/eval.php',
        '/exec.php',
        '/system.php',
        '/info.php',
        '/phpinfo.php',
        '/.htaccess',
        '/robots.txt.bak',
        '/sitemap.xml.bak',
        # Note: /mock/ is allowed for Mock Payment testing
        '/.DS_Store',
        '/Thumbs.db',
        '/web.config',
        '/crossdomain.xml',
        '/clientaccesspolicy.xml',
    ]
    
    # Suspicious user agents
    SUSPICIOUS_USER_AGENTS = [
        'sqlmap',
        'nikto',
        'nmap',
        'masscan',
        'zap',
        'burp',
        'w3af',
        'acunetix',
        'nessus',
        'openvas',
        'skipfish',
        'wget',
        'curl',
        'python-requests',
        'python-urllib',
        'libwww-perl',
        'lwp-trivial',
        'java/',
        # Remove 'bot' and 'crawler' to allow legitimate search engine bots
        'spider',
        'scraper',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """Process incoming request for security checks"""
        
        # Get client IP
        client_ip = self.get_client_ip(request)

        # Allow authenticated staff access to application admin dashboard paths
        # Block non-staff users explicitly (403) without logging as suspicious
        if request.path.startswith('/store/admin/'):
            user = getattr(request, 'user', None)
            if user is None or not (user.is_authenticated and user.is_staff):
                logger.warning(f"Unauthorized admin dashboard access: {request.path} from {client_ip} - User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}")
                return HttpResponse("Forbidden", status=403)
            # Authenticated staff: permit request to proceed
            return None
        
        # Check for suspicious patterns
        if self.is_suspicious_request(request):
            logger.warning(f"Suspicious request blocked: {request.path} from {client_ip} - User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}")
            return HttpResponse("Access Denied", status=403)
        
        # Check for suspicious user agents
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if self.is_suspicious_user_agent(user_agent):
            logger.warning(f"Suspicious user agent blocked: {user_agent} from {client_ip}")
            return HttpResponse("Access Denied", status=403)
        
        return None
    
    def process_response(self, request, response):
        """Add security headers to response"""
        
        # Get user agent for browser-specific handling
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        is_edge = 'edge' in user_agent or 'edg/' in user_agent
        
        # Security Headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # HSTS (HTTP Strict Transport Security)
        if request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        # Content Security Policy (enhanced) - with Edge compatibility
        csp_timestamp = int(time.time())
        
        if is_edge:
            # Edge-specific CSP (more permissive for compatibility)
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://www.googletagmanager.com https://www.google-analytics.com https://ssl.google-analytics.com https://connect.facebook.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/; "
                "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
                "img-src 'self' data: blob: https: https://www.google-analytics.com https://ssl.google-analytics.com https://trustseal.enamad.ir; "
                "media-src 'self' blob: data: https:; "  # Allow blob URLs for video preview
                "connect-src 'self' https://www.google-analytics.com https://ssl.google-analytics.com https://www.googletagmanager.com https://region1.google-analytics.com https://*.google-analytics.com; "
                "frame-src 'self' https:;"  # Allow self and https for Edge compatibility
            )
        else:
            # Standard CSP for other browsers
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://www.googletagmanager.com https://www.google-analytics.com https://ssl.google-analytics.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/; "
                "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
                "img-src 'self' data: blob: https: https://www.google-analytics.com https://ssl.google-analytics.com https://trustseal.enamad.ir; "
                "media-src 'self' blob: data: https:; "  # Allow blob URLs for video preview
                "connect-src 'self' https://www.google-analytics.com https://ssl.google-analytics.com https://www.googletagmanager.com https://region1.google-analytics.com https://*.google-analytics.com; "
                "frame-src 'none';"
            )
        
        response['Content-Security-Policy'] = csp
        response['X-CSP-Timestamp'] = str(csp_timestamp)  # Cache busting header
        
        # Remove server information
        if 'Server' in response:
            del response['Server']
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_suspicious_request(self, request):
        """Check if request is suspicious"""
        path = request.path.lower()
        
        # Check for suspicious patterns
        for pattern in self.SUSPICIOUS_PATTERNS:
            if pattern.lower() in path:
                return True
        
        # Check for multiple slashes (potential path traversal)
        if '//' in path or '../' in path:
            return True
        
        # Check for suspicious file extensions
        suspicious_extensions = ['.php', '.asp', '.aspx', '.jsp', '.cgi', '.pl', '.py', '.sh', '.bat', '.exe']
        for ext in suspicious_extensions:
            if path.endswith(ext):
                return True
        
        return False
    
    def is_suspicious_user_agent(self, user_agent):
        """Check if user agent is suspicious"""
        if not user_agent:
            return False
        
        user_agent_lower = user_agent.lower()
        
        # Allow legitimate search engine bots
        legitimate_bots = [
            'googlebot',
            'bingbot',
            'slurp',  # Yahoo
            'duckduckbot',
            'baiduspider',
            'yandexbot',
            'facebookexternalhit',
            'twitterbot',
            'linkedinbot',
            'whatsapp',
            'telegrambot',
            'applebot',
            'ia_archiver',  # Internet Archive
        ]
        
        # Check if it's a legitimate bot
        for bot in legitimate_bots:
            if bot in user_agent_lower:
                return False
        
        # Check for suspicious patterns
        for pattern in self.SUSPICIOUS_USER_AGENTS:
            if pattern in user_agent_lower:
                return True
        
        # Check for empty or very short user agents
        if len(user_agent.strip()) < 10:
            return True
        
        return False


class RateLimitMiddleware(MiddlewareMixin):
    """
    Simple rate limiting middleware
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}
        super().__init__(get_response)
    
    def process_request(self, request):
        """Check rate limit"""
        client_ip = self.get_client_ip(request)
        current_time = time.time()
        
        # Clean old entries (older than 1 minute)
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip] 
                if current_time - req_time < 60
            ]
        else:
            self.requests[client_ip] = []
        
        # Check rate limit (max 60 requests per minute)
        if len(self.requests[client_ip]) >= 60:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return HttpResponse("Rate limit exceeded", status=429)
        
        # Add current request
        self.requests[client_ip].append(current_time)
        
        return None
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip