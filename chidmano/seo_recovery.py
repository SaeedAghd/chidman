#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
سیستم احیای کامل سئو بعد از downtime
Complete SEO Recovery System after Downtime
"""

from django.utils import timezone
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from datetime import datetime, date, timedelta
from store_analysis.models import StoreAnalysis, ServicePackage
import logging

logger = logging.getLogger(__name__)

class EnhancedHomeSitemap(Sitemap):
    """Sitemap پیشرفته برای صفحه اصلی"""
    changefreq = 'daily'
    priority = 1.0
    protocol = 'https'
    i18n = True
    
    def items(self):
        # لیست URL های صفحه اصلی
        try:
            return [
                reverse('home'),
                reverse('landing'),
            ]
        except Exception as e:
            logger.error(f"Error in EnhancedHomeSitemap.items: {e}")
            return ['/']
    
    def location(self, item):
        return item
    
    def lastmod(self, item):
        # به‌روزرسانی امروز (بعد از 10 روز downtime)
        return timezone.now().date()


class EnhancedPagesSitemap(Sitemap):
    """Sitemap برای صفحات استاتیک مهم"""
    changefreq = 'weekly'
    priority = 0.9
    protocol = 'https'
    
    def items(self):
        # لیست URL های صفحات استاتیک
        pages = []
        try:
            pages.append(('features', reverse('store_analysis:features')))
            pages.append(('products', reverse('store_analysis:products')))
            pages.append(('forms', reverse('store_analysis:forms')))
            pages.append(('about', reverse('about')))
            pages.append(('store_layout_guide', reverse('store_layout_guide')))
        except Exception as e:
            logger.error(f"Error in EnhancedPagesSitemap.items: {e}")
        
        return pages
    
    def location(self, item):
        return item[1]  # URL
    
    def lastmod(self, item):
        # به‌روزرسانی امروز برای signal freshness
        return timezone.now().date()
    
    def priority(self, item):
        # اولویت بالاتر برای صفحات مهم
        name = item[0]  # نام صفحه
        if name in ['features', 'products', 'forms']:
            return 0.9
        return 0.8


class GuidePagesSitemap(Sitemap):
    """Sitemap برای صفحات راهنما"""
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'
    
    def items(self):
        guides = [
            'store-layout',
            'supermarket-layout',
            'storefront-lighting',
            'store-layout-pillar',
            'color-psychology',
            'customer-journey',
            'lighting-design',
        ]
        return [{'slug': guide, 'url': f'/guide/{guide}/'} for guide in guides]
    
    def location(self, item):
        return item['url']
    
    def lastmod(self, item):
        # به‌روزرسانی امروز
        return timezone.now().date()


class ServicePackageSitemap(Sitemap):
    """Sitemap برای پکیج‌های خدمات"""
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'
    
    def items(self):
        try:
            return ServicePackage.objects.filter(is_active=True).order_by('price')
        except Exception as e:
            logger.error(f"Error fetching service packages: {e}")
            return []
    
    def location(self, obj):
        return f'/store/products/?package={obj.package_type}'
    
    def lastmod(self, obj):
        return obj.updated_at.date() if obj.updated_at else timezone.now().date()


class PublicAnalysesSitemap(Sitemap):
    """Sitemap برای تحلیل‌های عمومی (اگر is_public داشته باشند)"""
    changefreq = 'weekly'
    priority = 0.7
    protocol = 'https'
    limit = 500  # محدود به 500 مورد
    
    def items(self):
        try:
            # فقط تحلیل‌های تکمیل شده
            analyses = StoreAnalysis.objects.filter(
                status='completed'
            ).order_by('-updated_at', '-created_at')[:500]
            return analyses
        except Exception as e:
            logger.error(f"Error fetching analyses: {e}")
            return []
    
    def location(self, obj):
        return f'/store/analysis/{obj.id}/results/'
    
    def lastmod(self, obj):
        return (obj.updated_at or obj.created_at).date()
    
    def priority(self, obj):
        # اولویت بر اساس تازگی
        days_old = (timezone.now().date() - obj.created_at.date()).days
        
        if days_old < 7:
            return 0.9
        elif days_old < 30:
            return 0.8
        elif days_old < 90:
            return 0.7
        else:
            return 0.6


class ImageSitemap(Sitemap):
    """Sitemap برای تصاویر مهم سایت"""
    changefreq = 'monthly'
    priority = 0.6
    protocol = 'https'
    
    def items(self):
        return [
            {
                'url': '/static/images/logo.png',
                'title': 'لوگوی چیدمانو',
                'caption': 'لوگوی اصلی پلتفرم تحلیل هوشمند فروشگاه چیدمانو',
                'geo_location': 'Iran',
            },
            {
                'url': '/static/images/slider/background.jpg',
                'title': 'تحلیل هوشمند فروشگاه',
                'caption': 'نمونه تصویر تحلیل هوشمند چیدمان فروشگاه',
                'geo_location': 'Iran',
            },
        ]
    
    def location(self, obj):
        return obj['url']
    
    def lastmod(self, obj):
        return timezone.now().date()


class SEORecoveryManager:
    """مدیر احیای سئو"""
    
    def __init__(self):
        self.recovery_date = timezone.now().date()
        self.downtime_days = 10
        self.sitemaps = {
            'home': EnhancedHomeSitemap,
            'pages': EnhancedPagesSitemap,
            'guides': GuidePagesSitemap,
            'services': ServicePackageSitemap,
            'analyses': PublicAnalysesSitemap,
            'images': ImageSitemap,
        }
    
    def generate_robots_txt(self, allow_ai_bots=True):
        """تولید robots.txt بهینه برای احیای سئو با پشتیبانی از AI bots"""
        today = timezone.now().strftime('%Y-%m-%d')
        
        robots = f"""# robots.txt برای چیدمانو
# به‌روزرسانی شده در: {today}
# سایت پس از {self.downtime_days} روز downtime دوباره فعال شده است

User-agent: *
Allow: /
Crawl-delay: 1

# ===== Sitemaps =====
Sitemap: https://chidmano.ir/sitemap.xml
Sitemap: https://chidmano.ir/sitemap-images.xml

# ===== صفحات خصوصی - مسدود =====
Disallow: /admin/
Disallow: /api/
Disallow: /accounts/password_reset/
Disallow: /accounts/password_change/
Disallow: /store/dashboard/
Disallow: /store/analysis/*/download/
Disallow: /store/analysis/*/view-report/

# ===== صفحات عمومی - مجاز =====
Allow: /
Allow: /store/
Allow: /store/products/
Allow: /store/features/
Allow: /guide/
Allow: /about/
Allow: /landing/
Allow: /*.html$

# ===== فایل‌های استاتیک - مجاز =====
Allow: /static/
Allow: /media/public/
Allow: /*.css$
Allow: /*.js$
Allow: /*.png$
Allow: /*.jpg$
Allow: /*.jpeg$
Allow: /*.gif$
Allow: /*.svg$
Allow: /*.ico$
Allow: /*.webp$
Allow: /*.woff$
Allow: /*.woff2$
Allow: /*.ttf$

# ===== تنظیمات ویژه برای موتورهای جستجو =====

# Googlebot - اولویت بالا برای احیای سریع
User-agent: Googlebot
Allow: /
Crawl-delay: 0.5

User-agent: Googlebot-Image
Allow: /static/images/
Allow: /media/public/
Crawl-delay: 1

User-agent: Googlebot-Mobile
Allow: /
Crawl-delay: 0.5

# Bingbot
User-agent: Bingbot
Allow: /
Crawl-delay: 1

# Yandex
User-agent: Yandex
Allow: /
Crawl-delay: 1

# Baidu
User-agent: Baiduspider
Allow: /
Crawl-delay: 2

# DuckDuckGo
User-agent: DuckDuckBot
Allow: /
Crawl-delay: 1

# ===== مسدود کردن Bot های مخرب =====
User-agent: AhrefsBot
Disallow: /

User-agent: SemrushBot
Disallow: /

User-agent: MJ12bot
Disallow: /

User-agent: DotBot
Disallow: /

User-agent: BLEXBot
Disallow: /

# ===== AI Bots - مجاز برای SEO AI =====
# این bots اجازه دارند سایت را crawl کنند تا در ChatGPT, Perplexity, Claude و سایر AI systems نمایش داده شوند
# این کار باعث می‌شود سایت شما در AI responses بهتر و دقیق‌تر نمایش داده شود

# OpenAI / ChatGPT
User-agent: GPTBot
Allow: /
Crawl-delay: 1

User-agent: ChatGPT-User
Allow: /
Crawl-delay: 1

User-agent: ChatGPTBot
Allow: /
Crawl-delay: 1

# Google AI
User-agent: Google-Extended
Allow: /
Crawl-delay: 1

# Anthropic / Claude
User-agent: anthropic-ai
Allow: /
Crawl-delay: 1

User-agent: ClaudeBot
Allow: /
Crawl-delay: 1

# Perplexity
User-agent: PerplexityBot
Allow: /
Crawl-delay: 1

User-agent: Perplexity-AI
Allow: /
Crawl-delay: 1

# Microsoft AI
User-agent: BingPreview
Allow: /
Crawl-delay: 1

# Common Crawl (برای AI training)
User-agent: CCBot
Allow: /
Crawl-delay: 2

# Apple AI
User-agent: Applebot-Extended
Allow: /
Crawl-delay: 1

# ===== مسدود کردن Bot های مخرب =====

# ===== Social Media Bots - مجاز =====
User-agent: facebookexternalhit
Allow: /
Crawl-delay: 1

User-agent: Twitterbot
Allow: /
Crawl-delay: 1

User-agent: LinkedInBot
Allow: /
Crawl-delay: 1

User-agent: WhatsApp
Allow: /
Crawl-delay: 1

User-agent: TelegramBot
Allow: /
Crawl-delay: 1
"""
        return robots
    
    def get_recovery_stats(self):
        """آمار احیای سئو"""
        try:
            total_analyses = StoreAnalysis.objects.filter(status='completed').count()
            recent_analyses = StoreAnalysis.objects.filter(
                status='completed',
                updated_at__gte=timezone.now() - timedelta(days=30)
            ).count()
            
            total_packages = ServicePackage.objects.filter(is_active=True).count()
            
            return {
                'recovery_date': self.recovery_date.isoformat(),
                'downtime_days': self.downtime_days,
                'total_pages_in_sitemap': self._estimate_sitemap_size(),
                'total_analyses': total_analyses,
                'recent_analyses': recent_analyses,
                'active_packages': total_packages,
                'lastmod_date': self.recovery_date.isoformat(),
            }
        except Exception as e:
            logger.error(f"Error getting recovery stats: {e}")
            return {}
    
    def _estimate_sitemap_size(self):
        """تخمین تعداد صفحات در sitemap"""
        try:
            size = 0
            size += 2  # Home pages
            size += 5  # Static pages
            size += 7  # Guide pages
            size += ServicePackage.objects.filter(is_active=True).count()
            size += min(500, StoreAnalysis.objects.filter(status='completed').count())
            size += 2  # Images
            return size
        except:
            return 100  # تخمین پایه


# Instance global
seo_recovery_manager = SEORecoveryManager()

