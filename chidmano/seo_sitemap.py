"""
Sitemap Generator پیشرفته برای SEO
Advanced Sitemap Generator for SEO
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from store_analysis.models import StoreAnalysis
import logging

logger = logging.getLogger(__name__)

class HomeSitemap(Sitemap):
    """Sitemap برای صفحه اصلی"""
    changefreq = 'daily'
    priority = 1.0
    protocol = 'https'
    
    def items(self):
        return ['chidmano:home', 'chidmano:about', 'chidmano:store_layout_guide']
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        return timezone.now()

class AboutSitemap(Sitemap):
    """Sitemap برای صفحه درباره"""
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'
    
    def items(self):
        return ['chidmano:about']
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        return timezone.now()

class GuideSitemap(Sitemap):
    """Sitemap برای راهنماها"""
    changefreq = 'weekly'
    priority = 0.9
    protocol = 'https'
    
    def items(self):
        return ['chidmano:store_layout_guide']
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        return timezone.now()

class FeaturesSitemap(Sitemap):
    """Sitemap برای صفحه ویژگی‌ها"""
    changefreq = 'weekly'
    priority = 0.9
    protocol = 'https'
    
    def items(self):
        return ['store_analysis:features']
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        return timezone.now()

class FormsSitemap(Sitemap):
    """Sitemap برای صفحه فرم‌ها"""
    changefreq = 'weekly'
    priority = 0.9
    protocol = 'https'
    
    def items(self):
        return ['store_analysis:forms']
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        return timezone.now()

class AboutSitemap(Sitemap):
    """Sitemap برای صفحه درباره ما"""
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'
    
    def items(self):
        return ['chidmano:about']
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        return timezone.now()

class ContactSitemap(Sitemap):
    """Sitemap برای صفحه تماس"""
    changefreq = 'monthly'
    priority = 0.6
    protocol = 'https'
    
    def items(self):
        return ['chidmano:contact']
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        return timezone.now()

class AnalysisResultsSitemap(Sitemap):
    """Sitemap برای نتایج تحلیل (فقط تحلیل‌های عمومی)"""
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'
    
    def items(self):
        # فقط تحلیل‌های تکمیل شده و عمومی
        return StoreAnalysis.objects.filter(
            status='completed',
            is_public=True
        ).order_by('-created_at')[:100]  # محدود به 100 مورد اخیر
    
    def location(self, obj):
        return f'/store/analysis/{obj.pk}/results/'
    
    def lastmod(self, obj):
        return obj.updated_at or obj.created_at
    
    def priority(self, obj):
        # اولویت بر اساس تاریخ ایجاد
        days_old = (timezone.now() - obj.created_at).days
        if days_old < 7:
            return 0.9
        elif days_old < 30:
            return 0.8
        elif days_old < 90:
            return 0.7
        else:
            return 0.6

class BlogSitemap(Sitemap):
    """Sitemap برای مقالات وبلاگ (اگر وجود داشته باشد)"""
    changefreq = 'weekly'
    priority = 0.7
    protocol = 'https'
    
    def items(self):
        # در آینده می‌توان مقالات وبلاگ را اضافه کرد
        return []
    
    def location(self, obj):
        return f'/blog/{obj.slug}/'
    
    def lastmod(self, obj):
        return obj.updated_at or obj.created_at

class ImageSitemap(Sitemap):
    """Sitemap برای تصاویر"""
    changefreq = 'monthly'
    priority = 0.5
    protocol = 'https'
    
    def items(self):
        # تصاویر مهم سایت
        return [
            {
                'url': '/static/images/logo.png',
                'title': 'لوگوی چیدمانو',
                'caption': 'لوگوی اصلی پلتفرم تحلیل هوشمند فروشگاه چیدمانو'
            },
            {
                'url': '/static/images/seo/og-home.jpg',
                'title': 'چیدمانو - تحلیل هوشمند فروشگاه',
                'caption': 'تصویر معرفی چیدمانو برای شبکه‌های اجتماعی'
            },
            {
                'url': '/static/images/seo/og-analysis.jpg',
                'title': 'گزارش تحلیل فروشگاه',
                'caption': 'نمونه گزارش تحلیل فروشگاه با چیدمانو'
            }
        ]
    
    def location(self, obj):
        return obj['url']
    
    def lastmod(self, obj):
        return timezone.now()

class AdvancedSitemapGenerator:
    """تولیدکننده پیشرفته sitemap"""
    
    def __init__(self):
        self.sitemaps = {
            'home': HomeSitemap(),
            'features': FeaturesSitemap(),
            'forms': FormsSitemap(),
            'about': AboutSitemap(),
            'contact': ContactSitemap(),
            'analysis': AnalysisResultsSitemap(),
            'blog': BlogSitemap(),
            'images': ImageSitemap(),
        }
    
    def generate_sitemap_index(self):
        """تولید فهرست sitemap"""
        sitemap_index = {
            'sitemaps': []
        }
        
        for name, sitemap in self.sitemaps.items():
            sitemap_index['sitemaps'].append({
                'loc': f'https://chidmano.ir/sitemap-{name}.xml',
                'lastmod': timezone.now().strftime('%Y-%m-%d')
            })
        
        return sitemap_index
    
    def get_sitemap_urls(self):
        """دریافت تمام URL های sitemap"""
        all_urls = []
        
        for name, sitemap in self.sitemaps.items():
            try:
                items = sitemap.items()
                for item in items:
                    url_data = {
                        'loc': f"https://chidmano.ir{sitemap.location(item)}",
                        'lastmod': sitemap.lastmod(item).strftime('%Y-%m-%d'),
                        'changefreq': sitemap.changefreq,
                        'priority': sitemap.priority
                    }
                    all_urls.append(url_data)
            except Exception as e:
                logger.error(f"Error generating sitemap for {name}: {e}")
                continue
        
        return all_urls
    
    def generate_robots_txt(self):
        """تولید robots.txt"""
        robots_content = """User-agent: *
Allow: /

# Sitemaps
Sitemap: https://chidmano.ir/sitemap.xml
Sitemap: https://chidmano.ir/sitemap-images.xml

# Crawl-delay for respectful crawling
Crawl-delay: 1

# Disallow admin areas
Disallow: /admin/
Disallow: /api/
Disallow: /static/admin/
Disallow: /media/
Disallow: /accounts/
Disallow: /store/dashboard/
Disallow: /store/analysis/*/results/

# Allow important pages
Allow: /store/
Allow: /guide/
Allow: /case-studies/
Allow: /partnership/
Allow: /about/
Allow: /contact/
Allow: /privacy-policy/
Allow: /terms-of-service/

# Allow static files
Allow: /static/
Allow: /*.css
Allow: /*.js
Allow: /*.png
Allow: /*.jpg
Allow: /*.jpeg
Allow: /*.gif
Allow: /*.svg
Allow: /*.ico
Allow: /*.woff
Allow: /*.woff2
Allow: /*.ttf
Allow: /*.eot

# Specific bot instructions
User-agent: Googlebot
Allow: /
Crawl-delay: 1

User-agent: Bingbot
Allow: /
Crawl-delay: 1

User-agent: Slurp
Allow: /
Crawl-delay: 2

User-agent: DuckDuckBot
Allow: /
Crawl-delay: 1

User-agent: Baiduspider
Allow: /
Crawl-delay: 2

User-agent: YandexBot
Allow: /
Crawl-delay: 2

# Block bad bots
User-agent: AhrefsBot
Disallow: /

User-agent: MJ12bot
Disallow: /

User-agent: DotBot
Disallow: /

User-agent: SemrushBot
Disallow: /

User-agent: AhrefsSiteAudit
Disallow: /

User-agent: BLEXBot
Disallow: /
"""
        return robots_content

# Instance for global use
sitemap_generator = AdvancedSitemapGenerator()
