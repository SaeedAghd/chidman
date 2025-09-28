# Generated manually to fix SiteStats table issue

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0006_create_pageview_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True, verbose_name='تاریخ')),
                ('total_views', models.PositiveIntegerField(default=0, verbose_name='کل بازدیدها')),
                ('unique_visitors', models.PositiveIntegerField(default=0, verbose_name='بازدیدکنندگان منحصر به فرد')),
                ('new_users', models.PositiveIntegerField(default=0, verbose_name='کاربران جدید')),
                ('page_views', models.PositiveIntegerField(default=0, verbose_name='بازدید صفحات')),
                ('avg_session_duration', models.DurationField(blank=True, null=True, verbose_name='میانگین مدت جلسه')),
                ('bounce_rate', models.FloatField(default=0, verbose_name='نرخ پرش')),
            ],
            options={
                'verbose_name': 'آمار سایت',
                'verbose_name_plural': 'آمارهای سایت',
                'ordering': ['-date'],
            },
        ),
    ]
