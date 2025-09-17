# راهنمای دیپلوی چیدمانو در لیارا

## 🚀 مراحل دیپلوی

### 1. آماده‌سازی Environment Variables

در پنل لیارا، متغیرهای محیطی زیر را تنظیم کنید:

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-here-change-this-in-production
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,*.liara.ir

# Database (PostgreSQL)
DATABASE_URL=postgresql://username:password@host:port/database_name

# Security Settings (HTTPS disabled for Liara)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# OpenAI API
OPENAI_API_KEY=your-openai-api-key

# Liara AI Settings
LIARA_AI_API_KEY=your_liara_ai_api_key_here
USE_LIARA_AI=True
FALLBACK_TO_OLLAMA=True

# Media and Static Files
MEDIA_URL=/media/
MEDIA_ROOT=/app/media

# Performance Settings
PERFORMANCE_MONITORING=True
```

### 2. تنظیمات دیتابیس

- از PostgreSQL استفاده کنید
- اتصال SSL را فعال کنید
- Connection pooling را تنظیم کنید

### 3. تنظیمات Static Files

- WhiteNoise برای serving static files
- CDN برای فایل‌های استاتیک (اختیاری)

### 4. تنظیمات امنیتی

- HTTPS را فعال کنید
- Security headers را تنظیم کنید
- Rate limiting را فعال کنید

### 5. مانیتورینگ

- Log files را بررسی کنید
- Performance metrics را مانیتور کنید
- Error tracking را فعال کنید

## 🔧 تنظیمات خاص لیارا

### Procfile
```
web: gunicorn chidmano.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120 --max-requests 1000 --max-requests-jitter 100
```

### Runtime
```
python-3.11.9
```

### Buildpack
```
https://github.com/heroku/heroku-buildpack-python
```

## 📋 چک‌لیست قبل از دیپلوی

- [ ] SECRET_KEY تغییر کرده
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS تنظیم شده
- [ ] دیتابیس PostgreSQL آماده
- [ ] Static files جمع‌آوری شده
- [ ] Migrations اجرا شده
- [ ] Environment variables تنظیم شده
- [ ] SSL certificate فعال
- [ ] Error handlers تست شده
- [ ] Performance optimization فعال

## 🚨 نکات مهم

1. **SECRET_KEY**: حتماً یک کلید امن و منحصر به فرد استفاده کنید
2. **Database**: از PostgreSQL در production استفاده کنید
3. **Static Files**: WhiteNoise برای serving فایل‌های استاتیک
4. **Logging**: فایل‌های log را مانیتور کنید
5. **Backup**: دیتابیس را به‌طور منظم backup کنید

## 🔍 تست پس از دیپلوی

1. صفحه اصلی بارگذاری می‌شود
2. فرم ثبت‌نام کار می‌کند
3. تحلیل فروشگاه انجام می‌شود
4. PDF دانلود می‌شود
5. پردازش Ollama کار می‌کند
6. Error pages نمایش داده می‌شوند

## 📞 پشتیبانی

در صورت بروز مشکل، لاگ‌ها را بررسی کنید و با تیم فنی تماس بگیرید.
