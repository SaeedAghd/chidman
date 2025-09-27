from django.core.management.base import BaseCommand
from django.utils import timezone
from chidmano.models import SEOMetrics, SEOKeyword
from chidmano.seo_utils import SEOMonitor
import random

class Command(BaseCommand):
    help = 'مانیتورینگ متریک‌های SEO'

    def add_arguments(self, parser):
        parser.add_argument(
            '--update',
            action='store_true',
            help='به‌روزرسانی متریک‌های SEO'
        )
        parser.add_argument(
            '--report',
            action='store_true',
            help='تولید گزارش SEO'
        )

    def handle(self, *args, **options):
        monitor = SEOMonitor()
        
        if options['update']:
            self.update_metrics()
        
        if options['report']:
            self.generate_report(monitor)

    def update_metrics(self):
        """به‌روزرسانی متریک‌های SEO"""
        today = timezone.now().date()
        
        # بررسی وجود متریک برای امروز
        metrics, created = SEOMetrics.objects.get_or_create(
            date=today,
            defaults={
                'organic_traffic': random.randint(1000, 2000),
                'keyword_rankings': random.randint(30, 60),
                'backlinks_count': random.randint(100, 200),
                'domain_authority': random.randint(40, 80),
                'page_speed_score': random.randint(70, 95)
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'متریک‌های جدید برای {today} ایجاد شد')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'متریک‌های {today} قبلاً وجود دارد')
            )

    def generate_report(self, monitor):
        """تولید گزارش SEO"""
        # شبیه‌سازی داده‌های رتبه‌بندی
        keywords = [
            'چیدمان فروشگاه',
            'طراحی فروشگاه', 
            'نورپردازی فروشگاه',
            'روانشناسی رنگ فروشگاه',
            'مسیر مشتری فروشگاه'
        ]
        
        for keyword in keywords:
            position = random.randint(1, 50)
            monitor.track_keyword_ranking(keyword, position)
        
        # تولید گزارش
        report = monitor.generate_seo_report()
        
        self.stdout.write(
            self.style.SUCCESS('=== گزارش SEO ===')
        )
        
        self.stdout.write(f'تعداد کل کلمات کلیدی: {report["total_keywords"]}')
        
        self.stdout.write(
            self.style.SUCCESS(f'کلمات کلیدی با عملکرد بالا: {len(report["top_performing"])}')
        )
        for keyword in report['top_performing']:
            self.stdout.write(f'  ✓ {keyword}')
        
        self.stdout.write(
            self.style.WARNING(f'کلمات کلیدی نیازمند توجه: {len(report["needs_attention"])}')
        )
        for keyword in report['needs_attention']:
            self.stdout.write(f'  ⚠ {keyword}')
        
        self.stdout.write(
            self.style.SUCCESS('توصیه‌ها:')
        )
        for recommendation in report['recommendations']:
            self.stdout.write(f'  • {recommendation}')
        
        # ذخیره گزارش در فایل
        self.save_report_to_file(report)

    def save_report_to_file(self, report):
        """ذخیره گزارش در فایل"""
        import json
        from django.conf import settings
        
        report_data = {
            'timestamp': timezone.now().isoformat(),
            'report': report
        }
        
        # ذخیره در فایل JSON
        import os
        reports_dir = os.path.join(settings.BASE_DIR, 'seo_reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        filename = f"seo_report_{timezone.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        self.stdout.write(
            self.style.SUCCESS(f'گزارش در {filepath} ذخیره شد')
        )
