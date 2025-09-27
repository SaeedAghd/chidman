from django.core.management.base import BaseCommand
from django.utils import timezone
from chidmano.reports import SEOReportGenerator
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'تولید گزارش‌های SEO'

    def add_arguments(self, parser):
        parser.add_argument(
            '--daily',
            action='store_true',
            help='تولید گزارش روزانه'
        )
        parser.add_argument(
            '--weekly',
            action='store_true',
            help='تولید گزارش هفتگی'
        )
        parser.add_argument(
            '--monthly',
            action='store_true',
            help='تولید گزارش ماهانه'
        )
        parser.add_argument(
            '--summary',
            action='store_true',
            help='تولید گزارش خلاصه'
        )
        parser.add_argument(
            '--date',
            type=str,
            help='تاریخ خاص (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['json', 'csv'],
            default='json',
            help='فرمت گزارش'
        )

    def handle(self, *args, **options):
        generator = SEOReportGenerator()
        
        if options['daily']:
            self.generate_daily_report(generator, options)
        elif options['weekly']:
            self.generate_weekly_report(generator, options)
        elif options['monthly']:
            self.generate_monthly_report(generator, options)
        elif options['summary']:
            self.generate_summary_report(generator, options)
        else:
            self.stdout.write(
                self.style.ERROR('لطفاً نوع گزارش را انتخاب کنید: --daily، --weekly، --monthly یا --summary')
            )

    def generate_daily_report(self, generator, options):
        """تولید گزارش روزانه"""
        date = None
        if options['date']:
            try:
                date = datetime.strptime(options['date'], '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('فرمت تاریخ اشتباه است. از YYYY-MM-DD استفاده کنید.')
                )
                return
        
        self.stdout.write(
            self.style.SUCCESS('تولید گزارش روزانه...')
        )
        
        report = generator.generate_daily_report(date)
        if not report:
            self.stdout.write(
                self.style.WARNING('داده‌ای برای تاریخ مشخص شده یافت نشد.')
            )
            return
        
        # ذخیره گزارش
        filepath = generator.save_report(report, options['format'])
        
        self.stdout.write(
            self.style.SUCCESS(f'گزارش روزانه در {filepath} ذخیره شد')
        )
        
        # نمایش خلاصه
        self.print_daily_summary(report)

    def generate_weekly_report(self, generator, options):
        """تولید گزارش هفتگی"""
        start_date = None
        if options['date']:
            try:
                start_date = datetime.strptime(options['date'], '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('فرمت تاریخ اشتباه است. از YYYY-MM-DD استفاده کنید.')
                )
                return
        
        self.stdout.write(
            self.style.SUCCESS('تولید گزارش هفتگی...')
        )
        
        report = generator.generate_weekly_report(start_date)
        if not report:
            self.stdout.write(
                self.style.WARNING('داده‌ای برای دوره مشخص شده یافت نشد.')
            )
            return
        
        # ذخیره گزارش
        filepath = generator.save_report(report, options['format'])
        
        self.stdout.write(
            self.style.SUCCESS(f'گزارش هفتگی در {filepath} ذخیره شد')
        )
        
        # نمایش خلاصه
        self.print_weekly_summary(report)

    def generate_monthly_report(self, generator, options):
        """تولید گزارش ماهانه"""
        year = None
        month = None
        
        if options['date']:
            try:
                date = datetime.strptime(options['date'], '%Y-%m-%d')
                year = date.year
                month = date.month
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('فرمت تاریخ اشتباه است. از YYYY-MM-DD استفاده کنید.')
                )
                return
        
        self.stdout.write(
            self.style.SUCCESS('تولید گزارش ماهانه...')
        )
        
        report = generator.generate_monthly_report(year, month)
        if not report:
            self.stdout.write(
                self.style.WARNING('داده‌ای برای ماه مشخص شده یافت نشد.')
            )
            return
        
        # ذخیره گزارش
        filepath = generator.save_report(report, options['format'])
        
        self.stdout.write(
            self.style.SUCCESS(f'گزارش ماهانه در {filepath} ذخیره شد')
        )
        
        # نمایش خلاصه
        self.print_monthly_summary(report)

    def generate_summary_report(self, generator, options):
        """تولید گزارش خلاصه"""
        self.stdout.write(
            self.style.SUCCESS('تولید گزارش خلاصه...')
        )
        
        report = generator.generate_summary_report()
        
        # ذخیره گزارش
        filepath = generator.save_report(report, options['format'])
        
        self.stdout.write(
            self.style.SUCCESS(f'گزارش خلاصه در {filepath} ذخیره شد')
        )
        
        # نمایش خلاصه
        self.print_summary(report)

    def print_daily_summary(self, report):
        """چاپ خلاصه گزارش روزانه"""
        self.stdout.write('\n=== خلاصه گزارش روزانه ===')
        
        metrics = report['metrics']
        self.stdout.write(f'ترافیک ارگانیک: {metrics["organic_traffic"]:,}')
        self.stdout.write(f'کلمات کلیدی رتبه‌دار: {metrics["keyword_rankings"]}')
        self.stdout.write(f'بک‌لینک‌ها: {metrics["backlinks_count"]}')
        self.stdout.write(f'اعتبار دامنه: {metrics["domain_authority"]}')
        self.stdout.write(f'سرعت صفحه: {metrics["page_speed_score"]}')
        
        if report['recommendations']:
            self.stdout.write('\nتوصیه‌ها:')
            for rec in report['recommendations']:
                self.stdout.write(f'  • {rec}')

    def print_weekly_summary(self, report):
        """چاپ خلاصه گزارش هفتگی"""
        self.stdout.write('\n=== خلاصه گزارش هفتگی ===')
        
        period = report['period']
        self.stdout.write(f'دوره: {period["start_date"]} تا {period["end_date"]}')
        
        avg_metrics = report['average_metrics']
        self.stdout.write(f'میانگین ترافیک: {avg_metrics["avg_traffic"]:.0f}')
        self.stdout.write(f'میانگین کلمات کلیدی: {avg_metrics["avg_keywords"]:.0f}')
        self.stdout.write(f'میانگین بک‌لینک: {avg_metrics["avg_backlinks"]:.0f}')
        self.stdout.write(f'میانگین سرعت: {avg_metrics["avg_speed"]:.0f}')
        
        changes = report['changes']
        self.stdout.write('\nتغییرات:')
        self.stdout.write(f'  ترافیک: {changes["traffic_change"]:+}')
        self.stdout.write(f'  کلمات کلیدی: {changes["keywords_change"]:+}')
        self.stdout.write(f'  بک‌لینک: {changes["backlinks_change"]:+}')
        self.stdout.write(f'  سرعت: {changes["speed_change"]:+}')
        
        if report['recommendations']:
            self.stdout.write('\nتوصیه‌ها:')
            for rec in report['recommendations']:
                self.stdout.write(f'  • {rec}')

    def print_monthly_summary(self, report):
        """چاپ خلاصه گزارش ماهانه"""
        self.stdout.write('\n=== خلاصه گزارش ماهانه ===')
        
        period = report['period']
        self.stdout.write(f'ماه: {period["year"]}/{period["month"]}')
        
        stats = report['statistics']
        self.stdout.write(f'کل ترافیک: {stats["total_traffic"]:,}')
        self.stdout.write(f'میانگین ترافیک: {stats["avg_traffic"]:.0f}')
        self.stdout.write(f'حداکثر ترافیک: {stats["max_traffic"]:,}')
        self.stdout.write(f'حداقل ترافیک: {stats["min_traffic"]:,}')
        
        growth = report['growth_analysis']
        self.stdout.write(f'رشد ترافیک: {growth["traffic_growth"]:+.1f}%')
        self.stdout.write(f'رشد کلمات کلیدی: {growth["keywords_growth"]:+.1f}%')
        
        if report['recommendations']:
            self.stdout.write('\nتوصیه‌ها:')
            for rec in report['recommendations']:
                self.stdout.write(f'  • {rec}')

    def print_summary(self, report):
        """چاپ خلاصه کلی"""
        self.stdout.write('\n=== گزارش خلاصه SEO ===')
        
        self.stdout.write(f'امتیاز کلی: {report["overall_score"]}/100')
        
        if report['daily']:
            daily = report['daily']
            self.stdout.write(f'ترافیک امروز: {daily["metrics"]["organic_traffic"]:,}')
            self.stdout.write(f'سرعت امروز: {daily["metrics"]["page_speed_score"]}')
        
        if report['weekly']:
            weekly = report['weekly']
            self.stdout.write(f'میانگین ترافیک هفته: {weekly["average_metrics"]["avg_traffic"]:.0f}')
        
        if report['monthly']:
            monthly = report['monthly']
            self.stdout.write(f'کل ترافیک ماه: {monthly["statistics"]["total_traffic"]:,}')
        
        # توصیه‌های کلی
        self.stdout.write('\nتوصیه‌های کلی:')
        self.stdout.write('  • بهبود سرعت صفحه')
        self.stdout.write('  • افزایش ترافیک ارگانیک')
        self.stdout.write('  • بهینه‌سازی کلمات کلیدی')
        self.stdout.write('  • تولید محتوای جدید')
