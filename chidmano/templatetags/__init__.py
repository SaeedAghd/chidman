from django import template
from django.utils.safestring import mark_safe
from django.utils.html import format_html
import json

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
