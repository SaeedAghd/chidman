# 🎬 راهنمای اجرای ویدیو چیدمانو

## مرحله 1: نصب ImageMagick (ضروری برای متن)

### دانلود:
https://imagemagick.org/script/download.php#windows

یا مستقیم:
https://download.imagemagick.org/ImageMagick/download/binaries/ImageMagick-7.1.1-44-Q16-x64-dll.exe

### نصب:
1. اجرای فایل دانلود شده
2. ✅ **مهم:** گزینه "Install legacy utilities (e.g. convert)" را حتماً تیک بزنید
3. ✅ **مهم:** گزینه "Add application directory to system path" را حتماً تیک بزنید
4. کلیک روی "Install"

### تست نصب:
```bash
# PowerShell را ببندید و دوباره باز کنید
# سپس تست کنید:
convert -version
```

اگر نسخه ImageMagick را نشان داد، نصب موفق بوده است! ✅

---

## مرحله 2: اجرای ویدیو

### گزینه A: ویدیوی ساده (بدون متن) - آماده است!
```bash
python test_video_minimal.py
```
**خروجی:** `test_minimal.mp4` (5 ثانیه، رنگ چیدمانو)

---

### گزینه B: ویدیوی با متن (نیاز به ImageMagick)
```bash
python test_video_no_audio.py
```
**خروجی:** `test_output.mp4` (10 ثانیه، با متن)

---

### گزینه C: ویدیوی کامل 30 ثانیه‌ای (نیاز به ImageMagick)
```bash
python generate_chidmano_video.py
```
**خروجی:** `video_output/chidmano_ad_30s.mp4`

---

## مرحله 3: مشاهده ویدیو

ویدیوهای تولید شده در همان پوشه پروژه ذخیره می‌شوند:
- `test_minimal.mp4`
- `test_output.mp4`
- `video_output/chidmano_ad_30s.mp4`

با هر video player باز کنید (VLC, Windows Media Player, و...)

---

## 🐛 عیب‌یابی

### خطا: "ImageMagick not found"
راه‌حل:
1. ImageMagick را نصب کنید (بالا)
2. PowerShell را ببندید و دوباره باز کنید
3. تست: `convert -version`

### خطا: "FFmpeg not found"
راه‌حل: (معمولاً نیاز نیست، چون با moviepy نصب شده)
```bash
pip install imageio-ffmpeg
```

### ویدیو خیلی کند تولید می‌شود
عادی است! اولین بار 5-10 دقیقه طول می‌کشد.

---

## ⚡ شروع سریع (بدون نصب اضافی)

اگر نمی‌خواهید ImageMagick نصب کنید:

```bash
# ویدیوی ساده (فقط رنگ):
python test_video_minimal.py
```

این ویدیو بدون متن است ولی عملکرد سیستم را تست می‌کند! ✅

---

## 🎯 توصیه

**برای شروع:**
```bash
# 1. ابتدا تست ساده:
python test_video_minimal.py

# 2. اگر کار کرد، ImageMagick نصب کنید

# 3. سپس ویدیوی کامل:
python generate_chidmano_video.py
```

موفق باشید! 🚀

