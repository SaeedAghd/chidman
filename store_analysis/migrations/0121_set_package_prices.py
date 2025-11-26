from django.db import migrations


def set_package_prices(apps, schema_editor):
    ServicePackage = apps.get_model('store_analysis', 'ServicePackage')
    # Define target packages by package_type (basic, professional, enterprise)
    targets = [
        {'package_type': 'professional', 'name': 'تحلیل کامل فروشگاه', 'price': 2000000, 'currency': 'IRR', 'max_analyses': 3, 'validity_days': 60, 'is_active': True, 'sort_order': 1},
        {'package_type': 'basic', 'name': 'تحلیل اولیه فروشگاه', 'price': 500000, 'currency': 'IRR', 'max_analyses': 1, 'validity_days': 30, 'is_active': True, 'sort_order': 0},
        {'package_type': 'enterprise', 'name': 'تحلیل سازمانی فروشگاه', 'price': 5000000, 'currency': 'IRR', 'max_analyses': 10, 'validity_days': 90, 'is_active': True, 'sort_order': 2},
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
                'sort_order': t['sort_order'],
                'features': [],
            }
        )


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0120_payment_client_ip_payment_client_location'),
    ]

    operations = [
        migrations.RunPython(set_package_prices, migrations.RunPython.noop),
    ]


