from django.core.management.base import BaseCommand
from django.utils import timezone
from chidmano.alerts import SEOAlertSystem, SEOHealthChecker

class Command(BaseCommand):
    help = 'بررسی و ارسال هشدارهای SEO'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check',
            action='store_true',
            help='بررسی هشدارها'
        )
        parser.add_argument(
            '--send',
            action='store_true',
            help='ارسال هشدارها'
        )
        parser.add_argument(
            '--health',
            action='store_true',
            help='بررسی سلامت SEO'
        )

    def handle(self, *args, **options):
        if options['check']:
            self.check_alerts()
        elif options['send']:
            self.send_alerts()
        elif options['health']:
            self.check_health()
        else:
            self.stdout.write(
                self.style.ERROR('لطفاً یکی از گزینه‌های --check، --send یا --health را انتخاب کنید')
            )

    def check_alerts(self):
        """بررسی هشدارها"""
        alert_system = SEOAlertSystem()
        
        self.stdout.write(
            self.style.SUCCESS('بررسی هشدارهای SEO...')
        )
        
        alerts = alert_system.check_all_alerts()
        
        if not alerts:
            self.stdout.write(
                self.style.SUCCESS('هیچ هشداری یافت نشد!')
            )
            return
        
        self.stdout.write(
            self.style.WARNING(f'{len(alerts)} هشدار یافت شد:')
        )
        
        for alert in alerts:
            severity_color = {
                'high': self.style.ERROR,
                'medium': self.style.WARNING,
                'low': self.style.SUCCESS
            }
            
            color = severity_color.get(alert['severity'], self.style.NOTICE)
            self.stdout.write(
                color(f'  {alert["severity"].upper()}: {alert["message"]}')
            )

    def send_alerts(self):
        """ارسال هشدارها"""
        alert_system = SEOAlertSystem()
        
        self.stdout.write(
            self.style.SUCCESS('ارسال هشدارهای SEO...')
        )
        
        result = alert_system.process_alerts()
        
        if result['processed'] == 0:
            self.stdout.write(
                self.style.SUCCESS('هیچ هشداری برای ارسال وجود ندارد!')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(f'{result["sent"]}/{result["processed"]} هشدار ارسال شد')
        )
        
        if result['sent'] < result['processed']:
            self.stdout.write(
                self.style.WARNING('برخی هشدارها ارسال نشدند. لطفاً تنظیمات ایمیل را بررسی کنید.')
            )

    def check_health(self):
        """بررسی سلامت SEO"""
        health_checker = SEOHealthChecker()
        
        self.stdout.write(
            self.style.SUCCESS('بررسی سلامت SEO...')
        )
        
        results = health_checker.run_health_check()
        health_score = health_checker.get_health_score(results)
        
        self.stdout.write('=== گزارش سلامت SEO ===')
        self.stdout.write(f'امتیاز کلی: {health_score["score"]}/100')
        self.stdout.write(f'بررسی‌های موفق: {health_score["good"]}/{health_score["total_checks"]}')
        
        if health_score['warning'] > 0:
            self.stdout.write(
                self.style.WARNING(f'هشدارها: {health_score["warning"]}')
            )
        
        if health_score['error'] > 0:
            self.stdout.write(
                self.style.ERROR(f'خطاها: {health_score["error"]}')
            )
        
        self.stdout.write('\nجزئیات بررسی‌ها:')
        for check_name, result in results.items():
            status_color = {
                'good': self.style.SUCCESS,
                'warning': self.style.WARNING,
                'error': self.style.ERROR
            }
            
            color = status_color.get(result['status'], self.style.NOTICE)
            self.stdout.write(
                color(f'  {check_name}: {result["message"]}')
            )
        
        # توصیه‌ها
        self.stdout.write('\nتوصیه‌ها:')
        if health_score['score'] < 80:
            self.stdout.write('  • بهبود سرعت صفحه')
            self.stdout.write('  • بهینه‌سازی تصاویر')
            self.stdout.write('  • بررسی لینک‌های داخلی')
        
        if health_score['error'] > 0:
            self.stdout.write('  • رفع خطاهای شناسایی شده')
            self.stdout.write('  • بررسی تنظیمات SSL')
        
        if health_score['warning'] > 0:
            self.stdout.write('  • بهبود هشدارهای شناسایی شده')
            self.stdout.write('  • بهینه‌سازی محتوا')
