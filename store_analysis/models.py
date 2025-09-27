"""
Store Analysis Models
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import uuid

class Payment(models.Model):
    """
    Payment model for tracking all payment transactions
    """
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('processing', 'در حال پردازش'),
        ('completed', 'تکمیل شده'),
        ('failed', 'ناموفق'),
        ('cancelled', 'لغو شده'),
        ('refunded', 'برگشت شده'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('ping_payment', 'پی پینگ'),
        ('zarinpal', 'زرین‌پال'),
        ('manual', 'دستی'),
    ]
    
    # Primary fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.CharField(max_length=100, unique=True, verbose_name='شناسه سفارش')
    payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='شناسه پرداخت')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='شناسه تراکنش')
    
    # User and customer info
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    customer_name = models.CharField(max_length=100, blank=True, verbose_name='نام مشتری')
    customer_email = models.EmailField(blank=True, verbose_name='ایمیل مشتری')
    customer_phone = models.CharField(max_length=20, blank=True, verbose_name='شماره تلفن')
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='مبلغ')
    currency = models.CharField(max_length=3, default='IRR', verbose_name='واحد پول')
    description = models.TextField(verbose_name='توضیحات')
    
    # Status and method
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='ping_payment', verbose_name='روش پرداخت')
    
    # Gateway specific fields
    gateway_response = models.JSONField(blank=True, null=True, verbose_name='پاسخ درگاه')
    callback_data = models.JSONField(blank=True, null=True, verbose_name='داده‌های بازگشت')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ تکمیل')
    
    # Additional fields
    is_test = models.BooleanField(default=True, verbose_name='تست')
    notes = models.TextField(blank=True, verbose_name='یادداشت‌ها')
    
    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت‌ها'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['payment_id']),
            models.Index(fields=['transaction_id']),
            models.Index(fields=['status']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Payment {self.order_id} - {self.amount} {self.currency}"
    
    def mark_completed(self):
        """Mark payment as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
    
    def mark_failed(self):
        """Mark payment as failed"""
        self.status = 'failed'
        self.save()
    
    def mark_cancelled(self):
        """Mark payment as cancelled"""
        self.status = 'cancelled'
        self.save()
    
    def is_successful(self):
        """Check if payment is successful"""
        return self.status == 'completed'
    
    def get_status_display_fa(self):
        """Get Persian status display"""
        status_map = {
            'pending': 'در انتظار پرداخت',
            'processing': 'در حال پردازش',
            'completed': 'تکمیل شده',
            'failed': 'ناموفق',
            'cancelled': 'لغو شده',
            'refunded': 'برگشت شده',
        }
        return status_map.get(self.status, self.status)
    
    def get_payment_method_display_fa(self):
        """Get Persian payment method display"""
        method_map = {
            'ping_payment': 'پی پینگ',
            'zarinpal': 'زرین‌پال',
            'manual': 'دستی',
        }
        return method_map.get(self.payment_method, self.payment_method)


class PaymentLog(models.Model):
    """
    Payment log for tracking all payment-related activities
    """
    
    LOG_TYPE_CHOICES = [
        ('payment_created', 'ایجاد پرداخت'),
        ('payment_redirected', 'هدایت به درگاه'),
        ('payment_callback', 'بازگشت از درگاه'),
        ('payment_verified', 'تایید پرداخت'),
        ('payment_failed', 'شکست پرداخت'),
        ('payment_cancelled', 'لغو پرداخت'),
        ('payment_refunded', 'برگشت پرداخت'),
        ('error', 'خطا'),
    ]
    
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='logs', verbose_name='پرداخت')
    log_type = models.CharField(max_length=20, choices=LOG_TYPE_CHOICES, verbose_name='نوع لاگ')
    message = models.TextField(verbose_name='پیام')
    data = models.JSONField(blank=True, null=True, verbose_name='داده‌ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'لاگ پرداخت'
        verbose_name_plural = 'لاگ‌های پرداخت'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment']),
            models.Index(fields=['log_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_log_type_display()} - {self.payment.order_id}"


class ServicePackage(models.Model):
    """
    Service packages for store analysis
    """
    
    PACKAGE_TYPE_CHOICES = [
        ('basic', 'پایه'),
        ('professional', 'حرفه‌ای'),
        ('enterprise', 'سازمانی'),
        ('custom', 'سفارشی'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='نام بسته')
    description = models.TextField(verbose_name='توضیحات')
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPE_CHOICES, verbose_name='نوع بسته')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت')
    currency = models.CharField(max_length=3, default='IRR', verbose_name='واحد پول')
    
    # Features
    features = models.JSONField(default=list, verbose_name='ویژگی‌ها')
    max_analyses = models.PositiveIntegerField(default=1, verbose_name='حداکثر تحلیل')
    validity_days = models.PositiveIntegerField(default=30, verbose_name='اعتبار (روز)')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_popular = models.BooleanField(default=False, verbose_name='محبوب')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'بسته خدمات'
        verbose_name_plural = 'بسته‌های خدمات'
        ordering = ['sort_order', 'price']
        indexes = [
            models.Index(fields=['package_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['price']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.price} {self.currency}"


class UserSubscription(models.Model):
    """
    User subscription to service packages
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='بسته')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name='پرداخت')
    
    # Subscription details
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    # Usage tracking
    analyses_used = models.PositiveIntegerField(default=0, verbose_name='تحلیل‌های استفاده شده')
    max_analyses = models.PositiveIntegerField(verbose_name='حداکثر تحلیل')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'اشتراک کاربر'
        verbose_name_plural = 'اشتراک‌های کاربران'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['package']),
            models.Index(fields=['is_active']),
            models.Index(fields=['end_date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.package.name}"
    
    def is_expired(self):
        """Check if subscription is expired"""
        return timezone.now() > self.end_date
    
    def can_use_analysis(self):
        """Check if user can use analysis"""
        return self.is_active and not self.is_expired() and self.analyses_used < self.max_analyses
    
    def use_analysis(self):
        """Use one analysis"""
        if self.can_use_analysis():
            self.analyses_used += 1
            self.save()
            return True
        return False