"""
Security Headers Middleware for enhanced security
"""

import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.conf import settings
import time

logger = logging.getLogger(__name__)

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
        '/backup/',
        '/test/',
        '/debug/',
        '/api/v1/admin',
        '/admin/',
        '/administrator/',
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
        'bot',
        'crawler',
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
        
        # Security Headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # HSTS (HTTP Strict Transport Security)
        if request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        # Content Security Policy (basic)
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://www.googletagmanager.com https://www.google-analytics.com https://ssl.google-analytics.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
            "img-src 'self' data: https: https://www.google-analytics.com https://ssl.google-analytics.com https://trustseal.enamad.ir; "
            "connect-src 'self' https://www.google-analytics.com https://ssl.google-analytics.com https://www.googletagmanager.com; "
            "frame-src 'none';"
        )
        response['Content-Security-Policy'] = csp
        
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