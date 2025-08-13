
from django.contrib import admin
from django.utils.html import format_html
from .models import StoreAnalysis, StoreAnalysisResult, Payment, Article, ArticleCategory

@admin.action(description="تایید گروهی تحلیل‌ها")
def approve_analyses(modeladmin, request, queryset):
    """تایید گروهی تحلیل‌های انتخاب شده"""
    updated_count = queryset.update(status='completed')
    modeladmin.message_user(
        request, 
        f'{updated_count} تحلیل با موفقیت تایید شد.'
    )

@admin.register(StoreAnalysis)
class StoreAnalysisAdmin(admin.ModelAdmin):
    """
    Admin configuration for StoreAnalysis model with advanced features.
    """
    list_display = (
        'store_name', 'user', 'status', 'created_at', 'updated_at',
        'thumbnail', 'video_link',
    )
    list_filter = (
        'status', 'created_at', 'updated_at', 'store_type', 'city', 'has_surveillance'
    )
    search_fields = ('store_name', 'description', 'user__username', 'city', 'area')
    readonly_fields = ('created_at', 'updated_at', 'thumbnail', 'video_link')
    list_editable = ('status',)
    actions = [approve_analyses]

    fieldsets = (
        (None, {
            'fields': ('user', 'store_name', 'store_location', 'store_type', 'store_size')
        }),
        ('وضعیت', {
            'fields': ('status', 'error_message')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail(self, obj):
        """نمایش پیش‌نمایش تصویر فروشگاه"""
        if hasattr(obj, 'store_photos') and obj.store_photos:
            return format_html(
                '<img src="{}" width="60" style="border-radius:8px; box-shadow:0 2px 6px #ccc;" />', 
                obj.store_photos.url
            )
        return "-"
    thumbnail.short_description = "پیش‌نمایش فروشگاه"

    def video_link(self, obj):
        """نمایش لینک دانلود ویدیو"""
        if hasattr(obj, 'customer_video_file') and obj.customer_video_file:
            return format_html(
                '<a href="{}" target="_blank" class="btn btn-sm btn-outline-primary">دانلود ویدیو</a>', 
                obj.customer_video_file.url
            )
        return "-"
    video_link.short_description = "ویدیوی مسیر مشتری"
