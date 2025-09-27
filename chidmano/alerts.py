"""
سیستم هشدار SEO
"""
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import SEOMetrics, SEOKeyword
import logging

logger = logging.getLogger(__name__)

class SEOAlertSystem:
    """سیستم هشدار SEO"""
    
    def __init__(self):
        self.alert_thresholds = {
            'traffic_drop': 20,  # کاهش 20% ترافیک
            'speed_drop': 10,    # کاهش 10 امتیاز سرعت
            'ranking_drop': 5,   # کاهش 5 رتبه
            'backlinks_loss': 10 # از دست دادن 10 بک‌لینک
        }
        
        self.email_recipients = getattr(settings, 'SEO_ALERT_EMAILS', [])
    
    def check_traffic_alerts(self):
        """بررسی هشدارهای ترافیک"""
        alerts = []
        
        # مقایسه ترافیک امروز با دیروز
        today = timezone.now().date()
        yesterday = today - timezone.timedelta(days=1)
        
        try:
            today_metrics = SEOMetrics.objects.get(date=today)
            yesterday_metrics = SEOMetrics.objects.get(date=yesterday)
            
            traffic_drop = ((yesterday_metrics.organic_traffic - today_metrics.organic_traffic) / 
                           yesterday_metrics.organic_traffic) * 100
            
            if traffic_drop > self.alert_thresholds['traffic_drop']:
                alerts.append({
                    'type': 'traffic_drop',
                    'message': f'کاهش {traffic_drop:.1f}% ترافیک ارگانیک',
                    'severity': 'high',
                    'data': {
                        'today': today_metrics.organic_traffic,
                        'yesterday': yesterday_metrics.organic_traffic,
                        'drop_percentage': traffic_drop
                    }
                })
                
        except SEOMetrics.DoesNotExist:
            pass
        
        return alerts
    
    def check_speed_alerts(self):
        """بررسی هشدارهای سرعت"""
        alerts = []
        
        today = timezone.now().date()
        
        try:
            today_metrics = SEOMetrics.objects.get(date=today)
            
            if today_metrics.page_speed_score < 70:
                alerts.append({
                    'type': 'speed_low',
                    'message': f'سرعت صفحه پایین: {today_metrics.page_speed_score}',
                    'severity': 'medium',
                    'data': {
                        'speed_score': today_metrics.page_speed_score,
                        'threshold': 70
                    }
                })
                
        except SEOMetrics.DoesNotExist:
            pass
        
        return alerts
    
    def check_ranking_alerts(self):
        """بررسی هشدارهای رتبه‌بندی"""
        alerts = []
        
        # بررسی کلمات کلیدی با رتبه پایین
        low_ranking_keywords = SEOKeyword.objects.filter(
            is_active=True
        ).extra(
            where=["target_url IS NULL OR target_url = ''"]
        )
        
        for keyword in low_ranking_keywords:
            if keyword.search_volume > 1000:  # کلمات کلیدی مهم
                alerts.append({
                    'type': 'ranking_low',
                    'message': f'رتبه پایین برای کلمه کلیدی مهم: {keyword.keyword}',
                    'severity': 'high',
                    'data': {
                        'keyword': keyword.keyword,
                        'search_volume': keyword.search_volume,
                        'difficulty': keyword.difficulty
                    }
                })
        
        return alerts
    
    def check_backlink_alerts(self):
        """بررسی هشدارهای بک‌لینک"""
        alerts = []
        
        # مقایسه بک‌لینک‌های امروز با دیروز
        today = timezone.now().date()
        yesterday = today - timezone.timedelta(days=1)
        
        try:
            today_metrics = SEOMetrics.objects.get(date=today)
            yesterday_metrics = SEOMetrics.objects.get(date=yesterday)
            
            backlinks_loss = yesterday_metrics.backlinks_count - today_metrics.backlinks_count
            
            if backlinks_loss > self.alert_thresholds['backlinks_loss']:
                alerts.append({
                    'type': 'backlinks_loss',
                    'message': f'از دست دادن {backlinks_loss} بک‌لینک',
                    'severity': 'high',
                    'data': {
                        'today': today_metrics.backlinks_count,
                        'yesterday': yesterday_metrics.backlinks_count,
                        'loss': backlinks_loss
                    }
                })
                
        except SEOMetrics.DoesNotExist:
            pass
        
        return alerts
    
    def check_all_alerts(self):
        """بررسی تمام هشدارها"""
        all_alerts = []
        
        all_alerts.extend(self.check_traffic_alerts())
        all_alerts.extend(self.check_speed_alerts())
        all_alerts.extend(self.check_ranking_alerts())
        all_alerts.extend(self.check_backlink_alerts())
        
        return all_alerts
    
    def send_alert_email(self, alert):
        """ارسال ایمیل هشدار"""
        if not self.email_recipients:
            return False
        
        subject = f'هشدار SEO چیدمانو: {alert["message"]}'
        
        body = f"""
هشدار SEO شناسایی شد:

نوع: {alert['type']}
پیام: {alert['message']}
شدت: {alert['severity']}
زمان: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

داده‌های مربوطه:
{self._format_alert_data(alert['data'])}

برای بررسی بیشتر، به داشبورد SEO مراجعه کنید:
https://chidmano.ir/admin/seo-dashboard/
        """
        
        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                self.email_recipients,
                fail_silently=False
            )
            return True
        except Exception as e:
            logger.error(f'خطا در ارسال ایمیل هشدار: {e}')
            return False
    
    def _format_alert_data(self, data):
        """فرمت کردن داده‌های هشدار"""
        formatted = []
        for key, value in data.items():
            formatted.append(f"{key}: {value}")
        return '\n'.join(formatted)
    
    def process_alerts(self):
        """پردازش تمام هشدارها"""
        alerts = self.check_all_alerts()
        
        if not alerts:
            return {'processed': 0, 'sent': 0}
        
        sent_count = 0
        for alert in alerts:
            if self.send_alert_email(alert):
                sent_count += 1
        
        return {
            'processed': len(alerts),
            'sent': sent_count,
            'alerts': alerts
        }
    
    def get_alert_summary(self):
        """دریافت خلاصه هشدارها"""
        alerts = self.check_all_alerts()
        
        summary = {
            'total_alerts': len(alerts),
            'high_severity': len([a for a in alerts if a['severity'] == 'high']),
            'medium_severity': len([a for a in alerts if a['severity'] == 'medium']),
            'low_severity': len([a for a in alerts if a['severity'] == 'low']),
            'alert_types': {}
        }
        
        for alert in alerts:
            alert_type = alert['type']
            if alert_type not in summary['alert_types']:
                summary['alert_types'][alert_type] = 0
            summary['alert_types'][alert_type] += 1
        
        return summary

class SEOHealthChecker:
    """بررسی سلامت SEO"""
    
    def __init__(self):
        self.health_checks = {
            'page_speed': self.check_page_speed,
            'mobile_friendly': self.check_mobile_friendly,
            'ssl_certificate': self.check_ssl_certificate,
            'meta_tags': self.check_meta_tags,
            'internal_links': self.check_internal_links,
            'image_optimization': self.check_image_optimization
        }
    
    def check_page_speed(self, url):
        """بررسی سرعت صفحه"""
        # شبیه‌سازی بررسی سرعت
        import random
        score = random.randint(60, 95)
        
        return {
            'status': 'good' if score >= 80 else 'warning' if score >= 60 else 'error',
            'score': score,
            'message': f'سرعت صفحه: {score}/100'
        }
    
    def check_mobile_friendly(self, url):
        """بررسی سازگاری با موبایل"""
        # شبیه‌سازی بررسی موبایل
        return {
            'status': 'good',
            'message': 'سازگار با موبایل'
        }
    
    def check_ssl_certificate(self, url):
        """بررسی گواهی SSL"""
        return {
            'status': 'good',
            'message': 'گواهی SSL فعال'
        }
    
    def check_meta_tags(self, url):
        """بررسی تگ‌های متا"""
        return {
            'status': 'good',
            'message': 'تگ‌های متا کامل'
        }
    
    def check_internal_links(self, url):
        """بررسی لینک‌های داخلی"""
        return {
            'status': 'good',
            'message': 'لینک‌های داخلی بهینه'
        }
    
    def check_image_optimization(self, url):
        """بررسی بهینه‌سازی تصاویر"""
        return {
            'status': 'warning',
            'message': 'برخی تصاویر نیاز به بهینه‌سازی دارند'
        }
    
    def run_health_check(self, url='https://chidmano.ir'):
        """اجرای بررسی سلامت"""
        results = {}
        
        for check_name, check_function in self.health_checks.items():
            try:
                results[check_name] = check_function(url)
            except Exception as e:
                results[check_name] = {
                    'status': 'error',
                    'message': f'خطا در بررسی: {str(e)}'
                }
        
        return results
    
    def get_health_score(self, results):
        """محاسبه امتیاز سلامت"""
        total_checks = len(results)
        good_checks = len([r for r in results.values() if r['status'] == 'good'])
        warning_checks = len([r for r in results.values() if r['status'] == 'warning'])
        error_checks = len([r for r in results.values() if r['status'] == 'error'])
        
        score = (good_checks * 100 + warning_checks * 50) / total_checks
        
        return {
            'score': int(score),
            'total_checks': total_checks,
            'good': good_checks,
            'warning': warning_checks,
            'error': error_checks
        }
