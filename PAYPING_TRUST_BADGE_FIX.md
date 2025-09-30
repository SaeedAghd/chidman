# راهنمای حل مشکل نماد اعتماد PayPing

## 🔍 مشکل فعلی:
- PayPing می‌گوید نماد اعتماد ندارید
- Token جدید دریافت کرده‌اید ولی کار نمی‌کند
- صفحه لود نمی‌شود

## ✅ راه‌حل‌های اعمال شده:

### 1. **بروزرسانی تنظیمات PayPing:**
```python
# در settings.py
PAYMENT_GATEWAY = {
    'PING_PAYMENT': {
        'MERCHANT_ID': '17D62CFE490EA7C6BF20090BEA12A49FEB4482B02F8534696215A6DE23DF684A-1',
        'API_KEY': '9CB1E1741B931D55964DC4933CA11B35CDBFB0B18F636F3125D7071BB1AB0522-1',
        'CALLBACK_URL': 'https://chidmano.ir/store/payment/payping/callback/',
        'RETURN_URL': 'https://chidmano.ir/store/payment/payping/return/',
        'SANDBOX': False,
        'API_URL': 'https://api.pingpayment.ir',
        'TRUST_BADGE': True,  # فعال‌سازی نماد اعتماد
        'VERIFY_SSL': True
    }
}
```

### 2. **بروزرسانی Token:**
```python
# در settings.py
PAYPING_TOKEN = '9CB1E1741B931D55964DC4933CA11B35CDBFB0B18F636F3125D7071BB1AB0522-1'
```

### 3. **تست اتصال PayPing:**
- URL جدید: `/store/test/payping/`
- فقط برای ادمین‌ها قابل دسترسی

## 🔧 مراحل حل مشکل:

### مرحله 1: بررسی تنظیمات PayPing
1. وارد پنل PayPing شوید
2. تنظیمات نماد اعتماد را بررسی کنید
3. مطمئن شوید که نماد اعتماد فعال است

### مرحله 2: بررسی Domain
1. در پنل PayPing، domain `chidmano.ir` را اضافه کنید
2. مطمئن شوید که callback URL درست است
3. SSL certificate را بررسی کنید

### مرحله 3: تست اتصال
1. وارد admin panel شوید
2. به `/store/test/payping/` بروید
3. نتیجه تست را بررسی کنید

### مرحله 4: بررسی Logs
1. لاگ‌های سرور را بررسی کنید
2. خطاهای PayPing را پیدا کنید
3. در صورت نیاز تنظیمات را اصلاح کنید

## 🚨 مشکلات احتمالی:

### 1. **مشکل SSL:**
- مطمئن شوید که SSL certificate معتبر است
- `VERIFY_SSL: True` را در تنظیمات قرار دهید

### 2. **مشکل Domain:**
- Domain باید در پنل PayPing ثبت شده باشد
- Callback URL باید دقیقاً مطابق باشد

### 3. **مشکل Token:**
- Token باید جدید و معتبر باشد
- Token باید برای production باشد (نه sandbox)

## 📋 چک‌لیست:

- [ ] Token جدید در settings.py قرار گرفته
- [ ] Domain در پنل PayPing ثبت شده
- [ ] SSL certificate معتبر است
- [ ] Callback URL درست است
- [ ] نماد اعتماد در پنل PayPing فعال است
- [ ] تست اتصال موفق است

## 🔄 در صورت ادامه مشکل:

1. **تماس با پشتیبانی PayPing:**
   - شماره: 021-9100-9100
   - ایمیل: support@payping.ir

2. **ارسال اطلاعات:**
   - Domain: chidmano.ir
   - Merchant ID: 17D62CFE490EA7C6BF20090BEA12A49FEB4482B02F8534696215A6DE23DF684A-1
   - مشکل: نماد اعتماد فعال نیست

3. **درخواست فعال‌سازی:**
   - درخواست فعال‌سازی نماد اعتماد
   - بررسی تنظیمات domain
   - تست اتصال API

## 📞 پشتیبانی:
- **PayPing:** 021-9100-9100
- **پنل PayPing:** https://panel.payping.ir
- **مستندات:** https://docs.payping.ir

---
**تاریخ:** 2025-09-30
**وضعیت:** در انتظار تست
