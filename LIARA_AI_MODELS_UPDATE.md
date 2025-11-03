# به‌روزرسانی مدل‌های Liara AI با مستندات Gemini

## تغییرات انجام شده

بر اساس [مستندات رسمی لیارا برای Google Gemini](https://docs.liara.ir/ai/google-gemini/)، کد برنامه به‌روزرسانی شد.

### 1. مدل‌های Gemini اضافه شده

مدل‌های زیر از لیارا پشتیبانی می‌شوند و در کد اضافه شدند:

- ✅ `google/gemini-2.5-flash` - سریع و کارآمد (پیشنهادی برای اکثر تحلیل‌ها)
- ✅ `google/gemini-2.5-pro-preview` - قدرتمندترین مدل (برای تحلیل‌های enterprise)
- ✅ `google/gemini-2.0-flash-001` - سریع و پایدار
- ✅ `google/gemini-2.0-flash-lite-001` - سبک‌ترین مدل (برای تحلیل‌های اولیه)

### 2. تغییرات در `liara_ai_service.py`

**قبل:**
```python
self.models = {
    'analysis': 'openai/gpt-4.1',
    'design': 'openai/gpt-4.1',
    'marketing': 'openai/gpt-4.1',
    # ...
}
```

**بعد:**
```python
self.models = {
    'analysis': 'openai/gpt-4.1',           # تحلیل اصلی - قدرتمندترین
    'design': 'google/gemini-2.5-flash',    # سریع و بهینه
    'marketing': 'google/gemini-2.5-flash',  # سریع
    'psychology': 'openai/gpt-4.1',         # نیاز به دقت
    'optimization': 'google/gemini-2.5-flash',
    'summary': 'google/gemini-2.5-flash'
}
```

### 3. تغییرات در `premium_report_generator.py`

**قبل:**
```python
self.model_map = {
    'professional': 'google/gemini-2.0-flash',
    # ...
}
```

**بعد:**
```python
self.model_map = {
    'preliminary': 'google/gemini-2.0-flash-lite-001',
    'basic': 'google/gemini-2.5-flash',
    'professional': 'google/gemini-2.5-flash',  # به‌روز شده
    'enterprise': 'google/gemini-2.5-pro-preview',
}
```

## مزایای استفاده از Gemini

1. **سرعت بالاتر**: مدل‌های Gemini Flash بسیار سریع‌تر از GPT-4 هستند
2. **هزینه کمتر**: Gemini معمولاً ارزان‌تر است
3. **چندوجهی بودن**: Gemini می‌تواند با تصویر، صدا و ویدیو هم کار کند
4. **بهینه‌سازی شده**: برای کاربردهای فارسی بهینه‌سازی شده است

## نکات مهم

1. **سازگاری با OpenAI SDK**: تمام مدل‌های لیارا (شامل Gemini) سازگار با OpenAI SDK هستند
2. **Base URL**: URL در کد به صورت hardcoded است و نیازی به تغییر ندارد
3. **API Key**: همان `LIARA_AI_API_KEY` برای همه مدل‌ها استفاده می‌شود

## مراجع

- [مستندات رسمی Google Gemini در لیارا](https://docs.liara.ir/ai/google-gemini/)
- تمام مدل‌های لیارا سازگار با OpenAI SDK هستند
- ساختار درخواست‌ها یکسان است

## تست

بعد از deploy، باید بررسی کنید که:
1. تحلیل‌های طراحی با Gemini انجام می‌شوند
2. سرعت تحلیل‌ها افزایش یافته باشد
3. کیفیت تحلیل‌ها حفظ شده باشد

