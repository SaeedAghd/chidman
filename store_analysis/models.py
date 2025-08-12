from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.urls import reverse

# --- Choices Constants ---
STORE_TYPE_CHOICES = [
    ('supermarket', 'سوپرمارکت'),
    ('clothing', 'فروشگاه پوشاک'),
    ('appliance', 'لوازم خانگی'),
    ('bookstore', 'کتاب‌فروشی'),
    ('pharmacy', 'داروخانه'),
    ('other', 'سایر'),
]

DESIGN_STYLES = [
    ('traditional', 'سنتی'),
    ('modern', 'مدرن'),
    ('minimal', 'خلوت'),
    ('busy', 'شلوغ'),
    ('simple', 'ساده'),
    ('bright', 'پرنور'),
    ('dim', 'کم‌نور'),
]

UNUSED_AREA_TYPES = [
    ('empty', 'منطقه خالی'),
    ('low_traffic', 'کم‌ترافیک'),
    ('storage', 'انبار'),
    ('staff', 'فضای کارکنان'),
    ('other', 'سایر')
]

CUSTOMER_PATH_DIRECTIONS = [
    ('clockwise', 'ساعتگرد'),
    ('counterclockwise', 'پادساعتگرد'),
    ('mixed', 'مختلط')
]

PRODUCT_CATEGORY_CHOICES = [
    ('beverages', 'نوشیدنی'),
    ('food', 'خوراکی'),
    ('womens_clothing', 'پوشاک زنانه'),
    ('mens_clothing', 'پوشاک مردانه'),
    ('kids_clothing', 'پوشاک بچگانه'),
    ('electronics', 'الکترونیک'),
    ('home', 'لوازم خانگی'),
    ('beauty', 'آرایشی و بهداشتی'),
    ('books', 'کتاب'),
    ('pharmacy', 'دارویی'),
    ('other', 'سایر'),
]

# مدل اصلی تحلیل فروشگاه (کد کامل قبلی شما)
class StoreAnalysis(models.Model):
    STATUS_CHOICES = [
        ('pending', _('در انتظار')),
        ('processing', _('در حال پردازش')),
        ('completed', _('تکمیل شده')),
        ('failed', _('ناموفق')),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    store_name = models.CharField(max_length=200, verbose_name='نام فروشگاه')
    store_location = models.CharField(max_length=200, verbose_name='موقعیت فروشگاه', null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name='شهر', null=True, blank=True)
    area = models.CharField(max_length=100, verbose_name='منطقه', null=True, blank=True)
    store_type = models.CharField(max_length=50, choices=STORE_TYPE_CHOICES, verbose_name='نوع فروشگاه')
    store_size = models.PositiveIntegerField(verbose_name='متراژ فروشگاه (متر مربع)', null=True, blank=True)
    store_dimensions = models.CharField(max_length=200, verbose_name='ابعاد فروشگاه', null=True, blank=True)
    entrances = models.PositiveIntegerField(verbose_name='تعداد ورودی‌ها', null=True, blank=True)
    shelf_count = models.PositiveIntegerField(verbose_name='تعداد قفسه اصلی', null=True, blank=True)
    shelf_dimensions = models.TextField(verbose_name='ابعاد تقریبی هر قفسه', null=True, blank=True)
    shelf_contents = models.TextField(verbose_name='نوع محصولات هر قفسه', null=True, blank=True)
    checkout_location = models.TextField(verbose_name='محل صندوق‌های پرداخت', null=True, blank=True)
    unused_area_type = models.CharField(max_length=20, choices=UNUSED_AREA_TYPES, default='empty', verbose_name='نوع منطقه بلااستفاده', null=True, blank=True)
    unused_area_size = models.PositiveIntegerField(default=0, verbose_name='متراژ منطقه بلااستفاده')
    unused_area_reason = models.TextField(default='', verbose_name='دلیل بلااستفاده بودن')
    unused_areas = models.TextField(verbose_name='توضیحات تکمیلی مناطق بلااستفاده', null=True, blank=True)
    product_categories = models.JSONField(verbose_name='دسته‌بندی محصولات', null=True, blank=True)
    top_products = models.TextField(verbose_name='پرفروش‌ترین محصولات', null=True, blank=True)
    sales_volume = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='حجم فروش روزانه', null=True, blank=True)
    pos_system = models.CharField(max_length=100, verbose_name='نرم‌افزار صندوق', blank=True)
    sales_file = models.FileField(upload_to='sales_files/', verbose_name='فایل فروش', null=True, blank=True)
    has_surveillance = models.BooleanField(default=False, verbose_name='دوربین نظارتی')
    camera_count = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد دوربین‌ها')
    camera_locations = models.TextField(null=True, blank=True, verbose_name='موقعیت دوربین‌ها')
    camera_coverage = models.TextField(null=True, blank=True, verbose_name='مناطق تحت پوشش')
    video_duration = models.PositiveIntegerField(null=True, blank=True, verbose_name='مدت زمان ویدیو')
    video_date = models.DateField(null=True, blank=True, verbose_name='تاریخ ضبط ویدیو')
    video_time = models.TimeField(null=True, blank=True, verbose_name='ساع�� ضبط ویدیو')
    customer_video_file = models.FileField(upload_to='customer_videos/', verbose_name='ویدیوی مسیر مشتری', null=True, blank=True)
    customer_path_notes = models.TextField(verbose_name='توضیحات تکمیلی', null=True, blank=True)
    customer_movement_paths = models.CharField(max_length=20, choices=[('clockwise', 'ساعتگرد'), ('counterclockwise', 'پادساعتگرد'), ('mixed', 'مختلط'), ('random', 'تصادفی')], default='mixed', verbose_name='مسیر معمول حرکت مشتریان')
    high_traffic_areas = models.TextField(verbose_name='مناطق پرتردد', null=True, blank=True)
    peak_hours = models.CharField(max_length=100, verbose_name='ساعات پیک فروش', null=True, blank=True)
    design_style = models.CharField(max_length=50, choices=DESIGN_STYLES, verbose_name='سبک طراحی', null=True, blank=True)
    brand_colors = models.CharField(max_length=200, verbose_name='رنگ‌های اصلی', null=True, blank=True)
    decorative_elements = models.TextField(verbose_name='عناصر دکوراتیو', blank=True)
    layout_restrictions = models.TextField(verbose_name='محدودیت‌های چیدمان', blank=True)
    store_plan = models.FileField(upload_to='store_plans/', validators=[FileExtensionValidator(['jpg', 'pdf', 'dwg'])], verbose_name='نقشه فروشگاه', null=True, blank=True)
    store_photos = models.FileField(upload_to='store_photos/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])], verbose_name='عکس‌های فروشگاه', null=True, blank=True)
    product_catalog = models.FileField(upload_to='product_catalogs/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])], verbose_name='کاتالوگ محصولات', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('وضعیت'))
    results = models.JSONField(null=True, blank=True, verbose_name=_('نتایج'))
    error_message = models.TextField(blank=True, null=True, verbose_name=_('پیام خطا'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ به‌روزرسانی'))
    def __str__(self):
        return f"{self.store_name} - {self.city}"
    class Meta:
        verbose_name = _('تحلیل فروشگاه')
        verbose_name_plural = _('تحلیل‌های فروشگاه')
        ordering = ['-created_at']

class StoreAnalysisResult(models.Model):
    store_analysis = models.OneToOneField(StoreAnalysis, on_delete=models.CASCADE, related_name='analysis_result')
    overall_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='امتیاز کلی')
    layout_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='امتیاز چیدمان')
    traffic_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='امتیاز ترافیک')
    design_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='امتیاز طراحی')
    sales_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='امتیاز فروش')
    layout_analysis = models.TextField(verbose_name='تحلیل چیدمان')
    traffic_analysis = models.TextField(verbose_name='تحلیل ترافیک')
    design_analysis = models.TextField(verbose_name='تحلیل طراحی')
    sales_analysis = models.TextField(verbose_name='تحلیل فروش')
    overall_analysis = models.TextField(verbose_name='تحلیل کلی')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"تحلیل {self.store_analysis.store_name} - امتیاز: {self.overall_score}"
    class Meta:
        verbose_name = 'نتیجه تحلیل'
        verbose_name_plural = 'نتایج تحلیل'
        ordering = ['-created_at']

class DetailedAnalysis(models.Model):
    store_analysis = models.OneToOneField(StoreAnalysis, on_delete=models.CASCADE, related_name='detailed_analysis_data', verbose_name='تحلیل فروشگاه')
    traffic_analysis = models.JSONField(verbose_name='تحلیل ترافیک')
    layout_analysis = models.JSONField(verbose_name='تحلیل چیدمان')
    customer_behavior = models.JSONField(verbose_name='رفتار مشتری')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    class Meta:
        verbose_name = 'تحلیل تکمیلی'
        verbose_name_plural = 'تحلیل‌های تکمیلی'
    def __str__(self):
        return f"تحلیل تکمیلی {self.store_analysis}"

class Cache(models.Model):
    CACHE_TYPES = [
        ('analysis_results', 'نتایج تحلیل'),
        ('user_analyses', 'تحلیل‌های کاربر'),
        ('statistics', 'آمار'),
        ('api_response', 'پاسخ API'),
    ]
    key = models.CharField(max_length=255, unique=True, verbose_name='کلید کش')
    value = models.JSONField(verbose_name='مقدار کش')
    cache_type = models.CharField(max_length=50, choices=CACHE_TYPES, verbose_name='نوع کش')
    expires_at = models.DateTimeField(verbose_name='تاریخ انقضا')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    class Meta:
        verbose_name = 'کش'
        verbose_name_plural = 'کش‌ها'
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['cache_type']),
            models.Index(fields=['expires_at']),
        ]
    def __str__(self):
        return f"{self.cache_type}: {self.key}"
    def is_expired(self):
        return timezone.now() > self.expires_at
    @classmethod
    def get_cache(cls, key, cache_type=None):
        try:
            cache_obj = cls.objects.get(key=key)
            if cache_obj.is_expired():
                cache_obj.delete()
                return None
            return cache_obj.value
        except cls.DoesNotExist:
            return None
    @classmethod
    def set_cache(cls, key, value, cache_type, expires_in_minutes=60):
        expires_at = timezone.now() + timezone.timedelta(minutes=expires_in_minutes)
        cls.objects.update_or_create(
            key=key,
            defaults={
                'value': value,
                'cache_type': cache_type,
                'expires_at': expires_at,
            }
        )
    @classmethod
    def clear_expired(cls):
        cls.objects.filter(expires_at__lt=timezone.now()).delete()
    @classmethod
    def clear_by_type(cls, cache_type):
        cls.objects.filter(cache_type=cache_type).delete()

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('completed', 'پرداخت شده'),
        ('failed', 'ناموفق'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('online', 'پرداخت آنلاین'),
        ('wallet', 'کیف پول'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    store_analysis = models.ForeignKey('StoreAnalysis', on_delete=models.CASCADE, related_name='payments', null=True, blank=True, verbose_name='تحلیل فروشگاه')
    amount = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='مبلغ (تومان)')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='online', verbose_name='روش پرداخت')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name='وضعیت پرداخت')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='شناسه تراکنش')
    def __str__(self):
        return f"پرداخت {self.user.username} - {self.amount} تومان"
    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت‌ها'
        ordering = ['-created_at']

# --- کتابخانه مقالات ---
class ArticleCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='دسته‌بندی')
    slug = models.SlugField(unique=True, verbose_name='اسلاگ')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    class Meta:
        verbose_name = 'دسته‌بندی مقاله'
        verbose_name_plural = 'دسته‌بندی‌های مقاله'
    def __str__(self):
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان مقاله')
    slug = models.SlugField(unique=True, verbose_name='اسلاگ')
    summary = models.TextField(verbose_name='خلاصه')
    content = models.TextField(verbose_name='متن کامل مقاله')
    author = models.CharField(max_length=100, verbose_name='نویسنده/مترجم')
    source_url = models.URLField(verbose_name='لینک منبع اصلی', blank=True)
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name='دسته‌بندی')
    tags = models.CharField(max_length=200, blank=True, verbose_name='برچسب‌ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    is_featured = models.BooleanField(default=False, verbose_name='مقاله ویژه')
    views = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')
    image = models.ImageField(upload_to='article_images/', null=True, blank=True, verbose_name='تصویر مقاله')
    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-created_at']
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('store_analysis:article_detail', args=[self.slug])
