# 🗑️ راهنمای پاک‌سازی دیتابیس

## ⚠️ هشدار مهم

این عملیات **غیرقابل بازگشت** است! تمام داده‌های زیر حذف می‌شوند:

- ✅ تمام تحلیل‌های فروشگاه (StoreAnalysis)
- ✅ تمام سفارشات (Order)
- ✅ تمام تیکت‌های پشتیبانی (SupportTicket)
- ✅ تمام کاربران غیر admin
- ✅ تمام پرداخت‌ها و داده‌های مرتبط

**فقط کاربران admin باقی می‌مانند!**

---

## 📋 روش اجرا

### روش 1: اجرای مستقیم در Liara Shell

```bash
# اتصال به shell Liara
liara shell

# اجرای اسکریپت
python cleanup_database.py
```

### روش 2: اجرا از Django Shell

```bash
# اتصال به Django shell در Liara
liara shell
python manage.py shell

# سپس در shell:
exec(open('cleanup_database.py').read())
```

### روش 3: اجرای دستور مستقیم

```bash
# در Liara shell:
python manage.py shell <<EOF
from django.contrib.auth.models import User
from store_analysis.models import StoreAnalysis, Order, SupportTicket

# حذف تحلیل‌ها
StoreAnalysis.objects.all().delete()

# حذف سفارشات
Order.objects.all().delete()

# حذف تیکت‌ها
SupportTicket.objects.all().delete()

# حذف کاربران غیر admin
User.objects.filter(is_staff=False, is_superuser=False).delete()
EOF
```

---

## 🔒 نکات امنیتی

1. ✅ قبل از اجرا، از دیتابیس backup بگیرید
2. ✅ مطمئن شوید که کاربران admin را می‌شناسید
3. ✅ اسکریپت دو بار تأیید می‌گیرد
4. ✅ تمام عملیات در یک transaction انجام می‌شود (یا همه یا هیچ!)

---

## ✅ بعد از پاک‌سازی

بعد از اجرای اسکریپت:
- تمام تحلیل‌ها حذف شده‌اند
- فقط کاربران admin باقی مانده‌اند
- دیتابیس آماده برای شروع جدید است

---

## 📝 تست

بعد از پاک‌سازی می‌توانید بررسی کنید:

```python
from django.contrib.auth.models import User
from store_analysis.models import StoreAnalysis

# بررسی کاربران
print(f"تعداد کاربران: {User.objects.count()}")
print(f"کاربران admin: {User.objects.filter(is_staff=True).count()}")

# بررسی تحلیل‌ها
print(f"تعداد تحلیل‌ها: {StoreAnalysis.objects.count()}")
```

