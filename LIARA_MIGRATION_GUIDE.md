# 🚀 راهنمای اجرای Migration در Liara

این راهنما به شما کمک می‌کند تا Migration ها را در محیط Liara اجرا کنید.

## 📋 روش‌های مختلف اجرای Migration

### روش 1: استفاده از اسکریپت (ساده‌ترین)

#### Windows (PowerShell):
```powershell
.\liara_migrate.ps1
```

#### Linux/Mac (Bash):
```bash
chmod +x liara_migrate.sh
./liara_migrate.sh
```

### روش 2: دستور مستقیم Liara CLI

#### اجرای Migration 0116 (فقط فیلدهای missing):
```bash
liara shell -c "python manage.py migrate store_analysis 0116 --verbosity=2"
```

#### اجرای تمام Migration ها:
```bash
liara shell -c "python manage.py migrate --verbosity=2"
```

#### بررسی وضعیت Migration ها:
```bash
liara shell -c "python manage.py showmigrations store_analysis"
```

### روش 3: Shell دستی (برای کارهای پیچیده)

#### باز کردن Shell دستی:
```bash
liara shell
```

#### سپس در Shell اجرا کنید:
```bash
# بررسی وضعیت
python manage.py showmigrations store_analysis

# اجرای Migration 0116
python manage.py migrate store_analysis 0116

# یا اجرای تمام Migration ها
python manage.py migrate

# خروج
exit
```

## 🔍 بررسی وضعیت Migration

### بررسی Migration های انجام نشده:
```bash
liara shell -c "python manage.py showmigrations store_analysis | grep '\[ \]'"
```

### بررسی Migration های انجام شده:
```bash
liara shell -c "python manage.py showmigrations store_analysis | grep '\[X\]'"
```

## ⚠️ عیب‌یابی

### مشکل 1: Liara CLI نصب نیست
```bash
npm install -g @liara/cli
liara login
```

### مشکل 2: خطای Database Connection
- مطمئن شوید `DATABASE_URL` در محیط Liara تنظیم شده است
- بررسی کنید که PostgreSQL service در Liara فعال است

### مشکل 3: خطای Permission
```bash
# بررسی لاگ‌ها
liara logs

# یا در Shell
liara shell -c "python manage.py migrate --verbosity=2"
```

## 📊 Migration 0116 - جزئیات

این Migration فیلدهای زیر را اضافه می‌کند:
- `package_type` (VARCHAR 20, default: 'basic')
- `store_address` (TEXT, nullable)

### بررسی وجود فیلدها:
```bash
liara shell -c "python -c \"from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT column_name FROM information_schema.columns WHERE table_name=\\'store_analysis_storeanalysis\\' AND column_name IN (\\'package_type\\', \\'store_address\\')'); print([row[0] for row in cursor.fetchall()])\""
```

## ✅ چک‌لیست پس از Migration

1. ✅ بررسی لاگ‌ها برای خطا:
   ```bash
   liara logs | grep -i migration
   ```

2. ✅ تست داشبورد کاربر:
   - باز کردن `/store/dashboard/`
   - باید بدون خطای 500 کار کند

3. ✅ بررسی فیلدها در دیتابیس:
   ```bash
   liara shell -c "python run_migration_116.py"
   ```

## 🆘 پشتیبانی

در صورت مشکل:
1. لاگ‌های Liara را بررسی کنید: `liara logs`
2. از Shell دستی برای دیباگ استفاده کنید: `liara shell`
3. Migration را به صورت دستی اجرا کنید

## 📝 نکات مهم

- ⚠️ Migration 0116 **Safe** است - اگر فیلدها وجود داشته باشند، اضافه نمی‌شوند
- ✅ می‌توانید چندبار اجرا کنید بدون مشکل
- 🔒 در production همیشه قبل از migration، backup بگیرید
- 📊 برای بررسی وضعیت از `showmigrations` استفاده کنید

