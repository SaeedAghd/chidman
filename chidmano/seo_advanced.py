"""
سیستم SEO پیشرفته چیدمانو
Advanced SEO System for Chidmano Store Analysis Platform
"""

import json
from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AdvancedSEO:
    """کلاس مدیریت SEO پیشرفته"""
    
    def __init__(self):
        self.base_domain = getattr(settings, 'BASE_DOMAIN', 'chidmano.ir')
        self.site_name = "چیدمانو - تحلیل هوشمند فروشگاه و مغازه"
        self.default_keywords = [
            "تحلیل فروشگاه", "طراحی مغازه", "چیدمان فروشگاه", "بهینه سازی فروشگاه",
            "طراحی داخلی مغازه", "تحلیل هوش مصنوعی فروشگاه", "مشاوره فروشگاه",
            "طراحی ویترین", "چیدمان قفسه", "تحلیل ترافیک مشتری", "بهینه سازی فروش",
            "طراحی تجاری", "مشاوره خرده فروشی", "تحلیل عملکرد فروشگاه", "طراحی مدرن مغازه"
        ]
        
    def generate_meta_tags(self, page_type="home", **kwargs):
        """تولید متاتگ‌های SEO پیشرفته"""
        
        if page_type == "home":
            return self._home_meta_tags()
        elif page_type == "analysis":
            return self._analysis_meta_tags(**kwargs)
        elif page_type == "features":
            return self._features_meta_tags()
        elif page_type == "about":
            return self._about_meta_tags()
        elif page_type == "contact":
            return self._contact_meta_tags()
        else:
            return self._default_meta_tags(**kwargs)
    
    def _home_meta_tags(self):
        """متاتگ‌های صفحه اصلی"""
        return {
            'title': 'چیدمانو - تحلیل هوشمند فروشگاه و مغازه | طراحی و بهینه‌سازی فروشگاه',
            'description': 'چیدمانو اولین پلتفرم تحلیل هوشمند فروشگاه و مغازه در ایران. با استفاده از هوش مصنوعی پیشرفته، فروشگاه شما را تحلیل کرده و راهکارهای افزایش فروش ارائه می‌دهیم.',
            'keywords': ', '.join(self.default_keywords + [
                "پلتفرم تحلیل فروشگاه", "هوش مصنوعی فروشگاه", "نرم افزار تحلیل مغازه",
                "مشاوره رایگان فروشگاه", "تحلیل عملکرد مغازه", "بهینه سازی خرده فروشی"
            ]),
            'canonical': f'https://{self.base_domain}/',
            'og_title': 'چیدمانو - تحلیل هوشمند فروشگاه و مغازه',
            'og_description': 'اولین پلتفرم تحلیل هوشمند فروشگاه در ایران. افزایش فروش با تحلیل علمی و هوش مصنوعی.',
            'og_image': f'https://{self.base_domain}/static/images/seo/og-home.jpg',
            'twitter_card': 'summary_large_image',
            'twitter_title': 'چیدمانو - تحلیل هوشمند فروشگاه',
            'twitter_description': 'افزایش فروش فروشگاه شما با تحلیل هوش مصnوعی پیشرفته',
            'twitter_image': f'https://{self.base_domain}/static/images/seo/twitter-home.jpg'
        }
    
    def _analysis_meta_tags(self, store_name=None, analysis_id=None):
        """متاتگ‌های صفحه تحلیل"""
        title = f'تحلیل فروشگاه {store_name or "شما"} - گزارش جامع چیدمانو'
        description = f'گزارش تحلیل جامع فروشگاه {store_name or "شما"} با استفاده از هوش مصنوعی پیشرفته. شامل نقاط قوت، ضعف و راهکارهای افزایش فروش.'
        
        return {
            'title': title,
            'description': description,
            'keywords': f'تحلیل فروشگاه {store_name}, گزارش فروشگاه, تحلیل مغازه, بهینه سازی فروشگاه {store_name}',
            'canonical': f'https://{self.base_domain}/store/analysis/{analysis_id}/results/' if analysis_id else f'https://{self.base_domain}/store/analysis/',
            'og_title': title,
            'og_description': description,
            'og_image': f'https://{self.base_domain}/static/images/seo/og-analysis.jpg',
            'twitter_card': 'summary_large_image',
            'twitter_title': title,
            'twitter_description': description,
            'twitter_image': f'https://{self.base_domain}/static/images/seo/twitter-analysis.jpg'
        }
    
    def _features_meta_tags(self):
        """متاتگ‌های صفحه ویژگی‌ها"""
        return {
            'title': 'ویژگی‌های چیدمانو - تحلیل هوشمند فروشگاه و مغازه',
            'description': 'آشنایی با ویژگی‌های پیشرفته چیدمانو: تحلیل هوش مصنوعی، گزارش جامع، مشاوره تخصصی و راهکارهای افزایش فروش فروشگاه.',
            'keywords': 'ویژگی های چیدمانو, قابلیت های تحلیل فروشگاه, امکانات نرم افزار مغازه, تحلیل هوش مصنوعی فروشگاه',
            'canonical': f'https://{self.base_domain}/store/features/',
            'og_title': 'ویژگی‌های چیدمانو - تحلیل هوشمند فروشگاه',
            'og_description': 'قابلیت‌های پیشرفته تحلیل فروشگاه با هوش مصنوعی',
            'og_image': f'https://{self.base_domain}/static/images/seo/og-features.jpg'
        }
    
    def _about_meta_tags(self):
        """متاتگ‌های صفحه درباره ما"""
        return {
            'title': 'درباره چیدمانو - تیم متخصص تحلیل فروشگاه و مغازه',
            'description': 'آشنایی با تیم چیدمانو، متخصصان تحلیل فروشگاه و طراحی مغازه. تجربه و تخصص ما در خدمت موفقیت کسب‌وکار شما.',
            'keywords': 'درباره چیدمانو, تیم تحلیل فروشگاه, متخصصان طراحی مغازه, درباره ما',
            'canonical': f'https://{self.base_domain}/about/',
            'og_title': 'درباره چیدمانو - تیم متخصص تحلیل فروشگاه',
            'og_description': 'تیم متخصص تحلیل فروشگاه و طراحی مغازه'
        }
    
    def _contact_meta_tags(self):
        """متاتگ‌های صفحه تماس"""
        return {
            'title': 'تماس با چیدمانو - مشاوره رایگان تحلیل فروشگاه',
            'description': 'تماس با تیم چیدمانو برای مشاوره رایگان تحلیل فروشگاه و مغازه. پاسخگویی سریع و مشاوره تخصصی.',
            'keywords': 'تماس با چیدمانو, مشاوره رایگان فروشگاه, پشتیبانی چیدمانو, تماس',
            'canonical': f'https://{self.base_domain}/contact/',
            'og_title': 'تماس با چیدمانو - مشاوره رایگان',
            'og_description': 'مشاوره رایگان تحلیل فروشگاه و مغازه'
        }
    
    def _default_meta_tags(self, **kwargs):
        """متاتگ‌های پیش‌فرض"""
        return {
            'title': kwargs.get('title', self.site_name),
            'description': kwargs.get('description', 'چیدمانو - تحلیل هوشمند فروشگاه و مغازه'),
            'keywords': kwargs.get('keywords', ', '.join(self.default_keywords)),
            'canonical': kwargs.get('canonical', f'https://{self.base_domain}/'),
            'og_title': kwargs.get('og_title', self.site_name),
            'og_description': kwargs.get('og_description', 'تحلیل هوشمند فروشگاه و مغازه'),
            'og_image': kwargs.get('og_image', f'https://{self.base_domain}/static/images/seo/og-default.jpg')
        }
    
    def generate_structured_data(self, page_type="home", **kwargs):
        """تولید داده‌های ساختاریافته Schema.org"""
        
        if page_type == "home":
            return self._home_structured_data()
        elif page_type == "analysis":
            return self._analysis_structured_data(**kwargs)
        elif page_type == "business":
            return self._business_structured_data()
        else:
            return self._default_structured_data(**kwargs)
    
    def _home_structured_data(self):
        """داده‌های ساختاریافته صفحه اصلی"""
        return {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "چیدمانو",
            "alternateName": "Chidmano",
            "url": f"https://{self.base_domain}",
            "description": "اولین پلتفرم تحلیل هوشمند فروشگاه و مغازه در ایران",
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"https://{self.base_domain}/search?q={{search_term_string}}",
                "query-input": "required name=search_term_string"
            },
            "publisher": {
                "@type": "Organization",
                "name": "چیدمانو",
                "url": f"https://{self.base_domain}",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"https://{self.base_domain}/static/images/logo.png"
                }
            }
        }
    
    def _analysis_structured_data(self, store_name=None, analysis_id=None):
        """داده‌های ساختاریافته صفحه تحلیل"""
        return {
            "@context": "https://schema.org",
            "@type": "AnalysisReport",
            "name": f"گزارش تحلیل فروشگاه {store_name or 'شما'}",
            "description": f"گزارش جامع تحلیل فروشگاه {store_name or 'شما'} با استفاده از هوش مصنوعی",
            "url": f"https://{self.base_domain}/store/analysis/{analysis_id}/results/" if analysis_id else f"https://{self.base_domain}/store/analysis/",
            "datePublished": datetime.now().isoformat(),
            "author": {
                "@type": "Organization",
                "name": "چیدمانو",
                "url": f"https://{self.base_domain}"
            },
            "provider": {
                "@type": "Organization",
                "name": "چیدمانو",
                "url": f"https://{self.base_domain}"
            }
        }
    
    def _business_structured_data(self):
        """داده‌های ساختاریافته کسب‌وکار"""
        return {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "چیدمانو",
            "alternateName": "Chidmano",
            "url": f"https://{self.base_domain}",
            "logo": f"https://{self.base_domain}/static/images/logo.png",
            "description": "اولین پلتفرم تحلیل هوشمند فروشگاه و مغازه در ایران",
            "foundingDate": "2024",
            "address": {
                "@type": "PostalAddress",
                "addressCountry": "IR",
                "addressLocality": "تهران"
            },
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+98-21-12345678",
                "contactType": "customer service",
                "availableLanguage": ["Persian", "English"]
            },
            "sameAs": [
                "https://instagram.com/chidmano",
                "https://linkedin.com/company/chidmano"
            ],
            "service": {
                "@type": "Service",
                "name": "تحلیل هوشمند فروشگاه",
                "description": "تحلیل جامع فروشگاه و مغازه با استفاده از هوش مصنوعی",
                "provider": {
                    "@type": "Organization",
                    "name": "چیدمانو"
                }
            }
        }
    
    def _default_structured_data(self, **kwargs):
        """داده‌های ساختاریافته پیش‌فرض"""
        return {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": kwargs.get('title', self.site_name),
            "description": kwargs.get('description', 'چیدمانو - تحلیل هوشمند فروشگاه و مغازه'),
            "url": kwargs.get('canonical', f'https://{self.base_domain}/'),
            "publisher": {
                "@type": "Organization",
                "name": "چیدمانو",
                "url": f"https://{self.base_domain}"
            }
        }
    
    def generate_breadcrumbs(self, items):
        """تولید breadcrumbs"""
        breadcrumb_data = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": []
        }
        
        for i, item in enumerate(items):
            breadcrumb_data["itemListElement"].append({
                "@type": "ListItem",
                "position": i + 1,
                "name": item['name'],
                "item": item['url']
            })
        
        return breadcrumb_data
    
    def generate_sitemap_data(self):
        """تولید داده‌های sitemap"""
        return {
            'urls': [
                {
                    'loc': f'https://{self.base_domain}/',
                    'lastmod': datetime.now().strftime('%Y-%m-%d'),
                    'changefreq': 'daily',
                    'priority': '1.0'
                },
                {
                    'loc': f'https://{self.base_domain}/store/forms/',
                    'lastmod': datetime.now().strftime('%Y-%m-%d'),
                    'changefreq': 'weekly',
                    'priority': '0.9'
                },
                {
                    'loc': f'https://{self.base_domain}/store/features/',
                    'lastmod': datetime.now().strftime('%Y-%m-%d'),
                    'changefreq': 'monthly',
                    'priority': '0.8'
                },
                {
                    'loc': f'https://{self.base_domain}/about/',
                    'lastmod': datetime.now().strftime('%Y-%m-%d'),
                    'changefreq': 'monthly',
                    'priority': '0.7'
                },
                {
                    'loc': f'https://{self.base_domain}/contact/',
                    'lastmod': datetime.now().strftime('%Y-%m-%d'),
                    'changefreq': 'monthly',
                    'priority': '0.6'
                }
            ]
        }
    
    def render_meta_tags(self, meta_data):
        """رندر متاتگ‌ها به HTML"""
        tags = []
        
        # Title
        tags.append(f'<title>{meta_data["title"]}</title>')
        
        # Meta tags
        tags.append(f'<meta name="description" content="{meta_data["description"]}">')
        tags.append(f'<meta name="keywords" content="{meta_data["keywords"]}">')
        tags.append(f'<meta name="robots" content="index, follow">')
        tags.append(f'<meta name="author" content="چیدمانو">')
        tags.append(f'<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        
        # Canonical
        tags.append(f'<link rel="canonical" href="{meta_data["canonical"]}">')
        
        # Open Graph
        tags.append(f'<meta property="og:title" content="{meta_data["og_title"]}">')
        tags.append(f'<meta property="og:description" content="{meta_data["og_description"]}">')
        tags.append(f'<meta property="og:url" content="{meta_data["canonical"]}">')
        tags.append(f'<meta property="og:type" content="website">')
        tags.append(f'<meta property="og:site_name" content="چیدمانو">')
        tags.append(f'<meta property="og:image" content="{meta_data["og_image"]}">')
        tags.append(f'<meta property="og:locale" content="fa_IR">')
        
        # Twitter Cards
        if 'twitter_card' in meta_data:
            tags.append(f'<meta name="twitter:card" content="{meta_data["twitter_card"]}">')
            tags.append(f'<meta name="twitter:title" content="{meta_data["twitter_title"]}">')
            tags.append(f'<meta name="twitter:description" content="{meta_data["twitter_description"]}">')
            tags.append(f'<meta name="twitter:image" content="{meta_data["twitter_image"]}">')
        
        return mark_safe('\n'.join(tags))
    
    def render_structured_data(self, structured_data):
        """رندر داده‌های ساختاریافته به JSON-LD"""
        return format_html(
            '<script type="application/ld+json">{}</script>',
            json.dumps(structured_data, ensure_ascii=False, indent=2)
        )

# Instance for global use
seo_manager = AdvancedSEO()
