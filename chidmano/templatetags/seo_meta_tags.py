"""
SEO Meta Tags Generator
تولید meta tags برای بهبود SEO
"""

from django.conf import settings
from django.utils.safestring import mark_safe
from django.template import Library

register = Library()

@register.simple_tag
def seo_meta_tags(page_type='home', title='', description='', keywords='', image=''):
    """تولید meta tags برای SEO"""
    
    # تنظیمات پیش‌فرض
    default_title = "چیدمانو - تحلیل هوشمند فروشگاه با هوش مصنوعی"
    default_description = "تحلیل پیشرفته فروشگاه با هوش مصنوعی. بهبود چیدمان، روشنایی و تجربه مشتری برای افزایش فروش."
    default_keywords = "تحلیل فروشگاه، چیدمان فروشگاه، هوش مصنوعی، تحلیل فروش، بهینه‌سازی فروشگاه"
    default_image = "https://chidmano.ir/static/images/logo.png"
    
    # تنظیمات بر اساس نوع صفحه
    if page_type == 'home':
        title = title or default_title
        description = description or default_description
        keywords = keywords or default_keywords
        image = image or default_image
    elif page_type == 'store':
        title = title or "تحلیل فروشگاه - چیدمانو"
        description = description or "تحلیل هوشمند فروشگاه شما با تکنولوژی هوش مصنوعی پیشرفته"
        keywords = keywords or "تحلیل فروشگاه، چیدمان، روشنایی، تجربه مشتری"
    elif page_type == 'guide':
        title = title or "راهنمای چیدمان فروشگاه - چیدمانو"
        description = description or "راهنمای کامل چیدمان فروشگاه برای افزایش فروش و بهبود تجربه مشتری"
        keywords = keywords or "راهنمای چیدمان، فروشگاه، افزایش فروش"
    
    meta_tags = f"""
    <!-- Primary Meta Tags -->
    <title>{title}</title>
    <meta name="title" content="{title}">
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="چیدمانو">
    <meta name="robots" content="index, follow">
    <meta name="language" content="Persian">
    <meta name="revisit-after" content="1 days">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://chidmano.ir/">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{image}">
    <meta property="og:site_name" content="چیدمانو">
    <meta property="og:locale" content="fa_IR">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://chidmano.ir/">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{description}">
    <meta property="twitter:image" content="{image}">
    
    <!-- Additional SEO Tags -->
    <meta name="theme-color" content="#3b82f6">
    <meta name="msapplication-TileColor" content="#3b82f6">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="چیدمانو">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://chidmano.ir/">
    
    <!-- Alternate Languages -->
    <link rel="alternate" hreflang="fa" href="https://chidmano.ir/">
    <link rel="alternate" hreflang="x-default" href="https://chidmano.ir/">
    
    <!-- Preconnect to external domains -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <!-- DNS Prefetch -->
    <link rel="dns-prefetch" href="//www.google-analytics.com">
    <link rel="dns-prefetch" href="//www.googletagmanager.com">
    """
    
    return mark_safe(meta_tags)

@register.simple_tag
def seo_structured_data():
    """تولید structured data برای SEO"""
    
    structured_data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "چیدمانو",
        "alternateName": "Chidmano",
        "url": "https://chidmano.ir",
        "description": "تحلیل پیشرفته فروشگاه با هوش مصنوعی. بهبود چیدمان، روشنایی و تجربه مشتری برای افزایش فروش.",
        "inLanguage": "fa-IR",
        "copyrightYear": "2025",
        "creator": {
            "@type": "Organization",
            "name": "چیدمانو",
            "url": "https://chidmano.ir"
        },
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://chidmano.ir/search?q={search_term_string}",
            "query-input": "required name=search_term_string"
        }
    }
    
    return mark_safe(f'<script type="application/ld+json">{structured_data}</script>')

@register.simple_tag
def seo_analytics():
    """تولید کدهای analytics برای SEO"""
    
    analytics_code = """
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'GA_MEASUREMENT_ID');
    </script>
    
    <!-- Google Search Console -->
    <meta name="google-site-verification" content="YOUR_VERIFICATION_CODE">
    
    <!-- Bing Webmaster Tools -->
    <meta name="msvalidate.01" content="YOUR_BING_VERIFICATION_CODE">
    
    <!-- Yandex Webmaster -->
    <meta name="yandex-verification" content="YOUR_YANDEX_VERIFICATION_CODE">
    """
    
    return mark_safe(analytics_code)

@register.simple_tag
def seo_performance_hints():
    """تولید performance hints برای SEO"""
    
    performance_hints = """
    <!-- Performance Hints -->
    <link rel="preload" href="/static/css/main.css" as="style">
    <link rel="preload" href="/static/js/main.js" as="script">
    <link rel="preload" href="/static/fonts/Vazir.ttf" as="font" type="font/ttf" crossorigin>
    
    <!-- Critical CSS -->
    <style>
        /* Critical CSS for above-the-fold content */
        body { margin: 0; font-family: 'Vazir', sans-serif; }
        .header { background: #3b82f6; color: white; padding: 1rem; }
        .hero { text-align: center; padding: 2rem; }
    </style>
    
    <!-- Resource Hints -->
    <link rel="prefetch" href="/static/images/hero-image.jpg">
    <link rel="prefetch" href="/static/js/forms-simple.js">
    """
    
    return mark_safe(performance_hints)
