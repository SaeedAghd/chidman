# 🚀 راهنمای گام به گام دیپلوی

## مرحله 1: ورود به Liara
1. برو به: https://liara.ir
2. روی "ورود" کلیک کن
3. اطلاعات حساب کاربری را وارد کن
4. وارد داشبورد شو

## مرحله 2: انتخاب پروژه
1. در داشبورد، پروژه `chidmano` را پیدا کن
2. روی نام پروژه کلیک کن
3. وارد پنل مدیریت پروژه شو

## مرحله 3: تنظیم Environment Variables
1. در منوی سمت راست، روی "Environment Variables" کلیک کن
2. این متغیرها را اضافه کن:

### متغیرهای اصلی:
```
SECRET_KEY = 1-++(gh-*#+j1@5_c&ls2te#1n44iii98r%-0^2aan3h$&$esj
DEBUG = False
PRODUCTION = True
```

### متغیرهای پرداخت (تست):
```
PING_SANDBOX = True
PING_API_KEY = test-api-key-for-development
PING_CALLBACK_URL = https://chidmano.liara.app/payment/callback/
PING_RETURN_URL = https://chidmano.liara.app/payment/return/
```

### متغیرهای سایت:
```
SITE_URL = https://chidmano.liara.app
ALLOWED_HOSTS = chidmano.liara.app,*.liara.app,*.liara.run
```

### متغیرهای ایمیل (اختیاری):
```
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = your-email@gmail.com
EMAIL_HOST_PASSWORD = your-app-password
DEFAULT_FROM_EMAIL = noreply@chidmano.ir
```

## مرحله 4: دیپلوی
1. روی تب "Deploy" کلیک کن
2. روی دکمه "Deploy Now" کلیک کن
3. منتظر بمان تا فرآیند دیپلوی کامل شود
4. وقتی "Deployed Successfully" نمایش داده شد، دیپلوی تمام شده

## مرحله 5: تست سایت
بعد از دیپلوی موفق، این لینک‌ها را چک کن:

### تست‌های اولیه:
- https://chidmano.liara.app/ (صفحه اصلی)
- https://chidmano.liara.app/sitemap.xml (sitemap)
- https://chidmano.liara.app/robots.txt (robots)
- https://chidmano.liara.app/store/ (صفحه فروشگاه)

### تست کیف پول:
1. وارد حساب کاربری شو
2. برو به: https://chidmano.liara.app/store/wallet/
3. روی "شارژ کیف پول" کلیک کن
4. مبلغی وارد کن (مثلاً 10,000 تومان)
5. بررسی کن که پیغام موفقیت نمایش داده می‌شود

### تست تیکت پشتیبانی:
1. برو به: https://chidmano.liara.app/store/support/
2. تیکت جدید ایجاد کن
3. بررسی کن که پیغام موفقیت نمایش داده می‌شود

## مرحله 6: تغییر به کلید اصلی
اگر همه تست‌ها موفق بود:

1. در Environment Variables:
   - `PING_SANDBOX` را به `False` تغییر بده
   - `PING_API_KEY` را به کلید واقعی پی پینگ تغییر بده

2. دوباره دیپلوی کن

## 🔍 عیب‌یابی احتمالی:

### اگر سایت لود نمی‌شود:
- Environment Variables را چک کن
- Logs را در Liara بررسی کن
- SECRET_KEY و DEBUG را چک کن

### اگر کیف پول کار نمی‌کند:
- PING_SANDBOX را چک کن
- PING_API_KEY را چک کن
- Callback URLs را چک کن

### اگر SEO کار نمی‌کند:
- Sitemap و robots را چک کن
- ALLOWED_HOSTS را چک کن

---

## 📞 پشتیبانی:
اگر مشکلی پیش آمد، خطاها را کپی کن و بفرست تا کمکت کنم.

**حالا دیپلوی کن و نتیجه را بگو! 🚀**
