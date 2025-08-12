
from django.contrib import admin
from django.utils.html import format_html
from .models import StoreAnalysis

@admin.action(description="تایید گروهی تحلیل‌ها")
def approve_analyses(modeladmin, request, queryset):
    queryset.update(status='completed')

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
            'fields': ('user', 'store_name', 'description', 'layout_image', 'thumbnail')
        }),
        ('وضعیت', {
            'fields': ('status', 'results', 'error_message', 'video_link')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail(self, obj):
        if hasattr(obj, 'layout_image') and obj.layout_image:
            return format_html('<img src="{}" width="60" style="border-radius:8px; box-shadow:0 2px 6px #ccc;" />', obj.layout_image.url)
        return "-"
    thumbnail.short_description = "پیش‌نمایش چیدمان"

    def video_link(self, obj):
        if hasattr(obj, 'customer_video_file') and obj.customer_video_file:
            return format_html('<a href="{}" target="_blank" class="btn btn-sm btn-outline-primary">دانلود ویدیو</a>', obj.customer_video_file.url)
        return "-"
    video_link.short_description = "ویدیوی مسیر مشتری"
