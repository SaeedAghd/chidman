
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponse
import csv
from datetime import datetime, timedelta
from .models import (
    StoreAnalysis, StoreAnalysisResult, DetailedAnalysis, Payment, 
    Article, ArticleCategory, StoreBasicInfo, StoreLayout, StoreTraffic, 
    StoreDesign, StoreSurveillance, StoreProducts, AIConsultantSession, 
    AIConsultantQuestion, AIConsultantPayment, DiscountCode, EmailVerification,
    FAQCategory, FAQ, SupportTicket, TicketMessage, TicketTemplate,
    Wallet, Transaction
)

# --- Custom Filters ---
class StatusFilter(SimpleListFilter):
    """فیلتر بر اساس وضعیت تحلیل"""
    title = 'وضعیت تحلیل'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('pending', 'در انتظار'),
            ('processing', 'در حال پردازش'),
            ('completed', 'تکمیل شده'),
            ('failed', 'ناموفق'),
            ('cancelled', 'لغو شده'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())

class StoreTypeFilter(SimpleListFilter):
    """فیلتر بر اساس نوع فروشگاه"""
    title = 'نوع فروشگاه'
    parameter_name = 'store_type'

    def lookups(self, request, model_admin):
        return [
            ('supermarket', 'سوپرمارکت'),
            ('hypermarket', 'هایپرمارکت'),
            ('clothing', 'فروشگاه پوشاک'),
            ('appliance', 'لوازم خانگی'),
            ('electronics', 'الکترونیک'),
            ('pharmacy', 'داروخانه'),
            ('bookstore', 'کتاب‌فروشی'),
            ('jewelry', 'جواهرات'),
            ('sports', 'ورزشی'),
            ('beauty', 'آرایشی و بهداشتی'),
            ('other', 'سایر'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(store_info__store_type=self.value())

class DateRangeFilter(SimpleListFilter):
    """فیلتر بر اساس بازه زمانی"""
    title = 'بازه زمانی'
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return (
            ('today', 'امروز'),
            ('week', 'هفته جاری'),
            ('month', 'ماه جاری'),
            ('quarter', 'سه ماهه جاری'),
            ('year', 'سال جاری'),
        )

    def queryset(self, request, queryset):
        if self.value():
            now = timezone.now()
            if self.value() == 'today':
                return queryset.filter(created_at__date=now.date())
            elif self.value() == 'week':
                return queryset.filter(created_at__gte=now - timedelta(days=7))
            elif self.value() == 'month':
                return queryset.filter(created_at__month=now.month, created_at__year=now.year)
            elif self.value() == 'quarter':
                quarter_start = now.replace(month=((now.month - 1) // 3) * 3 + 1, day=1)
                return queryset.filter(created_at__gte=quarter_start)
            elif self.value() == 'year':
                return queryset.filter(created_at__year=now.year)
        return queryset

# --- Admin Actions ---
def export_to_csv(modeladmin, request, queryset):
    """اکسپورت به CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="store_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'نام فروشگاه', 'نوع فروشگاه', 'شهر', 'وضعیت', 'تاریخ ایجاد', 
        'مدت تخمینی', 'مدت واقعی', 'کاربر'
    ])
    
    for obj in queryset:
        writer.writerow([
            obj.get_store_name(),
            obj.store_info.store_type if obj.store_info else '',
            obj.store_info.city if obj.store_info else '',
            obj.get_status_display(),
            obj.created_at.strftime('%Y-%m-%d %H:%M'),
            obj.estimated_duration,
            obj.actual_duration or '',
            obj.user.username,
        ])
    
    return response
export_to_csv.short_description = "اکسپورت انتخاب شده‌ها به CSV"

def mark_as_completed(modeladmin, request, queryset):
    """علامت‌گذاری به عنوان تکمیل شده"""
    updated = queryset.update(status='completed', updated_at=timezone.now())
    modeladmin.message_user(request, f'{updated} تحلیل با موفقیت تکمیل شد.')
mark_as_completed.short_description = "علامت‌گذاری به عنوان تکمیل شده"

def mark_as_failed(modeladmin, request, queryset):
    """علامت‌گذاری به عنوان ناموفق"""
    updated = queryset.update(status='failed', updated_at=timezone.now())
    modeladmin.message_user(request, f'{updated} تحلیل به عنوان ناموفق علامت‌گذاری شد.')
mark_as_failed.short_description = "علامت‌گذاری به عنوان ناموفق"

def recalculate_analysis(modeladmin, request, queryset):
    """محاسبه مجدد تحلیل‌ها"""
    for obj in queryset:
        if obj.status in ['completed', 'failed']:
            obj.status = 'pending'
            obj.error_message = ''
            obj.save()
    modeladmin.message_user(request, f'{queryset.count()} تحلیل برای محاسبه مجدد آماده شد.')
recalculate_analysis.short_description = "محاسبه مجدد تحلیل‌ها"

# --- StoreAnalysis Admin ---
@admin.register(StoreAnalysis)
class StoreAnalysisAdmin(admin.ModelAdmin):
    """مدیریت تحلیل‌های فروشگاه"""
    list_display = [
        'get_store_name', 'get_store_type', 'get_city', 'user', 'status', 
        'priority', 'created_at', 'get_duration', 'get_progress_bar'
    ]
    list_filter = [
        StatusFilter, StoreTypeFilter, DateRangeFilter,
        'priority', 'created_at', 'updated_at'
    ]
    search_fields = [
        'store_info__store_name', 'store_info__store_location', 
        'store_info__city', 'user__username', 'user__email'
    ]
    list_editable = ['status', 'priority']
    readonly_fields = [
        'created_at', 'updated_at', 'get_store_info_link', 
        'get_analysis_duration', 'get_progress_percentage'
    ]
    actions = [export_to_csv, mark_as_completed, mark_as_failed, recalculate_analysis]
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('user', 'store_info', 'status', 'priority')
        }),
        ('زمان‌بندی', {
            'fields': ('estimated_duration', 'actual_duration', 'created_at', 'updated_at')
        }),
        ('نتایج', {
            'fields': ('results', 'error_message'),
            'classes': ('collapse',)
        }),
        ('لینک‌های مرتبط', {
            'fields': ('get_store_info_link', 'get_analysis_duration', 'get_progress_percentage'),
            'classes': ('collapse',)
        }),
    )

    def get_store_name(self, obj):
        """نام فروشگاه"""
        if obj.store_info:
            return obj.store_info.store_name
        return '-'
    get_store_name.short_description = 'نام فروشگاه'
    get_store_name.admin_order_field = 'store_info__store_name'

    def get_store_type(self, obj):
        """نوع فروشگاه"""
        if obj.store_info:
            return obj.store_info.get_store_type_display()
        return '-'
    get_store_type.short_description = 'نوع فروشگاه'
    get_store_type.admin_order_field = 'store_info__store_type'

    def get_city(self, obj):
        """شهر"""
        if obj.store_info:
            return obj.store_info.city
        return '-'
    get_city.short_description = 'شهر'
    get_city.admin_order_field = 'store_info__city'

    def get_priority(self, obj):
        """اولویت با رنگ"""
        colors = {
            'low': 'green',
            'medium': 'orange',
            'high': 'red',
            'urgent': 'purple'
        }
        color = colors.get(obj.priority, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_priority_display()
        )
    get_priority.short_description = 'اولویت'

    def get_duration(self, obj):
        """مدت زمان تحلیل"""
        if obj.actual_duration:
            return f"{obj.actual_duration} دقیقه"
        elif obj.estimated_duration:
            return f"~{obj.estimated_duration} دقیقه"
        return '-'
    get_duration.short_description = 'مدت زمان'

    def get_progress_bar(self, obj):
        """نوار پیشرفت"""
        progress = obj.get_progress()
        color = 'green' if progress == 100 else 'orange' if progress > 0 else 'red'
        return format_html(
            '<div style="width: 100px; background-color: #f0f0f0; border-radius: 10px; overflow: hidden;">'
            '<div style="width: {}%; height: 20px; background-color: {}; text-align: center; color: white; font-size: 12px; line-height: 20px;">'
            '{}%</div></div>',
            progress, color, progress
        )
    get_progress_bar.short_description = 'پیشرفت'

    def get_store_info_link(self, obj):
        """لینک به اطلاعات فروشگاه"""
        if obj.store_info:
            url = reverse('admin:store_analysis_storebasicinfo_change', args=[obj.store_info.id])
            return format_html('<a href="{}">مشاهده اطلاعات فروشگاه</a>', url)
        return '-'
    get_store_info_link.short_description = 'لینک اطلاعات فروشگاه'

    def get_analysis_duration(self, obj):
        """مدت زمان تحلیل"""
        duration = obj.get_analysis_duration()
        if duration:
            return f"{duration:.1f} ثانیه"
        return 'محاسبه نشده'
    get_analysis_duration.short_description = 'مدت زمان تحلیل'

    def get_progress_percentage(self, obj):
        """درصد پیشرفت"""
        return f"{obj.get_progress()}%"
    get_progress_percentage.short_description = 'درصد پیشرفت'

    def get_queryset(self, request):
        """بهینه‌سازی کوئری"""
        return super().get_queryset(request).select_related(
            'user', 'store_info'
        ).prefetch_related(
            'analysis_result'
        )

    def save_model(self, request, obj, form, change):
        """ذخیره مدل با اعتبارسنجی"""
        if change and 'status' in form.changed_data:
            # اعتبارسنجی تغییر وضعیت
            old_status = form.initial.get('status')
            if old_status == 'processing' and obj.status in ['completed', 'failed']:
                obj.actual_duration = obj.estimated_duration  # تخمینی
        super().save_model(request, obj, form, change)

# --- StoreBasicInfo Admin ---
@admin.register(StoreBasicInfo)
class StoreBasicInfoAdmin(admin.ModelAdmin):
    """مدیریت اطلاعات پایه فروشگاه"""
    list_display = [
        'store_name', 'store_type', 'city', 'area', 'store_size', 
        'user', 'created_at', 'get_analysis_count'
    ]
    list_filter = [
        'store_type', 'city', 'area', 'created_at'
    ]
    search_fields = [
        'store_name', 'store_location', 'city', 'area', 'user__username'
    ]
    readonly_fields = ['created_at', 'updated_at', 'get_analysis_link']

    fieldsets = (
        ('اطلاعات فروشگاه', {
            'fields': ('user', 'store_name', 'store_location', 'city', 'area')
        }),
        ('مشخصات', {
            'fields': ('store_type', 'store_size', 'store_dimensions')
        }),
        ('تماس', {
            'fields': ('phone', 'email')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
        ('لینک‌ها', {
            'fields': ('get_analysis_link',),
            'classes': ('collapse',)
        }),
    )

    def get_analysis_count(self, obj):
        """تعداد تحلیل‌ها"""
        return obj.analysis_set.count()
    get_analysis_count.short_description = 'تعداد تحلیل‌ها'

    def get_analysis_link(self, obj):
        """لینک به تحلیل‌ها"""
        analyses = obj.analysis_set.all()
        if analyses:
            links = []
            for analysis in analyses[:5]:  # حداکثر 5 لینک
                url = reverse('admin:store_analysis_storeanalysis_change', args=[analysis.id])
                links.append(f'<a href="{url}">تحلیل {analysis.id}</a>')
            return mark_safe('<br>'.join(links))
        return 'هیچ تحلیلی یافت نشد'
    get_analysis_link.short_description = 'تحلیل‌های مرتبط'

# --- StoreLayout Admin ---
@admin.register(StoreLayout)
class StoreLayoutAdmin(admin.ModelAdmin):
    """مدیریت چیدمان فروشگاه"""
    list_display = [
        'get_store_name', 'entrances', 'shelf_count', 'unused_area_type', 
        'unused_area_size', 'get_thumbnail'
    ]
    list_filter = ['unused_area_type', 'entrances']
    search_fields = ['store_info__store_name']
    readonly_fields = ['created_at', 'updated_at', 'get_thumbnail', 'get_video_link']
    
    fieldsets = (
        ('اطلاعات چیدمان', {
            'fields': ('store_info', 'entrances', 'shelf_count', 'shelf_dimensions', 'shelf_contents')
        }),
        ('صندوق‌ها', {
            'fields': ('checkout_location',)
        }),
        ('مناطق بلااستفاده', {
            'fields': ('unused_area_type', 'unused_area_size', 'unused_area_reason', 'unused_areas')
        }),
        ('محدودیت‌ها', {
            'fields': ('layout_restrictions',)
        }),
        ('فایل‌ها', {
            'fields': ('store_plan', 'store_photos', 'get_thumbnail')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_store_name(self, obj):
        return obj.store_info.store_name if obj.store_info else '-'
    get_store_name.short_description = 'نام فروشگاه'

    def get_thumbnail(self, obj):
        """نمایش تصویر بندانگشتی"""
        if obj.store_photos:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.store_photos.url
            )
        return 'تصویر موجود نیست'
    get_thumbnail.short_description = 'تصویر فروشگاه'

    def get_video_link(self, obj):
        """لینک ویدیو"""
        if obj.store_plan:
            return format_html('<a href="{}">دانلود نقشه</a>', obj.store_plan.url)
        return 'فایل موجود نیست'

# --- StoreTraffic Admin ---
@admin.register(StoreTraffic)
class StoreTrafficAdmin(admin.ModelAdmin):
    """مدیریت ترافیک فروشگاه"""
    list_display = [
        'get_store_name', 'customer_traffic', 'customer_movement_paths', 
        'has_customer_video', 'video_duration', 'get_video_link'
    ]
    list_filter = ['customer_traffic', 'customer_movement_paths', 'has_customer_video']
    search_fields = ['store_info__store_name']
    readonly_fields = ['created_at', 'updated_at', 'get_video_link']
    
    fieldsets = (
        ('ترافیک مشتری', {
            'fields': ('store_info', 'customer_traffic', 'peak_hours')
        }),
        ('رفتار مشتری', {
            'fields': ('customer_movement_paths', 'high_traffic_areas', 'customer_path_notes')
        }),
        ('ویدیو', {
            'fields': ('has_customer_video', 'video_duration', 'video_date', 'video_time', 'customer_video_file', 'get_video_link')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_store_name(self, obj):
        return obj.store_info.store_name if obj.store_info else '-'
    get_store_name.short_description = 'نام فروشگاه'

    def get_video_link(self, obj):
        """لینک ویدیو"""
        if obj.customer_video_file:
            return format_html('<a href="{}">دانلود ویدیو</a>', obj.customer_video_file.url)
        return 'فایل موجود نیست'

# --- StoreDesign Admin ---
@admin.register(StoreDesign)
class StoreDesignAdmin(admin.ModelAdmin):
    """مدیریت طراحی فروشگاه"""
    list_display = [
        'get_store_name', 'design_style', 'main_lighting', 
        'lighting_intensity', 'color_temperature'
    ]
    list_filter = ['design_style', 'main_lighting', 'lighting_intensity', 'color_temperature']
    search_fields = ['store_info__store_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('سبک طراحی', {
            'fields': ('store_info', 'design_style', 'brand_colors')
        }),
        ('نورپردازی', {
            'fields': ('main_lighting', 'lighting_intensity', 'color_temperature')
        }),
        ('دکوراسیون', {
            'fields': ('decorative_elements',)
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_store_name(self, obj):
        return obj.store_info.store_name if obj.store_info else '-'
    get_store_name.short_description = 'نام فروشگاه'

# --- StoreSurveillance Admin ---
@admin.register(StoreSurveillance)
class StoreSurveillanceAdmin(admin.ModelAdmin):
    """مدیریت نظارت فروشگاه"""
    list_display = [
        'get_store_name', 'has_surveillance', 'camera_count', 
        'recording_quality', 'storage_duration'
    ]
    list_filter = ['has_surveillance', 'recording_quality']
    search_fields = ['store_info__store_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('نظارت', {
            'fields': ('store_info', 'has_surveillance', 'camera_count')
        }),
        ('پوشش', {
            'fields': ('camera_locations', 'camera_coverage')
        }),
        ('کیفیت', {
            'fields': ('recording_quality', 'storage_duration')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_store_name(self, obj):
        return obj.store_info.store_name if obj.store_info else '-'
    get_store_name.short_description = 'نام فروشگاه'

# --- StoreProducts Admin ---
@admin.register(StoreProducts)
class StoreProductsAdmin(admin.ModelAdmin):
    """مدیریت محصولات فروشگاه"""
    list_display = [
        'get_store_name', 'sales_volume', 'pos_system', 
        'supplier_count', 'get_file_links'
    ]
    list_filter = ['pos_system']
    search_fields = ['store_info__store_name', 'top_products']
    readonly_fields = ['created_at', 'updated_at', 'get_file_links']
    
    fieldsets = (
        ('محصولات', {
            'fields': ('store_info', 'product_categories', 'top_products')
        }),
        ('فروش', {
            'fields': ('sales_volume', 'pos_system', 'inventory_system')
        }),
        ('تامین‌کنندگان', {
            'fields': ('supplier_count',)
        }),
        ('فایل‌ها', {
            'fields': ('sales_file', 'product_catalog', 'get_file_links')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_store_name(self, obj):
        return obj.store_info.store_name if obj.store_info else '-'
    get_store_name.short_description = 'نام فروشگاه'

    def get_file_links(self, obj):
        """لینک‌های فایل‌ها"""
        links = []
        if obj.sales_file:
            links.append(f'<a href="{obj.sales_file.url}">فایل فروش</a>')
        if obj.product_catalog:
            links.append(f'<a href="{obj.product_catalog.url}">کاتالوگ محصولات</a>')
        return mark_safe('<br>'.join(links)) if links else 'فایل موجود نیست'
    get_file_links.short_description = 'فایل‌ها'

# --- سایر مدل‌ها ---
@admin.register(StoreAnalysisResult)
class StoreAnalysisResultAdmin(admin.ModelAdmin):
    """مدیریت نتایج تحلیل"""
    list_display = ['store_analysis', 'created_at', 'get_result_summary']
    list_filter = ['created_at']
    search_fields = ['store_analysis__store_info__store_name']
    readonly_fields = ['created_at', 'updated_at']

    def get_result_summary(self, obj):
        """خلاصه نتایج"""
        try:
            if hasattr(obj, 'overall_score') and obj.overall_score:
                return f"امتیاز کلی: {obj.overall_score}"
            return 'بدون نتیجه'
        except:
            return 'بدون نتیجه'
    get_result_summary.short_description = 'خلاصه نتایج'

@admin.register(DetailedAnalysis)
class DetailedAnalysisAdmin(admin.ModelAdmin):
    """مدیریت تحلیل تفصیلی"""
    list_display = ['store_analysis', 'created_at']
    list_filter = ['created_at']
    search_fields = ['store_analysis__store_info__store_name']
    readonly_fields = ['created_at']  # حذف updated_at چون در مدل وجود ندارد

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """مدیریت پرداخت‌ها"""
    list_display = ['user', 'amount', 'payment_method', 'created_at']
    list_filter = ['payment_method', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """مدیریت مقالات"""
    list_display = ['title', 'category', 'author', 'is_featured', 'views', 'created_at']
    list_filter = ['category', 'is_featured', 'created_at']
    search_fields = ['title', 'summary', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات مقاله', {
            'fields': ('title', 'slug', 'category', 'author')
        }),
        ('محتوای مقاله', {
            'fields': ('summary', 'content', 'tags')
        }),
        ('تنظیمات', {
            'fields': ('is_featured', 'views')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    """مدیریت دسته‌بندی مقالات"""
    list_display = ['title', 'slug', 'get_article_count']  # حذف created_at
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}  # تغییر از name به title
    readonly_fields = []  # حذف created_at و updated_at

    def get_article_count(self, obj):
        return obj.articles.count()
    get_article_count.short_description = 'تعداد مقالات'

# --- تنظیمات Admin Site ---
# --- AI Consultant Admin ---
@admin.register(AIConsultantSession)
class AIConsultantSessionAdmin(admin.ModelAdmin):
    """مدیریت جلسات مشاوره هوش مصنوعی"""
    list_display = ['session_id', 'user', 'store_analysis', 'status', 'is_paid', 'free_questions_used', 'paid_questions_used', 'expires_at', 'created_at']
    list_filter = ['status', 'is_paid', 'created_at', 'expires_at']
    search_fields = ['user__username', 'user__email', 'store_analysis__store_name', 'session_id']
    readonly_fields = ['session_id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('اطلاعات جلسه', {
            'fields': ('session_id', 'user', 'store_analysis', 'status')
        }),
        ('آمار سوالات', {
            'fields': ('free_questions_used', 'paid_questions_used', 'is_paid')
        }),
        ('زمان‌بندی', {
            'fields': ('expires_at', 'created_at', 'updated_at')
        }),
    )

@admin.register(AIConsultantQuestion)
class AIConsultantQuestionAdmin(admin.ModelAdmin):
    """مدیریت سوالات مشاوره"""
    list_display = ['id', 'session', 'question_short', 'is_answered', 'is_free', 'response_time', 'created_at']
    list_filter = ['is_answered', 'is_free', 'created_at']
    search_fields = ['question', 'answer', 'session__user__username']
    readonly_fields = ['created_at', 'updated_at', 'response_time']
    ordering = ['-created_at']
    
    def question_short(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_short.short_description = 'سوال'
    
    fieldsets = (
        ('اطلاعات سوال', {
            'fields': ('session', 'question', 'is_free')
        }),
        ('پاسخ', {
            'fields': ('answer', 'is_answered', 'response_time')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(AIConsultantPayment)
class AIConsultantPaymentAdmin(admin.ModelAdmin):
    """مدیریت پرداخت‌های مشاوره"""
    list_display = ['payment_id', 'session', 'amount', 'status', 'payment_gateway', 'transaction_id', 'created_at']
    list_filter = ['status', 'payment_gateway', 'created_at']
    search_fields = ['payment_id', 'transaction_id', 'session__user__username']
    readonly_fields = ['payment_id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('اطلاعات پرداخت', {
            'fields': ('payment_id', 'session', 'amount', 'status')
        }),
        ('جزئیات تراکنش', {
            'fields': ('payment_gateway', 'transaction_id')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )

# --- Discount Code Admin ---
@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    """مدیریت کدهای تخفیف"""
    list_display = [
        'code', 'discount_type', 'percentage', 'fixed_amount', 'event_type',
        'max_usage', 'used_count', 'is_active', 'valid_from', 'valid_until'
    ]
    list_filter = ['discount_type', 'event_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['code', 'event_type']
    list_editable = ['is_active']
    readonly_fields = ['used_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات کد تخفیف', {
            'fields': ('code', 'event_type')
        }),
        ('نوع تخفیف', {
            'fields': ('discount_type', 'percentage', 'fixed_amount')
        }),
        ('محدودیت‌ها', {
            'fields': ('max_usage', 'used_count')
        }),
        ('زمان‌بندی', {
            'fields': ('valid_from', 'valid_until', 'is_active')
        }),
        ('زمان ایجاد', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# --- Email Verification Admin ---
@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """مدیریت تاییدیه‌های ایمیل"""
    list_display = [
        'user', 'email', 'verification_code', 'is_verified', 
        'attempts', 'expires_at', 'created_at'
    ]
    list_filter = ['is_verified', 'created_at', 'expires_at']
    search_fields = ['user__username', 'user__email', 'email']
    readonly_fields = ['verification_code', 'created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user', 'email')
        }),
        ('تاییدیه', {
            'fields': ('verification_code', 'is_verified', 'attempts')
        }),
        ('زمان‌بندی', {
            'fields': ('expires_at', 'created_at', 'updated_at')
        }),
    )

# --- FAQ Category Admin ---
@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    """مدیریت دسته‌بندی‌های سوالات متداول"""
    list_display = ['name', 'icon', 'order', 'is_active', 'get_faq_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_faq_count(self, obj):
        return obj.faqs.count()
    get_faq_count.short_description = 'تعداد سوالات'

# --- FAQ Admin ---
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """مدیریت سوالات متداول"""
    list_display = [
        'question_short', 'category', 'view_count', 'is_active', 
        'order', 'created_at'
    ]
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer', 'keywords']
    list_editable = ['is_active', 'order']
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات سوال', {
            'fields': ('category', 'question', 'order', 'is_active')
        }),
        ('پاسخ', {
            'fields': ('answer',)
        }),
        ('کلمات کلیدی', {
            'fields': ('keywords',)
        }),
        ('آمار', {
            'fields': ('view_count',)
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def question_short(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_short.short_description = 'سوال'

# --- Support Ticket Admin ---
@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    """مدیریت تیکت‌های پشتیبانی"""
    list_display = [
        'ticket_id', 'user', 'subject_short', 'category', 'priority', 
        'status', 'assigned_to', 'created_at'
    ]
    list_filter = ['category', 'priority', 'status', 'assigned_to', 'created_at']
    search_fields = ['ticket_id', 'subject', 'description', 'user__username']
    list_editable = ['status', 'assigned_to']
    readonly_fields = ['ticket_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات تیکت', {
            'fields': ('ticket_id', 'user', 'category', 'subject')
        }),
        ('محتوا', {
            'fields': ('description',)
        }),
        ('وضعیت', {
            'fields': ('priority', 'status', 'assigned_to')
        }),
        ('پیوست‌ها و برچسب‌ها', {
            'fields': ('attachments', 'tags'),
            'classes': ('collapse',)
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subject_short(self, obj):
        return obj.subject[:30] + '...' if len(obj.subject) > 30 else obj.subject
    subject_short.short_description = 'موضوع'

# --- Ticket Message Admin ---
@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    """مدیریت پیام‌های تیکت"""
    list_display = [
        'ticket', 'sender', 'message_type', 'content_short', 
        'is_internal', 'created_at'
    ]
    list_filter = ['message_type', 'is_internal', 'created_at']
    search_fields = ['content', 'ticket__ticket_id', 'sender__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات پیام', {
            'fields': ('ticket', 'sender', 'message_type', 'is_internal')
        }),
        ('محتوا', {
            'fields': ('content',)
        }),
        ('پیوست‌ها', {
            'fields': ('attachments',),
            'classes': ('collapse',)
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_short(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_short.short_description = 'محتوا'

# --- Ticket Template Admin ---
@admin.register(TicketTemplate)
class TicketTemplateAdmin(admin.ModelAdmin):
    """مدیریت قالب‌های پاسخ تیکت"""
    list_display = [
        'name', 'category', 'is_active', 'created_at'
    ]
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'content', 'keywords']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات قالب', {
            'fields': ('name', 'category', 'is_active')
        }),
        ('محتوا', {
            'fields': ('content',)
        }),
        ('کلمات کلیدی', {
            'fields': ('keywords',)
        }),
        ('آمار', {
            'fields': ()
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# --- تنظیمات Admin Site ---
admin.site.site_header = "مدیریت سیستم تحلیل فروشگاه چیدمانو"
admin.site.site_title = "چیدمانو - پنل مدیریت"
admin.site.index_title = "پنل مدیریت حرفه‌ای"

# Import dashboard
from .admin_dashboard import admin_dashboard_view


# ==================== سیستم کیف پول ====================

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'balance_display', 'is_active', 'created_at', 'updated_at'
    ]
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('اطلاعات کیف پول', {
            'fields': ('user', 'balance', 'is_active')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def balance_display(self, obj):
        return f"{obj.balance:,} تومان"
    balance_display.short_description = 'موجودی'
    balance_display.admin_order_field = 'balance'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'wallet_user', 'transaction_type', 'amount_display', 'status', 
        'description', 'created_at'
    ]
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = [
        'wallet__user__username', 'wallet__user__email', 
        'description', 'reference_id'
    ]
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('اطلاعات تراکنش', {
            'fields': ('wallet', 'transaction_type', 'amount', 'description')
        }),
        ('وضعیت و مرجع', {
            'fields': ('status', 'reference_id', 'order')
        }),
        ('موجودی پس از تراکنش', {
            'fields': ('balance_after',)
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def wallet_user(self, obj):
        return obj.wallet.user.username
    wallet_user.short_description = 'کاربر'
    wallet_user.admin_order_field = 'wallet__user__username'
    
    def amount_display(self, obj):
        return f"{obj.amount:,} تومان"
    amount_display.short_description = 'مبلغ'
    amount_display.admin_order_field = 'amount'
