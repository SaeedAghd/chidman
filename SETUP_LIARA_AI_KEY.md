# راهنمای تنظیم LIARA_AI_API_KEY در لیارا

## روش 1: از طریق داشبورد لیارا (پیشنهادی)

1. وارد داشبورد لیارا شوید: https://console.liara.ir
2. به بخش **Apps** بروید
3. اپلیکیشن **chidmano** را انتخاب کنید
4. به بخش **Environment Variables** بروید
5. روی **Add Variable** کلیک کنید
6. مقادیر زیر را وارد کنید:
   - **Name**: `LIARA_AI_API_KEY`
   - **Value**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2OGM3MjU1NjJlYTVmMGYxNTA3MWU5ZDgiLCJ0eXBlIjoiYXV0aCIsImlhdCI6MTc2MjIwOTI0M30.8PSRh1ms7CDy4dcODcNNZ1z8DC7bo_xAVD_3h4JGROU`
7. روی **Save** کلیک کنید
8. **مهم**: باید اپلیکیشن را **restart** کنید تا تغییرات اعمال شود

## روش 2: از طریق CLI لیارا

```bash
# نصب CLI (اگر نصب نشده)
npm install -g @liara/cli

# ورود به لیارا
liara login

# تنظیم متغیر محیطی
liara env:set LIARA_AI_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2OGM3MjU1NjJlYTVmMGYxNTA3MWU5ZDgiLCJ0eXBlIjoiYXV0aCIsImlhdCI6MTc2MjIwOTI0M30.8PSRh1ms7CDy4dcODcNNZ1z8DC7bo_xAVD_3h4JGROU" --app chidmano

# restart کردن اپلیکیشن
liara restart --app chidmano
```

## بررسی تنظیمات

بعد از تنظیم، می‌توانید از طریق لاگ‌ها بررسی کنید:

```bash
# مشاهده لاگ‌های اپلیکیشن
liara logs --app chidmano --follow

# یا در داشبورد لیارا:
# Apps > chidmano > Logs
```

اگر تنظیمات درست باشد، باید پیام زیر را ببینید:
```
✅ Liara AI configured (base_url=https://ai.liara.ir/api/68cb388afcfe30ace3a2a314/v1)
✅ LiaraAIService initialized successfully
```

## نکات مهم

1. **امنیت**: این token را در هیچ جا به اشتراک نگذارید
2. **Restart**: بعد از تنظیم environment variable، حتماً اپلیکیشن را restart کنید
3. **URL**: URL API در کد به صورت hardcoded است: `https://ai.liara.ir/api/68cb388afcfe30ace3a2a314/v1`
4. **مدل**: مدل پیش‌فرض استفاده شده: `openai/gpt-4.1`

## تست بعد از تنظیم

1. یک تحلیل جدید ایجاد کنید
2. لاگ‌ها را بررسی کنید
3. اگر خطا دیدید، بررسی کنید که:
   - Token درست تنظیم شده باشد
   - اپلیکیشن restart شده باشد
   - URL API صحیح باشد

## عیب‌یابی

اگر بعد از تنظیم هنوز خطا می‌بینید:

1. بررسی کنید که token در environment variables ذخیره شده باشد:
   ```bash
   liara env:list --app chidmano
   ```

2. بررسی لاگ‌ها برای خطاهای API:
   ```bash
   liara logs --app chidmano | grep -i "liara\|api\|error"
   ```

3. اگر خطای `401 Unauthorized` می‌بینید، token نامعتبر است
4. اگر خطای `timeout` می‌بینید، ممکن است مشکل شبکه باشد

