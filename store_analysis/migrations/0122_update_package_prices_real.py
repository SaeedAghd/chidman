from django.db import migrations


def update_package_prices_real(apps, schema_editor):
    """Update package prices to real values based on user requirements"""
    ServicePackage = apps.get_model('store_analysis', 'ServicePackage')
    
    # Real prices based on image: 1,500,000 original -> 10,000 with 80% discount
    # So original should be 50,000 to get 10,000 with 80% discount
    # But user wants 1,500,000 original, so discount is actually 99.33%
    # However, based on user's previous request: professional=2M, basic=500K, enterprise=5M
    # And from image: 1,500,000 original -> 10,000 discounted
    
    # Based on image showing 1,500,000 -> 10,000, this seems to be professional package
    # But 80% of 1,500,000 = 300,000, not 10,000
    # So either:
    # 1. Original is 50,000 (80% discount = 10,000) - but image shows 1,500,000
    # 2. Discount is 99.33% (1,500,000 -> 10,000)
    
    # Based on user's previous messages and image, I'll set:
    # - basic: 500,000 (80% discount = 100,000)
    # - professional: 1,500,000 (80% discount = 300,000) - but image shows 10,000
    # - enterprise: 5,000,000 (80% discount = 1,000,000)
    
    # Actually, looking at the image more carefully:
    # The image shows 1,500,000 original -> 10,000 discounted with 80% discount
    # This doesn't match mathematically. Let me use the values from user's previous request:
    # professional (popular): 2,000,000 -> 400,000 (80% discount)
    # basic: 500,000 -> 100,000 (80% discount)
    # enterprise: 5,000,000 -> 1,000,000 (80% discount)
    
    # But the image clearly shows 1,500,000 -> 10,000
    # So I'll update professional to 1,500,000 and let the discount calculation handle it
    # Or maybe the user wants a special promotional price
    
    targets = [
        {
            'package_type': 'basic',
            'name': 'تحلیل اولیه فروشگاه',
            'price': 500000,
            'currency': 'IRR',
            'max_analyses': 1,
            'validity_days': 30,
            'is_active': True,
            'sort_order': 0,
            'description': 'تحلیل پایه و اولیه فروشگاه شما'
        },
        {
            'package_type': 'professional',
            'name': 'تحلیل کامل فروشگاه',
            'price': 1500000,  # From image: 1,500,000 original
            'currency': 'IRR',
            'max_analyses': 3,
            'validity_days': 60,
            'is_active': True,
            'is_popular': True,
            'sort_order': 1,
            'description': 'تحلیل حرفه‌ای و کامل فروشگاه شما'
        },
        {
            'package_type': 'enterprise',
            'name': 'تحلیل سازمانی فروشگاه',
            'price': 5000000,
            'currency': 'IRR',
            'max_analyses': 10,
            'validity_days': 90,
            'is_active': True,
            'sort_order': 2,
            'description': 'تحلیل سازمانی و پیشرفته فروشگاه شما'
        },
    ]
    
    for t in targets:
        obj, created = ServicePackage.objects.update_or_create(
            package_type=t['package_type'],
            defaults={
                'name': t['name'],
                'description': t.get('description', ''),
                'price': t['price'],
                'currency': t['currency'],
                'max_analyses': t['max_analyses'],
                'validity_days': t['validity_days'],
                'is_active': t['is_active'],
                'is_popular': t.get('is_popular', False),
                'sort_order': t['sort_order'],
            }
        )
        action = 'Created' if created else 'Updated'
        print(f"{action} package {t['package_type']}: {t['name']} - {t['price']} {t['currency']}")


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0121_set_package_prices'),
    ]

    operations = [
        migrations.RunPython(update_package_prices_real, migrations.RunPython.noop),
    ]

