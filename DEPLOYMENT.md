# راهنمای دیپلوی Chidmano روی لیارا

این فایل شامل دستورالعمل‌های کامل برای دیپلوی پروژه Chidmano روی پلتفرم لیارا است.

## 📋 پیش‌نیازها

1. **نصب Node.js و npm** (برای نصب Liara CLI)
2. **حساب کاربری لیارا** (ثبت‌نام در [liara.ir](https://liara.ir))
3. **دسترسی به پروژه** (Git repository)

## 🔧 نصب و راه‌اندازی

### 1. نصب Liara CLI

```bash
npm install -g @liara/cli
```

### 2. ورود به حساب کاربری لیارا

```bash
liara login
```

### 3. ایجاد پروژه در لیارا (اگر قبلاً ایجاد نشده)

```bash
liara app:create chidmano --platform django
```

## 📁 فایل‌های دیپلوی

پروژه شامل فایل‌های زیر برای دیپلوی است:

- **`liara.json`**: تنظیمات پلتفرم لیارا
- **`Procfile`**: فرمان اجرای برنامه (`web: python3 main.py`)
- **`runtime.txt`**: نسخه پایتون (3.11.0)
- **`main.py`**: نقطه ورود اصلی که مایگریشن‌ها را اجرا می‌کند و Gunicorn را راه‌اندازی می‌کند
- **`gunicorn.conf.py`**: تنظیمات Gunicorn
- **`requirements.txt`**: وابستگی‌های Python

## ⚙️ تنظیم متغیرهای محیطی

در داشبورد لیارا یا با CLI، متغیرهای زیر را تنظیم کنید:

### متغیرهای ضروری:

```bash
# Django Core
SECRET_KEY=your-super-secret-key-here
DEBUG=False
PRODUCTION=True
LIARA=true
ALLOWED_HOSTS=chidmano.liara.app,chidmano.ir,www.chidmano.ir

# Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# AI Configuration
LIARA_AI_API_KEY=your_liara_ai_api_key
LIARA_AI_PROJECT_ID=690f9dd94e6dbd1c22243c26
LIARA_AI_MODEL=openai/gpt-4o-mini
USE_LIARA_AI=True

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=info@chidmano.com

# Payment Gateway (PayPing)
PAYPING_TOKEN=851E282188994B8B0D7C94106BABC5FAC9A967E4B65059CB9D290A7A030C1ECF-1
PAYPING_SANDBOX=False
PAYPING_CALLBACK_URL=https://chidmano.ir/store/payment/payping/callback/
PAYPING_RETURN_URL=https://chidmano.ir/store/payment/payping/return/
PING_API_KEY=851E282188994B8B0D7C94106BABC5FAC9A967E4B65059CB9D290A7A030C1ECF-1
PING_CALLBACK_URL=https://chidmano.ir/store/payment/payping/callback/
PING_RETURN_URL=https://chidmano.ir/store/payment/payping/return/
```

### تنظیم با CLI:

```bash
# تنظیم متغیرهای محیطی
liara env:set SECRET_KEY="your-secret-key" --app chidmano
liara env:set DEBUG="False" --app chidmano
liara env:set DATABASE_URL="postgresql://..." --app chidmano
```

## 🗄️ تنظیم دیتابیس PostgreSQL

1. در داشبورد لیارا، یک سرویس PostgreSQL ایجاد کنید
2. از بخش «اتصال»، مقدار `DATABASE_URL` را کپی کنید
3. آن را به عنوان متغیر محیطی تنظیم کنید
4. مطمئن شوید که SSL غیرفعال است (در کد پیش‌فرض غیرفعال شده است)

## 🚀 دیپلوی

### روش 1: استفاده از اسکریپت deploy.sh

```bash
chmod +x deploy.sh
./deploy.sh
```

### روش 2: دیپلوی مستقیم با Liara CLI

```bash
liara deploy
```

یا برای برنامه خاص:

```bash
liara deploy --app chidmano
```

## 📊 فرآیند دیپلوی

هنگام دیپلوی، مراحل زیر به صورت خودکار انجام می‌شود:

1. **Build**: فایل‌های پروژه آپلود می‌شوند
2. **Collectstatic**: فایل‌های استاتیک جمع‌آوری می‌شوند (در مرحله build)
3. **Migration**: مایگریشن‌ها به صورت خودکار اجرا می‌شوند (در `main.py`)
4. **Start**: Gunicorn با تنظیمات `gunicorn.conf.py` راه‌اندازی می‌شود

## 🔍 Health Check

پروژه شامل یک endpoint برای health check است:

- **URL**: `/health`
- **Method**: GET
- **Response**: `OK` (200)

این endpoint در `liara.json` تنظیم شده است و لیارا از آن برای بررسی سلامت برنامه استفاده می‌کند.

## 🐛 عیب‌یابی

### بررسی لاگ‌ها

```bash
liara logs --app chidmano
```

### بررسی وضعیت برنامه

```bash
liara app:status --app chidmano
```

### اجرای دستورات در محیط production

```bash
liara shell --app chidmano
```

### مشکلات رایج

1. **خطای مایگریشن**: مایگریشن‌ها به صورت خودکار در `main.py` اجرا می‌شوند. اگر خطایی رخ داد، لاگ‌ها را بررسی کنید.

2. **خطای collectstatic**: فایل‌های استاتیک در مرحله build جمع‌آوری می‌شوند. اگر خطایی رخ داد، مطمئن شوید که `STATIC_ROOT` در `settings.py` تنظیم شده است.

3. **خطای دیتابیس**: مطمئن شوید که `DATABASE_URL` به درستی تنظیم شده و SSL غیرفعال است.

4. **خطای timeout**: timeout پیش‌فرض 300 ثانیه (5 دقیقه) است. اگر نیاز به تغییر دارید، متغیر `TIMEOUT` را تنظیم کنید.

## 📝 نکات مهم

- فایل `.env` در production استفاده نمی‌شود. همه متغیرهای محیطی باید در لیارا تنظیم شوند.
- فایل‌های `media/` و `staticfiles/` در production باید از طریق storage service (مثل S3) سرو شوند.
- برای بهینه‌سازی عملکرد، `WEB_CONCURRENCY` روی 1 تنظیم شده است (برای کاهش مصرف حافظه).

## 🔐 امنیت

- `DEBUG` باید در production روی `False` باشد
- `SECRET_KEY` باید یک مقدار تصادفی و امن باشد
- SSL/TLS به صورت خودکار توسط لیارا فعال می‌شود
- تنظیمات امنیتی Django در `settings.py` برای production فعال شده‌اند

## 📞 پشتیبانی

برای مشکلات و سوالات:
- مستندات لیارا: [docs.liara.ir](https://docs.liara.ir)
- پشتیبانی لیارا: [support@liara.ir](mailto:support@liara.ir)

