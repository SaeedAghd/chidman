# 🔧 راهنمای دیباگ فرم ثبت‌نام

## ✅ **تغییرات انجام شده:**

### 1. **اصلاح Template (signup.html)**
- ✅ فیلد `email` حالا به Django form متصل شده (`{{ form.email.name }}`)
- ✅ فیلد `phone` حالا به Django form متصل شده (`{{ form.phone.name }}`)
- ✅ اضافه شدن فیلدهای `first_name` و `last_name`
- ✅ نمایش خطاهای فیلد `email` و `phone`
- ✅ حفظ مقدار فیلدها با `value="{{ form.field.value|default:'' }}"`

### 2. **اصلاح View (signup_view)**
- ✅ اضافه شدن لاگ برای دیباگ: `logger.info(f"📥 Signup POST data: {request.POST}")`
- ✅ لاگ کردن خطاهای فرم: `logger.error(f"❌ Form validation errors: {form.errors}")`
- ✅ نمایش بهتر خطاها با ذکر نام فیلد

### 3. **بررسی Database**
- ✅ جدول `UserProfile` وجود دارد
- ✅ ستون `phone` با نوع `varchar(20)` وجود دارد
- ✅ ستون `phone` به صورت `NOT NULL` تعریف شده

---

## 🧪 **نحوه تست:**

### **مرحله 1: تست در Production (chidmano.ir)**
1. برید به: `https://chidmano.ir/accounts/signup/`
2. فرم رو پر کنید با این مقادیر:
   - **نام کاربری:** `test_user_001`
   - **ایمیل:** `test@example.com`
   - **نام:** `علی`
   - **نام خانوادگی:** `احمدی`
   - **شماره موبایل:** `09123456789`
   - **رمز عبور:** `TestPass123!`
   - **تأیید رمز عبور:** `TestPass123!`
3. روی دکمه **ثبت‌نام** کلیک کنید

### **مرحله 2: چک کردن Logs**
اگر خطایی بود، توی لاگ‌های Liara این موارد رو ببینید:

```bash
# در Liara Console بخش Logs:
📥 Signup POST data: <QueryDict: {...}>
❌ Form validation errors: {...}
❌ Form data: {...}
```

---

## 🐛 **خطاهای احتمالی و راه‌حل:**

### **خطا 1: "This field is required" برای phone**
**علت:** فیلد `phone` در POST data نیست یا خالیه

**راه‌حل:**
- چک کنید که `name="phone"` در input درست باشه ✅ (الان درسته)
- چک کنید که JavaScript فرم رو تغییر نمیده
- چک کنید که browser autocomplete مشکل نساخته

### **خطا 2: "این شماره موبایل قبلاً ثبت شده است"**
**علت:** این شماره قبلاً استفاده شده

**راه‌حل:**
- از شماره دیگه‌ای استفاده کنید
- یا در Django Admin، UserProfile مربوطه رو پاک کنید

### **خطا 3: Database Error**
**علت:** جدول `UserProfile` یا ستون `phone` وجود نداره

**راه‌حل Production:**
```bash
# در Liara Console:
python manage.py migrate
```

---

## 📋 **فیلدهای الزامی فرم:**

| فیلد | نام در Form | الزامی | Validation |
|------|------------|--------|------------|
| نام کاربری | `username` | ✅ | کاراکترهای معتبر |
| ایمیل | `email` | ✅ | فرمت ایمیل + یونیک |
| نام | `first_name` | ✅ | - |
| نام خانوادگی | `last_name` | ✅ | - |
| شماره موبایل | `phone` | ✅ | 11 رقم، شروع با 09، یونیک |
| رمز عبور | `password1` | ✅ | قوانین رمز عبور Django |
| تأیید رمز | `password2` | ✅ | مطابقت با password1 |

---

## 🔍 **بررسی در Production:**

### **چک کردن UserProfile Table:**
در Liara Console > Django Shell:
```python
from store_analysis.models import UserProfile
from django.db import connection

# بررسی ساختار جدول
cursor = connection.cursor()
cursor.execute("""
    SELECT column_name, data_type, character_maximum_length, is_nullable
    FROM information_schema.columns 
    WHERE table_name = 'store_analysis_userprofile'
    ORDER BY ordinal_position
""")
for col in cursor.fetchall():
    print(col)
```

### **چک کردن تعداد Users:**
```python
from django.contrib.auth.models import User
from store_analysis.models import UserProfile

print(f"Total Users: {User.objects.count()}")
print(f"Total UserProfiles: {UserProfile.objects.count()}")
```

---

## ✅ **انتظار موفقیت:**

اگر همه چی درست باشه، بعد از Submit:
1. ✅ کاربر ایجاد میشه
2. ✅ UserProfile با شماره موبایل ایجاد میشه
3. ✅ کاربر login میشه
4. ✅ Redirect به Dashboard: `https://chidmano.ir/store/dashboard/`
5. ✅ پیام موفقیت: "✅ حساب کاربری شما با موفقیت ایجاد شد!"

---

## 📞 **اگر باز هم مشکل داشت:**

1. Screenshot از خطا بفرستید
2. لاگ‌های Liara رو کپی کنید (خصوصاً خطوط با `📥` و `❌`)
3. بررسی کنید که آیا در Network Tab مرورگر، درخواست POST ارسال میشه یا نه

---

**تاریخ:** 2025-10-14
**نسخه:** v1.0

