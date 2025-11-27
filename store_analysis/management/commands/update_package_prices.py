"""
Management command to update ServicePackage prices to final values
Usage: python manage.py update_package_prices
"""
from django.core.management.base import BaseCommand
from store_analysis.models import ServicePackage
from decimal import Decimal


class Command(BaseCommand):
    help = 'Update ServicePackage prices to final values: Basic=1M, Professional=5M, Enterprise=15M'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔄 Updating package prices...'))
        
        targets = [
            {
                'package_type': 'basic',
                'name': 'تحلیل اولیه فروشگاه',
                'price': Decimal('1000000'),  # 1,000,000 Toman
                'is_popular': False,
            },
            {
                'package_type': 'professional',
                'name': 'تحلیل کامل فروشگاه',
                'price': Decimal('5000000'),  # 5,000,000 Toman
                'is_popular': True,  # Popular plan
            },
            {
                'package_type': 'enterprise',
                'name': 'تحلیل سازمانی فروشگاه',
                'price': Decimal('15000000'),  # 15,000,000 Toman
                'is_popular': False,
            },
        ]
        
        for t in targets:
            try:
                obj, created = ServicePackage.objects.update_or_create(
                    package_type=t['package_type'],
                    defaults={
                        'name': t['name'],
                        'price': t['price'],
                        'is_popular': t.get('is_popular', False),
                        'is_active': True,
                    }
                )
                status = 'Created' if created else 'Updated'
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ {status} package {t["package_type"]}: {t["name"]} - {t["price"]:,} تومان'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Error updating package {t["package_type"]}: {e}'
                    )
                )
        
        # Verify prices
        self.stdout.write(self.style.SUCCESS('\n📊 Verifying prices:'))
        packages = ServicePackage.objects.filter(is_active=True).order_by('sort_order', 'price')
        for pkg in packages:
            discount_pct = 80
            discounted = float(pkg.price) * (1 - discount_pct / 100.0)
            self.stdout.write(
                f'  {pkg.name} ({pkg.package_type}): '
                f'{pkg.price:,} تومان → {discounted:,.0f} تومان (با {discount_pct}% تخفیف)'
            )
        
        self.stdout.write(self.style.SUCCESS('\n✅ Price update completed!'))

