# راهنمای احیای کامل سئو چیدمانو
## SEO Recovery Guide - Chidmano

### 📋 وضعیت
سایت پس از **10 روز downtime** دوباره فعال شده و نیاز به احیای کامل سئو دارد.

---

## ✅ کارهای انجام شده

### 1. به‌روزرسانی Dynamic Sitemap
- ✅ Sitemap با Django Sitemap Framework پیاده‌سازی شد
- ✅ **lastmod** همه صفحات به امروز (2025-11-02) به‌روز شد
- ✅ Sitemap شامل:
  - صفحات اصلی (home, landing)
  - صفحات استاتیک (features, products, forms, about, guides)
  - پکیج‌های خدمات
  - تحلیل‌های عمومی (حداکثر 500 مورد)
  - تصاویر مهم

### 2. بهینه‌سازی robots.txt
- ✅ robots.txt به‌روزرسانی شد
- ✅ تنظیمات ویژه برای Googlebot, Bingbot, Yandex
- ✅ مسدود کردن bot های مخرب
- ✅ مجاز کردن Social Media bots
- ✅ Cache delay تنظیم شد

### 3. سیستم ارسال به Google
- ✅ Google Search Console API integration
- ✅ Bing Webmaster Tools ping
- ✅ Endpoint برای re-submit: `/seo/submit-google/`

### 4. Content Freshness Signals
- ✅ همه lastmod ها به امروز تنظیم شد
- ✅ changefreq بهینه‌سازی شد
- ✅ priority بر اساس اهمیت صفحات

---

## 🚀 مراحل بعدی (اقدامات لازم)

### مرحله 1: بررسی Sitemap (فوری)
```bash
# بررسی sitemap در مرورگر
https://chidmano.ir/sitemap.xml
https://chidmano.ir/sitemap-images.xml
https://chidmano.ir/robots.txt
```

### مرحله 2: ارسال Sitemap به Google Search Console
1. ورود به [Google Search Console](https://search.google.com/search-console)
2. انتخاب property: `chidmano.ir`
3. رفتن به بخش **Sitemaps**
4. افزودن sitemap: `https://chidmano.ir/sitemap.xml`
5. افزودن sitemap تصاویر: `https://chidmano.ir/sitemap-images.xml`

### مرحله 3: Request Indexing برای صفحات مهم
در Google Search Console:
1. استفاده از **URL Inspection Tool**
2. وارد کردن صفحات مهم:
   - `/`
   - `/store/products/`
   - `/store/features/`
   - `/store/forms/`
   - `/guide/store-layout/`
   - `/about/`
3. کلیک روی **Request Indexing** برای هر URL

### مرحله 4: استفاده از API (اختیاری)
اگر API credentials تنظیم شده باشد:
```python
# از طریق Django admin یا shell
from chidmano.seo_google_submit import google_submitter

# ارسال sitemap
result = google_submitter.submit_sitemap()

# ارسال صفحات مهم
result = google_submitter.submit_important_pages()
```

### مرحله 5: بررسی و نظارت
1. **Google Search Console**:
   - بررسی Coverage report
   - بررسی Performance report
   - بررسی Mobile Usability

2. **Google Analytics**:
   - ردیابی Organic Traffic
   - بررسی صفحات پر بازدید

3. **Bing Webmaster Tools**:
   - ارسال sitemap به Bing
   - بررسی Indexing Status

---

## 📊 تنظیمات Environment Variables (اختیاری)

برای استفاده کامل از API features:

```bash
# Google Search Console API
GOOGLE_SEARCH_CONSOLE_API_KEY=your_api_key
GOOGLE_ACCESS_TOKEN=your_access_token

# Bing Webmaster Tools
BING_WEBMASTER_API_KEY=your_bing_api_key

# Site URL
SITE_URL=https://chidmano.ir
```

---

## 🔍 بررسی وضعیت

### بررسی Sitemap:
- تعداد صفحات: ~500+ صفحه
- آخرین به‌روزرسانی: 2025-11-02
- Status: Active ✅

### بررسی Robots.txt:
- Status: Active ✅
- Googlebot: Allowed ✅
- Bingbot: Allowed ✅

---

## 📈 انتظارات

### هفته اول:
- Google شروع به crawl کردن مجدد سایت می‌کند
- صفحات مهم دوباره index می‌شوند

### هفته دوم تا چهارم:
- افزایش تدریجی indexed pages
- بهبود organic traffic

### ماه اول تا سوم:
- بازگشت کامل سئو
- بهبود ranking برای keywords اصلی

---

## ⚠️ نکات مهم

1. **صبر کنید**: احیای کامل سئو ممکن است 1-3 ماه طول بکشد
2. **محتوای جدید**: تولید محتوای جدید و به‌روزرسانی محتوای قدیمی کمک می‌کند
3. **Backlinks**: بررسی کنید که backlinks هنوز فعال هستند
4. **Internal Linking**: اطمینان حاصل کنید internal linking درست است
5. **Performance**: سایت باید سریع باشد (Core Web Vitals)

---

## 🛠️ Troubleshooting

### مشکل: Sitemap نمایش داده نمی‌شود
**راه‌حل**: بررسی کنید که `/sitemap.xml` در دسترس است و خطایی ندارد

### مشکل: Google صفحات را index نمی‌کند
**راه‌حل**: 
1. بررسی robots.txt
2. استفاده از URL Inspection Tool
3. بررسی noindex tags

### مشکل: خطا در ارسال API
**راه‌حل**: 
1. بررسی API credentials
2. استفاده از روش manual submission در Search Console

---

## 📞 پشتیبانی

برای مشکلات یا سوالات، لاگ‌ها را بررسی کنید:
```bash
# لاگ‌های Django
tail -f logs/django.log | grep -i seo
```

---

**تاریخ ایجاد**: 2025-11-02  
**نسخه**: 1.0.0  
**وضعیت**: ✅ آماده برای استفاده

