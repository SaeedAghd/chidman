# چیدمانو

سیستم هوشمند تحلیل و بهینه‌سازی چیدمان فروشگاه

## ویژگی‌ها

- تحلیل هوشمند چیدمان فروشگاه
- پیشنهادات بهینه‌سازی
- گزارش‌گیری
- پنل مدیریت

## نصب و راه‌اندازی

1. نصب وابستگی‌های Python:
```bash
pip install -r requirements.txt
```

2. نصب وابستگی‌های Node.js:
```bash
npm install
```

3. تنظیم متغیرهای محیطی:
```bash
# فایل .env را ایجاد کنید و متغیرهای زیر را تنظیم کنید:
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
OPENAI_API_KEY=your-openai-api-key
```

4. اجرای مایگریشن‌ها:
```bash
python manage.py migrate
```

5. ایجاد کاربر ادمین:
```bash
python manage.py createsuperuser
```

6. اجرای سرور:
```bash
python manage.py runserver
```

7. اجرای Celery (در ترمینال جداگانه):
```bash
celery -A chidmano worker --loglevel=info
```

8. اجرای Redis (در ترمینال جداگانه):
```bash
redis-server
```

## استفاده

1. وارد پنل مدیریت شوید
2. یک تحلیل جدید ایجاد کنید
3. اطلاعات فروشگاه را وارد کنید
4. منتظر نتیجه تحلیل بمانید

## توسعه

برای توسعه پروژه:

1. از محیط مجازی استفاده کنید
2. از فرمت‌دهنده کد استفاده کنید
3. تست‌ها را اجرا کنید
4. مستندات را به‌روز کنید

## مجوز

این پروژه تحت مجوز MIT منتشر شده است. 