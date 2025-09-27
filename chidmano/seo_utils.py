"""
ابزارهای SEO خاکستری محدود و کنترل‌شده
"""
import random
import re
from django.utils import timezone
from django.db.models import Q
from .models import BlogPost, SEOKeyword, InternalLink, SEOMetrics

class ContentGenerator:
    """تولیدکننده محتوای خودکار"""
    
    def __init__(self):
        self.keywords = [
            "چیدمان فروشگاه", "طراحی فروشگاه", "بهینه‌سازی فروشگاه",
            "نورپردازی فروشگاه", "مسیر مشتری", "روانشناسی رنگ",
            "فروشگاه مدرن", "چیدمان سوپرمارکت", "ویترین فروشگاه",
            "تحلیل فروشگاه", "هوش مصنوعی فروشگاه", "نرم‌افزار فروشگاه"
        ]
        
        self.templates = {
            "tips": [
                "10 نکته طلایی برای {keyword}",
                "راهنمای کامل {keyword} در سال 2025",
                "چگونه {keyword} را بهینه کنیم؟",
                "اسرار موفقیت در {keyword}",
                "بهترین روش‌های {keyword}"
            ],
            "comparison": [
                "مقایسه {keyword} با روش‌های سنتی",
                "تفاوت {keyword} در فروشگاه‌های مختلف",
                "مزایا و معایب {keyword}",
                "بررسی {keyword} در بازار ایران"
            ],
            "case_study": [
                "مطالعه موردی: موفقیت با {keyword}",
                "نمونه واقعی {keyword} در فروشگاه ایرانی",
                "تجربه موفق {keyword} در تهران",
                "داستان موفقیت: {keyword} در عمل"
            ]
        }
    
    def generate_content(self, keyword, content_type="tips"):
        """تولید محتوای خودکار"""
        template = random.choice(self.templates[content_type])
        title = template.format(keyword=keyword)
        
        content = self._generate_body(keyword, content_type)
        
        return {
            'title': title,
            'content': content,
            'excerpt': content[:200] + "...",
            'meta_description': f"راهنمای جامع {keyword} - نکات و تکنیک‌های حرفه‌ای برای بهینه‌سازی فروشگاه",
            'meta_keywords': f"{keyword}, چیدمان فروشگاه, بهینه‌سازی, فروشگاه مدرن"
        }
    
    def _generate_body(self, keyword, content_type):
        """تولید متن اصلی"""
        intro_templates = [
            f"در دنیای امروز، {keyword} یکی از مهم‌ترین عوامل موفقیت در کسب‌وکار خرده‌فروشی است.",
            f"تحقیقات نشان می‌دهد که {keyword} می‌تواند فروش را تا 30% افزایش دهد.",
            f"برای موفقیت در {keyword}، باید اصول و تکنیک‌های حرفه‌ای را بدانید."
        ]
        
        body_templates = {
            "tips": [
                "در این مقاله، مهم‌ترین نکات و تکنیک‌های حرفه‌ای را بررسی می‌کنیم.",
                "این راهنما شامل نکات عملی و قابل اجرا برای بهبود عملکرد فروشگاه است.",
                "با رعایت این نکات، می‌توانید فروشگاه خود را به بهترین شکل بهینه کنید."
            ],
            "comparison": [
                "در این مقاله، روش‌های مختلف را با هم مقایسه می‌کنیم.",
                "هر روش مزایا و معایب خاص خود را دارد که در ادامه بررسی می‌کنیم.",
                "انتخاب بهترین روش بستگی به شرایط و نیازهای فروشگاه شما دارد."
            ],
            "case_study": [
                "در این مطالعه موردی، نمونه واقعی موفقیت را بررسی می‌کنیم.",
                "این تجربه می‌تواند الهام‌بخش سایر فروشگاه‌داران باشد.",
                "نکات کلیدی این موفقیت را در ادامه بررسی می‌کنیم."
            ]
        }
        
        intro = random.choice(intro_templates)
        body = random.choice(body_templates[content_type])
        
        return f"{intro}\n\n{body}\n\nبرای اطلاعات بیشتر و تحلیل حرفه‌ای فروشگاه خود، با چیدمانو تماس بگیرید."

class LinkBuilder:
    """سازنده لینک‌های داخلی"""
    
    def __init__(self):
        self.internal_pages = [
            {'url': '/چیدمان-فروشگاه/', 'title': 'راهنمای جامع چیدمان فروشگاه'},
            {'url': '/guide/store-layout/', 'title': 'راهنمای چیدمان فروشگاه'},
            {'url': '/guide/supermarket-layout/', 'title': 'راهنمای چیدمان سوپرمارکت'},
            {'url': '/guide/storefront-lighting/', 'title': 'نورپردازی فروشگاه'},
            {'url': '/guide/color-psychology/', 'title': 'روانشناسی رنگ'},
            {'url': '/guide/customer-journey/', 'title': 'مسیر مشتری'},
            {'url': '/guide/lighting-design/', 'title': 'طراحی نورپردازی'},
            {'url': '/case-studies/', 'title': 'مطالعات موردی'},
            {'url': '/partnership/', 'title': 'همکاری با ما'},
            {'url': '/store/forms/submit/', 'title': 'تحلیل فروشگاه'}
        ]
    
    def add_internal_links(self, content, max_links=3):
        """اضافه کردن لینک‌های داخلی به محتوا"""
        links_added = 0
        modified_content = content
        
        for page in self.internal_pages:
            if links_added >= max_links:
                break
                
            # جستجوی کلمات کلیدی مرتبط
            keywords = ['چیدمان', 'فروشگاه', 'نورپردازی', 'رنگ', 'مشتری', 'تحلیل']
            
            for keyword in keywords:
                if keyword in content and page['title'] not in modified_content:
                    # اضافه کردن لینک
                    link_text = f"<a href='{page['url']}' title='{page['title']}'>{page['title']}</a>"
                    modified_content = modified_content.replace(
                        keyword, 
                        link_text, 
                        1
                    )
                    links_added += 1
                    break
        
        return modified_content
    
    def create_contextual_links(self, source_url, content):
        """ایجاد لینک‌های متنی"""
        contextual_links = []
        
        for page in self.internal_pages:
            if page['url'] != source_url:
                # جستجوی کلمات کلیدی مرتبط
                if any(keyword in content for keyword in ['چیدمان', 'فروشگاه', 'نورپردازی']):
                    contextual_links.append({
                        'url': page['url'],
                        'title': page['title'],
                        'anchor_text': page['title']
                    })
        
        return contextual_links[:5]  # حداکثر 5 لینک

class KeywordOptimizer:
    """بهینه‌ساز کلمات کلیدی"""
    
    def __init__(self):
        self.primary_keywords = [
            "چیدمان فروشگاه", "طراحی فروشگاه", "بهینه‌سازی فروشگاه",
            "نورپردازی فروشگاه", "مسیر مشتری", "روانشناسی رنگ"
        ]
        
        self.long_tail_keywords = [
            "چیدمان فروشگاه مدرن", "طراحی فروشگاه کوچک",
            "بهینه‌سازی فضای فروشگاه", "نورپردازی فروشگاه لوکس",
            "مسیر مشتری در سوپرمارکت", "روانشناسی رنگ در فروشگاه"
        ]
    
    def optimize_content(self, content, target_keyword):
        """بهینه‌سازی محتوا برای کلمه کلیدی"""
        # بررسی تراکم کلمه کلیدی
        keyword_density = self._calculate_density(content, target_keyword)
        
        # اضافه کردن کلمات کلیدی طولانی
        long_tail = self._find_relevant_long_tail(target_keyword)
        
        # بهینه‌سازی تگ‌ها
        optimized_content = self._add_keyword_variations(content, target_keyword)
        
        return {
            'content': optimized_content,
            'keyword_density': keyword_density,
            'long_tail_keywords': long_tail,
            'optimization_score': self._calculate_score(keyword_density, len(long_tail))
        }
    
    def _calculate_density(self, content, keyword):
        """محاسبه تراکم کلمه کلیدی"""
        words = content.split()
        keyword_count = content.lower().count(keyword.lower())
        return (keyword_count / len(words)) * 100 if words else 0
    
    def _find_relevant_long_tail(self, keyword):
        """یافتن کلمات کلیدی طولانی مرتبط"""
        relevant = []
        for long_tail in self.long_tail_keywords:
            if keyword in long_tail:
                relevant.append(long_tail)
        return relevant
    
    def _add_keyword_variations(self, content, keyword):
        """اضافه کردن تغییرات کلمه کلیدی"""
        variations = [
            keyword,
            keyword.replace("فروشگاه", "فروشگاه‌ها"),
            keyword + " حرفه‌ای",
            "بهترین " + keyword
        ]
        
        optimized = content
        for variation in variations[1:]:  # از تغییر اول صرف نظر می‌کنیم
            if variation not in optimized:
                optimized += f"\n\nبرای اطلاعات بیشتر درباره {variation}، با ما تماس بگیرید."
                break
        
        return optimized
    
    def _calculate_score(self, density, long_tail_count):
        """محاسبه امتیاز بهینه‌سازی"""
        # تراکم ایده‌آل: 1-3%
        density_score = 100 - abs(density - 2) * 20
        long_tail_score = min(long_tail_count * 20, 100)
        
        return (density_score + long_tail_score) / 2

class SEOMonitor:
    """مانیتورینگ SEO"""
    
    def __init__(self):
        self.metrics = {}
    
    def track_keyword_ranking(self, keyword, position):
        """ردیابی رتبه کلمه کلیدی"""
        if keyword not in self.metrics:
            self.metrics[keyword] = {'positions': [], 'best_position': 999}
        
        self.metrics[keyword]['positions'].append({
            'position': position,
            'date': timezone.now().date()
        })
        
        if position < self.metrics[keyword]['best_position']:
            self.metrics[keyword]['best_position'] = position
    
    def get_keyword_trends(self, keyword):
        """دریافت روند کلمه کلیدی"""
        if keyword not in self.metrics:
            return None
        
        positions = self.metrics[keyword]['positions']
        if len(positions) < 2:
            return "داده کافی نیست"
        
        latest = positions[-1]['position']
        previous = positions[-2]['position']
        
        if latest < previous:
            return f"بهبود {previous - latest} رتبه"
        elif latest > previous:
            return f"کاهش {latest - previous} رتبه"
        else:
            return "بدون تغییر"
    
    def generate_seo_report(self):
        """تولید گزارش SEO"""
        report = {
            'total_keywords': len(self.metrics),
            'top_performing': [],
            'needs_attention': [],
            'recommendations': []
        }
        
        for keyword, data in self.metrics.items():
            if data['best_position'] <= 10:
                report['top_performing'].append(keyword)
            elif data['best_position'] > 50:
                report['needs_attention'].append(keyword)
        
        # توصیه‌ها
        if len(report['needs_attention']) > 0:
            report['recommendations'].append("بهبود محتوای کلمات کلیدی با رتبه پایین")
        
        if len(report['top_performing']) < 5:
            report['recommendations'].append("افزایش تعداد کلمات کلیدی با رتبه بالا")
        
        return report
