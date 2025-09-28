# 🚀 راهنمای سریع دیپلوی

## مراحل دیپلوی در Liara:

### 1️⃣ ورود به Liara
- برو به: https://liara.ir
- وارد حساب کاربری شو
- پروژه `chidmano` را انتخاب کن

### 2️⃣ تنظیم Environment Variables
در بخش Environment Variables این مقادیر را اضافه کن:

```bash
# تنظیمات اصلی
SECRET_KEY=1-++(gh-*#+j1@5_c&ls2te#1n44iii98r%-0^2aan3h$&$esj
DEBUG=False
PRODUCTION=True

# تنظیمات پرداخت (تست)
PING_SANDBOX=True
PING_API_KEY=test-api-key-for-development
PING_CALLBACK_URL=https://chidmano.liara.app/payment/callback/
PING_RETURN_URL=https://chidmano.liara.app/payment/return/

# تنظیمات سایت
SITE_URL=https://chidmano.liara.app
ALLOWED_HOSTS=chidmano.liara.app,*.liara.app,*.liara.run

# تنظیمات ایمیل
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@chidmano.ir
```

### 3️⃣ دیپلوی
- روی "Deploy Now" کلیک کن
- منتظر بمان تا دیپلوی کامل شود

### 4️⃣ تست
بعد از دیپلوی این لینک‌ها را چک کن:

✅ **تست‌های اولیه:**
- https://chidmano.liara.app/
- https://chidmano.liara.app/sitemap.xml
- https://chidmano.liara.app/robots.txt
- https://chidmano.liara.app/store/

✅ **تست کیف پول:**
1. وارد حساب کاربری شو
2. برو به: https://chidmano.liara.app/store/wallet/
3. روی "شارژ کیف پول" کلیک کن
4. مبلغ وارد کن (مثلاً 10,000 تومان)
5. بررسی کن که پیغام موفقیت نمایش داده می‌شود

✅ **تست تیکت پشتیبانی:**
1. برو به: https://chidmano.liara.app/store/support/
2. تیکت جدید ایجاد کن
3. بررسی کن که پیغام موفقیت نمایش داده می‌شود

### 5️⃣ بعد از تست موفق
اگر همه چیز کار کرد، کلید اصلی پی پینگ را بگذار:

```bash
PING_SANDBOX=False
PING_API_KEY=your-real-ping-api-key
```

سپس دوباره دیپلوی کن.

---

## 🎯 نکات مهم:
- در حالت تست، پیغام موفقیت نمایش داده می‌شود
- در حالت production، به صفحه پی پینگ هدایت می‌شوی
- همه مشکلات قبلی حل شده‌اند
- SEO فعال است

**حالا دیپلوی کن! 🚀**
