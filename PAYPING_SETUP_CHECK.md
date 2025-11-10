# بررسی تنظیمات PayPing

## ✅ متغیرهای تنظیم شده در لیارا

از تصویر داشبورد لیارا مشخص است که این متغیرها تنظیم شده‌اند:

1. ✅ **PING_API_KEY**: `851E282188994B8B0D7C94106BABC5FAC9A967E4B65059CB9D290A7A030C1ECF-1`
2. ✅ **PING_CALLBACK_URL**: `https://chidmano.liara.app/store/payment/payping/callback/`
3. ✅ **PING_RETURN_URL**: `https://chidmano.liara.app/store/payment/payping/return/`
4. ✅ **PING_SANDBOX**: `False`

## ⚠️ متغیرهای اضافی مورد نیاز

کد پروژه از این متغیرها هم استفاده می‌کند که باید در لیارا تنظیم شوند:

### 1. PAYPING_TOKEN (ضروری)
این متغیر در `PaymentGatewayManager` و `PayPingGateway` استفاده می‌شود.

**مقدار:**
```
PAYPING_TOKEN=851E282188994B8B0D7C94106BABC5FAC9A967E4B65059CB9D290A7A030C1ECF-1
```

### 2. PAYPING_SANDBOX (ضروری)
این متغیر برای تعیین محیط استفاده می‌شود.

**مقدار:**
```
PAYPING_SANDBOX=False
```

### 3. PAYPING_CALLBACK_URL (اختیاری - اگر متفاوت است)
اگر می‌خواهید از URL متفاوتی استفاده کنید.

**مقدار:**
```
PAYPING_CALLBACK_URL=https://chidmano.liara.app/store/payment/payping/callback/
```

### 4. PAYPING_RETURN_URL (اختیاری - اگر متفاوت است)
**مقدار:**
```
PAYPING_RETURN_URL=https://chidmano.liara.app/store/payment/payping/return/
```

### 5. PAYPING_MOCK_MODE (اختیاری)
برای غیرفعال کردن حالت mock در production.

**مقدار:**
```
PAYPING_MOCK_MODE=False
```

## 📋 دستورات CLI برای تنظیم متغیرهای اضافی

```powershell
# تنظیم PAYPING_TOKEN
liara env:set PAYPING_TOKEN="851E282188994B8B0D7C94106BABC5FAC9A967E4B65059CB9D290A7A030C1ECF-1" --app chidmano

# تنظیم PAYPING_SANDBOX
liara env:set PAYPING_SANDBOX="False" --app chidmano

# تنظیم PAYPING_CALLBACK_URL (اگر نیاز است)
liara env:set PAYPING_CALLBACK_URL="https://chidmano.liara.app/store/payment/payping/callback/" --app chidmano

# تنظیم PAYPING_RETURN_URL (اگر نیاز است)
liara env:set PAYPING_RETURN_URL="https://chidmano.liara.app/store/payment/payping/return/" --app chidmano

# غیرفعال کردن mock mode
liara env:set PAYPING_MOCK_MODE="False" --app chidmano
```

## 🔍 بررسی استفاده در کد

### در `PaymentGatewayManager` (store_analysis/payment_gateways.py:387):
```python
payping_token = getattr(settings, 'PAYPING_TOKEN', '')
payping_sandbox = getattr(settings, 'PAYPING_SANDBOX', True)
```

### در `PayPingGateway` (store_analysis/payment_gateways.py:141):
```python
self.token = token or getattr(settings, 'PAYPING_TOKEN', '')
```

### در `PAYMENT_GATEWAY` (chidmano/settings.py:35):
```python
'API_KEY': os.getenv('PING_API_KEY', '...')
```

## ✅ خلاصه

**متغیرهای تنظیم شده:**
- ✅ PING_API_KEY
- ✅ PING_CALLBACK_URL
- ✅ PING_RETURN_URL
- ✅ PING_SANDBOX

**متغیرهای مورد نیاز اضافی:**
- ⚠️ PAYPING_TOKEN (باید اضافه شود)
- ⚠️ PAYPING_SANDBOX (باید اضافه شود - یا می‌توان از PING_SANDBOX استفاده کرد)
- ⚠️ PAYPING_MOCK_MODE (برای production باید False باشد)

## 🎯 توصیه

برای اطمینان از کارکرد صحیح، این متغیرها را در لیارا اضافه کنید:
1. `PAYPING_TOKEN` (با همان مقدار PING_API_KEY)
2. `PAYPING_SANDBOX` (با همان مقدار PING_SANDBOX)
3. `PAYPING_MOCK_MODE=False` (برای production)

یا می‌توانید کد را تغییر دهید تا از `PING_API_KEY` به جای `PAYPING_TOKEN` استفاده کند.

