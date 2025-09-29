# Generated manually to fix production database

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0008_aiconsultantservice_pricingplan_transaction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='currency',
            field=models.CharField(default='IRR', max_length=3, verbose_name='واحد پول'),
        ),
    ]
