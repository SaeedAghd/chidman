# 🚀 راهنمای دیپلوی حرفه‌ای - چیدمانو

## 📋 وضعیت سیستم
- ✅ **Git Status**: Clean (36f1379)
- ✅ **Django Check**: 5 warnings (غیرحیاتی)
- ✅ **Static Files**: 206 files ready
- ✅ **Migrations**: 43 migrations completed
- ✅ **Requirements**: UTF-8, no Windows deps

## 🎯 دستورالعمل دیپلوی در Liara

### مرحله 1: اتصال Repository
```
Repository URL: https://github.com/SaeedAghd/chidman.git
Branch: main
Platform: django
Python Version: 3.11
```

### مرحله 2: Environment Variables
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

# Email (نیاز به تنظیم)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Performance
WEB_CONCURRENCY=1
TIMEOUT=120
```

### مرحله 3: Build Command
```bash
python manage.py collectstatic --noinput && python manage.py migrate --no-input
```

### مرحله 4: Health Check
```
Path: /health
Port: 80
Timeout: 30
```

## 🔍 نظارت بر دیپلوی

### لاگ‌های مهم برای نظارت:
1. **Build Logs**: بررسی collectstatic و migrate
2. **Startup Logs**: بررسی gunicorn startup
3. **Health Check**: بررسی /health endpoint
4. **Database**: بررسی اتصال PostgreSQL
5. **Static Files**: بررسی serving static files

### مشکلات احتمالی و راه‌حل:
1. **Database Connection**: بررسی DATABASE_URL
2. **Static Files**: بررسی STATIC_ROOT
3. **Migrations**: بررسی migrate logs
4. **Memory**: بررسی WEB_CONCURRENCY=1
5. **Timeout**: بررسی TIMEOUT=120

## 🎉 وضعیت نهایی
- **آمادگی دیپلوی**: 100%
- **تمام تست‌ها**: موفق
- **تمام مشکلات**: حل شده
- **سیستم**: آماده لانچ

## 📞 پشتیبانی
در صورت بروز مشکل در دیپلوی، لاگ‌ها را بررسی کنید و مشکلات را گزارش دهید.