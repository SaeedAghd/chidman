# خلاصه تنظیمات مدل‌های AI

## ✅ تنظیمات نهایی

### 1. تحلیل رایگان (Free)
- **مدل**: Ollama (محلی، بدون هزینه API)
- **سرویس**: `FreeAnalysisService`
- **استفاده**: تحلیل‌های رایگان (`package_type='basic'` و `final_amount=0`)

### 2. تحلیل اولیه (Preliminary)
- **مدل**: `openai/gpt-4o-mini`
- **استفاده**: برای همه پلن‌ها (سریع و ارزان)
- **سرویس**: `PremiumReportGenerator`

### 3. تحلیل محبوب (Basic)
- **مدل**: `google/gemini-2.5-flash`
- **استفاده**: تحلیل‌های محبوب
- **سرویس**: `PremiumReportGenerator`

### 4. تحلیل پیشرفته (Professional)
- **مدل**: `openai/gpt-5-mini`
- **استفاده**: تحلیل‌های پیشرفته
- **سرویس**: `PremiumReportGenerator`

### 5. Enterprise
- **وضعیت**: حذف شده - Enterprise نداریم

## تغییرات انجام شده

1. ✅ تحلیل محبوب: از `gpt-4o-mini` به `gemini-2.5-flash` تغییر کرد
2. ✅ تحلیل پیشرفته: از `gemini-2.0-flash` به `gpt-5-mini` تغییر کرد
3. ✅ Enterprise: از `model_map` حذف شد

## فایل‌های تغییر یافته

- `store_analysis/services/premium_report_generator.py`: مدل‌های `model_map` به‌روزرسانی شد

