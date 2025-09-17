from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator, RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
import re
import os
import uuid

# --- Custom Validators ---
def validate_store_name(value):
    """اعتبارسنجی نام فروشگاه"""
    if len(value.strip()) < 3:
        raise ValidationError('نام فروشگاه باید حداقل 3 کاراکتر باشد')
    if not re.match(r'^[\u0600-\u06FF\w\s\-\.]+$', value):
        raise ValidationError('نام فروشگاه فقط می‌تواند شامل حروف فارسی، انگلیسی، اعداد و خط تیره باشد')

def validate_file_size(value):
    """اعتبارسنجی اندازه فایل (حداکثر 10MB)"""
    filesize = value.size
    if filesize > 10 * 1024 * 1024:  # 10MB
        raise ValidationError('حجم فایل نمی‌تواند بیشتر از 10 مگابایت باشد')

def validate_image_dimensions(value):
    """اعتبارسنجی ابعاد تصویر"""
    from PIL import Image
    img = Image.open(value)
    width, height = img.size
    if width > 4000 or height > 4000:
        raise ValidationError('ابعاد تصویر نمی‌تواند بیشتر از 4000x4000 پیکسل باشد')

# --- Choices Constants ---
STORE_TYPE_CHOICES = [
    ('supermarket', 'سوپرمارکت'),
    ('hypermarket', 'هایپرمارکت'),
    ('clothing', 'فروشگاه پوشاک'),
    ('appliance', 'لوازم خانگی'),
    ('bookstore', 'کتاب‌فروشی'),
    ('pharmacy', 'داروخانه'),
    ('electronics', 'الکترونیک'),
    ('jewelry', 'جواهرات'),
    ('sports', 'ورزشی'),
    ('beauty', 'آرایشی و بهداشتی'),
    ('other', 'سایر'),
]

DESIGN_STYLES = [
    ('traditional', 'سنتی'),
    ('modern', 'مدرن'),
    ('minimal', 'مینیمال'),
    ('luxury', 'لوکس'),
    ('industrial', 'صنعتی'),
    ('scandinavian', 'اسکاندیناوی'),
    ('vintage', 'کلاسیک'),
    ('contemporary', 'معاصر'),
    ('other', 'سایر'),
]

UNUSED_AREA_TYPES = [
    ('empty', 'منطقه خالی'),
    ('low_traffic', 'کم‌ترافیک'),
    ('storage', 'انبار'),
    ('staff', 'فضای کارکنان'),
    ('maintenance', 'نگهداری'),
    ('delivery', 'تحویل'),
    ('other', 'سایر')
]

CUSTOMER_PATH_DIRECTIONS = [
    ('clockwise', 'ساعتگرد'),
    ('counterclockwise', 'پادساعتگرد'),
    ('mixed', 'مختلط'),
    ('random', 'تصادفی'),
    ('direct', 'مستقیم'),
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
    ('sports', 'ورزشی'),
    ('jewelry', 'جواهرات'),
    ('other', 'سایر'),
]

# --- Abstract Base Models ---
class TimestampedModel(models.Model):
    """مدل پایه با timestamp"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ به‌روزرسانی'))

    class Meta:
        abstract = True

class UserOwnedModel(models.Model):
    """مدل پایه متعلق به کاربر"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('کاربر'))

    class Meta:
        abstract = True

# --- مدل پایه برای اطلاعات فروشگاه ---
class StoreBasicInfo(UserOwnedModel, TimestampedModel):
    """اطلاعات پایه فروشگاه"""
    store_name = models.CharField(
        max_length=200, 
        verbose_name='نام فروشگاه',
        validators=[validate_store_name],
        help_text='نام کامل فروشگاه (حداقل 3 کاراکتر)'
    )
    store_location = models.CharField(
        max_length=500, 
        verbose_name='آدرس کامل فروشگاه',
        help_text='آدرس دقیق فروشگاه'
    )
    city = models.CharField(
        max_length=100, 
        verbose_name='شهر',
        help_text='شهر محل فروشگاه'
    )
    area = models.CharField(
        max_length=100, 
        verbose_name='منطقه',
        help_text='منطقه یا محله فروشگاه'
    )
    store_type = models.CharField(
        max_length=50, 
        choices=STORE_TYPE_CHOICES, 
        verbose_name='نوع فروشگاه'
    )
    store_size = models.PositiveIntegerField(
        verbose_name='متراژ فروشگاه (متر مربع)',
        validators=[MinValueValidator(10), MaxValueValidator(100000)],
        help_text='متراژ کل فروشگاه (10 تا 100,000 متر مربع)'
    )
    store_dimensions = models.CharField(
        max_length=200, 
        verbose_name='ابعاد فروشگاه',
        help_text='ابعاد تقریبی (مثال: 20×30 متر)'
    )
    phone = models.CharField(
        max_length=20, 
        verbose_name='شماره تماس',
        validators=[RegexValidator(r'^[\d\-\+\(\)\s]+$', 'شماره تماس نامعتبر است')],
        blank=True
    )
    email = models.EmailField(
        verbose_name='ایمیل',
        blank=True,
        help_text='ایمیل برای ارسال گزارش‌ها'
    )
    establishment_year = models.PositiveIntegerField(
        verbose_name='سال تاسیس',
        validators=[MinValueValidator(1300), MaxValueValidator(1450)],
        blank=True,
        null=True,
        help_text='سال تاسیس فروشگاه (1300 تا 1450)'
    )

    def __str__(self):
        return f"{self.store_name} - {self.city}"

    def clean(self):
        """اعتبارسنجی سفارشی"""
        super().clean()
        if self.store_size and self.store_dimensions:
            # بررسی تناسب متراژ و ابعاد
            try:
                dimensions = re.findall(r'\d+', self.store_dimensions)
                if len(dimensions) >= 2:
                    calculated_size = int(dimensions[0]) * int(dimensions[1])
                    if abs(calculated_size - self.store_size) > calculated_size * 0.2:
                        raise ValidationError('متراژ و ابعاد فروشگاه همخوانی ندارند')
            except (ValueError, IndexError):
                pass

    class Meta:
        verbose_name = 'اطلاعات پایه فروشگاه'
        verbose_name_plural = 'اطلاعات پایه فروشگاه‌ها'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'store_type']),
            models.Index(fields=['city', 'area']),
            models.Index(fields=['created_at']),
        ]

# --- مدل چیدمان فروشگاه ---
class StoreLayout(TimestampedModel):
    """اطلاعات چیدمان فروشگاه"""
    store_info = models.OneToOneField(StoreBasicInfo, on_delete=models.CASCADE, related_name='layout')
    entrances = models.PositiveIntegerField(
        verbose_name='تعداد ورودی‌ها',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='تعداد ورودی‌های فروشگاه (1 تا 10)'
    )
    shelf_count = models.PositiveIntegerField(
        verbose_name='تعداد قفسه اصلی',
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        help_text='تعداد قفسه‌های اصلی فروشگاه'
    )
    shelf_dimensions = models.TextField(
        verbose_name='ابعاد تقریبی هر قفسه',
        help_text='ابعاد و مشخصات قفسه‌ها'
    )
    shelf_contents = models.TextField(
        verbose_name='نوع محصولات هر قفسه',
        help_text='توضیح محصولات موجود در هر قفسه'
    )
    checkout_location = models.TextField(
        verbose_name='محل صندوق‌های پرداخت',
        help_text='موقعیت و تعداد صندوق‌های پرداخت'
    )
    unused_area_type = models.CharField(
        max_length=20, 
        choices=UNUSED_AREA_TYPES, 
        default='empty', 
        verbose_name='نوع منطقه بلااستفاده'
    )
    unused_area_size = models.PositiveIntegerField(
        default=0, 
        verbose_name='متراژ منطقه بلااستفاده',
        validators=[MaxValueValidator(100000)],
        help_text='متراژ مناطق بلااستفاده یا کم‌ترافیک'
    )
    unused_area_reason = models.TextField(
        default='', 
        verbose_name='دلیل بلااستفاده بودن',
        help_text='توضیح دلیل بلااستفاده بودن مناطق'
    )
    unused_areas = models.TextField(
        verbose_name='توضیحات تکمیلی مناطق بلااستفاده',
        help_text='توضیح دقیق مناطق بلااستفاده'
    )
    layout_restrictions = models.TextField(
        verbose_name='محدودیت‌های چیدمان',
        help_text='محدودیت‌های موجود در چیدمان فروشگاه',
        blank=True
    )
    store_plan = models.FileField(
        upload_to='store_plans/',
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png', 'pdf', 'dwg']),
            validate_file_size
        ],
        verbose_name='نقشه فروشگاه',
        help_text='فایل نقشه یا طرح فروشگاه (حداکثر 10MB)',
        blank=True
    )
    store_photos = models.ImageField(
        upload_to='store_photos/',
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png']),
            validate_file_size,
            validate_image_dimensions
        ],
        verbose_name='عکس‌های فروشگاه',
        help_text='عکس‌های فروشگاه (حداکثر 10MB، 4000x4000 پیکسل)',
        blank=True
    )

    def clean(self):
        """اعتبارسنجی سفارشی"""
        super().clean()
        if self.unused_area_size and self.store_info:
            if self.unused_area_size > self.store_info.store_size:
                raise ValidationError('منطقه بلااستفاده نمی‌تواند بزرگتر از کل فروشگاه باشد')

    class Meta:
        verbose_name = 'چیدمان فروشگاه'
        verbose_name_plural = 'چیدمان‌های فروشگاه'
        indexes = [
            models.Index(fields=['unused_area_type']),
        ]

# --- مدل ترافیک و رفتار مشتری ---
class StoreTraffic(TimestampedModel):
    """اطلاعات ترافیک و رفتار مشتری"""
    store_info = models.OneToOneField(StoreBasicInfo, on_delete=models.CASCADE, related_name='traffic')
    customer_traffic = models.CharField(
        max_length=20, 
        choices=[
            ('low', 'کم (کمتر از 50 نفر در روز)'),
            ('medium', 'متوسط (50-200 نفر در روز)'),
            ('high', 'زیاد (200-500 نفر در روز)'),
            ('very_high', 'خیلی زیاد (بیش از 500 نفر در روز)'),
        ],
        verbose_name='ترافیک مشتری'
    )
    peak_hours = models.CharField(
        max_length=200, 
        verbose_name='ساعات پیک فروش',
        help_text='ساعات شلوغی فروشگاه (مثال: 18-22)'
    )
    customer_movement_paths = models.CharField(
        max_length=20, 
        choices=CUSTOMER_PATH_DIRECTIONS, 
        default='mixed', 
        verbose_name='مسیر معمول حرکت مشتریان'
    )
    high_traffic_areas = models.TextField(
        verbose_name='مناطق پرتردد',
        help_text='مناطقی که بیشترین ترافیک را دارند'
    )
    customer_path_notes = models.TextField(
        verbose_name='توضیحات تکمیلی',
        help_text='توضیحات بیشتر درباره رفتار مشتریان',
        blank=True
    )
    has_customer_video = models.BooleanField(
        default=False, 
        verbose_name='آیا ویدیوی مسیر مشتری دارید؟'
    )
    video_duration = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name='مدت زمان ویدیو (ثانیه)',
        validators=[MaxValueValidator(3600)],
        help_text='مدت زمان ویدیوی مسیر مشتری (حداکثر 1 ساعت)'
    )
    video_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name='تاریخ ضبط ویدیو'
    )
    video_time = models.TimeField(
        null=True, 
        blank=True, 
        verbose_name='ساعت ضبط ویدیو'
    )
    customer_video_file = models.FileField(
        upload_to='customer_videos/',
        validators=[
            FileExtensionValidator(['mp4', 'avi', 'mov', 'mkv']),
            validate_file_size
        ],
        verbose_name='ویدیوی مسیر مشتری',
        help_text='فایل ویدیوی مسیر مشتری (حداکثر 10MB)',
        blank=True
    )

    def clean(self):
        """اعتبارسنجی سفارشی"""
        super().clean()
        if self.has_customer_video and not self.customer_video_file:
            raise ValidationError('در صورت داشتن ویدیو، فایل ویدیو الزامی است')

    class Meta:
        verbose_name = 'ترافیک فروشگاه'
        verbose_name_plural = 'ترافیک‌های فروشگاه'
        indexes = [
            models.Index(fields=['customer_traffic']),
            models.Index(fields=['customer_movement_paths']),
        ]

# --- مدل طراحی و دکوراسیون ---
class StoreDesign(TimestampedModel):
    """اطلاعات طراحی و دکوراسیون"""
    store_info = models.OneToOneField(StoreBasicInfo, on_delete=models.CASCADE, related_name='design')
    design_style = models.CharField(
        max_length=50, 
        choices=DESIGN_STYLES, 
        verbose_name='سبک طراحی'
    )
    brand_colors = models.CharField(
        max_length=200, 
        verbose_name='رنگ‌های اصلی',
        help_text='رنگ‌های اصلی برند و دکوراسیون'
    )
    decorative_elements = models.TextField(
        verbose_name='عناصر دکوراتیو',
        help_text='عناصر تزئینی و دکوراتیو فروشگاه',
        blank=True
    )
    main_lighting = models.CharField(
        max_length=20, 
        choices=[
            ('natural', 'طبیعی (نور خورشید)'),
            ('artificial', 'مصنوعی (لامپ)'),
            ('mixed', 'ترکیبی (طبیعی + مصنوعی)'),
        ],
        verbose_name='نورپردازی اصلی'
    )
    lighting_intensity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'کم'),
            ('medium', 'متوسط'),
            ('high', 'زیاد'),
        ],
        verbose_name='شدت نورپردازی',
        default='medium'
    )
    color_temperature = models.CharField(
        max_length=20,
        choices=[
            ('warm', 'گرم (زرد)'),
            ('neutral', 'خنثی (سفید)'),
            ('cool', 'سرد (آبی)'),
        ],
        verbose_name='دمای رنگ نور',
        default='neutral'
    )

    class Meta:
        verbose_name = 'طراحی فروشگاه'
        verbose_name_plural = 'طراحی‌های فروشگاه'
        indexes = [
            models.Index(fields=['design_style']),
            models.Index(fields=['main_lighting']),
        ]

# --- مدل نظارت و امنیت ---
class StoreSurveillance(TimestampedModel):
    """اطلاعات نظارت و امنیت"""
    store_info = models.OneToOneField(StoreBasicInfo, on_delete=models.CASCADE, related_name='surveillance')
    has_surveillance = models.BooleanField(
        default=False, 
        verbose_name='دوربین نظارتی'
    )
    camera_count = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name='تعداد دوربین‌ها',
        validators=[MaxValueValidator(100)],
        help_text='تعداد دوربین‌های نظارتی (حداکثر 100)'
    )
    camera_locations = models.TextField(
        null=True, 
        blank=True, 
        verbose_name='موقعیت دوربین‌ها',
        help_text='توضیح موقعیت نصب دوربین‌ها'
    )
    camera_coverage = models.TextField(
        null=True, 
        blank=True, 
        verbose_name='مناطق تحت پوشش',
        help_text='مناطقی که تحت پوشش دوربین‌ها هستند'
    )
    recording_quality = models.CharField(
        max_length=20,
        choices=[
            ('low', 'کم (480p)'),
            ('medium', 'متوسط (720p)'),
            ('high', 'زیاد (1080p)'),
            ('ultra', 'خیلی زیاد (4K)'),
        ],
        verbose_name='کیفیت ضبط',
        default='medium'
    )
    storage_duration = models.PositiveIntegerField(
        verbose_name='مدت نگهداری فیلم (روز)',
        default=30,
        validators=[MinValueValidator(1), MaxValueValidator(365)],
        help_text='مدت نگهداری فیلم‌های دوربین (1 تا 365 روز)'
    )

    def clean(self):
        """اعتبارسنجی سفارشی"""
        super().clean()
        if self.has_surveillance and not self.camera_count:
            raise ValidationError('در صورت داشتن دوربین، تعداد دوربین‌ها الزامی است')

    class Meta:
        verbose_name = 'نظارت فروشگاه'
        verbose_name_plural = 'نظارت‌های فروشگاه'
        indexes = [
            models.Index(fields=['has_surveillance']),
        ]

# --- مدل محصولات و فروش ---
class StoreProducts(TimestampedModel):
    """اطلاعات محصولات و فروش"""
    store_info = models.OneToOneField(StoreBasicInfo, on_delete=models.CASCADE, related_name='products')
    product_categories = models.JSONField(
        verbose_name='دسته‌بندی محصولات',
        help_text='دسته‌بندی محصولات فروشگاه',
        blank=True
    )
    top_products = models.TextField(
        verbose_name='پرفروش‌ترین محصولات',
        help_text='لیست محصولات پرفروش',
        blank=True
    )
    sales_volume = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0, 
        verbose_name='حجم فروش روزانه (تومان)',
        help_text='متوسط فروش روزانه فروشگاه'
    )
    pos_system = models.CharField(
        max_length=100, 
        verbose_name='نرم‌افزار صندوق',
        help_text='نام نرم‌افزار صندوق فروش',
        blank=True
    )
    sales_file = models.FileField(
        upload_to='sales_files/',
        validators=[
            FileExtensionValidator(['xlsx', 'xls', 'csv', 'pdf']),
            validate_file_size
        ],
        verbose_name='فایل فروش',
        help_text='فایل گزارش فروش (حداکثر 10MB)',
        blank=True
    )
    product_catalog = models.FileField(
        upload_to='product_catalogs/',
        validators=[
            FileExtensionValidator(['pdf', 'doc', 'docx']),
            validate_file_size
        ],
        verbose_name='کاتالوگ محصولات',
        help_text='فایل کاتالوگ محصولات (حداکثر 10MB)',
        blank=True
    )
    inventory_system = models.CharField(
        max_length=100,
        verbose_name='سیستم موجودی',
        help_text='نرم‌افزار مدیریت موجودی',
        blank=True
    )
    supplier_count = models.PositiveIntegerField(
        verbose_name='تعداد تامین‌کنندگان',
        default=0,
        validators=[MaxValueValidator(1000)],
        help_text='تعداد تامین‌کنندگان محصولات'
    )

    class Meta:
        verbose_name = 'محصولات فروشگاه'
        verbose_name_plural = 'محصولات فروشگاه‌ها'
        indexes = [
            models.Index(fields=['sales_volume']),
        ]

# --- مدل اصلی تحلیل فروشگاه (ساده شده) ---
class StoreAnalysis(TimestampedModel):
    """مدل اصلی تحلیل فروشگاه - ساده شده"""
    STATUS_CHOICES = [
        ('pending', _('در انتظار')),
        ('preliminary_completed', _('پیش‌تحلیل تکمیل شده')),
        ('processing', _('در حال پردازش')),
        ('completed', _('تکمیل شده')),
        ('failed', _('ناموفق')),
        ('cancelled', _('لغو شده')),
    ]
    
    ANALYSIS_TYPE_CHOICES = [
        ('quick_free', _('تحلیل رایگان سریع')),
        ('comprehensive', _('تحلیل جامع')),
        ('ai_enhanced', _('تحلیل هوشمند')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('کاربر'))
    store_info = models.OneToOneField(StoreBasicInfo, on_delete=models.CASCADE, related_name='analysis', null=True, blank=True)
    analysis_type = models.CharField(
        max_length=20,
        choices=ANALYSIS_TYPE_CHOICES,
        default='quick_free',
        verbose_name=_('نوع تحلیل')
    )
    store_name = models.CharField(
        max_length=200,
        verbose_name=_('نام فروشگاه'),
        null=True,
        blank=True
    )
    store_type = models.CharField(
        max_length=50,
        choices=STORE_TYPE_CHOICES,
        verbose_name=_('نوع فروشگاه'),
        null=True,
        blank=True
    )
    store_size = models.CharField(
        max_length=50,
        verbose_name=_('اندازه فروشگاه'),
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=25, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name=_('وضعیت')
    )
    preliminary_analysis = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('پیش‌تحلیل'),
        help_text='تحلیل اولیه که بلافاصله پس از پرداخت نمایش داده می‌شود'
    )
    results = models.JSONField(
        null=True, 
        blank=True, 
        verbose_name=_('نتایج'),
        help_text='نتایج تحلیل به صورت JSON'
    )
    error_message = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_('پیام خطا'),
        help_text='پیام خطا در صورت عدم موفقیت'
    )
    priority = models.CharField(
        max_length=20,
        choices=[
            ('low', 'کم'),
            ('medium', 'متوسط'),
            ('high', 'زیاد'),
            ('urgent', 'فوری'),
        ],
        default='medium',
        verbose_name='اولویت تحلیل'
    )
    estimated_duration = models.PositiveIntegerField(
        verbose_name='مدت زمان تخمینی (دقیقه)',
        default=30,
        help_text='مدت زمان تخمینی برای تکمیل تحلیل'
    )
    actual_duration = models.PositiveIntegerField(
        verbose_name='مدت زمان واقعی (دقیقه)',
        null=True,
        blank=True,
        help_text='مدت زمان واقعی صرف شده برای تحلیل'
    )
    analysis_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_('داده‌های تحلیل'),
        help_text='داده‌های ارسالی از فرم'
    )
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='analyses', verbose_name='سفارش')

    def __str__(self):
        store_name = self.store_name or (self.store_info.store_name if self.store_info else 'نامشخص')
        return f"تحلیل {store_name} - {self.get_status_display()}"
    
    def get_absolute_url(self):
        return reverse('store_analysis:analysis_detail', args=[self.pk])
    
    def get_analysis_data(self):
        """دریافت داده‌های تحلیل"""
        if self.analysis_data:
            return self.analysis_data
        return {}
    
    def set_analysis_data(self, data):
        """تنظیم داده‌های تحلیل"""
        self.analysis_data = data
        self.save()
    
    @property
    def is_completed(self):
        return self.status == 'completed'
    
    @property
    def is_processing(self):
        return self.status == 'processing'
    
    @property
    def is_failed(self):
        return self.status == 'failed'
    
    @property
    def has_preliminary(self):
        return bool(self.preliminary_analysis)
    
    @property
    def has_results(self):
        """بررسی وجود نتایج تحلیل"""
        return bool(self.results) or hasattr(self, 'analysis_result')
    
    @property
    def can_generate_report(self):
        """بررسی امکان تولید گزارش"""
        return (self.status == 'completed' or 
                self.has_results or 
                self.has_preliminary or
                hasattr(self, 'analysis_result'))
    
    def get_analysis_duration(self):
        """محاسبه مدت زمان تحلیل"""
        if self.status == 'completed' and hasattr(self, 'analysis_result'):
            return (self.analysis_result.created_at - self.created_at).total_seconds()
        return None
    
    def get_progress(self):
        """درصد پیشرفت تحلیل"""
        if self.status == 'completed':
            return 100
        elif self.status == 'preliminary_completed':
            return 25
        elif self.status == 'processing':
            return 50
        elif self.status == 'failed':
            return 0
        elif self.status == 'cancelled':
            return 0
        return 10
    
    def clean(self):
        """اعتبارسنجی سفارشی"""
        super().clean()
        if self.actual_duration and self.estimated_duration:
            if self.actual_duration > self.estimated_duration * 3:
                raise ValidationError('مدت زمان واقعی نمی‌تواند بیش از 3 برابر مدت تخمینی باشد')

    class Meta:
        verbose_name = _('تحلیل فروشگاه')
        verbose_name_plural = _('تحلیل‌های فروشگاه')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['created_at']),
            models.Index(fields=['analysis_type']),
        ]
        permissions = [
            ("can_cancel_analysis", "Can cancel analysis"),
            ("can_prioritize_analysis", "Can prioritize analysis"),
        ]

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
        try:
            store_name = self.store_analysis.store_info.store_name if self.store_analysis and self.store_analysis.store_info else "نامشخص"
            return f"تحلیل {store_name} - امتیاز: {self.overall_score}"
        except:
            return f"تحلیل - امتیاز: {self.overall_score}"
    
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

class StoreAnalysisDetail(models.Model):
    store_analysis = models.ForeignKey('StoreAnalysis', on_delete=models.CASCADE, related_name='details', verbose_name='تحلیل فروشگاه')
    description = models.TextField(verbose_name='توضیحات')
    recommendations = models.TextField(verbose_name='توصیه‌ها', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'جزئیات تحلیل فروشگاه'
        verbose_name_plural = 'جزئیات تحلیل‌های فروشگاه'
        ordering = ['-created_at']

    def __str__(self):
        return f"جزئیات {self.store_analysis.store_info.store_name}"

class PricingPlan(models.Model):
    """مدل پلن‌های قیمت‌گذاری"""
    PLAN_TYPES = [
        ('one_time', 'تحلیل یکباره'),
        ('monthly', 'پلن ماهیانه'),
        ('yearly', 'پلن سالیانه'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="نام پلن")
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, verbose_name="نوع پلن")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت (تومان)")
    original_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت اصلی")
    discount_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="درصد تخفیف")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    features = models.JSONField(default=list, verbose_name="ویژگی‌ها")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "پلن قیمت‌گذاری"
        verbose_name_plural = "پلن‌های قیمت‌گذاری"
    
    def __str__(self):
        return f"{self.name} - {self.price:,} تومان"

class DiscountCode(models.Model):
    """مدل کدهای تخفیف"""
    DISCOUNT_TYPES = [
        ('percentage', 'درصدی'),
        ('fixed', 'مبلغ ثابت'),
        ('seasonal', 'فصلی'),
        ('event', 'مناسبتی'),
    ]
    
    EVENT_TYPES = [
        ('opening', 'افتتاحیه'),
        ('spring', 'بهار'),
        ('summer', 'تابستان'),
        ('autumn', 'پاییز'),
        ('winter', 'زمستان'),
        ('nowruz', 'نوروز'),
        ('yalda', 'شب یلدا'),
        ('ramadan', 'رمضان'),
        ('black_friday', 'جمعه سیاه'),
        ('new_year', 'سال نو'),
    ]
    
    code = models.CharField(max_length=50, unique=True, verbose_name="کد تخفیف")
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, default='percentage', verbose_name="نوع تخفیف")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, blank=True, null=True, verbose_name="نوع مناسبت")
    percentage = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(70)], verbose_name="درصد تخفیف")
    fixed_amount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="مبلغ ثابت")
    max_usage = models.PositiveIntegerField(default=100, verbose_name="حداکثر استفاده")
    used_count = models.PositiveIntegerField(default=0, verbose_name="تعداد استفاده شده")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    valid_from = models.DateTimeField(verbose_name="اعتبار از")
    valid_until = models.DateTimeField(verbose_name="اعتبار تا")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"
    
    def __str__(self):
        return f"{self.code} - {self.percentage}% تخفیف"
    
    def is_valid(self):
        """بررسی اعتبار کد تخفیف"""
        from django.utils import timezone
        now = timezone.now()
        return (
            self.is_active and
            self.used_count < self.max_usage and
            self.valid_from <= now <= self.valid_until
        )
    
    def can_use(self):
        """بررسی امکان استفاده از کد تخفیف"""
        return self.is_valid()
    
    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"
    
    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"

class Order(models.Model):
    """مدل سفارش"""
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('completed', 'تکمیل شده'),
        ('failed', 'ناموفق'),
    ]
    
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name="شناسه سفارش")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE, null=True, blank=True, verbose_name="پلن انتخاب شده")
    original_amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="مبلغ اصلی")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="مبلغ تخفیف")
    final_amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="مبلغ نهایی")
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کد تخفیف")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    payment_method = models.CharField(max_length=50, blank=True, verbose_name="روش پرداخت")
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name="شناسه تراکنش")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
    
    def __str__(self):
        return f"سفارش {self.order_id} - {self.user.username}"

class AnalysisRequest(models.Model):
    """مدل درخواست تحلیل"""
    STATUS_CHOICES = [
        ('pending', 'در انتظار پردازش'),
        ('processing', 'در حال پردازش'),
        ('completed', 'تکمیل شده'),
        ('failed', 'ناموفق'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="سفارش")
    store_analysis_data = models.JSONField(verbose_name="داده‌های تحلیل فروشگاه")
    initial_analysis = models.TextField(blank=True, verbose_name="تحلیل اولیه")
    ai_analysis = models.TextField(blank=True, verbose_name="تحلیل هوش مصنوعی")
    ai_analysis_results = models.JSONField(blank=True, null=True, verbose_name="نتایج تحلیل هوش مصنوعی")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    estimated_completion = models.DateTimeField(null=True, blank=True, verbose_name="زمان تخمینی تکمیل")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان تکمیل")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "درخواست تحلیل"
        verbose_name_plural = "درخواست‌های تحلیل"
    
    def __str__(self):
        return f"تحلیل {self.order.order_id} - {self.status}"

class PromotionalBanner(models.Model):
    """مدل بنر تبلیغاتی تخفیف"""
    title = models.CharField(max_length=200, verbose_name="عنوان")
    subtitle = models.CharField(max_length=300, verbose_name="زیرعنوان")
    discount_percentage = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name="درصد تخفیف")
    discount_text = models.CharField(max_length=100, default="تخفیف", verbose_name="متن تخفیف")
    background_color = models.CharField(max_length=7, default="#FF6B6B", verbose_name="رنگ پس‌زمینه")
    text_color = models.CharField(max_length=7, default="#FFFFFF", verbose_name="رنگ متن")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(verbose_name="تاریخ پایان")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "بنر تبلیغاتی"
        verbose_name_plural = "بنرهای تبلیغاتی"
    
    def __str__(self):
        return f"{self.title} - {self.discount_percentage}% تخفیف"

# --- AI Consultant Models ---
class AIConsultantSession(TimestampedModel):
    """جلسه مشاوره هوش مصنوعی"""
    STATUS_CHOICES = [
        ('active', 'فعال'),
        ('expired', 'منقضی شده'),
        ('completed', 'تکمیل شده'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    store_analysis = models.ForeignKey('StoreAnalysis', on_delete=models.CASCADE, verbose_name='تحلیل فروشگاه')
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='شناسه جلسه')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='وضعیت')
    free_questions_used = models.PositiveIntegerField(default=0, verbose_name='سوالات رایگان استفاده شده')
    paid_questions_used = models.PositiveIntegerField(default=0, verbose_name='سوالات پولی استفاده شده')
    expires_at = models.DateTimeField(verbose_name='تاریخ انقضا')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده')
    
    class Meta:
        verbose_name = 'جلسه مشاوره هوش مصنوعی'
        verbose_name_plural = 'جلسات مشاوره هوش مصنوعی'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"مشاوره {self.user.username} - {self.store_analysis.store_name}"
    
    def can_ask_free_question(self):
        """آیا می‌تواند سوال رایگان بپرسد؟"""
        return self.free_questions_used < 3 and self.status == 'active'
    
    def can_ask_paid_question(self):
        """آیا می‌تواند سوال پولی بپرسد؟"""
        return self.is_paid and self.status == 'active' and timezone.now() < self.expires_at
    
    def get_remaining_free_questions(self):
        """تعداد سوالات رایگان باقی‌مانده"""
        return max(0, 3 - self.free_questions_used)

class AIConsultantQuestion(TimestampedModel):
    """سوالات مشاوره هوش مصنوعی"""
    session = models.ForeignKey(AIConsultantSession, on_delete=models.CASCADE, related_name='questions', verbose_name='جلسه')
    question = models.TextField(verbose_name='سوال')
    answer = models.TextField(blank=True, null=True, verbose_name='پاسخ')
    is_answered = models.BooleanField(default=False, verbose_name='پاسخ داده شده')
    is_free = models.BooleanField(default=True, verbose_name='رایگان')
    response_time = models.DurationField(blank=True, null=True, verbose_name='زمان پاسخ')
    
    class Meta:
        verbose_name = 'سوال مشاوره'
        verbose_name_plural = 'سوالات مشاوره'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"سوال: {self.question[:50]}..."

class AIConsultantPayment(TimestampedModel):
    """پرداخت‌های مشاوره هوش مصنوعی"""
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('completed', 'تکمیل شده'),
        ('failed', 'ناموفق'),
        ('cancelled', 'لغو شده'),
    ]
    
    session = models.OneToOneField(AIConsultantSession, on_delete=models.CASCADE, verbose_name='جلسه')
    amount = models.PositiveIntegerField(default=200000, verbose_name='مبلغ (تومان)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    payment_id = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='شناسه پرداخت')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='شناسه تراکنش')
    payment_gateway = models.CharField(max_length=50, default='zarinpal', verbose_name='درگاه پرداخت')
    
    class Meta:
        verbose_name = 'پرداخت مشاوره'
        verbose_name_plural = 'پرداخت‌های مشاوره'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"پرداخت {self.amount:,} تومان - {self.session.user.username}"


class EmailVerification(TimestampedModel):
    """تاییدیه ایمیل برای ثبت نام"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    email = models.EmailField(verbose_name='ایمیل')
    verification_code = models.CharField(max_length=6, verbose_name='کد تایید')
    is_verified = models.BooleanField(default=False, verbose_name='تایید شده')
    attempts = models.PositiveIntegerField(default=0, verbose_name='تعداد تلاش')
    expires_at = models.DateTimeField(verbose_name='انقضا')
    
    class Meta:
        verbose_name = 'تاییدیه ایمیل'
        verbose_name_plural = 'تاییدیه‌های ایمیل'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"تاییدیه {self.email} - {self.user.username}"
    
    def is_expired(self):
        """بررسی انقضای کد"""
        return timezone.now() > self.expires_at
    
    def can_resend(self):
        """بررسی امکان ارسال مجدد"""
        return self.attempts < 3 and not self.is_verified
    
    def generate_new_code(self):
        """تولید کد جدید"""
        import random
        self.verification_code = str(random.randint(100000, 999999))
        self.expires_at = timezone.now() + timedelta(minutes=10)  # 10 دقیقه
        self.attempts = 0
        self.save()
        return self.verification_code


class FAQCategory(TimestampedModel):
    """دسته‌بندی سوالات متداول"""
    name = models.CharField(max_length=100, verbose_name="نام دسته")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    icon = models.CharField(max_length=50, default="fas fa-question-circle", verbose_name="آیکون")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    class Meta:
        verbose_name = 'دسته‌بندی سوالات متداول'
        verbose_name_plural = 'دسته‌بندی‌های سوالات متداول'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class FAQ(TimestampedModel):
    """سوالات متداول"""
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, verbose_name="دسته‌بندی")
    question = models.CharField(max_length=200, verbose_name="سوال")
    answer = models.TextField(verbose_name="پاسخ")
    keywords = models.TextField(blank=True, help_text="کلمات کلیدی جدا شده با کاما", verbose_name="کلمات کلیدی")
    view_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")
    
    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول'
        ordering = ['category__order', 'order', 'question']
    
    def __str__(self):
        return f"{self.category.name} - {self.question}"
    
    def increment_view(self):
        """افزایش تعداد بازدید"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class SupportTicket(TimestampedModel):
    """تیکت‌های پشتیبانی"""
    PRIORITY_CHOICES = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'بالا'),
        ('urgent', 'فوری'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'باز'),
        ('in_progress', 'در حال بررسی'),
        ('waiting_user', 'در انتظار کاربر'),
        ('resolved', 'حل شده'),
        ('closed', 'بسته'),
    ]
    
    CATEGORY_CHOICES = [
        ('general', 'عمومی'),
        ('technical', 'فنی'),
        ('billing', 'پرداخت'),
        ('feature_request', 'درخواست ویژگی'),
        ('bug_report', 'گزارش باگ'),
        ('account', 'حساب کاربری'),
    ]
    
    ticket_id = models.CharField(max_length=20, unique=True, verbose_name="شناسه تیکت")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general', verbose_name="دسته‌بندی")
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    description = models.TextField(verbose_name="توضیحات")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="اولویت")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name="وضعیت")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets', verbose_name="واگذار شده به")
    attachments = models.JSONField(default=list, blank=True, verbose_name="پیوست‌ها")
    tags = models.JSONField(default=list, blank=True, verbose_name="برچسب‌ها")
    
    class Meta:
        verbose_name = 'تیکت پشتیبانی'
        verbose_name_plural = 'تیکت‌های پشتیبانی'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"#{self.ticket_id} - {self.subject}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = self.generate_ticket_id()
        super().save(*args, **kwargs)
    
    def generate_ticket_id(self):
        """تولید شناسه تیکت"""
        import random
        import string
        while True:
            ticket_id = f"TK{''.join(random.choices(string.digits, k=6))}"
            if not SupportTicket.objects.filter(ticket_id=ticket_id).exists():
                return ticket_id


class TicketMessage(TimestampedModel):
    """پیام‌های تیکت"""
    MESSAGE_TYPE_CHOICES = [
        ('user', 'کاربر'),
        ('admin', 'مدیر'),
        ('system', 'سیستم'),
    ]
    
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages', verbose_name="تیکت")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="فرستنده")
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='user', verbose_name="نوع پیام")
    content = models.TextField(verbose_name="محتوا")
    is_internal = models.BooleanField(default=False, verbose_name="داخلی")
    attachments = models.JSONField(default=list, blank=True, verbose_name="پیوست‌ها")
    
    class Meta:
        verbose_name = 'پیام تیکت'
        verbose_name_plural = 'پیام‌های تیکت'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.ticket.ticket_id} - {self.sender.username}"


class TicketTemplate(TimestampedModel):
    """قالب‌های پاسخ تیکت"""
    name = models.CharField(max_length=100, verbose_name="نام قالب")
    category = models.CharField(max_length=20, choices=SupportTicket.CATEGORY_CHOICES, verbose_name="دسته‌بندی")
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    content = models.TextField(verbose_name="محتوا")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    class Meta:
        verbose_name = 'قالب پاسخ'
        verbose_name_plural = 'قالب‌های پاسخ'
        ordering = ['name']
    
    def __str__(self):
        return self.name


# ==================== سیستم کیف پول ====================

class Wallet(TimestampedModel):
    """کیف پول کاربر"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    balance = models.DecimalField(
        max_digits=12, 
        decimal_places=0, 
        default=0, 
        validators=[MinValueValidator(0)],
        verbose_name='موجودی (تومان)'
    )
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف پول‌ها'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"کیف پول {self.user.username} - {self.balance:,} تومان"
    
    def get_balance_display(self):
        """نمایش موجودی با فرمت مناسب"""
        return f"{self.balance:,} تومان"
    
    def can_withdraw(self, amount):
        """بررسی امکان برداشت"""
        return self.balance >= amount and self.is_active
    
    def deposit(self, amount, description="واریز"):
        """واریز به کیف پول"""
        if amount <= 0:
            raise ValueError("مبلغ باید مثبت باشد")
        
        self.balance += amount
        self.save()
        
        # ایجاد تراکنش
        Transaction.objects.create(
            wallet=self,
            transaction_type='deposit',
            amount=amount,
            description=description,
            balance_after=self.balance
        )
        
        return self.balance
    
    def withdraw(self, amount, description="برداشت"):
        """برداشت از کیف پول"""
        if amount <= 0:
            raise ValueError("مبلغ باید مثبت باشد")
        
        if not self.can_withdraw(amount):
            raise ValueError("موجودی کافی نیست")
        
        self.balance -= amount
        self.save()
        
        # ایجاد تراکنش
        Transaction.objects.create(
            wallet=self,
            transaction_type='withdraw',
            amount=amount,
            description=description,
            balance_after=self.balance
        )
        
        return self.balance


class Transaction(TimestampedModel):
    """تراکنش‌های کیف پول"""
    
    TRANSACTION_TYPES = [
        ('deposit', 'واریز'),
        ('withdraw', 'برداشت'),
        ('payment', 'پرداخت'),
        ('refund', 'بازگشت'),
        ('bonus', 'پاداش'),
        ('penalty', 'جریمه'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('completed', 'تکمیل شده'),
        ('failed', 'ناموفق'),
        ('cancelled', 'لغو شده'),
    ]
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions', verbose_name='کیف پول')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, verbose_name='نوع تراکنش')
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=0, 
        validators=[MinValueValidator(0)],
        verbose_name='مبلغ (تومان)'
    )
    description = models.CharField(max_length=200, verbose_name='توضیحات')
    balance_after = models.DecimalField(
        max_digits=12, 
        decimal_places=0, 
        verbose_name='موجودی پس از تراکنش'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed', verbose_name='وضعیت')
    reference_id = models.CharField(max_length=100, blank=True, verbose_name='شناسه مرجع')
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='سفارش مرتبط')
    
    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount:,} تومان - {self.wallet.user.username}"
    
    def get_amount_display(self):
        """نمایش مبلغ با فرمت مناسب"""
        return f"{self.amount:,} تومان"
    
    def get_balance_after_display(self):
        """نمایش موجودی پس از تراکنش"""
        return f"{self.balance_after:,} تومان"
    
    def is_positive(self):
        """بررسی مثبت بودن تراکنش"""
        return self.transaction_type in ['deposit', 'refund', 'bonus']
    
    def get_transaction_icon(self):
        """آیکون مناسب برای نوع تراکنش"""
        icons = {
            'deposit': '💰',
            'withdraw': '💸',
            'payment': '💳',
            'refund': '↩️',
            'bonus': '🎁',
            'penalty': '⚠️',
        }
        return icons.get(self.transaction_type, '💱')
