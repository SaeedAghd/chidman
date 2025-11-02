# 🚀 راهنمای کامل Migration در Liara

## 📊 وضعیت فعلی Migration ها:

✅ **Migration 0074**: FAKED (انجام شد)
✅ **Migration 0075**: OK (انجام شد)
❌ **Migration 0076**: خطا - فیلد `authority` از قبل وجود دارد
⏳ **Migration 0116**: انجام نشده - فیلدهای `store_address` و `package_type` نیاز دارند
⏳ **Migration 0117**: انجام نشده - فیلد `address` برای UserProfile

---

## 🔧 مراحل رفع مشکل:

### Step 1: Fake کردن Migration 0076
در Liara Shell:
```bash
python manage.py migrate store_analysis 0076 --fake
```

### Step 2: ادامه Migration ها
```bash
python manage.py migrate store_analysis --verbosity=2
```

### Step 3: بررسی نتیجه
```bash
python manage.py showmigrations store_analysis | grep -E "(0076|0116|0117)"
```

---

## 🎯 دستورات کامل (کپی و اجرا):

```bash
# وارد Shell شوید
liara shell

# Fake کردن 0076
python manage.py migrate store_analysis 0076 --fake

# ادامه Migration ها
python manage.py migrate store_analysis --verbosity=2

# بررسی
python manage.py showmigrations store_analysis | tail -10

# خروج
exit
```

---

## ✅ چک لیست بعد از Migration:

- [ ] Migration 0076: FAKED ✅
- [ ] Migration 0116: اجرا شد (store_address, package_type) ✅
- [ ] Migration 0117: اجرا شد (address) ✅
- [ ] داشبورد کار می‌کند: `/store/dashboard/` ✅
- [ ] لاگ‌ها خطا ندارند ✅

---

## 🔍 بررسی دستی فیلدها:

```bash
python manage.py shell
```

سپس:
```python
from django.db import connection
cursor = connection.cursor()

# بررسی StoreAnalysis
cursor.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name='store_analysis_storeanalysis' 
    AND column_name IN ('package_type', 'store_address')
""")
print("StoreAnalysis fields:", [row[0] for row in cursor.fetchall()])

# بررسی UserProfile
cursor.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name='store_analysis_userprofile' 
    AND column_name='address'
""")
print("UserProfile address:", [row[0] for row in cursor.fetchall()])

# بررسی Payment
cursor.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name='store_analysis_payment' 
    AND column_name='authority'
""")
print("Payment authority:", [row[0] for row in cursor.fetchall()])

exit()
```

---

## 🆘 اگر خطا داشتید:

### خطای DuplicateColumn:
```bash
# Fake کردن migration مشکل‌دار
python manage.py migrate store_analysis <MIGRATION_NUMBER> --fake
```

### خطای Missing Column:
```bash
# اجرای migration خاص
python manage.py migrate store_analysis <MIGRATION_NUMBER>
```

### بررسی Migration های انجام شده:
```bash
python manage.py showmigrations store_analysis
```

