# ساختار پروژه چیدمانو

## 📁 **ساختار کلی**

```
chidmano/                    # اپ اصلی (SEO, Landing, Admin)
├── models.py               # مدل‌های SEO (BlogPost, SEOKeyword, etc.)
├── views.py                # Views اصلی (landing, admin dashboard, SEO guides)
├── urls.py                 # URLs اصلی (ساده و منظم)
├── templates/              # Templates اصلی
│   ├── chidmano/          # Templates اپ اصلی
│   │   ├── landing.html   # صفحه اصلی
│   │   ├── admin/         # داشبورد ادمین
│   │   └── guides/        # راهنماهای SEO
│   └── verification/       # فایل‌های تأیید
├── static/                 # فایل‌های استاتیک اصلی
├── management/             # دستورات مدیریت SEO
└── seo_utils.py           # ابزارهای SEO

store_analysis/             # اپ تحلیل فروشگاه
├── models.py              # مدل‌های تحلیل (StoreAnalysis, Order, etc.)
├── views.py               # Views تحلیل (forms, payment, analysis)
├── urls.py                # URLs تحلیل (ساده و منظم)
├── templates/             # Templates تحلیل
│   └── store_analysis/    # Templates اپ تحلیل
├── static/                # فایل‌های استاتیک تحلیل
├── payment_gateways.py    # درگاه‌های پرداخت
└── ai_services/           # سرویس‌های AI
```

## 🎯 **تقسیم مسئولیت‌ها**

### **chidmano/ (اپ اصلی)**
- **صفحه اصلی**: Landing page حرفه‌ای
- **SEO**: راهنماها، مقالات، pillar page
- **داشبورد ادمین**: مدیریت سیستم
- **احراز هویت**: Login, Signup, Password
- **فایل‌های SEO**: sitemap.xml, robots.txt

### **store_analysis/ (اپ تحلیل)**
- **فرم‌ها**: فرم تحلیل فروشگاه
- **پرداخت**: درگاه‌های پرداخت
- **تحلیل**: AI analysis, ML processing
- **پشتیبانی**: سیستم تیکت
- **کیف پول**: مدیریت اعتبار

## 🔗 **URL Structure**

### **URLs اصلی (chidmano/)**
```
/                           # صفحه اصلی
/landing/                   # صفحه اصلی (alias)
/store/                     # اپ تحلیل فروشگاه
/accounts/                  # احراز هویت
/guide/                     # راهنماهای SEO
/case-studies/              # مطالعات موردی
/partnership/               # همکاری
/admin/                     # ادمین
/sitemap.xml                # فایل‌های SEO
/robots.txt
```

### **URLs تحلیل (store_analysis/)**
```
/store/                     # صفحه اصلی تحلیل
/store/forms/               # فرم‌ها
/store/analysis/            # مدیریت تحلیل‌ها
/store/support/             # پشتیبانی
/store/wallet/              # کیف پول
/store/education/           # آموزش
```

## 📊 **مدل‌های داده**

### **chidmano/models.py**
- `BlogPost`: مقالات SEO
- `SEOKeyword`: کلمات کلیدی
- `SEOMetrics`: متریک‌های SEO
- `InternalLink`: لینک‌های داخلی

### **store_analysis/models.py**
- `StoreAnalysis`: تحلیل فروشگاه
- `Order`: سفارشات
- `UserProfile`: پروفایل کاربر
- `SupportTicket`: تیکت‌های پشتیبانی

## 🎨 **Templates**

### **chidmano/templates/**
- `landing.html`: صفحه اصلی
- `admin/dashboard.html`: داشبورد ادمین
- `guides/`: راهنماهای SEO
- `case_studies.html`: مطالعات موردی

### **store_analysis/templates/**
- `forms.html`: فرم تحلیل
- `payment_page.html`: صفحه پرداخت
- `support_center.html`: مرکز پشتیبانی
- `wallet_dashboard.html`: داشبورد کیف پول

## ⚙️ **تنظیمات**

### **INSTALLED_APPS**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'store_analysis.apps.StoreAnalysisConfig',  # اپ تحلیل
    'chidmano',                                 # اپ اصلی
]
```

## 🚀 **مزایای ساختار جدید**

### ✅ **سادگی**
- URLs منظم و قابل فهم
- تقسیم مسئولیت‌ها واضح
- ساختار منطقی

### ✅ **قابلیت نگهداری**
- کدهای مرتبط در یک جا
- تغییرات آسان
- تست‌پذیری بالا

### ✅ **مقیاس‌پذیری**
- افزودن اپ‌های جدید آسان
- جداسازی عملکردها
- توسعه مستقل

### ✅ **عملکرد**
- بارگذاری سریع‌تر
- کش‌گذاری بهتر
- بهینه‌سازی آسان

## 🔧 **دستورات مفید**

### **تولید محتوای SEO**
```bash
python manage.py generate_seo_content --count 5
python manage.py monitor_seo --update
python manage.py generate_seo_reports --daily
```

### **مدیریت تحلیل‌ها**
```bash
python manage.py shell
>>> from store_analysis.models import StoreAnalysis
>>> StoreAnalysis.objects.count()
```

### **تست سیستم**
```bash
python manage.py runserver
# http://localhost:8000/          # صفحه اصلی
# http://localhost:8000/store/    # تحلیل فروشگاه
# http://localhost:8000/admin/dashboard/  # داشبورد ادمین
```

## 📝 **نکات مهم**

1. **جداسازی**: هر اپ مسئولیت خاص خود را دارد
2. **سادگی**: URLs کوتاه و قابل فهم
3. **منطق**: ساختار منطقی و قابل پیش‌بینی
4. **انعطاف**: قابلیت افزودن اپ‌های جدید
5. **امنیت**: دسترسی‌های محدود و کنترل شده

---

**نتیجه**: ساختار ساده، منظم و حرفه‌ای که قابلیت نگهداری و توسعه بالایی دارد.
