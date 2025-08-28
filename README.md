# 🏪 چیدمان - تحلیل هوشمند فروشگاه

سیستم تحلیل هوشمند فروشگاه با استفاده از هوش مصنوعی برای بهینه‌سازی چیدمان و افزایش فروش.

## 🚀 ویژگی‌ها

- **تحلیل هوشمند چیدمان**: استفاده از AI برای تحلیل و بهینه‌سازی چیدمان فروشگاه
- **گزارش‌های حرفه‌ای**: تولید گزارش‌های مدیریتی جامع
- **پیش‌بینی مالی**: پیش‌بینی درآمد و ROI
- **راهنمایی عملی**: ارائه راهکارهای عملی برای بهبود فروش
- **ربات مشاور**: ربات هوش مصنوعی برای پاسخ به سوالات

## 🛠️ تکنولوژی‌ها

- **Backend**: Django 5.2.1
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: PostgreSQL
- **AI**: OpenAI API
- **Deployment**: Render

## 📦 نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.13+
- PostgreSQL
- OpenAI API Key

### نصب محلی

1. **کلون کردن پروژه**:
```bash
git clone https://github.com/your-username/chidman.git
cd chidman
```

2. **ایجاد محیط مجازی**:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# یا
.venv\Scripts\activate  # Windows
```

3. **نصب وابستگی‌ها**:
```bash
pip install -r requirements.txt
```

4. **تنظیم متغیرهای محیطی**:
```bash
cp env.example .env
# ویرایش فایل .env با مقادیر مناسب
```

5. **اجرای مایگریشن‌ها**:
```bash
python manage.py migrate
```

6. **ایجاد سوپر یوزر**:
```bash
python manage.py createsuperuser
```

7. **اجرای سرور**:
```bash
python manage.py runserver
```

## 🌐 دیپلوی روی Render

### مراحل دیپلوی:

1. **اتصال به گیت‌هاب**:
   - پروژه را در گیت‌هاب push کنید
   - در Render، "New Web Service" را انتخاب کنید
   - گیت‌هاب repository را متصل کنید

2. **تنظیمات Render**:
   - **Environment**: Python
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn chidmano.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

3. **متغیرهای محیطی**:
   - `SECRET_KEY`: (توسط Render تولید می‌شود)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com`
   - `DATABASE_URL`: (از Render Database)
   - `OPENAI_API_KEY`: کلید API شما

4. **دیتابیس**:
   - در Render، یک PostgreSQL database ایجاد کنید
   - `DATABASE_URL` را به متغیرهای محیطی اضافه کنید

## 📁 ساختار پروژه

```
chidman/
├── chidmano/                 # تنظیمات اصلی Django
│   ├── settings.py          # تنظیمات پروژه
│   ├── urls.py              # URL های اصلی
│   └── wsgi.py              # WSGI configuration
├── store_analysis/          # اپلیکیشن اصلی
│   ├── models.py            # مدل‌های دیتابیس
│   ├── views.py             # View ها
│   ├── urls.py              # URL های اپلیکیشن
│   └── templates/           # قالب‌های HTML
├── static/                  # فایل‌های استاتیک
├── media/                   # فایل‌های آپلود شده
├── requirements.txt         # وابستگی‌های Python
├── render.yaml             # تنظیمات Render
├── build.sh                # اسکریپت build
└── Procfile                # تنظیمات Heroku/Render
```

## 🔧 تنظیمات مهم

### متغیرهای محیطی ضروری:
- `SECRET_KEY`: کلید امنیتی Django
- `DATABASE_URL`: آدرس دیتابیس PostgreSQL
- `OPENAI_API_KEY`: کلید API OpenAI
- `ALLOWED_HOSTS`: دامنه‌های مجاز

### تنظیمات امنیتی:
- `DEBUG=False` در production
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`

## 🧪 تست

برای اجرای تست‌های جامع:

```bash
python professional_test.py
```

## 📊 عملکرد

- **نرخ موفقیت تست**: 93.3%
- **زمان بارگذاری**: < 1 ثانیه
- **پشتیبانی از موبایل**: کامل
- **امنیت**: بالا

## 🤝 مشارکت

1. Fork کنید
2. Branch جدید ایجاد کنید (`git checkout -b feature/amazing-feature`)
3. تغییرات را commit کنید (`git commit -m 'Add amazing feature'`)
4. Push کنید (`git push origin feature/amazing-feature`)
5. Pull Request ایجاد کنید

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

## 📞 پشتیبانی

برای سوالات و مشکلات:
- Email: support@chidman.com
- GitHub Issues: [اینجا](https://github.com/your-username/chidman/issues)

---

**توسعه‌دهنده**: تیم چیدمان  
**نسخه**: 1.0.0  
**آخرین بروزرسانی**: آگوست 2025 