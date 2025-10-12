# 🎬 راهنمای سریع تولید ویدیوی چیدمانو

## 📦 نصب

### گام 1: نصب FFmpeg (ضروری)

#### Windows:
```bash
# دانلود از: https://www.gyan.dev/ffmpeg/builds/
# یا با chocolatey:
choco install ffmpeg
```

#### Mac:
```bash
brew install ffmpeg
```

#### Linux:
```bash
sudo apt-get install ffmpeg
```

### گام 2: نصب کتابخانه‌های Python

```bash
pip install -r video_requirements.txt
```

---

## 🚀 اجرا

### روش ساده:
```bash
python generate_chidmano_video.py
```

### اجرا در PowerShell:
```powershell
python generate_chidmano_video.py
```

---

## 📁 ساختار فایل‌ها

```
chideman/
├── generate_chidmano_video.py  # اسکریپت اصلی
├── video_requirements.txt       # کتابخانه‌های مورد نیاز
├── video_assets/                # فایل‌های تولید شده (خودکار)
│   ├── vo_scene1.mp3
│   ├── vo_scene2.mp3
│   ├── vo_scene3.mp3
│   ├── vo_scene4.mp3
│   ├── bg_chaos.png
│   ├── bg_ai.png
│   ├── bg_order.png
│   └── bg_cta.png
└── video_output/                # ویدیوی نهایی (خودکار)
    └── chidmano_ad_30s.mp4
```

---

## ⚙️ تنظیمات (در کد)

### تغییر رزولوشن به Landscape (YouTube):
```python
# در فایل generate_chidmano_video.py:
class Config:
    WIDTH = 1920   # بود: 1080
    HEIGHT = 1080  # بود: 1920
```

### تغییر رنگ‌ها:
```python
COLOR_TEAL = (26, 188, 156)  # رنگ اصلی
COLOR_WHITE = (255, 255, 255)
COLOR_GOLD = (243, 156, 18)
```

### تغییر متن‌های نریشن:
```python
narrations = {
    'scene1': "متن دلخواه شما...",
    'scene2': "متن دلخواه شما...",
    # ...
}
```

---

## 🎥 خروجی

- **فرمت:** MP4 (H.264)
- **رزولوشن:** 1080×1920 (Portrait برای استوری)
- **FPS:** 30
- **مدت زمان:** ~30 ثانیه
- **حجم:** ~15-25 MB

---

## 🐛 عیب‌یابی

### خطا: "FFmpeg not found"
```bash
# نصب FFmpeg (بالا را ببینید)
# یا:
pip install imageio-ffmpeg
```

### خطا: "No module named 'moviepy'"
```bash
pip install moviepy
```

### خطا: "Cannot import name 'AudioFileClip'"
```bash
pip uninstall moviepy
pip install moviepy==1.0.3
```

### ویدیو بدون صدا:
```bash
# نصب پکیج‌های صوتی:
pip install pydub
# Windows: نصب ffmpeg از سایت رسمی
```

### فونت فارسی نمایش نمی‌دهد:
```python
# در کد، فونت پیش‌فرض استفاده می‌شود
# برای بهتر شدن، فونت Vazirmatn را دانلود کنید:
# https://github.com/rastikerdar/vazirmatn
```

---

## 🎨 سفارشی‌سازی پیشرفته

### اضافه کردن لوگو:
```python
# در Scene 4:
logo = ImageClip("path/to/logo.png")
logo = logo.resize(height=200).set_position('center')
```

### تغییر موسیقی پس‌زمینه:
```python
# اضافه کردن موسیقی:
bg_music = AudioFileClip("music.mp3").volumex(0.3)
final_video = final_video.set_audio(
    CompositeAudioClip([final_video.audio, bg_music])
)
```

### افزودن ترانزیشن:
```python
from moviepy.video.compositing.transitions import crossfadein

scene2 = scene2.crossfadein(1)  # fade in 1 second
```

---

## 📤 انتشار

### Instagram Story (1080×1920):
- ✅ آماده است! فایل خروجی همین است

### YouTube Shorts (1080×1920):
- ✅ آماده است!

### YouTube Regular (1920×1080):
```python
# تغییر رزولوشن در Config:
WIDTH = 1920
HEIGHT = 1080
```

### Instagram Feed (1080×1080):
```python
# crop به مربع:
from moviepy.video.fx.all import crop
square = final_video.crop(
    x_center=final_video.w/2,
    width=1080,
    height=1080
)
```

---

## 💡 نکات مهم

1. **زمان اجرا:** اولین بار ~5-10 دقیقه طول می‌کشد
2. **حجم RAM:** حداقل 4GB RAM توصیه می‌شود
3. **فضای دیسک:** حداقل 500MB فضای خالی
4. **اینترنت:** برای gTTS (تولید صدا) نیاز است

---

## 🚀 نسخه حرفه‌ای

برای کیفیت بالاتر:

### 1. استفاده از ElevenLabs (Voice AI):
```bash
pip install elevenlabs
# در کد از ElevenLabs به جای gTTS استفاده کنید
```

### 2. ویدیوهای واقعی:
```python
# به جای تصاویر ثابت، ویدیوهای واقعی قرار دهید:
scene1_bg = VideoFileClip("real_store_chaos.mp4")
```

### 3. موسیقی حرفه‌ای:
```python
# دانلود از YouTube Audio Library یا Epidemic Sound
bg_music = AudioFileClip("cinematic_music.mp3")
```

---

## 📞 پشتیبانی

اگر مشکلی داشتید:
1. ابتدا FFmpeg را نصب کنید
2. Python 3.8+ استفاده کنید
3. کتابخانه‌ها را دوباره نصب کنید:
   ```bash
   pip install --upgrade -r video_requirements.txt
   ```

---

## 🎉 موفق باشید!

ویدیوی تولید شده را در شبکه‌های اجتماعی منتشر کنید و نتایج را با ما به اشتراک بگذارید!

**#چیدمانو #هوش_مصنوعی #افزایش_فروش**

