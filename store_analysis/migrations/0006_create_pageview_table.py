# Generated manually to fix PageView table issue

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency('auth.User'),
        ('store_analysis', '0005_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_url', models.URLField(verbose_name='آدرس صفحه')),
                ('page_title', models.CharField(max_length=200, verbose_name='عنوان صفحه')),
                ('ip_address', models.GenericIPAddressField(verbose_name='آدرس IP')),
                ('user_agent', models.TextField(verbose_name='User Agent')),
                ('referrer', models.URLField(blank=True, null=True, verbose_name='صفحه مرجع')),
                ('session_id', models.CharField(max_length=100, verbose_name='شناسه جلسه')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ بازدید')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'بازدید صفحه',
                'verbose_name_plural': 'بازدیدهای صفحات',
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['page_url'], name='store_analy_page_ur_ab76b5_idx'),
                    models.Index(fields=['created_at'], name='store_analy_created_0b9e65_idx'),
                    models.Index(fields=['user'], name='store_analy_user_id_c92766_idx'),
                    models.Index(fields=['session_id'], name='store_analy_session_49fb1a_idx'),
                ],
            },
        ),
    ]
