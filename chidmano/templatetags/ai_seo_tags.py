#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Template Tags برای بهینه‌سازی سئو AI
AI SEO Template Tags
"""

from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.simple_tag
def ai_friendly_summary(content, max_length=300):
    """تولید خلاصه AI-friendly از محتوا"""
    import re
    
    # حذف HTML tags
    clean_content = re.sub(r'<[^>]+>', '', content)
    clean_content = re.sub(r'\s+', ' ', clean_content).strip()
    
    # محدود کردن طول
    if len(clean_content) > max_length:
        clean_content = clean_content[:max_length] + '...'
    
    return clean_content


@register.simple_tag
def ai_structured_data(page_type='home', **kwargs):
    """تولید Structured Data بهینه برای AI"""
    from chidmano.ai_seo_optimizer import AISEOOptimizer
    
    # ساختار پایه
    structured_data = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": kwargs.get('title', 'چیدمانو'),
        "description": kwargs.get('description', ''),
        "url": kwargs.get('url', 'https://chidmano.ir/'),
    }
    
    # بهبود برای AI
    enhanced = AISEOOptimizer.enhance_structured_data_for_ai(structured_data)
    
    # تبدیل به JSON
    json_data = json.dumps(enhanced, ensure_ascii=False, indent=2)
    
    return mark_safe(f'<script type="application/ld+json">{json_data}</script>')


@register.simple_tag(takes_context=True)
def ai_meta_tags(context):
    """تولید Meta Tags بهینه برای AI"""
    request = context.get('request')
    
    # بررسی اینکه آیا AI bot است
    is_ai_bot = False
    if request and hasattr(request, 'is_ai_bot'):
        is_ai_bot = request.is_ai_bot
    
    meta_tags = []
    
    # Meta tags برای AI
    if is_ai_bot or context.get('page_type') in ['home', 'features', 'products']:
        title = context.get('page_title', 'چیدمانو - تحلیل هوشمند فروشگاه')
        description = context.get('page_description', '')
        
        meta_tags.append(f'<meta name="ai-friendly" content="true">')
        meta_tags.append(f'<meta name="ai-summary" content="{description[:200]}">')
    
    return mark_safe('\n'.join(meta_tags))


@register.simple_tag
def ai_readable_content(content):
    """تبدیل محتوا به فرمت قابل خواندن برای AI"""
    import re
    
    # حذف HTML tags
    text = re.sub(r'<[^>]+>', '', content)
    
    # حذف whitespace اضافی
    text = re.sub(r'\s+', ' ', text).strip()
    
    # تقسیم به پاراگراف‌ها
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    
    return '\n\n'.join(paragraphs)


@register.filter
def ai_format(content):
    """فرمت کردن محتوا برای AI"""
    import re
    
    # حذف HTML
    text = re.sub(r'<[^>]+>', '', str(content))
    
    # حذف whitespace اضافی
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

