from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.http import HttpResponse, HttpResponsePermanentRedirect


class UltraLightHealthMiddleware:
    """Return 200 OK immediately for /health and /health/ without touching DB or sessions.
    Place this middleware at the very top of MIDDLEWARE.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path == '/health' or path == '/health/':
            # Return immediately without any Django processing
            response = HttpResponse('OK', content_type='text/plain', status=200)
            # Add CORS headers if needed
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        return self.get_response(request)


class CanonicalHostRedirectMiddleware:
    """Redirect all requests to the canonical host in production.

    - Preserves path and query string
    - Skips for health, admin, static, media
    - Only active when PRODUCTION=True
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.canonical_host = 'chidmano.ir'

    def __call__(self, request):
        # Only redirect in production, not in development
        is_production = getattr(settings, 'PRODUCTION', False)
        is_debug = getattr(settings, 'DEBUG', True)
        
        # Only redirect if we're in production AND not in debug mode
        if is_production and not is_debug:
            host = request.get_host().split(':')[0]
            path = request.path
            if host and host != self.canonical_host:
                # Skip safe paths
                if not (path.startswith('/health') or path.startswith('/admin') or path.startswith('/static') or path.startswith('/media') or path.startswith('/favicon.ico')):
                    scheme = 'https'
                    parts = urlsplit(request.build_absolute_uri())
                    new_url = urlunsplit((scheme, self.canonical_host, parts.path, parts.query, parts.fragment))
                    return HttpResponsePermanentRedirect(new_url)

        response = self.get_response(request)
        return response


class NoIndexPrivatePathsMiddleware:
    """Add X-Robots-Tag: noindex for private areas without touching templates."""

    PRIVATE_PREFIXES = (
        '/admin',
        '/accounts',
        '/store/dashboard',
        '/store/analysis',
        '/api',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        for prefix in self.PRIVATE_PREFIXES:
            if request.path.startswith(prefix):
                response.headers['X-Robots-Tag'] = 'noindex, follow'
                break
        return response


class CSPMiddleware:
    """Content Security Policy middleware to allow blob URLs for video previews."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add CSP header to allow CDN resources and blob URLs
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://code.jquery.com; "
            "script-src-elem 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://code.jquery.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com https://fonts.gstatic.com; "
            "style-src-elem 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com https://fonts.gstatic.com; "
            "img-src 'self' data: blob: https:; "
            "media-src 'self' blob: data: https:; "
            "font-src 'self' data: https: https://fonts.gstatic.com https://cdn.jsdelivr.net; "
            "connect-src 'self' data: blob: https://api.payping.ir https://payping.ir https://cdn.jsdelivr.net https://fonts.googleapis.com https://fonts.gstatic.com https://code.jquery.com; "
            "frame-src 'self' https://payping.ir; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self' https://payping.ir https://api.payping.ir https:; "
            "worker-src 'self' blob:; "
            "child-src 'self' blob:"
        )
        
        response.headers['Content-Security-Policy'] = csp_policy
        return response


class CacheAndTimingMiddleware:
    """Add Cache-Control for homepage and basic Server-Timing metrics."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import time
        start_ts = time.perf_counter()

        response = self.get_response(request)

        total_ms = int((time.perf_counter() - start_ts) * 1000)
        response.headers['Server-Timing'] = f'total;dur={total_ms}'

        if request.path in ('/', ''):
            # cache HTML for a short time to improve TTFB on repeat views
            response.headers.setdefault('Cache-Control', 'public, max-age=60')

        return response
