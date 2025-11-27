from django.db import migrations
from decimal import Decimal


def update_package_prices_final(apps, schema_editor):
    """
    Update package prices to final values:
    - Basic: 1,000,000 Toman (10,000,000 Rials) - Free plan
    - Professional: 5,000,000 Toman (50,000,000 Rials) - Popular plan
    - Enterprise: 15,000,000 Toman (150,000,000 Rials)
    """
    ServicePackage = apps.get_model('store_analysis', 'ServicePackage')
    
    targets = [
        {
            'package_type': 'basic',
            'name': 'تحلیل اولیه فروشگاه',
            'price': Decimal('1000000'),  # 1,000,000 Toman = 10,000,000 Rials
            'currency': 'IRR',
            'max_analyses': 1,
            'validity_days': 30,
            'is_active': True,
            'is_popular': False,
            'sort_order': 0,
            'description': 'تحلیل پایه و اولیه فروشگاه شما - رایگان'
        },
        {
            'package_type': 'professional',
            'name': 'تحلیل کامل فروشگاه',
            'price': Decimal('5000000'),  # 5,000,000 Toman = 50,000,000 Rials
            'currency': 'IRR',
            'max_analyses': 3,
            'validity_days': 60,
            'is_active': True,
            'is_popular': True,  # Popular plan
            'sort_order': 1,
            'description': 'تحلیل حرفه‌ای و کامل فروشگاه شما - پلن محبوب'
        },
        {
            'package_type': 'enterprise',
            'name': 'تحلیل سازمانی فروشگاه',
            'price': Decimal('15000000'),  # 15,000,000 Toman = 150,000,000 Rials
            'currency': 'IRR',
            'max_analyses': 10,
            'validity_days': 90,
            'is_active': True,
            'is_popular': False,
            'sort_order': 2,
            'description': 'تحلیل سازمانی و پیشرفته فروشگاه شما'
        },
    ]
    
    for t in targets:
        obj, created = ServicePackage.objects.update_or_create(
            package_type=t['package_type'],
            defaults={
                'name': t['name'],
                'price': t['price'],
                'currency': t['currency'],
                'max_analyses': t['max_analyses'],
                'validity_days': t['validity_days'],
                'is_active': t['is_active'],
                'is_popular': t.get('is_popular', False),
                'sort_order': t['sort_order'],
                'description': t.get('description', ''),
                'features': [],
            }
        )
        print(f"✅ Updated package {t['package_type']}: {t['name']} - {t['price']:,} {t['currency']}")


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0122_update_package_prices_real'),
    ]

    operations = [
        migrations.RunPython(update_package_prices_final, migrations.RunPython.noop),
    ]

