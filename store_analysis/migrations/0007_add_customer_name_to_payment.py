# Generated manually to fix missing customer_name column

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0006_add_missing_payment_fields'),
    ]

    operations = [
        # Add 'customer_name' to Payment model
        migrations.AddField(
            model_name='payment',
            name='customer_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='نام مشتری'),
        ),
        # Add 'customer_email' to Payment model
        migrations.AddField(
            model_name='payment',
            name='customer_email',
            field=models.EmailField(blank=True, verbose_name='ایمیل مشتری'),
        ),
        # Add 'customer_phone' to Payment model
        migrations.AddField(
            model_name='payment',
            name='customer_phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='شماره تلفن'),
        ),
        # Add 'callback_data' to Payment model
        migrations.AddField(
            model_name='payment',
            name='callback_data',
            field=models.JSONField(blank=True, null=True, verbose_name='داده‌های بازگشت'),
        ),
        # Add 'completed_at' to Payment model
        migrations.AddField(
            model_name='payment',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='تاریخ تکمیل'),
        ),
        # Add 'notes' to Payment model
        migrations.AddField(
            model_name='payment',
            name='notes',
            field=models.TextField(blank=True, verbose_name='یادداشت‌ها'),
        ),
    ]
