from django.core.management.base import BaseCommand
from django.utils import timezone
from chidmano.monitoring import SEOMonitoringService
from chidmano.models import SEOKeyword
import schedule
import time

class Command(BaseCommand):
    help = 'مانیتورینگ خودکار SEO'

    def add_arguments(self, parser):
        parser.add_argument(
            '--daemon',
            action='store_true',
            help='اجرای مداوم مانیتورینگ'
        )
        parser.add_argument(
            '--once',
            action='store_true',
            help='اجرای یکباره مانیتورینگ'
        )

    def handle(self, *args, **options):
        monitor = SEOMonitoringService()
        
        if options['once']:
            self.run_monitoring_once(monitor)
        elif options['daemon']:
            self.run_monitoring_daemon(monitor)
        else:
            self.stdout.write(
                self.style.ERROR('لطفاً یکی از گزینه‌های --once یا --daemon را انتخاب کنید')
            )

    def run_monitoring_once(self, monitor):
        """اجرای یکباره مانیتورینگ"""
        self.stdout.write(
            self.style.SUCCESS('شروع مانیتورینگ SEO...')
        )
        
        # به‌روزرسانی متریک‌های روزانه
        metrics = monitor.update_daily_metrics()
        self.stdout.write(
            self.style.SUCCESS(f'متریک‌های روزانه به‌روزرسانی شد: {metrics.date}')
        )
        
        # بررسی کلمات کلیدی
        keywords = [kw.keyword for kw in SEOKeyword.objects.filter(is_active=True)]
        if keywords:
            rankings = monitor.check_keyword_rankings(keywords)
            self.stdout.write(
                self.style.SUCCESS(f'رتبه‌بندی {len(rankings)} کلمه کلیدی بررسی شد')
            )
        
        # تولید گزارش هفتگی
        weekly_report = monitor.generate_weekly_report()
        if weekly_report:
            self.stdout.write(
                self.style.SUCCESS('گزارش هفتگی تولید شد')
            )
            self.print_weekly_report(weekly_report)
        
        # یافتن فرصت‌ها
        opportunities = monitor.get_keyword_opportunities()
        if opportunities:
            self.stdout.write(
                self.style.SUCCESS(f'{len(opportunities)} فرصت کلمات کلیدی یافت شد')
            )
            self.print_opportunities(opportunities)
        
        self.stdout.write(
            self.style.SUCCESS('مانیتورینگ تکمیل شد!')
        )

    def run_monitoring_daemon(self, monitor):
        """اجرای مداوم مانیتورینگ"""
        self.stdout.write(
            self.style.SUCCESS('شروع مانیتورینگ مداوم SEO...')
        )
        
        # تنظیم زمان‌بندی
        schedule.every().day.at("09:00").do(self.daily_monitoring, monitor)
        schedule.every().monday.at("10:00").do(self.weekly_report, monitor)
        schedule.every().hour.do(self.hourly_check, monitor)
        
        self.stdout.write('زمان‌بندی تنظیم شد:')
        self.stdout.write('  - مانیتورینگ روزانه: 09:00')
        self.stdout.write('  - گزارش هفتگی: دوشنبه 10:00')
        self.stdout.write('  - بررسی ساعتی: هر ساعت')
        self.stdout.write('برای توقف، Ctrl+C را فشار دهید')
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # بررسی هر دقیقه
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING('مانیتورینگ متوقف شد')
            )

    def daily_monitoring(self, monitor):
        """مانیتورینگ روزانه"""
        self.stdout.write(f'مانیتورینگ روزانه - {timezone.now()}')
        
        # به‌روزرسانی متریک‌ها
        metrics = monitor.update_daily_metrics()
        self.stdout.write(f'متریک‌های روزانه: ترافیک {metrics.organic_traffic}, کلمات {metrics.keyword_rankings}')
        
        # بررسی کلمات کلیدی
        keywords = [kw.keyword for kw in SEOKeyword.objects.filter(is_active=True)]
        if keywords:
            rankings = monitor.check_keyword_rankings(keywords)
            good_rankings = sum(1 for r in rankings.values() if r and r <= 10)
            self.stdout.write(f'کلمات کلیدی با رتبه بالا: {good_rankings}/{len(rankings)}')

    def weekly_report(self, monitor):
        """گزارش هفتگی"""
        self.stdout.write(f'تولید گزارش هفتگی - {timezone.now()}')
        
        report = monitor.generate_weekly_report()
        if report:
            self.print_weekly_report(report)
            
            # ذخیره گزارش
            self.save_report(report)

    def hourly_check(self, monitor):
        """بررسی ساعتی"""
        # بررسی سرعت صفحه
        speed = monitor.check_page_speed('https://chidmano.ir')
        if speed < 80:
            self.stdout.write(
                self.style.WARNING(f'سرعت صفحه پایین: {speed}')
            )

    def print_weekly_report(self, report):
        """چاپ گزارش هفتگی"""
        self.stdout.write('=== گزارش هفتگی SEO ===')
        self.stdout.write(f'دوره: {report["period"]}')
        self.stdout.write(f'ترافیک: {report["current_metrics"]["traffic"]} ({report["traffic_change"]:+})')
        self.stdout.write(f'کلمات کلیدی: {report["current_metrics"]["keywords"]} ({report["keywords_change"]:+})')
        self.stdout.write(f'بک‌لینک: {report["current_metrics"]["backlinks"]} ({report["backlinks_change"]:+})')
        self.stdout.write(f'سرعت: {report["current_metrics"]["speed"]} ({report["speed_change"]:+})')
        self.stdout.write(f'اعتبار دامنه: {report["current_metrics"]["authority"]}')

    def print_opportunities(self, opportunities):
        """چاپ فرصت‌ها"""
        self.stdout.write('=== فرصت‌های کلمات کلیدی ===')
        for opp in opportunities[:5]:  # نمایش 5 فرصت اول
            self.stdout.write(f'{opp["keyword"]}: حجم {opp["search_volume"]}, سختی {opp["difficulty"]}')
            self.stdout.write(f'  توصیه: {opp["recommendation"]}')

    def save_report(self, report):
        """ذخیره گزارش"""
        import json
        import os
        from django.conf import settings
        
        reports_dir = os.path.join(settings.BASE_DIR, 'seo_reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        filename = f"weekly_report_{timezone.now().strftime('%Y%m%d')}.json"
        filepath = os.path.join(reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        self.stdout.write(f'گزارش در {filepath} ذخیره شد')
