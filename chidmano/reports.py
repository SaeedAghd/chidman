"""
سیستم گزارش‌گیری SEO پیشرفته
"""
from django.utils import timezone
from django.db.models import Avg, Count, Sum
from datetime import datetime, timedelta
from .models import SEOMetrics, SEOKeyword, BlogPost
import json
import csv
import os
from django.conf import settings

class SEOReportGenerator:
    """تولیدکننده گزارش‌های SEO"""
    
    def __init__(self):
        self.reports_dir = os.path.join(settings.BASE_DIR, 'seo_reports')
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_daily_report(self, date=None):
        """تولید گزارش روزانه"""
        if not date:
            date = timezone.now().date()
        
        try:
            metrics = SEOMetrics.objects.get(date=date)
        except SEOMetrics.DoesNotExist:
            return None
        
        report = {
            'date': date.isoformat(),
            'type': 'daily',
            'metrics': {
                'organic_traffic': metrics.organic_traffic,
                'keyword_rankings': metrics.keyword_rankings,
                'backlinks_count': metrics.backlinks_count,
                'domain_authority': metrics.domain_authority,
                'page_speed_score': metrics.page_speed_score
            },
            'keywords_summary': self._get_keywords_summary(),
            'content_summary': self._get_content_summary(),
            'recommendations': self._get_daily_recommendations(metrics)
        }
        
        return report
    
    def generate_weekly_report(self, start_date=None):
        """تولید گزارش هفتگی"""
        if not start_date:
            start_date = timezone.now().date() - timedelta(days=7)
        
        end_date = start_date + timedelta(days=6)
        
        weekly_metrics = SEOMetrics.objects.filter(
            date__range=[start_date, end_date]
        ).order_by('date')
        
        if not weekly_metrics.exists():
            return None
        
        # محاسبه میانگین‌ها
        avg_metrics = weekly_metrics.aggregate(
            avg_traffic=Avg('organic_traffic'),
            avg_keywords=Avg('keyword_rankings'),
            avg_backlinks=Avg('backlinks_count'),
            avg_authority=Avg('domain_authority'),
            avg_speed=Avg('page_speed_score')
        )
        
        # محاسبه تغییرات
        first_metrics = weekly_metrics.first()
        last_metrics = weekly_metrics.last()
        
        report = {
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            },
            'type': 'weekly',
            'average_metrics': avg_metrics,
            'changes': {
                'traffic_change': last_metrics.organic_traffic - first_metrics.organic_traffic,
                'keywords_change': last_metrics.keyword_rankings - first_metrics.keyword_rankings,
                'backlinks_change': last_metrics.backlinks_count - first_metrics.backlinks_count,
                'authority_change': last_metrics.domain_authority - first_metrics.domain_authority,
                'speed_change': last_metrics.page_speed_score - first_metrics.page_speed_score
            },
            'daily_data': [
                {
                    'date': m.date.isoformat(),
                    'traffic': m.organic_traffic,
                    'keywords': m.keyword_rankings,
                    'backlinks': m.backlinks_count,
                    'authority': m.domain_authority,
                    'speed': m.page_speed_score
                }
                for m in weekly_metrics
            ],
            'top_performing_keywords': self._get_top_keywords(),
            'content_performance': self._get_content_performance(),
            'recommendations': self._get_weekly_recommendations(avg_metrics, last_metrics)
        }
        
        return report
    
    def generate_monthly_report(self, year=None, month=None):
        """تولید گزارش ماهانه"""
        if not year or not month:
            now = timezone.now()
            year = now.year
            month = now.month
        
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1).date() - timedelta(days=1)
        
        monthly_metrics = SEOMetrics.objects.filter(
            date__range=[start_date, end_date]
        ).order_by('date')
        
        if not monthly_metrics.exists():
            return None
        
        # محاسبه آمار ماهانه
        monthly_stats = monthly_metrics.aggregate(
            total_traffic=Sum('organic_traffic'),
            avg_traffic=Avg('organic_traffic'),
            max_traffic=Max('organic_traffic'),
            min_traffic=Min('organic_traffic'),
            avg_keywords=Avg('keyword_rankings'),
            avg_backlinks=Avg('backlinks_count'),
            avg_authority=Avg('domain_authority'),
            avg_speed=Avg('page_speed_score')
        )
        
        report = {
            'period': {
                'year': year,
                'month': month,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            },
            'type': 'monthly',
            'statistics': monthly_stats,
            'growth_analysis': self._get_growth_analysis(start_date, end_date),
            'keyword_analysis': self._get_keyword_analysis(),
            'content_analysis': self._get_content_analysis(),
            'competitor_analysis': self._get_competitor_analysis(),
            'recommendations': self._get_monthly_recommendations(monthly_stats)
        }
        
        return report
    
    def _get_keywords_summary(self):
        """خلاصه کلمات کلیدی"""
        total_keywords = SEOKeyword.objects.filter(is_active=True).count()
        high_volume_keywords = SEOKeyword.objects.filter(
            is_active=True,
            search_volume__gte=1000
        ).count()
        
        return {
            'total_keywords': total_keywords,
            'high_volume_keywords': high_volume_keywords,
            'average_difficulty': SEOKeyword.objects.filter(
                is_active=True
            ).aggregate(avg=Avg('difficulty'))['avg'] or 0
        }
    
    def _get_content_summary(self):
        """خلاصه محتوا"""
        total_posts = BlogPost.objects.filter(published=True).count()
        recent_posts = BlogPost.objects.filter(
            published=True,
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        return {
            'total_posts': total_posts,
            'recent_posts': recent_posts,
            'total_views': BlogPost.objects.filter(
                published=True
            ).aggregate(total=Sum('views_count'))['total'] or 0
        }
    
    def _get_daily_recommendations(self, metrics):
        """توصیه‌های روزانه"""
        recommendations = []
        
        if metrics.page_speed_score < 80:
            recommendations.append('بهبود سرعت صفحه')
        
        if metrics.organic_traffic < 1000:
            recommendations.append('افزایش ترافیک ارگانیک')
        
        if metrics.keyword_rankings < 30:
            recommendations.append('بهبود رتبه‌بندی کلمات کلیدی')
        
        return recommendations
    
    def _get_top_keywords(self):
        """کلمات کلیدی برتر"""
        return list(SEOKeyword.objects.filter(
            is_active=True
        ).order_by('-search_volume')[:10].values(
            'keyword', 'search_volume', 'difficulty', 'cpc'
        ))
    
    def _get_content_performance(self):
        """عملکرد محتوا"""
        return list(BlogPost.objects.filter(
            published=True
        ).order_by('-views_count')[:5].values(
            'title', 'views_count', 'created_at'
        ))
    
    def _get_weekly_recommendations(self, avg_metrics, last_metrics):
        """توصیه‌های هفتگی"""
        recommendations = []
        
        if avg_metrics['avg_speed'] < 80:
            recommendations.append('بهبود سرعت صفحه')
        
        if avg_metrics['avg_traffic'] < 1500:
            recommendations.append('افزایش ترافیک ارگانیک')
        
        if last_metrics.keyword_rankings < 40:
            recommendations.append('بهبود رتبه‌بندی کلمات کلیدی')
        
        return recommendations
    
    def _get_growth_analysis(self, start_date, end_date):
        """تحلیل رشد"""
        # مقایسه با ماه قبل
        prev_start = start_date - timedelta(days=30)
        prev_end = start_date - timedelta(days=1)
        
        current_metrics = SEOMetrics.objects.filter(
            date__range=[start_date, end_date]
        ).aggregate(
            avg_traffic=Avg('organic_traffic'),
            avg_keywords=Avg('keyword_rankings')
        )
        
        prev_metrics = SEOMetrics.objects.filter(
            date__range=[prev_start, prev_end]
        ).aggregate(
            avg_traffic=Avg('organic_traffic'),
            avg_keywords=Avg('keyword_rankings')
        )
        
        traffic_growth = 0
        keywords_growth = 0
        
        if prev_metrics['avg_traffic']:
            traffic_growth = ((current_metrics['avg_traffic'] - prev_metrics['avg_traffic']) / 
                            prev_metrics['avg_traffic']) * 100
        
        if prev_metrics['avg_keywords']:
            keywords_growth = ((current_metrics['avg_keywords'] - prev_metrics['avg_keywords']) / 
                            prev_metrics['avg_keywords']) * 100
        
        return {
            'traffic_growth': traffic_growth,
            'keywords_growth': keywords_growth
        }
    
    def _get_keyword_analysis(self):
        """تحلیل کلمات کلیدی"""
        keywords = SEOKeyword.objects.filter(is_active=True)
        
        return {
            'total_keywords': keywords.count(),
            'high_volume': keywords.filter(search_volume__gte=1000).count(),
            'medium_difficulty': keywords.filter(difficulty__range=[40, 70]).count(),
            'high_cpc': keywords.filter(cpc__gte=2.0).count()
        }
    
    def _get_content_analysis(self):
        """تحلیل محتوا"""
        posts = BlogPost.objects.filter(published=True)
        
        return {
            'total_posts': posts.count(),
            'recent_posts': posts.filter(
                created_at__gte=timezone.now() - timedelta(days=30)
            ).count(),
            'total_views': posts.aggregate(total=Sum('views_count'))['total'] or 0,
            'avg_views': posts.aggregate(avg=Avg('views_count'))['avg'] or 0
        }
    
    def _get_competitor_analysis(self):
        """تحلیل رقبا"""
        # شبیه‌سازی تحلیل رقبا
        return {
            'market_position': 'رتبه 3 در کلمات کلیدی اصلی',
            'competitive_keywords': ['چیدمان فروشگاه', 'طراحی فروشگاه'],
            'opportunities': ['کلمات کلیدی طولانی', 'محتوای تخصصی']
        }
    
    def _get_monthly_recommendations(self, stats):
        """توصیه‌های ماهانه"""
        recommendations = []
        
        if stats['avg_speed'] < 80:
            recommendations.append('بهبود سرعت صفحه')
        
        if stats['avg_traffic'] < 2000:
            recommendations.append('افزایش ترافیک ارگانیک')
        
        if stats['avg_keywords'] < 50:
            recommendations.append('بهبود رتبه‌بندی کلمات کلیدی')
        
        recommendations.extend([
            'تولید محتوای جدید',
            'بهینه‌سازی لینک‌های داخلی',
            'بهبود تجربه کاربری'
        ])
        
        return recommendations
    
    def save_report(self, report, format='json'):
        """ذخیره گزارش"""
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{report['type']}_report_{timestamp}.{format}"
        filepath = os.path.join(self.reports_dir, filename)
        
        if format == 'json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
        elif format == 'csv':
            self._save_csv_report(report, filepath)
        
        return filepath
    
    def _save_csv_report(self, report, filepath):
        """ذخیره گزارش CSV"""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # نوشتن هدر
            writer.writerow(['Metric', 'Value'])
            
            # نوشتن متریک‌ها
            if 'metrics' in report:
                for key, value in report['metrics'].items():
                    writer.writerow([key, value])
            
            if 'average_metrics' in report:
                for key, value in report['average_metrics'].items():
                    writer.writerow([key, value])
    
    def generate_summary_report(self):
        """تولید گزارش خلاصه"""
        today = timezone.now().date()
        
        # گزارش امروز
        daily_report = self.generate_daily_report(today)
        
        # گزارش هفته گذشته
        weekly_report = self.generate_weekly_report(today - timedelta(days=7))
        
        # گزارش ماه گذشته
        last_month = today.replace(day=1) - timedelta(days=1)
        monthly_report = self.generate_monthly_report(
            last_month.year, last_month.month
        )
        
        summary = {
            'generated_at': timezone.now().isoformat(),
            'daily': daily_report,
            'weekly': weekly_report,
            'monthly': monthly_report,
            'overall_score': self._calculate_overall_score(daily_report)
        }
        
        return summary
    
    def _calculate_overall_score(self, daily_report):
        """محاسبه امتیاز کلی"""
        if not daily_report:
            return 0
        
        metrics = daily_report['metrics']
        
        # وزن‌دهی متریک‌ها
        weights = {
            'organic_traffic': 0.3,
            'keyword_rankings': 0.25,
            'page_speed_score': 0.2,
            'domain_authority': 0.15,
            'backlinks_count': 0.1
        }
        
        score = 0
        for metric, weight in weights.items():
            value = metrics.get(metric, 0)
            
            # نرمال‌سازی مقادیر
            if metric == 'organic_traffic':
                normalized = min(value / 5000, 1) * 100
            elif metric == 'keyword_rankings':
                normalized = min(value / 100, 1) * 100
            elif metric == 'page_speed_score':
                normalized = value
            elif metric == 'domain_authority':
                normalized = value
            elif metric == 'backlinks_count':
                normalized = min(value / 500, 1) * 100
            
            score += normalized * weight
        
        return int(score)
