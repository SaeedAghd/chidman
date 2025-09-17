# 🚀 چیدمانو - آماده برای آپلود در Liara

## ✅ وضعیت پروژه
- **Django Version**: 4.2.23
- **Python Version**: 3.11.9
- **Database**: PostgreSQL
- **Static Files**: جمع‌آوری شده (189 فایل)
- **Migrations**: آماده
- **Tests**: اصلاح شده

## 🎯 ویژگی‌های فعال

### 👑 داشبورد ادمین حرفه‌ای
- آمار جامع سیستم
- نمودارهای تعاملی
- فعالیت‌های اخیر
- دسترسی سریع

### 💳 سیستم کیف پول
- واریز و برداشت
- تراکنش‌ها
- پرداخت از کیف پول

### 🎫 سیستم پشتیبانی
- مرکز پشتیبانی
- FAQ
- تیکت‌ها

### 💰 پرداخت زرین‌پال
- درگاه پرداخت
- مدیریت تخفیف‌ها

### 🤖 AI Analysis
- GPT-4.1 (Liara AI)
- Ollama (Fallback)

## 📁 فایل‌های آماده

### Core Files
- ✅ `requirements.txt` - Dependencies کامل
- ✅ `Procfile` - Gunicorn configuration
- ✅ `runtime.txt` - Python 3.11.9
- ✅ `render.yaml` - Liara configuration
- ✅ `build.sh` - Build script

### Templates & Static
- ✅ `staticfiles/` - 189 فایل
- ✅ `templates/` - تمام templates
- ✅ `admin_dashboard.html` - داشبورد ادمین

## 🔧 Environment Variables مورد نیاز

```bash
# Django Core
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=chidmano.liara.app
DATABASE_URL=postgresql://...

# Payment
ZARINPAL_MERCHANT_ID=your-merchant-id
ZARINPAL_SANDBOX=True

# AI Services
LIARA_AI_API_KEY=your-liara-ai-key
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

## 🚀 مراحل آپلود

### 1. آپلود کد
```bash
git add .
git commit -m "Ready for Liara deployment"
git push origin main
```

### 2. ایجاد سرویس در Liara
1. وارد [Liara Dashboard](https://console.liara.ir) شوید
2. "ایجاد سرویس جدید" → "Web App"
3. نام: `chidmano`
4. پلتفرم: `Python`

### 3. تنظیم Environment Variables
تمام متغیرهای بالا را در Liara Dashboard اضافه کنید

### 4. ایجاد دیتابیس
1. "Database" → "PostgreSQL"
2. نام: `chidmano-db`
3. Plan: `Starter`

### 5. Build Commands
```bash
# Build Command
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

# Start Command
gunicorn chidmano.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
```

## 📊 آمار فعلی
- **کاربران**: 4
- **تحلیل‌ها**: 6
- **پرداخت‌ها**: 9
- **سفارش‌ها**: 9

## 🌐 URL های فعال

### کاربران
- `/` - صفحه اصلی
- `/store/dashboard/` - داشبورد کاربر
- `/store/wallet/` - کیف پول
- `/store/support/` - پشتیبانی

### ادمین‌ها
- `/store/admin-dashboard/` - داشبورد ادمین 👑
- `/store/admin/pricing/` - مدیریت قیمت‌ها
- `/store/admin/discounts/` - مدیریت تخفیف‌ها
- `/store/admin/support-tickets/` - تیکت‌های پشتیبانی
- `/store/admin/wallets/` - مدیریت کیف پول‌ها
- `/admin/` - پنل Django

## ⚠️ نکات مهم

1. **Zarinpal**: نیاز به تنظیم Merchant ID واقعی
2. **Email**: نیاز به تنظیم SMTP
3. **AI**: نیاز به تنظیم Liara AI API Key
4. **Domain**: تنظیم domain سفارشی (اختیاری)

## 🎉 نتیجه

**سیستم کاملاً آماده آپلود است!** 🚀

تمام ویژگی‌های اصلی کار می‌کنند و سیستم stable است. فقط نیاز به تنظیم environment variables در Liara دارد.

---

**تاریخ آماده‌سازی**: 2025-09-17  
**نسخه**: 1.0.0  
**وضعیت**: آماده برای Production
