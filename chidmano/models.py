from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BlogPost(models.Model):
    """مدل برای مقالات وبلاگ"""
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="اسلاگ")
    content = models.TextField(verbose_name="محتوای کامل")
    excerpt = models.TextField(max_length=500, verbose_name="خلاصه")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="نویسنده")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    published = models.BooleanField(default=False, verbose_name="منتشر شده")
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="تصویر شاخص")
    meta_description = models.CharField(max_length=160, verbose_name="توضیحات متا")
    meta_keywords = models.CharField(max_length=200, verbose_name="کلمات کلیدی")
    views_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    
    class Meta:
        verbose_name = "مقاله وبلاگ"
        verbose_name_plural = "مقالات وبلاگ"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class SEOKeyword(models.Model):
    """مدل برای مدیریت کلمات کلیدی SEO"""
    keyword = models.CharField(max_length=100, unique=True, verbose_name="کلمه کلیدی")
    search_volume = models.PositiveIntegerField(default=0, verbose_name="حجم جستجو")
    difficulty = models.PositiveIntegerField(default=0, verbose_name="سختی")
    cpc = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="هزینه کلیک")
    target_url = models.URLField(blank=True, null=True, verbose_name="URL هدف")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "کلمه کلیدی SEO"
        verbose_name_plural = "کلمات کلیدی SEO"
        ordering = ['-search_volume']
    
    def __str__(self):
        return self.keyword

class InternalLink(models.Model):
    """مدل برای مدیریت لینک‌های داخلی"""
    source_url = models.CharField(max_length=200, verbose_name="URL مبدأ")
    target_url = models.CharField(max_length=200, verbose_name="URL مقصد")
    anchor_text = models.CharField(max_length=100, verbose_name="متن لنگر")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "لینک داخلی"
        verbose_name_plural = "لینک‌های داخلی"
        unique_together = ['source_url', 'target_url', 'anchor_text']
    
    def __str__(self):
        return f"{self.source_url} -> {self.target_url}"

class SEOMetrics(models.Model):
    """مدل برای ذخیره متریک‌های SEO"""
    date = models.DateField(verbose_name="تاریخ")
    organic_traffic = models.PositiveIntegerField(default=0, verbose_name="ترافیک ارگانیک")
    keyword_rankings = models.PositiveIntegerField(default=0, verbose_name="رتبه‌بندی کلمات کلیدی")
    backlinks_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بک‌لینک")
    domain_authority = models.PositiveIntegerField(default=0, verbose_name="اعتبار دامنه")
    page_speed_score = models.PositiveIntegerField(default=0, verbose_name="امتیاز سرعت صفحه")
    
    class Meta:
        verbose_name = "متریک SEO"
        verbose_name_plural = "متریک‌های SEO"
        ordering = ['-date']
        unique_together = ['date']
    
    def __str__(self):
        return f"متریک‌های {self.date}"
