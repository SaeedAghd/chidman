# تشخیص مشکل عدم انجام تحلیل

## مشکلات شناسایی شده:

### 1. **عدم بررسی API Key قبل از شروع تحلیل**
   - **مشکل**: اگر `LIARA_AI_API_KEY` تنظیم نشده باشد، تحلیل شروع می‌شود اما با خطا مواجه می‌شود
   - **راه حل**: بررسی API key قبل از شروع تحلیل و نمایش پیام خطای واضح

### 2. **عدم مدیریت خطا در توابع تحلیل جزئی**
   - **مشکل**: توابع `_analyze_main_store`, `_analyze_store_design` و غیره در صورت خطا `None` برمی‌گردانند
   - **راه حل**: این توابع باید dict با `error` و `error_message` برگردانند

### 3. **عدم نمایش خطا به کاربر**
   - **مشکل**: اگر تحلیل با خطا مواجه شود، کاربر اطلاعی پیدا نمی‌کند و فقط وضعیت `processing` می‌ماند
   - **راه حل**: در صورت خطا، وضعیت تحلیل به `failed` تغییر کند و `error_message` ذخیره شود

### 4. **Exception handling در background thread**
   - **مشکل**: اگر خطا در background thread رخ دهد، ممکن است silent fail شود
   - **راه حل**: تمام خطاها باید catch و log شوند و وضعیت تحلیل به `failed` تغییر کند

## تغییرات انجام شده:

1. ✅ بررسی API key در `start_real_analysis` قبل از شروع تحلیل
2. ✅ بررسی API key در `LiaraAIService.__init__` و `analyze_store_comprehensive`
3. ✅ اصلاح `_make_request` برای برگرداندن dict با error به جای None
4. ✅ اصلاح تمام توابع تحلیل جزئی برای برگرداندن error dict
5. ✅ بهبود exception handling در background thread
6. ✅ ذخیره `error_message` در تحلیل در صورت خطا

## بررسی‌های لازم:

1. **بررسی وجود `LIARA_AI_API_KEY` در environment variables**
   ```bash
   # در shell لیارا
   echo $LIARA_AI_API_KEY
   ```

2. **بررسی لاگ‌ها برای خطاهای تحلیل**
   - خطاهای `LIARA_AI_API_KEY تنظیم نشده`
   - خطاهای `authentication_failed`
   - خطاهای `timeout` یا `connection_error`

3. **بررسی وضعیت تحلیل‌ها در دیتابیس**
   ```python
   # در shell لیارا
   StoreAnalysis.objects.filter(status='processing').count()
   StoreAnalysis.objects.filter(status='failed').count()
   ```

## نکات مهم:

- اگر `LIARA_AI_API_KEY` تنظیم نشده باشد، تمام تحلیل‌ها با خطا مواجه می‌شوند
- تحلیل‌های در حال پردازش که بیش از 1 ساعت در وضعیت `processing` هستند، احتمالاً با خطا مواجه شده‌اند
- بررسی `error_message` در تحلیل‌های `failed` برای تشخیص مشکل دقیق

