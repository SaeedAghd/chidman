# ⚡ اجرای سریع Migration در Liara

## 🎯 سریع‌ترین روش (کپی و اجرا)

### Windows (PowerShell):
```powershell
liara shell -c "python manage.py migrate store_analysis 0116 --verbosity=2"
```

### Linux/Mac:
```bash
liara shell -c "python manage.py migrate store_analysis 0116 --verbosity=2"
```

---

## 📝 مراحل کامل:

### 1. بررسی نصب Liara CLI:
```bash
liara --version
```

### 2. اگر نصب نیست:
```bash
npm install -g @liara/cli
liara login
```

### 3. اجرای Migration:
```bash
liara shell -c "python manage.py migrate store_analysis 0116 --verbosity=2"
```

### 4. بررسی نتیجه:
```bash
liara shell -c "python manage.py showmigrations store_analysis | grep 0116"
```

---

## 🐚 یا Shell دستی (برای کنترل بیشتر):

```bash
liara shell
```

سپس در Shell:
```bash
python manage.py migrate store_analysis 0116
python manage.py migrate
exit
```

---

## ✅ بعد از Migration:

1. بررسی لاگ:
   ```bash
   liara logs | grep -i migration
   ```

2. تست داشبورد:
   - باز کردن: `https://chidmano.ir/store/dashboard/`
   - باید بدون خطای 500 کار کند

