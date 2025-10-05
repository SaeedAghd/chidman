# 🚀 راهنمای دیپلوی در Liara - چیدمانو

## 📋 اطلاعات Repository
- **Repository URL**: `https://github.com/SaeidAghd/chidman.git`
- **Branch**: `main`
- **Latest Commit**: `0f31531 - Add Professional Deployment Guide`
- **Platform**: `django`
- **Python Version**: `3.11`

## 🎯 مراحل دیپلوی در Liara Dashboard

### مرحله 1: اتصال Repository
1. وارد **Liara Dashboard** شوید
2. روی **"New Project"** کلیک کنید
3. **"Connect Repository"** را انتخاب کنید
4. Repository URL را وارد کنید: `https://github.com/SaeidAghd/chidman.git`
5. Branch: `main`
6. Platform: `django`
7. Python Version: `3.11`

### مرحله 2: تنظیم Environment Variables
در بخش **Environment Variables** این متغیرها را اضافه کنید:

```bash
# Core Settings
DEBUG=False
PRODUCTION=True
SECRET_KEY=1-++(gh-*#+j1@5_c&ls2te#1n44iii98r%-0^2aan3h$&$esj
ALLOWED_HOSTS=*.liara.ir,*.liara.app,*.liara.run,chidmano.liara.app,chidmano.liara.run,chidmano.ir,www.chidmano.ir
DJANGO_SETTINGS_MODULE=chidmano.settings

# Database
DATABASE_URL=postgresql://root:rKAZUGyIPxZgL2iygIdb5ZBV@chidmano-db:5432/postgres?sslmode=disable
PGSSLMODE=disable

# Payment Gateway
PING_API_KEY=EB28E90039CB8FCD97F3D778FC7644917A1391217F9E47046EA864EA25331445-1
PING_CALLBACK_URL=https://chidmano.liara.app/store/payment/payping/callback/
PING_RETURN_URL=https://chidmano.liara.app/store/payment/payping/return/
PING_SANDBOX=False

# Static/Media
STATIC_URL=/static/
MEDIA_URL=/media/

# Redis/Celery
REDIS_URL=redis://default:redispass@redis.chidmano.liara.run:6379/0
CELERY_BROKER_URL=redis://default:redispass@redis.chidmano.liara.run:6379/0
CELERY_RESULT_BACKEND=redis://default:redispass@redis.chidmano.liara.run:6379/0

# Performance
WEB_CONCURRENCY=1
TIMEOUT=120
```

### مرحله 3: تنظیم Build Command
در بخش **Build Settings**:
```bash
python manage.py collectstatic --noinput && python manage.py migrate --no-input
```

### مرحله 4: تنظیم Health Check
- **Path**: `/health`
- **Port**: `80`
- **Timeout**: `30`

### مرحله 5: شروع دیپلوی
1. روی **"Deploy"** کلیک کنید
2. منتظر بمانید تا build کامل شود
3. لاگ‌ها را بررسی کنید

## 🔍 نظارت بر لاگ‌ها

### لاگ‌های مهم برای بررسی:
1. **Build Logs**: بررسی `collectstatic` و `migrate`
2. **Startup Logs**: بررسی `gunicorn` startup
3. **Health Check**: بررسی `/health` endpoint
4. **Database**: بررسی اتصال PostgreSQL
5. **Static Files**: بررسی serving static files

### مشکلات احتمالی و راه‌حل:
1. **Database Connection Error**: بررسی `DATABASE_URL`
2. **Static Files Error**: بررسی `STATIC_ROOT`
3. **Migration Error**: بررسی `migrate` logs
4. **Memory Error**: بررسی `WEB_CONCURRENCY=1`
5. **Timeout Error**: بررسی `TIMEOUT=120`

## 📊 وضعیت سیستم
- ✅ **Git Repository**: Clean
- ✅ **Django Settings**: Production ready
- ✅ **Static Files**: 206 files ready
- ✅ **Migrations**: 43 completed
- ✅ **Requirements**: UTF-8, no Windows deps
- ✅ **Deployment Guide**: Ready

## 🎉 نتیجه
سیستم کاملاً آماده دیپلوی است. تمام تنظیمات و فایل‌ها آماده‌اند.
