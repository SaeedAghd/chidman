"""
Admin configuration for Store Analysis
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Count, Sum
from django.utils import timezone
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponse
import csv
from datetime import datetime, timedelta
from .models import (
    Payment, PaymentLog, ServicePackage, UserSubscription,
    ChatSession, ChatMessage, FreeUsageTracking
)

# --- Custom Filters ---
class PaymentStatusFilter(SimpleListFilter):
    """فیلتر بر اساس وضعیت پرداخت"""
    title = 'وضعیت پرداخت'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('pending', 'در انتظار پرداخت'),
            ('processing', 'در حال پردازش'),
            ('completed', 'تکمیل شده'),
            ('failed', 'ناموفق'),
            ('cancelled', 'لغو شده'),
            ('refunded', 'برگشت شده'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset

class PaymentMethodFilter(SimpleListFilter):
    """فیلتر بر اساس روش پرداخت"""
    title = 'روش پرداخت'
    parameter_name = 'payment_method'

    def lookups(self, request, model_admin):
        return [
            ('ping_payment', 'پی پینگ'),
            ('zarinpal', 'زرین‌پال'),
            ('manual', 'دستی'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(payment_method=self.value())
        return queryset

class DateRangeFilter(SimpleListFilter):
    """فیلتر بر اساس بازه زمانی"""
    title = 'بازه زمانی'
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return [
            ('today', 'امروز'),
            ('week', 'این هفته'),
            ('month', 'این ماه'),
            ('year', 'امسال'),
        ]

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'today':
            return queryset.filter(created_at__date=now.date())
        elif self.value() == 'week':
            return queryset.filter(created_at__gte=now - timedelta(days=7))
        elif self.value() == 'month':
            return queryset.filter(created_at__gte=now - timedelta(days=30))
        elif self.value() == 'year':
            return queryset.filter(created_at__gte=now - timedelta(days=365))
        return queryset

class TestModeFilter(SimpleListFilter):
    """فیلتر بر اساس حالت تست"""
    title = 'حالت تست'
    parameter_name = 'is_test'

    def lookups(self, request, model_admin):
        return [
            ('true', 'تست'),
            ('false', 'واقعی'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(is_test=True)
        elif self.value() == 'false':
            return queryset.filter(is_test=False)
        return queryset

# --- Payment Admin ---
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'order_id', 'user', 'amount_display', 'status_display', 
        'payment_method_display', 'is_test_display', 'created_at'
    ]
    list_filter = [
        PaymentStatusFilter, PaymentMethodFilter, TestModeFilter, 
        DateRangeFilter, 'created_at'
    ]
    search_fields = ['order_id', 'payment_id', 'transaction_id', 'user__username', 'customer_name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'completed_at']
    ordering = ['-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('اطلاعات پرداخت', {
            'fields': ('id', 'order_id', 'payment_id', 'transaction_id', 'amount', 'currency')
        }),
        ('اطلاعات مشتری', {
            'fields': ('user', 'customer_name', 'customer_email', 'customer_phone')
        }),
        ('وضعیت و روش', {
            'fields': ('status', 'payment_method', 'description')
        }),
        ('اطلاعات درگاه', {
            'fields': ('gateway_response', 'callback_data', 'is_test')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
        ('یادداشت‌ها', {
            'fields': ('notes',)
        }),
    )
    
    def amount_display(self, obj):
        return f"{obj.amount:,} {obj.currency}"
    amount_display.short_description = 'مبلغ'
    amount_display.admin_order_field = 'amount'
    
    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'completed': 'green',
            'failed': 'red',
            'cancelled': 'gray',
            'refunded': 'purple',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'وضعیت'
    status_display.admin_order_field = 'status'
    
    def payment_method_display(self, obj):
        colors = {
            'ping_payment': 'blue',
            'zarinpal': 'green',
            'manual': 'gray',
        }
        color = colors.get(obj.payment_method, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_payment_method_display()
        )
    payment_method_display.short_description = 'روش پرداخت'
    payment_method_display.admin_order_field = 'payment_method'
    
    def is_test_display(self, obj):
        if obj.is_test:
            return format_html('<span style="color: orange; font-weight: bold;">تست</span>')
        else:
            return format_html('<span style="color: green; font-weight: bold;">واقعی</span>')
    is_test_display.short_description = 'حالت'
    is_test_display.admin_order_field = 'is_test'
    
    actions = ['export_payments_csv', 'mark_as_completed', 'mark_as_failed']
    
    def export_payments_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="payments.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Order ID', 'User', 'Amount', 'Currency', 'Status', 
            'Payment Method', 'Created At', 'Completed At'
        ])
        
        for payment in queryset:
            writer.writerow([
                payment.order_id,
                payment.user.username,
                payment.amount,
                payment.currency,
                payment.get_status_display(),
                payment.get_payment_method_display(),
                payment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                payment.completed_at.strftime('%Y-%m-%d %H:%M:%S') if payment.completed_at else '',
            ])
        
        return response
    export_payments_csv.short_description = 'صادر کردن CSV'
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'{updated} پرداخت به عنوان تکمیل شده علامت‌گذاری شد.')
    mark_as_completed.short_description = 'علامت‌گذاری به عنوان تکمیل شده'
    
    def mark_as_failed(self, request, queryset):
        updated = queryset.update(status='failed')
        self.message_user(request, f'{updated} پرداخت به عنوان ناموفق علامت‌گذاری شد.')
    mark_as_failed.short_description = 'علامت‌گذاری به عنوان ناموفق'

@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ['payment', 'log_type_display', 'message', 'created_at']
    list_filter = ['log_type', 'created_at']
    search_fields = ['payment__order_id', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    list_per_page = 25
    
    def log_type_display(self, obj):
        colors = {
            'payment_created': 'blue',
            'payment_redirected': 'orange',
            'payment_callback': 'purple',
            'payment_verified': 'green',
            'payment_failed': 'red',
            'payment_cancelled': 'gray',
            'payment_refunded': 'brown',
            'error': 'red',
        }
        color = colors.get(obj.log_type, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_log_type_display()
        )
    log_type_display.short_description = 'نوع لاگ'
    log_type_display.admin_order_field = 'log_type'

@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'package_type_display', 'price_display', 'currency', 
        'is_active_display', 'is_popular_display', 'sort_order'
    ]
    list_filter = ['package_type', 'is_active', 'is_popular', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['sort_order', 'price']
    list_per_page = 25
    
    fieldsets = (
        ('اطلاعات بسته', {
            'fields': ('name', 'description', 'package_type', 'price', 'currency')
        }),
        ('ویژگی‌ها', {
            'fields': ('features', 'max_analyses', 'validity_days')
        }),
        ('تنظیمات', {
            'fields': ('is_active', 'is_popular', 'sort_order')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def package_type_display(self, obj):
        colors = {
            'basic': 'blue',
            'professional': 'green',
            'enterprise': 'purple',
            'custom': 'orange',
        }
        color = colors.get(obj.package_type, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_package_type_display()
        )
    package_type_display.short_description = 'نوع بسته'
    package_type_display.admin_order_field = 'package_type'
    
    def price_display(self, obj):
        return f"{obj.price:,} {obj.currency}"
    price_display.short_description = 'قیمت'
    price_display.admin_order_field = 'price'
    
    def is_active_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">فعال</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">غیرفعال</span>')
    is_active_display.short_description = 'وضعیت'
    is_active_display.admin_order_field = 'is_active'
    
    def is_popular_display(self, obj):
        if obj.is_popular:
            return format_html('<span style="color: gold; font-weight: bold;">⭐ محبوب</span>')
        else:
            return format_html('<span style="color: gray;">-</span>')
    is_popular_display.short_description = 'محبوب'
    is_popular_display.admin_order_field = 'is_popular'
    
    actions = ['activate_packages', 'deactivate_packages', 'mark_as_popular']
    
    def activate_packages(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} بسته فعال شد.')
    activate_packages.short_description = 'فعال کردن بسته‌ها'
    
    def deactivate_packages(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} بسته غیرفعال شد.')
    deactivate_packages.short_description = 'غیرفعال کردن بسته‌ها'
    
    def mark_as_popular(self, request, queryset):
        updated = queryset.update(is_popular=True)
        self.message_user(request, f'{updated} بسته به عنوان محبوب علامت‌گذاری شد.')
    mark_as_popular.short_description = 'علامت‌گذاری به عنوان محبوب'

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'package', 'is_active_display', 'start_date', 
        'end_date', 'analyses_used', 'max_analyses', 'created_at'
    ]
    list_filter = ['is_active', 'package', 'start_date', 'end_date']
    search_fields = ['user__username', 'package__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('اطلاعات اشتراک', {
            'fields': ('user', 'package', 'payment')
        }),
        ('جزئیات اشتراک', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('استفاده', {
            'fields': ('analyses_used', 'max_analyses')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def is_active_display(self, obj):
        if obj.is_active and not obj.is_expired():
            return format_html('<span style="color: green; font-weight: bold;">فعال</span>')
        elif obj.is_expired():
            return format_html('<span style="color: red; font-weight: bold;">منقضی شده</span>')
        else:
            return format_html('<span style="color: gray; font-weight: bold;">غیرفعال</span>')
    is_active_display.short_description = 'وضعیت'
    is_active_display.admin_order_field = 'is_active'
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} اشتراک فعال شد.')
    activate_subscriptions.short_description = 'فعال کردن اشتراک‌ها'
    
    def deactivate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} اشتراک غیرفعال شد.')
    deactivate_subscriptions.short_description = 'غیرفعال کردن اشتراک‌ها'


# --- Chat Session & Chat Message Admin ---
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """مدیریت پیام‌های چت"""
    list_display = ('session', 'role', 'content_preview', 'ai_model', 'processing_time', 'created_at')
    list_filter = ('role', 'ai_model', 'created_at')
    search_fields = ('content', 'session__user__username', 'session__store_analysis__store_name')
    readonly_fields = ('session', 'role', 'content', 'ai_model', 'processing_time', 'tokens_used', 'created_at')
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        """نمایش پیش‌نمایش محتوا"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'محتوا'


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    """مدیریت جلسات چت"""
    list_display = ('user', 'store_analysis', 'title', 'messages_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'store_analysis__store_name', 'title')
    readonly_fields = ('id', 'user', 'store_analysis', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    def messages_count(self, obj):
        """تعداد پیام‌ها"""
        return obj.get_messages_count()
    messages_count.short_description = 'تعداد پیام‌ها'


# --- Free Usage Tracking Admin ---
@admin.register(FreeUsageTracking)
class FreeUsageTrackingAdmin(admin.ModelAdmin):
    """مدیریت ردیابی استفاده رایگان"""
    list_display = ('username', 'email', 'phone', 'is_blocked', 'first_usage', 'last_checked')
    list_filter = ('is_blocked', 'first_usage')
    search_fields = ('username', 'email', 'phone', 'store_name')
    readonly_fields = ('first_usage', 'last_checked', 'analysis_id')
    date_hierarchy = 'first_usage'
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('username', 'email', 'phone', 'ip_address')
        }),
        ('اطلاعات استفاده', {
            'fields': ('analysis_id', 'store_name', 'first_usage', 'last_checked')
        }),
        ('وضعیت', {
            'fields': ('is_blocked', 'block_reason')
        }),
        ('اطلاعات اضافی', {
            'fields': ('user_agent', 'additional_info'),
            'classes': ('collapse',)
        }),
    )


# --- Admin Site Configuration ---
admin.site.site_header = "مدیریت چیدمانو"
admin.site.site_title = "چیدمانو"
admin.site.index_title = "پنل مدیریت"