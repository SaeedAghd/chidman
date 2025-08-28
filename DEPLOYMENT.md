# 🚀 راهنمای کامل دیپلوی روی Render

این راهنما شامل تمام مراحل لازم برای دیپلوی موفق پروژه چیدمان روی Render است.

## 📋 پیش‌نیازها

### 1. حساب Render
- ثبت‌نام در [Render.com](https://render.com)
- اتصال حساب گیت‌هاب

### 2. کلیدهای API
- **OpenAI API Key**: برای قابلیت‌های AI
- **Email API** (اختیاری): برای ارسال ایمیل

## 🔧 مراحل دیپلوی

### مرحله 1: آماده‌سازی Repository

1. **اطمینان از وجود فایل‌های ضروری**:
   ```
   ✅ render.yaml
   ✅ build.sh
   ✅ requirements.txt
   ✅ runtime.txt
   ✅ Procfile
   ✅ chidmano/wsgi.py
   ✅ manage.py
   ```

2. **Push کردن کد به گیت‌هاب**:
   ```bash
   git add .
   git commit -m "آماده‌سازی برای دیپلوی روی Render"
   git push origin main
   ```

### مرحله 2: ایجاد سرویس در Render

1. **ورود به Render Dashboard**
2. **انتخاب "New Web Service"**
3. **اتصال به گیت‌هاب Repository**
4. **انتخاب Repository پروژه**

### مرحله 3: تنظیمات سرویس

#### تنظیمات اصلی:
- **Name**: `chidman-store-analysis`
- **Environment**: `Python`
- **Region**: نزدیک‌ترین منطقه به کاربران
- **Branch**: `main`
- **Root Directory**: (خالی بگذارید)

#### تنظیمات Build:
- **Build Command**: `chmod +x build.sh && ./build.sh`
- **Start Command**: `gunicorn chidmano.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

### مرحله 4: تنظیم متغیرهای محیطی

#### متغیرهای ضروری:
```
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=chidman-store-analysis.onrender.com
DATABASE_URL=postgresql://... (از Render Database)
OPENAI_API_KEY=your-openai-api-key
```

#### متغیرهای امنیتی:
```
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS=DENY
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### مرحله 5: ایجاد دیتابیس

1. **انتخاب "New PostgreSQL"**
2. **تنظیمات دیتابیس**:
   - Name: `chidman-db`
   - Database: `chidman`
   - User: `chidman_user`
   - Plan: `Free`

3. **اتصال دیتابیس به سرویس**:
   - در سرویس، متغیر `DATABASE_URL` را به دیتابیس متصل کنید

## 🔍 عیب‌یابی مشکلات رایج

### مشکل 1: Build Failed
**علت**: خطا در نصب dependencies
**راه‌حل**:
- بررسی `requirements.txt`
- اطمینان از سازگاری نسخه‌ها
- بررسی `runtime.txt`

### مشکل 2: Database Connection Error
**علت**: تنظیمات نادرست DATABASE_URL
**راه‌حل**:
- بررسی اتصال دیتابیس
- اطمینان از صحت متغیر DATABASE_URL

### مشکل 3: Static Files Not Found
**علت**: عدم جمع‌آوری فایل‌های static
**راه‌حل**:
- بررسی `STATIC_ROOT` در settings
- اطمینان از اجرای `collectstatic`

### مشکل 4: WSGI Application Error
**علت**: مسیر نادرست WSGI
**راه‌حل**:
- بررسی `chidmano/wsgi.py`
- اطمینان از صحت `DJANGO_SETTINGS_MODULE`

## 📊 مانیتورینگ و نگهداری

### 1. لاگ‌ها
- بررسی لاگ‌های Build
- بررسی لاگ‌های Runtime
- مانیتورینگ خطاها

### 2. عملکرد
- بررسی Response Time
- مانیتورینگ Memory Usage
- بررسی Database Performance

### 3. امنیت
- بررسی Security Headers
- مانیتورینگ Failed Login Attempts
- بررسی SSL Certificate

## 🔄 به‌روزرسانی

### 1. تغییرات کد
```bash
git add .
git commit -m "تغییرات جدید"
git push origin main
```

### 2. تغییرات متغیرهای محیطی
- در Render Dashboard
- تغییر متغیر مورد نظر
- Redeploy سرویس

### 3. تغییرات دیتابیس
- اجرای مایگریشن‌های جدید
- بررسی سازگاری داده‌ها

## 📞 پشتیبانی

### منابع مفید:
- [Render Documentation](https://render.com/docs)
- [Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

### تماس:
- **Issues**: برای گزارش مشکلات
- **Discussions**: برای سوالات
- **Email**: برای پشتیبانی مستقیم

## ✅ چک‌لیست نهایی

- [ ] Repository در گیت‌هاب آماده است
- [ ] فایل‌های ضروری موجود هستند
- [ ] متغیرهای محیطی تنظیم شده‌اند
- [ ] دیتابیس ایجاد و متصل شده است
- [ ] سرویس با موفقیت دیپلوی شده است
- [ ] تست‌های عملکرد انجام شده‌اند
- [ ] امنیت بررسی شده است
- [ ] SSL Certificate فعال است

**🎉 تبریک! پروژه شما با موفقیت روی Render دیپلوی شده است!**
