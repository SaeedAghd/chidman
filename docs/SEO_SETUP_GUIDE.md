# راهنمای کامل ثبت سایت در موتورهای جستجو

این راهنما به شما کمک می‌کند تا سایت چیدمانو را در Google Search Console و Bing Webmaster Tools ثبت کنید.

## ✅ بررسی‌های اولیه

قبل از شروع، مطمئن شوید که:

1. ✅ Sitemap در دسترس است: `https://chidmano.ir/sitemap.xml`
2. ✅ Robots.txt در دسترس است: `https://chidmano.ir/robots.txt`
3. ✅ سایت در دسترس است و SSL فعال است
4. ✅ Google Search Console verification code در template موجود است

---

## 🔍 مرحله 1: ثبت در Google Search Console

### 1.1 ورود به Google Search Console

1. به آدرس زیر بروید:
   ```
   https://search.google.com/search-console
   ```

2. با حساب Google خود وارد شوید

3. روی **"Add Property"** کلیک کنید

4. **"URL prefix"** را انتخاب کنید و آدرس سایت را وارد کنید:
   
   ⚠️ **مهم**: از URL **بدون www** استفاده کنید:
   ```
   https://chidmano.ir
   ```
   
   ❌ **نادرست**: `https://www.chidmano.ir` (استفاده نکنید)
   ✅ **درست**: `https://chidmano.ir` (استفاده کنید)
   
   **دلیل**: در کد سایت، canonical URL و BASE_DOMAIN بدون www تنظیم شده‌اند.

### 1.2 تایید مالکیت سایت

شما دو روش دارید:

#### روش 1: HTML Tag (توصیه می‌شود - قبلاً انجام شده)

کد تایید در template موجود است:
```html
<meta name="google-site-verification" content="nwfSSELzJ7fTRF7eeoXPZBq7K1OUnMTVOBZIK-FsYGY" />
```

1. در Google Search Console، **"HTML tag"** را انتخاب کنید
2. کد verification را کپی کنید
3. روی **"Verify"** کلیک کنید

#### روش 2: HTML File Upload

1. فایل HTML verification را دانلود کنید
2. آن را در پوشه `static/` قرار دهید
3. URL را به `urls.py` اضافه کنید

### 1.3 Submit کردن Sitemap

بعد از تایید مالکیت:

1. در منوی سمت چپ، **"Sitemaps"** را انتخاب کنید

2. در قسمت **"Add a new sitemap"**، آدرس sitemap را وارد کنید:
   ```
   https://chidmano.ir/sitemap.xml
   ```

3. روی **"Submit"** کلیک کنید

4. همچنین sitemap تصاویر را هم اضافه کنید:
   ```
   https://chidmano.ir/sitemap-images.xml
   ```

### 1.4 درخواست Index کردن صفحات مهم

1. در منوی سمت چپ، **"URL Inspection"** را انتخاب کنید

2. URL های مهم را وارد کنید و **"Request Indexing"** را بزنید:
   - `https://chidmano.ir/`
   - `https://chidmano.ir/landing/`
   - `https://chidmano.ir/store/products/`

---

## 🔍 مرحله 2: ثبت در Bing Webmaster Tools

### 2.1 ورود به Bing Webmaster Tools

1. به آدرس زیر بروید:
   ```
   https://www.bing.com/webmasters
   ```

2. با حساب Microsoft خود وارد شوید (یا یک حساب جدید بسازید)

3. روی **"Add a site"** کلیک کنید

4. آدرس سایت را وارد کنید:
   ```
   https://chidmano.ir
   ```

### 2.2 تایید مالکیت سایت

سه روش دارید:

#### روش 1: HTML Meta Tag (توصیه می‌شود)

1. کد verification را از Bing کپی کنید
2. آن را به `chidmano/templates/chidmano/landing.html` اضافه کنید:
   ```html
   <meta name="msvalidate.01" content="YOUR_BING_VERIFICATION_CODE" />
   ```
3. تغییرات را commit و push کنید
4. در Bing روی **"Verify"** کلیک کنید

#### روش 2: XML File Upload

1. فایل XML verification را دانلود کنید
2. آن را در پوشه `static/` قرار دهید
3. URL را به `urls.py` اضافه کنید

#### روش 3: CNAME Record

اگر دسترسی به DNS دارید، می‌توانید از CNAME استفاده کنید.

### 2.3 Submit کردن Sitemap

بعد از تایید مالکیت:

1. در منوی سمت چپ، **"Sitemaps"** را انتخاب کنید

2. آدرس sitemap را وارد کنید:
   ```
   https://chidmano.ir/sitemap.xml
   ```

3. روی **"Submit"** کلیک کنید

---

## 📊 مرحله 3: بررسی و مانیتورینگ

### 3.1 بررسی Index شدن

بعد از 1-2 هفته، بررسی کنید:

#### Google Search:
```
site:chidmano.ir چیدمان فروشگاه
site:chidmano.ir چیدمان مغازه
site:chidmano.ir چیدمان فروشگاه با هوش مصنوعی
```

#### Bing Search:
```
site:chidmano.ir چیدمان فروشگاه
```

### 3.2 بررسی Coverage در Google Search Console

1. در Google Search Console، **"Coverage"** را انتخاب کنید
2. بررسی کنید که صفحات مهم index شده‌اند
3. اگر خطایی وجود دارد، آن را برطرف کنید

### 3.3 بررسی Performance

1. در Google Search Console، **"Performance"** را انتخاب کنید
2. بررسی کنید که:
   - Impressions (تعداد نمایش) در حال افزایش است
   - Clicks (تعداد کلیک) در حال افزایش است
   - CTR (Click-Through Rate) مناسب است

---

## 🔧 ابزارهای مفید

### بررسی Sitemap:
```bash
curl https://chidmano.ir/sitemap.xml
```

### بررسی Robots.txt:
```bash
curl https://chidmano.ir/robots.txt
```

### تست Structured Data:
- Google Rich Results Test: https://search.google.com/test/rich-results
- Schema Markup Validator: https://validator.schema.org/

### تست Mobile-Friendly:
- Google Mobile-Friendly Test: https://search.google.com/test/mobile-friendly

### تست PageSpeed:
- Google PageSpeed Insights: https://pagespeed.web.dev/

---

## ⚠️ نکات مهم

1. **صبر کنید**: Index شدن ممکن است 2-4 هفته طول بکشد
2. **به‌روزرسانی منظم**: Sitemap به صورت خودکار هر 12 ساعت به‌روز می‌شود
3. **محتوا**: مطمئن شوید که محتوای صفحه به‌روز و با کیفیت است
4. **Backlinks**: سعی کنید backlink های با کیفیت دریافت کنید
5. **Social Signals**: سایت را در شبکه‌های اجتماعی به اشتراک بگذارید

---

## 📝 چک‌لیست نهایی

- [ ] Google Search Console ثبت شده
- [ ] Sitemap در Google Search Console submit شده
- [ ] Bing Webmaster Tools ثبت شده
- [ ] Sitemap در Bing Webmaster Tools submit شده
- [ ] صفحات مهم request indexing شده‌اند
- [ ] بعد از 1-2 هفته، بررسی index شدن انجام شده
- [ ] Performance و Coverage مانیتور می‌شود

---

## 🆘 مشکلات رایج

### مشکل: Sitemap submit نمی‌شود
**راه حل**: 
- بررسی کنید که sitemap در دسترس است: `curl https://chidmano.ir/sitemap.xml`
- مطمئن شوید که sitemap معتبر است (XML valid)
- بررسی کنید که robots.txt sitemap را allow می‌کند

### مشکل: صفحات index نمی‌شوند
**راه حل**:
- بررسی کنید که robots.txt صفحات را block نمی‌کند
- مطمئن شوید که صفحات noindex نیستند
- بررسی کنید که محتوا unique و با کیفیت است
- صبر کنید (ممکن است 2-4 هفته طول بکشد)

### مشکل: Verification failed
**راه حل**:
- مطمئن شوید که meta tag در `<head>` قرار دارد
- بررسی کنید که سایت در دسترس است
- Cache را clear کنید
- بررسی کنید که SSL فعال است

---

## 📞 پشتیبانی

اگر مشکلی دارید، می‌توانید:
1. مستندات رسمی را بررسی کنید:
   - Google Search Console: https://support.google.com/webmasters
   - Bing Webmaster Tools: https://www.bing.com/webmasters/help

2. با تیم توسعه تماس بگیرید

---

**آخرین به‌روزرسانی**: 2025-11-28

