from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0029_wallet_transaction'),  # اگر آخرین مایگریشن شما متفاوت است، اصلاح کن
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='wallettransaction',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='faqservice',
            name='sort_order',
            field=models.IntegerField(default=0),
        ),
    ]