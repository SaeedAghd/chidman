# راهنمای دیپلوی - چیدمانو

## تنظیمات Environment Variables برای Liara

### 1. تنظیمات اصلی Django
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
PRODUCTION=True
```

### 2. تنظیمات دیتابیس
```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

### 3. تنظیمات پرداخت - پی پینگ
```bash
PING_SANDBOX=False
PING_API_KEY=your-real-ping-api-key
PING_CALLBACK_URL=https://chidmano.ir/payment/callback/
PING_RETURN_URL=https://chidmano.ir/payment/return/
```

### 4. تنظیمات سایت
```bash
SITE_URL=https://chidmano.ir
ALLOWED_HOSTS=chidmano.ir,www.chidmano.ir,*.liara.app,*.liara.run
```

### 5. تنظیمات ایمیل
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@chidmano.ir
```

### 6. تنظیمات Liara AI
```bash
LIARA_AI_API_KEY=your-liara-ai-api-key
USE_LIARA_AI=True
FALLBACK_TO_OLLAMA=True
```

## مراحل دیپلوی

### 1. آماده‌سازی
- ✅ Static files جمع‌آوری شدند
- ✅ Migrations اعمال شدند
- ✅ Security settings تنظیم شدند
- ✅ SEO فعال شد

### 2. دیپلوی در Liara
1. کد را به repository push کنید
2. Environment variables را در Liara تنظیم کنید
3. Build و Deploy را اجرا کنید

### 3. تست‌های پس از دیپلوی

#### تست کیف پول:
1. وارد حساب کاربری شوید
2. به بخش کیف پول بروید
3. مبلغی برای شارژ وارد کنید
4. باید به صفحه پی پینگ هدایت شوید

#### تست SEO:
1. `/sitemap.xml` - باید قابل دسترس باشد
2. `/robots.txt` - باید قابل دسترس باشد
3. Meta tags در صفحات بررسی شوند

#### تست تیکت پشتیبانی:
1. تیکت جدید ایجاد کنید
2. پیغام موفقیت باید نمایش داده شود
3. تیکت در لیست نمایش داده شود

## نکات مهم

- در production، `PING_SANDBOX=False` تنظیم کنید
- کلید واقعی پی پینگ را وارد کنید
- SSL در Liara خودکار فعال است
- Static files از طریق WhiteNoise سرو می‌شوند

## عیب‌یابی

### اگر کیف پول کار نمی‌کند:
1. `PING_SANDBOX=False` بررسی کنید
2. `PING_API_KEY` واقعی باشد
3. Callback URLs صحیح باشند

### اگر SEO کار نمی‌کند:
1. `/sitemap.xml` و `/robots.txt` را چک کنید
2. Google Search Console را تنظیم کنید
3. Meta tags را بررسی کنید
