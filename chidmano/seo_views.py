"""
SEO Views for sitemap and robots.txt
"""

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import datetime


@cache_page(60 * 60 * 24)  # Cache for 24 hours
@require_http_methods(["GET"])
def sitemap_xml(request):
    """Generate sitemap.xml"""
    
    # Static pages
    static_pages = [
        {
            'url': reverse('home'),
            'lastmod': '2025-01-20',
            'changefreq': 'weekly',
            'priority': '1.0'
        },
        {
            'url': reverse('store_analysis:index'),
            'lastmod': '2025-01-20',
            'changefreq': 'weekly',
            'priority': '1.0'
        },
        {
            'url': reverse('store_analysis:forms'),
            'lastmod': '2025-01-20',
            'changefreq': 'monthly',
            'priority': '0.8'
        },
        {
            'url': reverse('store_analysis:features'),
            'lastmod': '2025-01-20',
            'changefreq': 'monthly',
            'priority': '0.7'
        },
        {
            'url': reverse('store_analysis:education_library'),
            'lastmod': '2025-01-20',
            'changefreq': 'monthly',
            'priority': '0.7'
        },
        {
            'url': reverse('store_analysis:support_center'),
            'lastmod': '2025-01-20',
            'changefreq': 'monthly',
            'priority': '0.6'
        },
    ]
    
    # Build full URLs
    base_url = getattr(settings, 'SITE_URL', 'https://chidmano.ir')
    for page in static_pages:
        page['url'] = f"{base_url}{page['url']}"
    
    context = {
        'pages': static_pages,
        'lastmod': datetime.now().strftime('%Y-%m-%d')
    }
    
    sitemap_content = render_to_string('sitemap.xml', context)
    
    response = HttpResponse(sitemap_content, content_type='application/xml')
    response['Cache-Control'] = 'public, max-age=86400'  # 24 hours
    return response


@cache_page(60 * 60 * 24)  # Cache for 24 hours
@require_http_methods(["GET"])
def robots_txt(request):
    """Generate robots.txt"""
    
    robots_content = render_to_string('robots.txt')
    
    response = HttpResponse(robots_content, content_type='text/plain')
    response['Cache-Control'] = 'public, max-age=86400'  # 24 hours
    return response
