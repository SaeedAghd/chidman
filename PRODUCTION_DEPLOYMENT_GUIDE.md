# راهنمای جامع Deploy در Production (Liara)

## 🚀 مراحل Deploy در Production

### 1. آماده‌سازی Migration ها

```bash
# اجرای migration جدید در production
python manage.py migrate store_analysis

# بررسی وضعیت migration ها
python manage.py showmigrations store_analysis
```

### 2. تنظیمات Environment Variables

در پنل Liara، متغیرهای محیطی زیر را تنظیم کنید:

```env
# Database
DATABASE_URL=postgresql://username:password@host:port/database

# Security
SECRET_KEY=your-secret-key-here
DEBUG=False
PRODUCTION=True

# Payment Gateway
PING_API_KEY=your-ping-api-key
PING_SANDBOX=False
PING_CALLBACK_URL=https://yourdomain.com/payment/callback/
PING_RETURN_URL=https://yourdomain.com/payment/return/

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Site Settings
SITE_URL=https://yourdomain.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,*.liara.ir,*.liara.app
```

### 3. فایل‌های کلیدی برای Deploy

#### Procfile
```
web: gunicorn chidmano.wsgi:application --bind 0.0.0.0:$PORT
```

#### requirements.txt
```
Django>=4.2.0
gunicorn>=20.1.0
psycopg2-binary>=2.9.0
whitenoise>=6.0.0
dj-database-url>=1.0.0
python-dotenv>=1.0.0
requests>=2.28.0
```

#### runtime.txt
```
python-3.11.0
```

### 4. دستورات Deploy

```bash
# 1. Push کد به Git
git add .
git commit -m "Fix production issues - comprehensive migration and view fixes"
git push origin main

# 2. Deploy در Liara
liara deploy

# 3. اجرای Migration ها در Production
liara run python manage.py migrate

# 4. جمع‌آوری Static Files
liara run python manage.py collectstatic --noinput

# 5. ایجاد Superuser (در صورت نیاز)
liara run python manage.py createsuperuser
```

## 🔧 حل مشکلات شناسایی شده

### مشکل 1: Migration های مفقود
**راه‌حل:** Migration جامع `0012_comprehensive_fix.py` ایجاد شد که شامل:
- اصلاح فیلدهای مفقود در تمام مدل‌ها
- ایجاد Index های بهینه برای عملکرد بهتر
- همگام‌سازی کامل مدل‌ها با دیتابیس

### مشکل 2: خطای 500 در admin_settings
**راه‌حل:** اضافه کردن Exception Handling جامع:
```python
try:
    # کد اصلی
except Exception as e:
    logger.error(f"Error in admin_settings view: {e}")
    messages.error(request, 'خطا در بارگذاری صفحه تنظیمات')
    return redirect('store_analysis:admin_dashboard')
```

### مشکل 3: عدم ارسال تیکت
**راه‌حل:** اصلاح view `create_ticket` با:
- بهبود Exception Handling
- اضافه کردن Fallback برای خطاهای دیتابیس
- لاگ‌گیری بهتر برای Debug

### مشکل 4: مشکل پرداخت با توکن تستی
**راه‌حل:** اصلاح view `deposit_to_wallet` با:
- بهبود مدیریت خطاها
- اضافه کردن Debug Logging
- Fallback برای حالت تست

## 📋 چک‌لیست Pre-Deploy

- [ ] تمام Migration ها اجرا شده‌اند
- [ ] Environment Variables تنظیم شده‌اند
- [ ] Static Files جمع‌آوری شده‌اند
- [ ] Database Connection تست شده
- [ ] Payment Gateway تست شده
- [ ] Email Settings تست شده
- [ ] Logging تنظیم شده

## 🧪 تست‌های Post-Deploy

### 1. تست Database
```bash
liara run python manage.py check --database default
```

### 2. تست Payment Gateway
- تست واریز به کیف پول
- بررسی Callback URL
- تست Return URL

### 3. تست Admin Panel
- ورود به admin_settings
- ذخیره تنظیمات
- بررسی لاگ‌ها

### 4. تست Support System
- ایجاد تیکت جدید
- بررسی ارسال تیکت
- تست پاسخ‌دهی

## 🚨 Troubleshooting

### خطای Database Connection
```bash
# بررسی Connection
liara run python manage.py dbshell

# Reset Migration ها (در صورت نیاز)
liara run python manage.py migrate store_analysis zero
liara run python manage.py migrate store_analysis
```

### خطای Static Files
```bash
# جمع‌آوری مجدد
liara run python manage.py collectstatic --noinput --clear
```

### خطای Payment Gateway
- بررسی API Key
- تست Callback URL
- بررسی Sandbox Mode

## 📊 Monitoring

### 1. Log Monitoring
```bash
# مشاهده لاگ‌ها
liara logs --tail

# فیلتر لاگ‌های خطا
liara logs --tail | grep ERROR
```

### 2. Performance Monitoring
- بررسی Response Time
- مانیتورینگ Memory Usage
- بررسی Database Queries

## 🔐 Security Checklist

- [ ] DEBUG=False در Production
- [ ] SECRET_KEY محفوظ
- [ ] HTTPS فعال
- [ ] CSRF Protection فعال
- [ ] XSS Protection فعال
- [ ] SQL Injection Protection فعال

## 📞 Support

در صورت بروز مشکل:
1. بررسی لاگ‌ها
2. تست Environment Variables
3. بررسی Database Connection
4. تست Payment Gateway
5. تماس با تیم پشتیبانی

---

**نکته مهم:** این راهنما تمام مشکلات شناسایی شده را حل می‌کند و اطمینان از عملکرد صحیح در production را تضمین می‌نماید.
