# چیدمان - تحلیل هوشمند فروشگاه

## 🚀 پروژه تحلیل هوشمند فروشگاه با Django

این پروژه یک سیستم تحلیل هوشمند فروشگاه است که با Django و Python ساخته شده است.

## ✨ ویژگی‌های کلیدی

- 🔐 سیستم احراز هویت کامل
- 📊 داشبورد مدیریتی
- 🤖 ربات هوش مصنوعی
- 📄 گزارش‌های حرفه‌ای
- 📱 رابط کاربری ریسپانسیو
- 🌐 پشتیبانی از زبان فارسی

## 🛠️ تکنولوژی‌های استفاده شده

- **Backend:** Django 5.2.1
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Database:** SQLite (Development), PostgreSQL (Production)
- **AI:** OpenAI API
- **Deployment:** Railway, Heroku, Render

## 📋 پیش‌نیازها

- Python 3.11+
- pip
- Git

## 🚀 نصب و راه‌اندازی

### 1. کلون کردن پروژه
```bash
git clone <repository-url>
cd chideman
```

### 2. ایجاد محیط مجازی
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# یا
.venv\Scripts\activate  # Windows
```

### 3. نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### 4. تنظیم متغیرهای محیطی
```bash
cp .env.example .env
# فایل .env را ویرایش کنید
```

### 5. اجرای مایگریشن‌ها
```bash
python manage.py migrate
```

### 6. ایجاد سوپر یوزر
```bash
python manage.py createsuperuser
```

### 7. اجرای سرور
```bash
python manage.py runserver
```

## 🌐 دیپلوی

### Railway (پیشنهاد اول)

1. **آماده‌سازی پروژه:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **اتصال به Railway:**
   - به https://railway.app بروید
   - با GitHub وارد شوید
   - پروژه را انتخاب کنید
   - Railway خودکار دیپلوی می‌کند

3. **تنظیم متغیرهای محیطی:**
   - `SECRET_KEY`: کلید امنیتی Django
   - `DEBUG`: False
   - `DATABASE_URL`: آدرس دیتابیس PostgreSQL
   - `ALLOWED_HOSTS`: دامنه‌های مجاز

### Render (پیشنهاد دوم)

1. **اتصال به Render:**
   - به https://render.com بروید
   - با GitHub وارد شوید
   - New Web Service را انتخاب کنید
   - پروژه را انتخاب کنید

2. **تنظیمات:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn chidmano.wsgi:application`
   - **Environment:** Python 3.11

### Heroku (پیشنهاد سوم)

1. **نصب Heroku CLI:**
   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI
   ```

2. **دیپلوی:**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

## 🔧 تنظیمات محیطی

### متغیرهای محیطی ضروری:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DATABASE_URL=postgresql://username:password@host:port/database_name

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# OpenAI API
OPENAI_API_KEY=your-openai-api-key
```

## 📁 ساختار پروژه

```
chidman/
├── chidmano/                 # تنظیمات اصلی Django
│   ├── settings.py          # تنظیمات پروژه
│   ├── urls.py              # URL های اصلی
│   └── wsgi.py              # WSGI configuration
├── store_analysis/          # اپلیکیشن اصلی
│   ├── models.py            # مدل‌های دیتابیس
│   ├── views.py             # ویوها
│   ├── forms.py             # فرم‌ها
│   └── templates/           # قالب‌های HTML
├── static/                  # فایل‌های استاتیک
├── media/                   # فایل‌های آپلود شده
├── requirements.txt         # وابستگی‌های Python
├── Procfile                 # تنظیمات Heroku/Railway
├── runtime.txt              # نسخه Python
└── README.md               # این فایل
```

## 🔐 امنیت

- ✅ HTTPS اجباری در تولید
- ✅ CSRF Protection
- ✅ XSS Protection
- ✅ SQL Injection Protection
- ✅ Rate Limiting
- ✅ Secure Headers

## 📊 تست

برای اجرای تست‌های کامل:

```bash
python final_complete_test.py
```

## 🤝 مشارکت

1. Fork کنید
2. Branch جدید بسازید (`git checkout -b feature/amazing-feature`)
3. Commit کنید (`git commit -m 'Add amazing feature'`)
4. Push کنید (`git push origin feature/amazing-feature`)
5. Pull Request بسازید

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

## 📞 پشتیبانی

برای سوالات و مشکلات:
- 📧 Email: support@chidman.com
- 💬 Telegram: @chidman_support
- 🌐 Website: https://chidman.com

## 🎯 ویژگی‌های آینده

- [ ] پشتیبانی از چندین زبان
- [ ] API کامل REST
- [ ] سیستم پرداخت
- [ ] گزارش‌های پیشرفته
- [ ] موبایل اپ

---

**ساخته شده با ❤️ در ایران** 