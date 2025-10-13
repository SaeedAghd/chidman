"""
Store Analysis Models
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import uuid
from datetime import timedelta

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
    
    # Primary key: use UUID to match current database schema
    id = models.AutoField(primary_key=True)
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
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    
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
    package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, blank=True, null=True, verbose_name='بسته')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True, verbose_name='پرداخت')
    
    # Subscription details
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    # Usage tracking
    analyses_used = models.PositiveIntegerField(default=0, verbose_name='تحلیل‌های استفاده شده')
    max_analyses = models.PositiveIntegerField(default=10, verbose_name='حداکثر تحلیل')
    
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


class StoreAnalysis(models.Model):
    """
    Store analysis model for tracking store analysis requests
    """
    
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('processing', 'در حال پردازش'),
        ('completed', 'تکمیل شده'),
        ('failed', 'ناموفق'),
        ('cancelled', 'لغو شده'),
    ]
    
    ANALYSIS_TYPE_CHOICES = [
        ('basic', 'پایه'),
        ('professional', 'حرفه‌ای'),
        ('advanced', 'پیشرفته'),
        ('custom', 'سفارشی'),
    ]
    
    # Primary fields
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    
    # Store information (match production DB schema)
    store_name = models.CharField(max_length=200, verbose_name='نام فروشگاه')
    store_url = models.URLField(blank=True, null=True, verbose_name='آدرس فروشگاه')
    
    # Analysis details
    analysis_type = models.CharField(max_length=20, choices=ANALYSIS_TYPE_CHOICES, default='basic', verbose_name='نوع تحلیل')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    priority = models.CharField(max_length=10, default='medium', verbose_name='اولویت')
    
    # Analysis data and order reference
    analysis_data = models.JSONField(default=dict, blank=True, verbose_name='داده‌های تحلیل')
    # AI results (structured)
    results = models.JSONField(default=dict, blank=True, null=True, verbose_name='نتایج هوش مصنوعی')
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='سفارش')
    
    # Results
    preliminary_analysis = models.TextField(blank=True, verbose_name='تحلیل اولیه')
    ai_insights = models.TextField(blank=True, verbose_name='بینش‌های هوش مصنوعی')
    recommendations = models.TextField(blank=True, verbose_name='توصیه‌ها')
    
    # Files
    store_images = models.JSONField(default=list, verbose_name='تصاویر فروشگاه')
    analysis_files = models.JSONField(default=list, verbose_name='فایل‌های تحلیل')
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='قیمت')
    currency = models.CharField(max_length=3, default='IRR', verbose_name='واحد پول')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ تکمیل')
    
    class Meta:
        verbose_name = 'تحلیل فروشگاه'
        verbose_name_plural = 'تحلیل‌های فروشگاه'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['analysis_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.store_name} - {self.get_status_display()}"
    
    def mark_completed(self):
        """Mark analysis as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
    
    def mark_failed(self):
        """Mark analysis as failed"""
        self.status = 'failed'
        self.save()
    
    def get_analysis_data(self):
        """Get analysis data for PDF generation"""
        return self.analysis_data or {}
    
    @property
    def has_results(self):
        """Check if analysis has AI results"""
        return bool(self.results and isinstance(self.results, dict))
    
    def get_progress(self):
        """Get analysis progress percentage"""
        if self.status == 'completed':
            return 100
        elif self.status == 'processing':
            return 75
        elif self.status == 'pending':
            return 25
        else:
            return 0


class Wallet(models.Model):
    """
    User wallet for managing credits and transactions
    """
    
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'واریز'),
        ('withdrawal', 'برداشت'),
        ('payment', 'پرداخت'),
        ('refund', 'برگشت'),
        ('bonus', 'پاداش'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='موجودی')
    currency = models.CharField(max_length=3, default='IRR', verbose_name='واحد پول')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف‌های پول'
        indexes = [
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.balance} {self.currency}"
    
    def add_balance(self, amount, transaction_type='deposit', description=''):
        """Add balance to wallet"""
        self.balance += amount
        self.save()
        
        # Create transaction record
        WalletTransaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            balance_after=self.balance
        )
    
    def deduct_balance(self, amount, transaction_type='payment', description=''):
        """Deduct balance from wallet"""
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            
            # Create transaction record
            WalletTransaction.objects.create(
                wallet=self,
                amount=-amount,
                transaction_type=transaction_type,
                description=description,
                balance_after=self.balance
            )
            return True
        return False


class WalletTransaction(models.Model):
    """
    Wallet transaction history
    """
    
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'واریز'),
        ('withdrawal', 'برداشت'),
        ('payment', 'پرداخت'),
        ('refund', 'برگشت'),
        ('bonus', 'پاداش'),
    ]
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions', verbose_name='کیف پول')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='مبلغ')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES, verbose_name='نوع تراکنش')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    balance_after = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='موجودی پس از تراکنش')
    
    # Reference to related objects
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='پرداخت')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'تراکنش کیف پول'
        verbose_name_plural = 'تراکنش‌های کیف پول'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['wallet']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.wallet.user.username} - {self.amount} {self.transaction_type}"


class SupportTicket(models.Model):
    """
    Support ticket model for customer support
    """
    
    STATUS_CHOICES = [
        ('open', 'باز'),
        ('in_progress', 'در حال بررسی'),
        ('resolved', 'حل شده'),
        ('closed', 'بسته'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'بالا'),
        ('urgent', 'فوری'),
    ]
    
    CATEGORY_CHOICES = [
        ('technical', 'فنی'),
        ('billing', 'صورت‌حساب'),
        ('general', 'عمومی'),
        ('feature_request', 'درخواست ویژگی'),
        ('bug_report', 'گزارش باگ'),
    ]
    
    # Primary fields - Use BigAutoField for production compatibility
    id = models.BigAutoField(primary_key=True)
    ticket_id = models.CharField(max_length=50, unique=True, default='TEMP-TICKET', verbose_name='شناسه تیکت')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    
    # Ticket details
    subject = models.CharField(max_length=200, verbose_name='موضوع')
    description = models.TextField(verbose_name='توضیحات')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='دسته‌بندی')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name='اولویت')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name='وضعیت')
    
    # Attachments and tags
    attachments = models.JSONField(default=list, verbose_name='پیوست‌ها')
    tags = models.JSONField(default=list, verbose_name='برچسب‌ها')
    
    # Assignment
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, 
                                   related_name='assigned_tickets', verbose_name='واگذار شده به')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    resolved_at = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ حل')
    
    class Meta:
        verbose_name = 'تیکت پشتیبانی'
        verbose_name_plural = 'تیکت‌های پشتیبانی'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['priority']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"#{self.id} - {self.subject}"
    
    def mark_resolved(self):
        """Mark ticket as resolved"""
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.save()
    
    def close_ticket(self):
        """Close ticket"""
        self.status = 'closed'
        self.save()


class FAQService(models.Model):
    """
    FAQ service model for frequently asked questions
    """
    
    CATEGORY_CHOICES = [
        ('general', 'عمومی'),
        ('technical', 'فنی'),
        ('billing', 'صورت‌حساب'),
        ('features', 'ویژگی‌ها'),
        ('troubleshooting', 'عیب‌یابی'),
    ]
    
    question = models.CharField(max_length=500, verbose_name='سوال')
    answer = models.TextField(verbose_name='پاسخ')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='دسته‌بندی')
    
    # SEO and display (keywords column not present in current DB)
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول'
        ordering = ['sort_order', 'category', 'question']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_featured']),
        ]
    
    def __str__(self):
        return self.question


class Order(models.Model):
    """
    Order model for tracking store analysis orders
    """
    
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('completed', 'تکمیل شده'),
        ('cancelled', 'لغو شده'),
        ('refunded', 'برگشت شده'),
    ]
    
    # Primary fields
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    
    # Order details
    order_number = models.CharField(max_length=50, unique=True, verbose_name='شماره سفارش')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    # Payment meta (present in production DB)
    payment_method = models.CharField(max_length=50, default='online', verbose_name='روش پرداخت')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='شناسه تراکنش')
    
    # Pricing
    original_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='مبلغ اصلی')
    base_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='مبلغ پایه')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='مبلغ تخفیف')
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='مبلغ نهایی')
    currency = models.CharField(max_length=3, default='IRR', verbose_name='واحد پول')
    
    # Plan reference
    plan = models.ForeignKey('ServicePackage', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='پکیج')
    
    # Payment reference
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='پرداخت')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['order_number']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Order {self.order_number} - {self.final_amount} {self.currency}"
    
    def save(self, *args, **kwargs):
        # Ensure payment_method always has a safe value to avoid NULL inserts
        if not getattr(self, 'payment_method', None):
            self.payment_method = 'online'
        # Ensure transaction_id is present to satisfy NOT NULL in production DB
        if not getattr(self, 'transaction_id', None):
            # Generate a placeholder transaction id; real id will be set after gateway
            try:
                import uuid as _uuid
                self.transaction_id = f"PENDING_{_uuid.uuid4().hex[:12].upper()}"
            except Exception:
                self.transaction_id = "PENDING_AUTO"
        super().save(*args, **kwargs)

    def mark_paid(self):
        """Mark order as paid"""
        self.status = 'paid'
        self.save()
    
    def mark_completed(self):
        """Mark order as completed"""
        self.status = 'completed'
        self.save()


class DiscountNotification(models.Model):
    """مدل اطلاعیه تخفیف"""
    title = models.CharField(max_length=200, verbose_name='عنوان')
    message = models.TextField(verbose_name='پیام')
    discount_percentage = models.IntegerField(default=0, verbose_name='درصد تخفیف')
    discount_type = models.CharField(max_length=50, choices=[
        ('opening', 'تخفیف افتتاحیه'),
        ('seasonal', 'تخفیف فصلی'),
        ('nowruz', 'تخفیف نوروزی'),
        ('special', 'تخفیف ویژه'),
    ], default='opening', verbose_name='نوع تخفیف')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'اطلاعیه تخفیف'
        verbose_name_plural = 'اطلاعیه‌های تخفیف'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.discount_percentage}%"
    
    @classmethod
    def get_active_notifications(cls):
        """دریافت اطلاعیه‌های فعال"""
        from django.utils import timezone
        now = timezone.now()
        return cls.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).order_by('-discount_percentage')
    
    @classmethod
    def get_current_discount(cls):
        """دریافت تخفیف فعلی"""
        notifications = cls.get_active_notifications()
        if notifications.exists():
            return notifications.first()
        return None

class SystemSettings(models.Model):
    """مدل تنظیمات سیستم"""
    key = models.CharField(max_length=100, unique=True, verbose_name='کلید')
    value = models.TextField(verbose_name='مقدار')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'تنظیمات سیستم'
        verbose_name_plural = 'تنظیمات سیستم'
        ordering = ['key']
    
    def __str__(self):
        return f"{self.key}: {self.value[:50]}..."
    
    @classmethod
    def get_setting(cls, key, default=None):
        """دریافت تنظیمات"""
        try:
            setting = cls.objects.get(key=key)
            return setting.value
        except cls.DoesNotExist:
            return default
    
    @classmethod
    def set_setting(cls, key, value, description=''):
        """تنظیم مقدار"""
        setting, created = cls.objects.get_or_create(
            key=key,
            defaults={'value': value, 'description': description}
        )
        if not created:
            setting.value = value
            setting.description = description
            setting.save()
        return setting


class PageView(models.Model):
    """مدل آمار بازدید صفحات"""
    page_url = models.URLField(verbose_name='آدرس صفحه')
    page_title = models.CharField(max_length=200, verbose_name='عنوان صفحه')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر')
    ip_address = models.GenericIPAddressField(verbose_name='آدرس IP')
    user_agent = models.TextField(verbose_name='User Agent')
    referrer = models.URLField(blank=True, null=True, verbose_name='صفحه مرجع')
    session_id = models.CharField(max_length=100, verbose_name='شناسه جلسه')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ بازدید')
    
    class Meta:
        verbose_name = 'بازدید صفحه'
        verbose_name_plural = 'بازدیدهای صفحات'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['page_url']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user']),
            models.Index(fields=['session_id']),
        ]
    
    def __str__(self):
        return f"{self.page_title} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class SiteStats(models.Model):
    """مدل آمار کلی سایت"""
    date = models.DateField(unique=True, verbose_name='تاریخ')
    total_views = models.PositiveIntegerField(default=0, verbose_name='کل بازدیدها')
    unique_visitors = models.PositiveIntegerField(default=0, verbose_name='بازدیدکنندگان منحصر به فرد')
    new_users = models.PositiveIntegerField(default=0, verbose_name='کاربران جدید')
    page_views = models.PositiveIntegerField(default=0, verbose_name='بازدید صفحات')
    avg_session_duration = models.DurationField(null=True, blank=True, verbose_name='میانگین مدت جلسه')
    bounce_rate = models.FloatField(default=0, verbose_name='نرخ پرش')
    
    class Meta:
        verbose_name = 'آمار سایت'
        verbose_name_plural = 'آمارهای سایت'
        ordering = ['-date']
    
    def __str__(self):
        return f"آمار {self.date} - {self.total_views} بازدید"


class Phonebook(models.Model):
    """دفتر تلفن فروشگاه‌ها"""
    
    # اطلاعات فروشگاه
    store_name = models.CharField(max_length=200, verbose_name='نام فروشگاه')
    store_type = models.CharField(max_length=50, blank=True, verbose_name='نوع فروشگاه')
    
    # اطلاعات تماس
    contact_name = models.CharField(max_length=200, verbose_name='نام و نام خانوادگی')
    contact_email = models.EmailField(verbose_name='ایمیل')
    contact_phone = models.CharField(max_length=20, verbose_name='شماره تماس')
    
    # اطلاعات اضافی
    additional_notes = models.TextField(blank=True, verbose_name='توضیحات اضافی')
    
    # اطلاعات سیستم
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    analysis = models.ForeignKey('StoreAnalysis', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='تحلیل مربوطه')
    
    # زمان‌ها
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'دفتر تلفن'
        verbose_name_plural = 'دفتر تلفن‌ها'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['store_name']),
            models.Index(fields=['contact_email']),
            models.Index(fields=['contact_phone']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.store_name} - {self.contact_name} ({self.contact_phone})"


class DiscountCode(models.Model):
    
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'درصدی'),
        ('fixed', 'مبلغ ثابت'),
    ]
    
    code = models.CharField(max_length=50, unique=True, verbose_name='کد تخفیف')
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='percentage', verbose_name='نوع تخفیف')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='مقدار تخفیف')
    discount_percentage = models.PositiveIntegerField(default=0, verbose_name='درصد تخفیف')
    
    # محدودیت‌ها
    max_uses = models.PositiveIntegerField(default=100, verbose_name='حداکثر استفاده')
    used_count = models.PositiveIntegerField(default=0, verbose_name='تعداد استفاده شده')
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='حداقل مبلغ سفارش')
    
    # تاریخ‌ها
    valid_from = models.DateTimeField(default=timezone.now, verbose_name='اعتبار از')
    valid_until = models.DateTimeField(verbose_name='اعتبار تا')
    
    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    # توضیحات
    description = models.TextField(blank=True, verbose_name='توضیحات')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
            models.Index(fields=['valid_from']),
            models.Index(fields=['valid_until']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"
    
    def is_valid(self):
        """بررسی اعتبار کد تخفیف"""
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            self.used_count < self.max_uses
        )
    
    def use_discount(self):
        """استفاده از کد تخفیف"""
        if self.is_valid():
            self.used_count += 1
            self.save()
            return True
        return False


class StoreBasicInfo(models.Model):
    """مدل اطلاعات پایه فروشگاه"""
    
    STORE_TYPE_CHOICES = [
        ('supermarket', 'سوپرمارکت'),
        ('convenience_store', 'فروشگاه کوچک'),
        ('department_store', 'فروشگاه بزرگ'),
        ('specialty_store', 'فروشگاه تخصصی'),
        ('pharmacy', 'داروخانه'),
        ('bookstore', 'کتابفروشی'),
        ('electronics', 'لوازم الکترونیکی'),
        ('clothing', 'پوشاک'),
        ('food', 'مواد غذایی'),
        ('other', 'سایر'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='کاربر')
    store_name = models.CharField(max_length=200, verbose_name='نام فروشگاه')
    store_type = models.CharField(max_length=20, choices=STORE_TYPE_CHOICES, verbose_name='نوع فروشگاه')
    store_location = models.CharField(max_length=300, verbose_name='موقعیت فروشگاه')
    area = models.CharField(max_length=100, verbose_name='منطقه')
    city = models.CharField(max_length=100, verbose_name='شهر')
    
    # اطلاعات تماس
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    
    # اطلاعات فیزیکی
    store_size = models.PositiveIntegerField(verbose_name='مساحت فروشگاه (متر مربع)')
    employee_count = models.PositiveIntegerField(default=1, verbose_name='تعداد کارکنان')
    
    # اطلاعات کسب‌وکار
    opening_hours = models.CharField(max_length=200, blank=True, verbose_name='ساعات کاری')
    established_year = models.PositiveIntegerField(null=True, blank=True, verbose_name='سال تاسیس')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'اطلاعات پایه فروشگاه'
        verbose_name_plural = 'اطلاعات پایه فروشگاه‌ها'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['store_type']),
            models.Index(fields=['city']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.store_name} - {self.get_store_type_display()}"


class StoreAnalysisResult(models.Model):
    """مدل نتایج تحلیل فروشگاه"""
    
    store_analysis = models.OneToOneField(StoreAnalysis, on_delete=models.CASCADE, verbose_name='تحلیل فروشگاه')
    
    # نتایج کلی
    overall_score = models.FloatField(default=0, verbose_name='امتیاز کلی')
    layout_score = models.FloatField(default=0, verbose_name='امتیاز چیدمان')
    lighting_score = models.FloatField(default=0, verbose_name='امتیاز نورپردازی')
    color_score = models.FloatField(default=0, verbose_name='امتیاز رنگ‌بندی')
    signage_score = models.FloatField(default=0, verbose_name='امتیاز تابلوها')

    # فیلدهای مورد استفاده در views (هم‌ترازسازی با کد)
    traffic_score = models.FloatField(default=0, verbose_name='امتیاز ترافیک')
    design_score = models.FloatField(default=0, verbose_name='امتیاز طراحی')
    sales_score = models.FloatField(default=0, verbose_name='امتیاز فروش')
    
    # توصیه‌ها
    layout_recommendations = models.TextField(blank=True, verbose_name='توصیه‌های چیدمان')
    lighting_recommendations = models.TextField(blank=True, verbose_name='توصیه‌های نورپردازی')
    color_recommendations = models.TextField(blank=True, verbose_name='توصیه‌های رنگ‌بندی')
    signage_recommendations = models.TextField(blank=True, verbose_name='توصیه‌های تابلوها')

    # تحلیل‌های متنی مورد استفاده در views
    overall_analysis = models.TextField(blank=True, verbose_name='تحلیل کلی')
    layout_analysis = models.TextField(blank=True, verbose_name='تحلیل چیدمان (متن)')
    traffic_analysis = models.TextField(blank=True, verbose_name='تحلیل ترافیک (متن)')
    design_analysis = models.TextField(blank=True, verbose_name='تحلیل طراحی (متن)')
    sales_analysis = models.TextField(blank=True, verbose_name='تحلیل فروش (متن)')
    
    # فایل‌های تولید شده
    report_file = models.FileField(upload_to='reports/', blank=True, null=True, verbose_name='فایل گزارش')
    images_analysis = models.JSONField(default=list, verbose_name='تحلیل تصاویر')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'نتیجه تحلیل فروشگاه'
        verbose_name_plural = 'نتایج تحلیل فروشگاه‌ها'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"نتیجه تحلیل {self.store_analysis.store_name}"


class TicketMessage(models.Model):
    """مدل پیام‌های تیکت پشتیبانی"""
    
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages', verbose_name='تیکت')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='فرستنده')
    content = models.TextField(verbose_name='محتوای پیام')
    
    # پیوست‌ها
    attachments = models.JSONField(default=list, verbose_name='پیوست‌ها')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'پیام تیکت'
        verbose_name_plural = 'پیام‌های تیکت'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['ticket']),
            models.Index(fields=['sender']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"پیام از {self.sender.username} - {self.ticket.ticket_id}"

    @property
    def is_admin_reply(self) -> bool:
        """بر اساس نقش فرستنده تشخیص می‌دهد پیام ادمین است یا خیر (بدون نیاز به ستون DB)."""
        try:
            return bool(self.sender and getattr(self.sender, 'is_staff', False))
        except Exception:
            return False


class UserProfile(models.Model):
    """مدل پروفایل کاربر"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    
    # اطلاعات شخصی
    phone = models.CharField(max_length=11, verbose_name='شماره موبایل', help_text='شماره موبایل برای پرداخت و ارسال پیامک الزامی است')
    address = models.TextField(blank=True, verbose_name='آدرس')
    birth_date = models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')
    
    # تنظیمات حساب
    legal_agreement_accepted = models.BooleanField(default=False, verbose_name='تایید تعهدنامه')
    legal_agreement_date = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ تایید تعهدنامه')
    newsletter_subscription = models.BooleanField(default=True, verbose_name='عضویت در خبرنامه')
    
    # تنظیمات اعلان‌ها
    email_notifications = models.BooleanField(default=True, verbose_name='اعلان‌های ایمیل')
    sms_notifications = models.BooleanField(default=False, verbose_name='اعلان‌های پیامک')
    
    # اطلاعات اضافی
    bio = models.TextField(blank=True, verbose_name='درباره من')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='تصویر پروفایل')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل‌های کاربران'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['legal_agreement_accepted']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"پروفایل {self.user.username}"
    
    def accept_legal_agreement(self):
        """تایید تعهدنامه"""
        self.legal_agreement_accepted = True
        self.legal_agreement_date = timezone.now()
        self.save()


# مدل‌های مفقود که در views.py استفاده می‌شوند
class AnalysisRequest(models.Model):
    """درخواست تحلیل"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سفارش')
    store_analysis_data = models.JSONField(default=dict, verbose_name='داده‌های تحلیل')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'درخواست تحلیل'
        verbose_name_plural = 'درخواست‌های تحلیل'


class StoreLayout(models.Model):
    """چیدمان فروشگاه"""
    store_info = models.ForeignKey(StoreBasicInfo, on_delete=models.CASCADE, verbose_name='اطلاعات فروشگاه')
    entrances = models.IntegerField(default=1, verbose_name='تعداد ورودی')
    exits = models.IntegerField(default=1, verbose_name='تعداد خروجی')
    checkout_location = models.CharField(max_length=200, verbose_name='محل صندوق')
    unused_area_type = models.CharField(max_length=50, verbose_name='نوع فضای خالی')
    unused_area_size = models.IntegerField(default=0, verbose_name='اندازه فضای خالی')
    unused_area_reason = models.TextField(blank=True, verbose_name='دلیل فضای خالی')
    unused_areas = models.TextField(blank=True, verbose_name='فضاهای خالی')
    layout_restrictions = models.TextField(blank=True, verbose_name='محدودیت‌های چیدمان')
    
    class Meta:
        verbose_name = 'چیدمان فروشگاه'
        verbose_name_plural = 'چیدمان‌های فروشگاه'


class StoreTraffic(models.Model):
    """ترافیک فروشگاه"""
    store_info = models.ForeignKey(StoreBasicInfo, on_delete=models.CASCADE, verbose_name='اطلاعات فروشگاه')
    customer_traffic = models.CharField(max_length=20, default='medium', verbose_name='ترافیک مشتری')
    peak_hours = models.CharField(max_length=100, blank=True, verbose_name='ساعات پیک')
    customer_movement_paths = models.CharField(max_length=100, default='mixed', verbose_name='مسیرهای حرکت مشتری')
    high_traffic_areas = models.CharField(max_length=200, blank=True, verbose_name='مناطق پرترافیک')
    customer_path_notes = models.CharField(max_length=200, blank=True, verbose_name='یادداشت‌های مسیر')
    has_customer_video = models.BooleanField(default=False, verbose_name='دارای ویدیو مشتری')
    video_duration = models.IntegerField(null=True, blank=True, verbose_name='مدت ویدیو')
    video_date = models.DateField(null=True, blank=True, verbose_name='تاریخ ویدیو')
    video_time = models.TimeField(null=True, blank=True, verbose_name='زمان ویدیو')
    
    class Meta:
        verbose_name = 'ترافیک فروشگاه'
        verbose_name_plural = 'ترافیک‌های فروشگاه'


class StoreDesign(models.Model):
    """طراحی فروشگاه"""
    store_info = models.ForeignKey(StoreBasicInfo, on_delete=models.CASCADE, verbose_name='اطلاعات فروشگاه')
    design_style = models.CharField(max_length=50, default='modern', verbose_name='سبک طراحی')
    brand_colors = models.CharField(max_length=200, blank=True, verbose_name='رنگ‌های برند')
    decorative_elements = models.CharField(max_length=200, blank=True, verbose_name='عناصر تزئینی')
    main_lighting = models.CharField(max_length=50, default='artificial', verbose_name='نورپردازی اصلی')
    lighting_intensity = models.CharField(max_length=20, default='medium', verbose_name='شدت نور')
    color_temperature = models.CharField(max_length=20, default='neutral', verbose_name='دمای رنگ')
    
    class Meta:
        verbose_name = 'طراحی فروشگاه'
        verbose_name_plural = 'طراحی‌های فروشگاه'


class StoreSurveillance(models.Model):
    """نظارت فروشگاه"""
    store_info = models.ForeignKey(StoreBasicInfo, on_delete=models.CASCADE, verbose_name='اطلاعات فروشگاه')
    has_surveillance = models.BooleanField(default=False, verbose_name='دارای نظارت')
    camera_count = models.IntegerField(null=True, blank=True, verbose_name='تعداد دوربین')
    camera_locations = models.CharField(max_length=200, blank=True, verbose_name='محل دوربین‌ها')
    camera_coverage = models.CharField(max_length=200, blank=True, verbose_name='پوشش دوربین')
    recording_quality = models.CharField(max_length=20, default='medium', verbose_name='کیفیت ضبط')
    storage_duration = models.IntegerField(default=30, verbose_name='مدت ذخیره')
    
    class Meta:
        verbose_name = 'نظارت فروشگاه'
        verbose_name_plural = 'نظارت‌های فروشگاه'


class StoreProducts(models.Model):
    """محصولات فروشگاه"""
    store_info = models.ForeignKey(StoreBasicInfo, on_delete=models.CASCADE, verbose_name='اطلاعات فروشگاه')
    product_categories = models.CharField(max_length=200, blank=True, verbose_name='دسته‌بندی محصولات')
    main_products = models.TextField(blank=True, verbose_name='محصولات اصلی')
    seasonal_products = models.TextField(blank=True, verbose_name='محصولات فصلی')
    product_display_method = models.CharField(max_length=100, blank=True, verbose_name='روش نمایش محصولات')
    
    class Meta:
        verbose_name = 'محصولات فروشگاه'
        verbose_name_plural = 'محصولات فروشگاه‌ها'


class PricingPlan(models.Model):
    """پلن قیمت‌گذاری"""
    name = models.CharField(max_length=100, verbose_name='نام پلن')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت')
    features = models.TextField(verbose_name='ویژگی‌ها')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'پلن قیمت‌گذاری'
        verbose_name_plural = 'پلن‌های قیمت‌گذاری'


class AIConsultantService(models.Model):
    """سرویس مشاوره هوش مصنوعی"""
    name = models.CharField(max_length=100, verbose_name='نام سرویس')
    description = models.TextField(verbose_name='توضیحات')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    class Meta:
        verbose_name = 'سرویس مشاوره هوش مصنوعی'
        verbose_name_plural = 'سرویس‌های مشاوره هوش مصنوعی'


class AIConsultantQuestion(models.Model):
    """سوال مشاوره هوش مصنوعی"""
    service = models.ForeignKey(AIConsultantService, on_delete=models.CASCADE, verbose_name='سرویس')
    question_text = models.TextField(verbose_name='متن سوال')
    answer_text = models.TextField(blank=True, verbose_name='متن پاسخ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'سوال مشاوره هوش مصنوعی'
        verbose_name_plural = 'سوالات مشاوره هوش مصنوعی'


class AIConsultantSession(models.Model):
    """جلسه مشاوره هوش مصنوعی"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    service = models.ForeignKey(AIConsultantService, on_delete=models.CASCADE, verbose_name='سرویس')
    session_id = models.CharField(max_length=100, unique=True, verbose_name='شناسه جلسه')
    status = models.CharField(max_length=20, default='active', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'جلسه مشاوره هوش مصنوعی'
        verbose_name_plural = 'جلسات مشاوره هوش مصنوعی'


class AIConsultantPayment(models.Model):
    """پرداخت مشاوره هوش مصنوعی"""
    session = models.ForeignKey(AIConsultantSession, on_delete=models.CASCADE, verbose_name='جلسه')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='مبلغ')
    status = models.CharField(max_length=20, default='pending', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'پرداخت مشاوره هوش مصنوعی'
        verbose_name_plural = 'پرداخت‌های مشاوره هوش مصنوعی'


class Transaction(models.Model):
    """تراکنش"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='مبلغ')
    transaction_type = models.CharField(max_length=20, verbose_name='نوع تراکنش')
    status = models.CharField(max_length=20, default='pending', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'


class PromotionalBanner(models.Model):
    """بنرهای تبلیغاتی سایت"""
    title = models.CharField(max_length=200, verbose_name='عنوان')
    content = models.TextField(verbose_name='محتوای تبلیغاتی')
    image_url = models.URLField(blank=True, verbose_name='آدرس تصویر')
    link_url = models.URLField(blank=True, verbose_name='لینک تبلیغاتی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    start_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(default=timezone.now() + timedelta(days=30), verbose_name='تاریخ پایان')
    priority = models.IntegerField(default=1, verbose_name='اولویت نمایش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')
    
    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنرهای تبلیغاتی'


class ChatSession(models.Model):
    """
    Chat Session - ذخیره جلسات چت بین کاربر و AI Consultant
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions', verbose_name='کاربر')
    store_analysis = models.ForeignKey(StoreAnalysis, on_delete=models.CASCADE, related_name='chat_sessions', verbose_name='تحلیل فروشگاه')
    
    title = models.CharField(max_length=200, default='مشاوره جدید', verbose_name='عنوان جلسه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    # محدودیت سوال: 3 سوال رایگان
    is_premium = models.BooleanField(default=False, verbose_name='حساب پریمیوم')
    premium_expires_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ انقضای پریمیوم')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')
    
    class Meta:
        verbose_name = 'جلسه چت'
        verbose_name_plural = 'جلسات چت'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def get_messages_count(self):
        """تعداد پیام‌های جلسه"""
        return self.messages.count()
    
    def get_user_questions_count(self):
        """تعداد سوالات کاربر"""
        return self.messages.filter(role='user').count()
    
    def has_free_questions_left(self):
        """آیا کاربر سوال رایگان باقی دارد؟"""
        if self.is_premium:
            from django.utils import timezone
            if self.premium_expires_at and self.premium_expires_at > timezone.now():
                return True  # پریمیوم فعال - نامحدود
        
        # 3 سوال رایگان
        return self.get_user_questions_count() < 3
    
    def get_last_message(self):
        """آخرین پیام"""
        return self.messages.order_by('-created_at').first()


class ChatMessage(models.Model):
    """
    Chat Message - ذخیره پیام‌های چت
    """
    ROLE_CHOICES = [
        ('user', 'کاربر'),
        ('assistant', 'دستیار هوشمند'),
        ('system', 'سیستم'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages', verbose_name='جلسه چت')
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='نقش')
    content = models.TextField(verbose_name='محتوای پیام')
    
    # متادیتا
    ai_model = models.CharField(max_length=50, blank=True, null=True, verbose_name='مدل AI')
    processing_time = models.FloatField(blank=True, null=True, verbose_name='زمان پردازش (ثانیه)')
    tokens_used = models.IntegerField(blank=True, null=True, verbose_name='تعداد توکن')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'پیام چت'
        verbose_name_plural = 'پیام‌های چت'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
        ordering = ['-priority', '-created_at']