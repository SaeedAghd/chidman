from django import template
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.conf import settings
import json
from datetime import datetime

register = template.Library()

@register.simple_tag
def seo_title(title, site_name="چیدمانو"):
    """Generate SEO optimized title"""
    if not title:
        return site_name
    return f"{title} | {site_name}"

@register.simple_tag
def seo_description(description, max_length=160):
    """Generate SEO optimized description"""
    if not description:
        return "چیدمانو - سیستم تحلیل هوشمند چیدمان فروشگاه با هوش مصنوعی"
    
    if len(description) > max_length:
        return description[:max_length-3] + "..."
    return description

@register.simple_tag
def breadcrumb_schema(items):
    """Generate breadcrumb schema markup"""
    if not items:
        return ""
    
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": []
    }
    
    for i, item in enumerate(items):
        schema["itemListElement"].append({
            "@type": "ListItem",
            "position": i + 1,
            "name": item.get('name', ''),
            "item": item.get('url', '')
        })
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>')

@register.simple_tag
def faq_schema(faqs):
    """Generate FAQ schema markup"""
    if not faqs:
        return ""
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    
    for faq in faqs:
        schema["mainEntity"].append({
            "@type": "Question",
            "name": faq.get('question', ''),
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq.get('answer', '')
            }
        })
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>')

@register.simple_tag
def article_schema(title, description, author, date_published, date_modified=None):
    """Generate article schema markup"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "author": {
            "@type": "Person",
            "name": author
        },
        "publisher": {
            "@type": "Organization",
            "name": "چیدمانو",
            "logo": {
                "@type": "ImageObject",
                "url": "https://chidmano.ir/static/images/logo.png"
            }
        },
        "datePublished": date_published,
        "dateModified": date_modified or date_published
    }
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>')

@register.simple_tag
def local_business_schema(name, description, address, phone, email, url):
    """Generate local business schema markup"""
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": name,
        "description": description,
        "url": url,
        "telephone": phone,
        "email": email,
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "IR",
            "addressRegion": "تهران",
            "addressLocality": "تهران"
        }
    }
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>')

@register.filter
def truncate_words_fa(text, num):
    """Truncate Persian text by word count"""
    if not text:
        return ""
    
    words = text.split()
    if len(words) <= num:
        return text
    
    return " ".join(words[:num]) + "..."

@register.simple_tag
def meta_robots(index=True, follow=True, noarchive=False, nosnippet=False, noimageindex=False):
    """Generate meta robots tag"""
    directives = []
    
    if not index:
        directives.append("noindex")
    else:
        directives.append("index")
    
    if not follow:
        directives.append("nofollow")
    else:
        directives.append("follow")
    
    if noarchive:
        directives.append("noarchive")
    
    if nosnippet:
        directives.append("nosnippet")
    
    if noimageindex:
        directives.append("noimageindex")
    
    return format_html('<meta name="robots" content="{}">', ", ".join(directives))

# Advanced SEO Tags
@register.simple_tag
def advanced_seo_meta(page_type="home", **kwargs):
    """تولید متاتگ‌های SEO پیشرفته"""
    try:
        from ..seo_advanced import seo_manager
        meta_data = seo_manager.generate_meta_tags(page_type, **kwargs)
        return seo_manager.render_meta_tags(meta_data)
    except ImportError:
        return ""

@register.simple_tag
def advanced_seo_structured_data(page_type="home", **kwargs):
    """تولید داده‌های ساختاریافته پیشرفته"""
    try:
        from ..seo_advanced import seo_manager
        structured_data = seo_manager.generate_structured_data(page_type, **kwargs)
        return seo_manager.render_structured_data(structured_data)
    except ImportError:
        return ""

@register.simple_tag
def seo_analytics_gtag():
    """تولید Google Analytics"""
    gtag_id = getattr(settings, 'GOOGLE_ANALYTICS_ID', None)
    if gtag_id:
        return format_html("""
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', '{}');
        </script>
        """, gtag_id, gtag_id)
    return ""

@register.simple_tag
def seo_google_search_console():
    """تولید Google Search Console verification"""
    gsc_verification = getattr(settings, 'GOOGLE_SEARCH_CONSOLE_VERIFICATION', None)
    if gsc_verification:
        return format_html('<meta name="google-site-verification" content="{}">', gsc_verification)
    return ""

@register.simple_tag
def seo_facebook_pixel():
    """تولید Facebook Pixel"""
    fb_pixel_id = getattr(settings, 'FACEBOOK_PIXEL_ID', None)
    if fb_pixel_id:
        return format_html("""
        <!-- Facebook Pixel Code -->
        <script>
        !function(f,b,e,v,n,t,s)
        {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', '{}');
        fbq('track', 'PageView');
        </script>
        <noscript><img height="1" width="1" style="display:none"
        src="https://www.facebook.com/tr?id={}&ev=PageView&noscript=1"
        /></noscript>
        """, fb_pixel_id, fb_pixel_id)
    return ""

@register.simple_tag
def seo_performance_monitoring():
    """تولید کدهای مانیتورینگ عملکرد"""
    return mark_safe("""
    <!-- Performance Monitoring -->
    <script>
    // Core Web Vitals monitoring
    function sendToAnalytics(metric) {
        if (typeof gtag !== 'undefined') {
            gtag('event', metric.name, {
                event_category: 'Web Vitals',
                event_label: metric.id,
                value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
                non_interaction: true,
            });
        }
    }
    
    // LCP
    new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
            sendToAnalytics({name: 'LCP', value: entry.startTime, id: entry.id});
        }
    }).observe({entryTypes: ['largest-contentful-paint']});
    
    // FID
    new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
            sendToAnalytics({name: 'FID', value: entry.processingStart - entry.startTime, id: entry.id});
        }
    }).observe({entryTypes: ['first-input']});
    
    // CLS
    let clsValue = 0;
    new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
            if (!entry.hadRecentInput) {
                clsValue += entry.value;
                sendToAnalytics({name: 'CLS', value: clsValue, id: entry.id});
            }
        }
    }).observe({entryTypes: ['layout-shift']});
    </script>
    """)

@register.simple_tag
def seo_robots_txt():
    """تولید robots.txt"""
    base_domain = getattr(settings, 'BASE_DOMAIN', 'chidmano.ir')
    robots_content = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /static/admin/
Disallow: /media/

Sitemap: https://{base_domain}/sitemap.xml
Sitemap: https://{base_domain}/sitemap-images.xml
"""
    return robots_content

@register.simple_tag
def seo_sitemap_urls():
    """تولید لیست URL های sitemap"""
    try:
        from ..seo_advanced import seo_manager
        sitemap_data = seo_manager.generate_sitemap_data()
        return sitemap_data['urls']
    except ImportError:
        return []

@register.simple_tag
def seo_canonical_url(request):
    """تولید canonical URL از request"""
    if request:
        return request.build_absolute_uri(request.path)
    return ""

@register.simple_tag
def seo_og_image(image_url=None, default_image="og-default.jpg"):
    """تولید Open Graph image"""
    if image_url:
        return image_url
    base_domain = getattr(settings, 'BASE_DOMAIN', 'chidmano.ir')
    return f"https://{base_domain}/static/images/seo/{default_image}"

@register.simple_tag
def seo_twitter_image(image_url=None, default_image="twitter-default.jpg"):
    """تولید Twitter image"""
    if image_url:
        return image_url
    base_domain = getattr(settings, 'BASE_DOMAIN', 'chidmano.ir')
    return f"https://{base_domain}/static/images/seo/{default_image}"

@register.simple_tag
def seo_keywords_list(*keywords):
    """تولید لیست کلمات کلیدی"""
    base_keywords = [
        "تحلیل فروشگاه", "طراحی مغازه", "چیدمان فروشگاه", "بهینه سازی فروشگاه",
        "طراحی داخلی مغازه", "تحلیل هوش مصنوعی فروشگاه", "مشاوره فروشگاه",
        "طراحی ویترین", "چیدمان قفسه", "تحلیل ترافیک مشتری", "بهینه سازی فروش"
    ]
    all_keywords = list(keywords) + base_keywords
    return ", ".join(set(all_keywords))

@register.simple_tag
def seo_json_ld(data):
    """تولید JSON-LD از داده"""
    return mark_safe(f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, indent=2)}</script>')

@register.simple_tag
def seo_article_schema(title, description, author="چیدمانو", date_published=None, date_modified=None):
    """تولید schema برای مقاله"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "author": {
            "@type": "Organization",
            "name": author,
            "url": f"https://{getattr(settings, 'BASE_DOMAIN', 'chidmano.ir')}"
        },
        "publisher": {
            "@type": "Organization",
            "name": "چیدمانو",
            "logo": {
                "@type": "ImageObject",
                "url": f"https://{getattr(settings, 'BASE_DOMAIN', 'chidmano.ir')}/static/images/logo.png"
            }
        },
        "datePublished": date_published or datetime.now().isoformat(),
        "dateModified": date_modified or date_published or datetime.now().isoformat()
    }
    return seo_json_ld(schema)

@register.simple_tag
def seo_website_schema():
    """تولید schema برای وب‌سایت"""
    base_domain = getattr(settings, 'BASE_DOMAIN', 'chidmano.ir')
    schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "چیدمانو",
        "alternateName": "Chidmano",
        "url": f"https://{base_domain}",
        "description": "اولین پلتفرم تحلیل هوشمند فروشگاه و مغازه در ایران",
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"https://{base_domain}/search?q={{search_term_string}}",
            "query-input": "required name=search_term_string"
        },
        "publisher": {
            "@type": "Organization",
            "name": "چیدمانو",
            "url": f"https://{base_domain}",
            "logo": {
                "@type": "ImageObject",
                "url": f"https://{base_domain}/static/images/logo.png"
            }
        }
    }
    return seo_json_ld(schema)
