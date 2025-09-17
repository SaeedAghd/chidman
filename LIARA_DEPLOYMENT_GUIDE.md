# راهنمای آپلود پروژه چیدمانو در Liara

## 🚀 مراحل آپلود

### 1. آماده‌سازی پروژه
```bash
# جمع‌آوری static files
python manage.py collectstatic --noinput

# بررسی migrations
python manage.py makemigrations --check

# تست سیستم
python manage.py check --deploy
```

### 2. آپلود در Liara

#### روش 1: از طریق Git
```bash
# اضافه کردن remote
git remote add liara https://git.liara.ir/your-username/chidmano.git

# آپلود کد
git add .
git commit -m "Ready for Liara deployment"
git push liara main
```

#### روش 2: از طریق Liara Dashboard
1. وارد [Liara Dashboard](https://console.liara.ir) شوید
2. روی "ایجاد سرویس جدید" کلیک کنید
3. "Web App" را انتخاب کنید
4. نام پروژه: `chidmano`
5. پلتفرم: `Python`
6. کد را آپلود کنید

### 3. تنظیم Environment Variables

در Liara Dashboard، بخش Environment Variables:

```bash
# Django Core
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=chidmano.liara.app,*.liara.app
DATABASE_URL=postgresql://username:password@host:port/database

# Security (برای Liara)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# Static Files
STATIC_URL=/static/
STATIC_ROOT=staticfiles/
MEDIA_URL=/media/
MEDIA_ROOT=media/

# Payment Gateway
ZARINPAL_MERCHANT_ID=your-zarinpal-merchant-id
ZARINPAL_SANDBOX=True

# AI Services
LIARA_AI_API_KEY=your-liara-ai-api-key
USE_LIARA_AI=True
FALLBACK_TO_OLLAMA=True

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@chidmano.com
SITE_URL=https://chidmano.liara.app
```

### 4. تنظیم دیتابیس PostgreSQL

1. در Liara Dashboard، "Database" را انتخاب کنید
2. PostgreSQL را انتخاب کنید
3. نام دیتابیس: `chidmano-db`
4. Plan: `Starter` (برای شروع)
5. پس از ایجاد، `DATABASE_URL` را کپی کنید

### 5. تنظیم Build Commands

```bash
# Build Command
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

# Start Command
gunicorn chidmano.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
```

### 6. تنظیم Domain

1. در بخش "Domains" سرویس
2. Domain پیش‌فرض: `chidmano.liara.app`
3. یا domain سفارشی خود را اضافه کنید

## 🔧 تنظیمات اضافی

### Static Files
```python
# در settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Media Files
```python
# در settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Security Headers
```python
# در settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

## 📊 مانیتورینگ

### Logs
- در Liara Dashboard، بخش "Logs" را بررسی کنید
- برای debug، `DEBUG=True` را موقتاً فعال کنید

### Performance
- از بخش "Metrics" برای بررسی عملکرد استفاده کنید
- CPU و Memory usage را مانیتور کنید

## 🚨 عیب‌یابی

### مشکلات رایج:

1. **Static Files لود نمی‌شوند**
   ```bash
   # بررسی STATIC_ROOT
   python manage.py collectstatic --noinput
   ```

2. **Database Connection Error**
   ```bash
   # بررسی DATABASE_URL
   echo $DATABASE_URL
   ```

3. **Import Error**
   ```bash
   # بررسی requirements.txt
   pip install -r requirements.txt
   ```

4. **Permission Error**
   ```bash
   # بررسی file permissions
   chmod +x manage.py
   ```

## 📱 تست نهایی

پس از آپلود، این URL ها را تست کنید:

- ✅ `https://chidmano.liara.app/` - صفحه اصلی
- ✅ `https://chidmano.liara.app/store/dashboard/` - داشبورد کاربر
- ✅ `https://chidmano.liara.app/store/admin-dashboard/` - داشبورد ادمین
- ✅ `https://chidmano.liara.app/admin/` - پنل Django
- ✅ `https://chidmano.liara.app/store/support/` - پشتیبانی
- ✅ `https://chidmano.liara.app/store/wallet/` - کیف پول

## 🎯 ویژگی‌های فعال

- ✅ **داشبورد ادمین حرفه‌ای**
- ✅ **سیستم کیف پول**
- ✅ **پشتیبانی و تیکت**
- ✅ **پرداخت زرین‌پال**
- ✅ **AI Analysis با GPT-4.1**
- ✅ **UI/UX مدرن**
- ✅ **Responsive Design**

## 📞 پشتیبانی

در صورت مشکل:
1. Logs را در Liara Dashboard بررسی کنید
2. Environment Variables را چک کنید
3. Database connection را تست کنید
4. Static files را دوباره collect کنید

---

**نکته**: این راهنما برای آپلود در Liara تنظیم شده است. برای سایر پلتفرم‌ها، تنظیمات متفاوت خواهد بود.
