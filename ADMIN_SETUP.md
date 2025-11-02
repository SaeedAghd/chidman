# 👤 راهنمای مدیریت ادمین در Liara

## 📋 گزینه‌های موجود:

### 1. ایجاد ادمین جدید
### 2. تغییر رمز ادمین موجود
### 3. بررسی ادمین‌های موجود

---

## 🚀 روش 1: ایجاد ادمین جدید (توصیه می‌شود)

### در Liara Shell:
```bash
liara shell
```

سپس:
```bash
python manage.py createsuperuser
```

شما باید اطلاعات زیر را وارد کنید:
- Username (نام کاربری)
- Email (ایمیل)
- Password (رمز عبور) - باید دو بار وارد کنید

---

## 🔑 روش 2: ایجاد ادمین با Python (بدون تعامل)

در Liara Shell:
```python
python manage.py shell
```

سپس:
```python
from django.contrib.auth.models import User

# بررسی ادمین‌های موجود
admins = User.objects.filter(is_superuser=True)
print(f"ادمین‌های موجود: {[u.username for u in admins]}")

# ایجاد ادمین جدید
username = "admin"
email = "admin@chidmano.ir"
password = "YourSecurePassword123!"

# بررسی وجود کاربر
if User.objects.filter(username=username).exists():
    print(f"⚠️ کاربر {username} از قبل وجود دارد")
    user = User.objects.get(username=username)
    user.is_superuser = True
    user.is_staff = True
    user.set_password(password)
    user.save()
    print(f"✅ ادمین {username} به‌روزرسانی شد")
else:
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✅ ادمین {username} ایجاد شد")

exit()
```

---

## 🔄 روش 3: تغییر رمز ادمین موجود

در Liara Shell:
```python
python manage.py shell
```

سپس:
```python
from django.contrib.auth.models import User

username = "admin"  # نام کاربری ادمین
new_password = "NewSecurePassword123!"

try:
    user = User.objects.get(username=username)
    user.set_password(new_password)
    user.save()
    print(f"✅ رمز ادمین {username} تغییر کرد")
except User.DoesNotExist:
    print(f"❌ کاربر {username} پیدا نشد")
    # لیست ادمین‌ها
    admins = User.objects.filter(is_superuser=True)
    print(f"ادمین‌های موجود: {[u.username for u in admins]}")

exit()
```

---

## 📋 روش 4: بررسی ادمین‌های موجود

در Liara Shell:
```python
python manage.py shell
```

سپس:
```python
from django.contrib.auth.models import User

# لیست تمام ادمین‌ها
admins = User.objects.filter(is_superuser=True)

print("=" * 50)
print("👤 لیست ادمین‌ها:")
print("=" * 50)

for admin in admins:
    print(f"\nUsername: {admin.username}")
    print(f"Email: {admin.email or 'ثبت نشده'}")
    print(f"Is Staff: {admin.is_staff}")
    print(f"Is Superuser: {admin.is_superuser}")
    print(f"Last Login: {admin.last_login or 'هرگز'}")
    print("-" * 50)

exit()
```

---

## 🎯 دستورات سریع (یک خطی)

### ایجاد ادمین جدید:
```bash
liara shell -c "python -c \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@chidmano.ir', 'YourPassword123!'); print('✅ ادمین ایجاد شد')\""
```

### تغییر رمز ادمین:
```bash
liara shell -c "python -c \"from django.contrib.auth.models import User; u = User.objects.get(username='admin'); u.set_password('NewPassword123!'); u.save(); print('✅ رمز تغییر کرد')\""
```

---

## 🔒 نکات امنیتی:

1. ✅ از رمز عبور قوی استفاده کنید (حداقل 12 کاراکتر، شامل حروف بزرگ، کوچک، اعداد و نمادها)
2. ✅ نام کاربری را به راحتی قابل حدس نکنید
3. ✅ ایمیل معتبر وارد کنید
4. ✅ رمز عبور را در جای امن نگه دارید
5. ✅ از رمز عبور یکسان برای چند حساب استفاده نکنید

---

## 📝 مثال کامل:

```bash
# 1. باز کردن Shell
liara shell

# 2. ایجاد ادمین
python manage.py createsuperuser

# یا با Python:
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_superuser('admin', 'admin@example.com', 'MySecurePass123!')
>>> exit()

# 3. بررسی
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.filter(is_superuser=True)
>>> exit()

# 4. خروج
exit
```

---

## 🆘 اگر فراموش کردید:

### بررسی تمام کاربران:
```python
python manage.py shell
>>> from django.contrib.auth.models import User
>>> for u in User.objects.all():
...     print(f"{u.username} - Superuser: {u.is_superuser}, Staff: {u.is_staff}")
>>> exit()
```

### ریست کردن رمز:
```python
python manage.py shell
>>> from django.contrib.auth.models import User
>>> u = User.objects.get(username='admin')
>>> u.set_password('NewPassword')
>>> u.save()
>>> exit()
```

