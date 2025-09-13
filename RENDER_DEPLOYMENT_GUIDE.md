# راهنمای کامل حل مشکل Server Error (500) در Render

## 🔍 تشخیص مشکل

مشکل Server Error (500) معمولاً به دلایل زیر رخ می‌دهد:

1. **مشکل در اتصال به دیتابیس**
2. **مشکل در Static Files**
3. **مشکل در Environment Variables**
4. **مشکل در Migrations**
5. **مشکل در Dependencies**

## 🛠️ راه‌حل‌های مرحله‌ای

### مرحله 1: بررسی Logs در Render

1. وارد Dashboard Render شوید
2. روی پروژه خود کلیک کنید
3. به بخش "Logs" بروید
4. خطاهای قرمز را بررسی کنید

### مرحله 2: تنظیم Environment Variables

در Render Dashboard، Environment Variables زیر را تنظیم کنید:

```bash
# Django Core
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DJANGO_SETTINGS_MODULE=chidmano.settings

# Database (اگر از PostgreSQL استفاده می‌کنید)
DATABASE_URL=postgresql://user:password@host:port/database

# یا تنظیمات جداگانه:
DB_NAME=chidman
DB_USER=chidman_user
DB_PASSWORD=your-password
DB_HOST=your-host
DB_PORT=5432

# Static Files
STATIC_URL=/static/
STATIC_ROOT=staticfiles/

# Security (برای production)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### مرحله 3: بررسی Build Command

در Render، Build Command را به این صورت تنظیم کنید:

```bash
chmod +x build.sh && ./build.sh
```

### مرحله 4: بررسی Start Command

Start Command:

```bash
gunicorn chidmano.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

### مرحله 5: تست محلی

قبل از deploy، محلی تست کنید:

```bash
# نصب dependencies
pip install -r requirements.txt

# اجرای migrations
python manage.py migrate

# جمع‌آوری static files
python manage.py collectstatic

# ایجاد superuser
python manage.py createsuperuser

# اجرای debug script
python debug_render.py

# تست سرور
python manage.py runserver
```

## 🔧 فایل‌های مهم

### 1. build.sh
```bash
#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
```

### 2. Procfile
```
web: gunicorn chidmano.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

### 3. requirements.txt
اطمینان حاصل کنید که تمام dependencies موجود است.

## 🚨 مشکلات رایج و راه‌حل

### مشکل 1: Database Connection Error
```python
# در settings.py
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)
```

### مشکل 2: Static Files Error
```python
# در settings.py
if not DEBUG:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### مشکل 3: Secret Key Error
```python
# در settings.py
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key-for-development')
```

### مشکل 4: Allowed Hosts Error
```python
# در settings.py
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

## 📋 چک‌لیست نهایی

- [ ] Environment Variables تنظیم شده
- [ ] Database connection کار می‌کند
- [ ] Static files جمع‌آوری شده
- [ ] Migrations اجرا شده
- [ ] Superuser ایجاد شده
- [ ] Build script اجرا می‌شود
- [ ] Start command صحیح است
- [ ] Dependencies نصب شده

## 🆘 در صورت ادامه مشکل

1. **Logs را بررسی کنید** - دقیقاً کدام خطا رخ می‌دهد
2. **Debug script اجرا کنید** - `python debug_render.py`
3. **محلی تست کنید** - `python manage.py runserver`
4. **Database را بررسی کنید** - اتصال و migrations
5. **Static files را بررسی کنید** - collectstatic

## 📞 پشتیبانی

اگر مشکل ادامه داشت، لطفاً:
1. Logs کامل Render را ارسال کنید
2. خروجی `debug_render.py` را ارسال کنید
3. Environment Variables را بررسی کنید

---

**نکته مهم:** همیشه قبل از deploy، محلی تست کنید!
