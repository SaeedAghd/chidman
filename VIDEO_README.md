# 🎬 سیستم تولید ویدیوی تبلیغاتی چیدمانو

## ✅ تست موفق!

ویدیوی ساده تولید شد: `test_minimal.mp4`

---

## 📋 وضعیت فعلی

### ✅ نصب شده:
- Python 3.11
- MoviePy 1.0.3
- Pillow (PIL)
- NumPy 1.24.3
- FFmpeg (از طریق imageio-ffmpeg)

### ⚠️ نیاز به نصب:
- **ImageMagick** - برای افزودن متن به ویدیو

---

## 🔧 نصب ImageMagick (Windows)

### گام 1: دانلود
https://imagemagick.org/script/download.php#windows

یا مستقیم:
https://download.imagemagick.org/ImageMagick/download/binaries/ImageMagick-7.1.1-44-Q16-x64-dll.exe

### گام 2: نصب
1. اجرای فایل نصب
2. ✅ حتماً گزینه "Install legacy utilities" را انتخاب کنید
3. ✅ گزینه "Add to PATH" را فعال کنید

### گام 3: راه‌اندازی مجدد
```bash
# بستن PowerShell و باز کردن مجدد
# تست:
convert -version
```

---

## 🚀 اجرای اسکریپت‌ها

### تست ساده (بدون متن):
```bash
python test_video_minimal.py
# خروجی: test_minimal.mp4 (5 ثانیه رنگ ثابت)
```

### تست کامل (با متن) - نیاز به ImageMagick:
```bash
python test_video_no_audio.py
# خروجی: test_output.mp4 (10 ثانیه با متن)
```

### ویدیوی نهایی 30 ثانیه‌ای:
```bash
python generate_chidmano_video.py
# خروجی: video_output/chidmano_ad_30s.mp4
```

---

## 🎨 محتوای ویدیوی نهایی

### صحنه 1 (0-6s): بی‌نظمی
- تصویر تیره با خطوط بی‌نظم
- متن: "مشکل واقعی: ۷۵٪ فروشگاه‌ها..."

### صحنه 2 (6-14s): هوش مصنوعی
- Grid دیجیتال با نقاط نورانی
- متن: "تحلیل چیدمان با هوش مصنوعی 🧠"
- زیرنویس: "GPT-4 • Claude • Computer Vision"

### صحنه 3 (14-22s): نظم و موفقیت
- گرادیانت روشن
- آمارها:
  - ↑ 47% افزایش فروش
  - ↑ 32% رضایت مشتری
  - ↑ 28% زمان ماندگاری

### صحنه 4 (22-30s): CTA
- پس‌زمینه سفید
- لوگو "چیدمانو"
- شعار: "نظم · فروش · آرامش"
- URL: www.chidmano.ir
- دکمه: "ثبت رایگان فروشگاه 🚀"

---

## 🎯 نسخه‌های مختلف

### Portrait (Story) - پیش‌فرض:
```python
WIDTH = 1080
HEIGHT = 1920
```

### Landscape (YouTube):
```python
WIDTH = 1920
HEIGHT = 1080
```

### Square (Instagram Feed):
```python
WIDTH = 1080
HEIGHT = 1080
```

---

## 📊 مشخصات فنی

- **Codec:** H.264 (libx264)
- **FPS:** 30
- **Audio:** AAC (اختیاری)
- **حجم:** ~15-25 MB
- **مدت زمان:** 30 ثانیه

---

## 🐛 عیب‌یابی

### خطا: "ImageMagick not found"
```
نصب ImageMagick + restart PowerShell
```

### خطا: "Language not supported: fa"
```
gTTS فارسی را پشتیبانی نمی‌کند
راه‌حل: استفاده از ElevenLabs یا Azure TTS
```

### خطا: "FFmpeg not found"
```
pip install imageio-ffmpeg
```

---

## 🔮 آپدیت آینده

### نسخه 2.0 (برنامه‌ریزی شده):
- [ ] صداگذاری فارسی با ElevenLabs
- [ ] ویدیوهای واقعی به جای تصاویر ثابت
- [ ] انیمیشن‌های پیشرفته‌تر
- [ ] موسیقی پس‌زمینه
- [ ] افکت‌های حرفه‌ای (glitch, particles)

### نسخه 3.0 (آینده):
- [ ] تولید خودکار با AI (DALL-E/Midjourney)
- [ ] انیمیشن با Runway ML
- [ ] صداگذاری با OpenAI TTS

---

## 📁 ساختار فایل‌ها

```
chideman/
├── generate_chidmano_video.py      # اسکریپت اصلی
├── test_video_minimal.py           # تست ساده (✅ کار می‌کند)
├── test_video_no_audio.py          # تست با متن (نیاز به ImageMagick)
├── video_requirements.txt          # کتابخانه‌های مورد نیاز
├── VIDEO_QUICK_START.md            # راهنمای سریع
├── CHIDMANO_VIDEO_PRODUCTION_GUIDE.md  # راهنمای کامل
├── VIDEO_README.md                 # این فایل
│
├── video_assets/                   # فایل‌های میانی (خودکار)
│   ├── bg_*.png
│   └── vo_*.mp3
│
└── video_output/                   # خروجی نهایی
    └── chidmano_ad_30s.mp4
```

---

## 🎉 مراحل بعدی

### 1. نصب ImageMagick:
```
https://imagemagick.org/script/download.php#windows
```

### 2. تست با متن:
```bash
python test_video_no_audio.py
```

### 3. تولید ویدیوی نهایی:
```bash
python generate_chidmano_video.py
```

### 4. انتشار:
- Instagram Story
- YouTube Shorts
- WhatsApp Status

---

## 💡 نکات مهم

1. **اولین بار:** نصب ImageMagick ضروری است
2. **زمان اجرا:** 5-10 دقیقه برای ویدیوی 30 ثانیه‌ای
3. **RAM:** حداقل 4GB توصیه می‌شود
4. **دیسک:** 500MB فضای خالی

---

## 🚀 موفق باشید!

برای سوالات یا مشکلات، مستندات را مطالعه کنید:
- `VIDEO_QUICK_START.md` - راهنمای سریع
- `CHIDMANO_VIDEO_PRODUCTION_GUIDE.md` - راهنمای کامل

**#چیدمانو #تبلیغات_ویدیویی #MoviePy**

