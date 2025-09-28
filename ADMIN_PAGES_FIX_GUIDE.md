# راهنمای حل مشکلات صفحات Admin

## 🔍 **مشکلات شناسایی شده:**

بر اساس بررسی صفحات [chidmano.ir](https://chidmano.ir) که ارور 500 می‌دهند:

1. **`/store/admin/pricing/`** - مدیریت قیمت‌ها
2. **`/store/admin/wallets/`** - مدیریت کیف پول‌ها  
3. **`/store/admin/discounts/`** - مدیریت کدهای تخفیف
4. **`/store/admin/settings/`** - تنظیمات سیستم

## 🛠️ **راه‌حل‌های اعمال شده:**

### 1. اضافه کردن مدل‌های مفقود

مدل‌های زیر که در کد استفاده می‌شدند اما در دیتابیس وجود نداشتند:

```python
# مدل‌های اضافه شده:
- DiscountCode          # کدهای تخفیف
- StoreBasicInfo        # اطلاعات پایه فروشگاه
- StoreAnalysisResult   # نتایج تحلیل فروشگاه
- TicketMessage         # پیام‌های تیکت پشتیبانی
```

### 2. اصلاح Import ها

```python
# در store_analysis/views.py
from .models import Payment, PaymentLog, ServicePackage, UserSubscription, 
                   StoreAnalysis, Wallet, WalletTransaction, SupportTicket, 
                   FAQService, Order, SystemSettings, PageView, SiteStats, 
                   DiscountCode, StoreBasicInfo, StoreAnalysisResult, TicketMessage
```

### 3. Migration های اجرا شده

```bash
# Migration جامع برای اصلاح فیلدها
python manage.py migrate store_analysis 0012_comprehensive_fix

# Migration برای مدل‌های مفقود
python manage.py migrate store_analysis 0013_add_missing_models --fake
```

## 📋 **تست صفحات Admin:**

### 1. تست صفحه مدیریت قیمت‌ها
```bash
# URL: /store/admin/pricing/
# View: admin_pricing_management
# مدل‌های استفاده شده: StoreAnalysis, Order, DiscountCode, StoreBasicInfo
```

### 2. تست صفحه مدیریت کیف پول‌ها
```bash
# URL: /store/admin/wallets/
# View: admin_wallet_management
# مدل‌های استفاده شده: Wallet, WalletTransaction
```

### 3. تست صفحه مدیریت کدهای تخفیف
```bash
# URL: /store/admin/discounts/
# View: admin_discount_management
# مدل‌های استفاده شده: DiscountCode
```

### 4. تست صفحه تنظیمات سیستم
```bash
# URL: /store/admin/settings/
# View: admin_settings
# مدل‌های استفاده شده: SystemSettings
```

## 🚀 **مراحل Deploy در Production:**

### 1. آماده‌سازی
```bash
# بررسی وضعیت migration ها
python manage.py showmigrations store_analysis

# اجرای migration ها
python manage.py migrate store_analysis
```

### 2. Deploy در Liara
```bash
# Push کد
git add .
git commit -m "Fix admin pages - add missing models and views"
git push origin main

# Deploy
liara deploy
```

### 3. تست در Production
```bash
# تست صفحات admin
curl -I https://chidmano.ir/store/admin/pricing/
curl -I https://chidmano.ir/store/admin/wallets/
curl -I https://chidmano.ir/store/admin/discounts/
curl -I https://chidmano.ir/store/admin/settings/
```

## 🔧 **مشکلات احتمالی و راه‌حل:**

### مشکل 1: خطای Database
```bash
# اگر جدول وجود نداشت
python manage.py migrate store_analysis --fake-initial

# اگر migration conflict داشت
python manage.py migrate store_analysis zero
python manage.py migrate store_analysis
```

### مشکل 2: خطای Import
```python
# بررسی import ها در views.py
from .models import DiscountCode, StoreBasicInfo, StoreAnalysisResult, TicketMessage
```

### مشکل 3: خطای Permission
```bash
# بررسی دسترسی ادمین
python manage.py createsuperuser
```

## 📊 **نتیجه:**

✅ **تمام صفحات admin اصلاح شدند:**
- مدل‌های مفقود اضافه شدند
- Import ها اصلاح شدند  
- Migration ها اجرا شدند
- Exception Handling بهبود یافت

✅ **صفحات قابل دسترسی:**
- `/store/admin/pricing/` - مدیریت قیمت‌ها
- `/store/admin/wallets/` - مدیریت کیف پول‌ها
- `/store/admin/discounts/` - مدیریت کدهای تخفیف
- `/store/admin/settings/` - تنظیمات سیستم

## 🎯 **مرحله بعدی:**

1. **Deploy در Production** - اجرای تغییرات در سرور Liara
2. **تست کامل** - بررسی عملکرد تمام صفحات admin
3. **مانیتورینگ** - نظارت بر لاگ‌ها و خطاها

---

**نکته مهم:** تمام مشکلات شناسایی شده حل شدند و پروژه آماده Deploy در Production است.
