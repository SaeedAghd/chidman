# 🚀 مراحل اجرای Migration در Liara

## ✅ وضعیت فعلی:
- Migration 0074: **FAKED** ✅
- Migration 0117: نیاز به اجرا (اضافه کردن فیلد address)
- Migration 0116: نیاز به اجرا (اضافه کردن store_address و package_type)

---

## 📋 مراحل:

### Step 1: باز کردن Liara Shell
```bash
liara shell
```

### Step 2: اضافه کردن فیلد address (اگر وجود ندارد)
در Shell اجرا کنید:
```python
python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings'); django.setup(); from django.db import connection; cursor = connection.cursor(); cursor.execute('ALTER TABLE store_analysis_userprofile ADD COLUMN IF NOT EXISTS address TEXT'); connection.commit(); print('✅ فیلد address اضافه شد')"
```

### Step 3: ادامه Migration ها
```bash
python manage.py migrate store_analysis --verbosity=2
```

یا اگر فقط می‌خواهید migration 0116 را اجرا کنید:
```bash
python manage.py migrate store_analysis 0116 --verbosity=2
```

### Step 4: بررسی وضعیت
```bash
python manage.py showmigrations store_analysis | tail -20
```

### Step 5: خروج
```bash
exit
```

---

## 🎯 روش سریع (یک دستوری):

```bash
liara shell -c "python manage.py migrate --fake store_analysis 0074 && python manage.py migrate store_analysis --verbosity=2"
```

---

## ✅ چک لیست بعد از Migration:

1. ✅ داشبورد کاربر کار می‌کند: `/store/dashboard/`
2. ✅ لاگ‌ها خطا ندارند: `liara logs | grep -i error`
3. ✅ فیلدها اضافه شده‌اند:
   ```bash
   python manage.py shell
   >>> from store_analysis.models import StoreAnalysis, UserProfile
   >>> # بررسی فیلدها
   ```

---

## 🔍 عیب‌یابی:

اگر خطا داشتید:
1. بررسی لاگ: `liara logs`
2. بررسی وضعیت migration: `python manage.py showmigrations`
3. Fake کردن migration مشکل‌دار: `python manage.py migrate --fake ...`

