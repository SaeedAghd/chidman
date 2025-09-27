class SEOMiddleware:
    """Middleware for SEO optimization"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add SEO headers
        if hasattr(response, 'headers'):
            # Security headers
            response.headers.setdefault('X-Content-Type-Options', 'nosniff')
            response.headers.setdefault('X-Frame-Options', 'DENY')
            response.headers.setdefault('X-XSS-Protection', '1; mode=block')
            response.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
            
            # Performance headers
            response.headers.setdefault('Cache-Control', 'public, max-age=3600')
            
            # SEO headers
            response.headers.setdefault('X-Robots-Tag', 'index, follow')
        
        return response
