# 🚀 راهنمای کامل دیپلوی روی Render

## 📋 مراحل دیپلوی

### 1. آماده‌سازی پروژه
```bash
# اطمینان از commit آخرین تغییرات
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. اتصال به Render

#### الف) ایجاد سرویس جدید:
1. به https://render.com بروید
2. با GitHub وارد شوید
3. "New Web Service" را کلیک کنید
4. Repository `chidman` را انتخاب کنید

#### ب) تنظیمات سرویس:
- **Name**: `chidman-store-analysis-v2`
- **Environment**: `Python`
- **Region**: نزدیک‌ترین منطقه
- **Branch**: `main`
- **Root Directory**: (خالی بگذارید)

#### ج) Build & Deploy:
- **Build Command**: `chmod +x build.sh && ./build.sh`
- **Start Command**: `gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

### 3. متغیرهای محیطی

در بخش "Environment Variables" این موارد را اضافه کنید:

```
SECRET_KEY: (توسط Render تولید می‌شود)
DEBUG: False
ALLOWED_HOSTS: chidman-store-analysis-v2.onrender.com
DJANGO_SETTINGS_MODULE: chidmano.settings
PYTHONPATH: /opt/render/project/src
OPENAI_API_KEY: کلید API شما
```

### 4. دیتابیس

#### الف) ایجاد دیتابیس:
1. در Render، "New PostgreSQL" را کلیک کنید
2. نام: `chidman-db`
3. Database: `chidman`
4. User: `chidman_user`

#### ب) اتصال دیتابیس:
1. در سرویس وب، "Environment" را کلیک کنید
2. "Link Database" را کلیک کنید
3. دیتابیس `chidman-db` را انتخاب کنید
4. متغیر `DATABASE_URL` خودکار اضافه می‌شود

### 5. دیپلوی

1. "Create Web Service" را کلیک کنید
2. منتظر بمانید تا build و deploy کامل شود
3. لاگ‌ها را بررسی کنید

## 🔧 عیب‌یابی

### مشکل: ModuleNotFoundError: No module named 'core'

#### راه حل 1: بررسی فایل‌ها
```bash
# اطمینان از وجود فایل‌ها
ls -la core/
ls -la core/wsgi.py
ls -la core/__init__.py
```

#### راه حل 2: تست محلی
```bash
# تست WSGI application
python -c "from core.wsgi import application; print('OK')"
```

#### راه حل 3: بررسی لاگ‌ها
- در Render، "Logs" را بررسی کنید
- خطاهای build را پیدا کنید

### مشکل: Database connection failed

#### راه حل:
1. اطمینان از اتصال دیتابیس
2. بررسی متغیر `DATABASE_URL`
3. اجرای مایگریشن‌ها

### مشکل: Static files not found

#### راه حل:
1. بررسی `STATIC_ROOT` در settings
2. اطمینان از اجرای `collectstatic`
3. بررسی `whitenoise` middleware

## 📊 مانیتورینگ

### Health Check:
- URL: `https://your-app.onrender.com/`
- باید Status 200 برگرداند

### لاگ‌ها:
- در Render dashboard، "Logs" را بررسی کنید
- خطاها و warnings را پیدا کنید

### عملکرد:
- Response time را بررسی کنید
- Memory usage را مانیتور کنید

## 🔒 امنیت

### SSL/HTTPS:
- Render خودکار SSL ارائه می‌دهد
- `SECURE_SSL_REDIRECT=True` در production

### متغیرهای حساس:
- `SECRET_KEY` را در production تغییر دهید
- `OPENAI_API_KEY` را محافظت کنید

## 📈 بهینه‌سازی

### Performance:
- `workers=2` برای free plan
- `timeout=120` برای AI processing
- `whitenoise` برای static files

### Database:
- Connection pooling
- Index optimization
- Query optimization

## 🆘 پشتیبانی

### مشکلات رایج:
1. **Build failed**: بررسی requirements.txt
2. **Import error**: بررسی PYTHONPATH
3. **Database error**: بررسی DATABASE_URL
4. **Static files**: بررسی whitenoise

### منابع:
- [Render Documentation](https://render.com/docs)
- [Django Deployment](https://docs.djangoproject.com/en/5.0/howto/deployment/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)

---

**نکته مهم**: اگر هنوز مشکل `core.wsgi:application` دارید، احتمالاً Render از cache استفاده می‌کند. سرویس را delete کنید و دوباره ایجاد کنید.
