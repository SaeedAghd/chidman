# 🎬 ابزارهای رایگان و Open Source برای تولید ویدیو تبلیغاتی

## 🏆 بهترین گزینه‌ها برای چیدمانو

### 1. **Stable Video Diffusion** ⭐ (پیشنهاد اول)
- **نوع**: AI Video Generation
- **قیمت**: کاملاً رایگان (Open Source)
- **قابلیت**: تولید ویدیو از تصویر
- **کیفیت**: عالی (SDXL کیفیت)
- **سرعت**: سریع با GPU
- **نصب**: 
  ```bash
  # استفاده از Hugging Face
  pip install diffusers transformers accelerate
  ```
- **مزایا**:
  - ✅ کیفیت بالا
  - ✅ رایگان و Open Source
  - ✅ قابل اجرا روی GPU محلی
  - ✅ بدون محدودیت استفاده
  
- **معایب**:
  - ⚠️ نیاز به GPU قدرتمند
  - ⚠️ نیاز به دانش فنی

**لینک**: https://github.com/Stability-AI/generative-models

---

### 2. **AnimateDiff** ⭐⭐ (پیشنهاد دوم)
- **نوع**: تبدیل تصویر به انیمیشن
- **قیمت**: کاملاً رایگان
- **قابلیت**: انیمیشن تصاویر استاتیک
- **کیفیت**: عالی
- **نصب**: 
  ```bash
  git clone https://github.com/guoyww/AnimateDiff.git
  ```
- **مزایا**:
  - ✅ انیمیشن نرم و طبیعی
  - ✅ کنترل کامل روی انیمیشن
  - ✅ رایگان

**لینک**: https://github.com/guoyww/AnimateDiff

---

### 3. **ComfyUI** ⭐⭐⭐ (پیشنهاد سوم - ساده‌ترین)
- **نوع**: رابط کاربری برای مدل‌های AI
- **قیمت**: کاملاً رایگان
- **قابلیت**: رابط گرافیکی برای Stable Diffusion, AnimateDiff, و...
- **کیفیت**: بستگی به مدل دارد
- **نصب**: 
  ```bash
  git clone https://github.com/comfyanonymous/ComfyUI.git
  cd ComfyUI
  pip install -r requirements.txt
  ```
- **مزایا**:
  - ✅ رابط کاربری ساده
  - ✅ پشتیبانی از چندین مدل
  - ✅ Workflow های آماده
  - ✅ بدون نیاز به کد نویسی

**لینک**: https://github.com/comfyanonymous/ComfyUI

---

### 4. **Remotion** (برای تولید ویدیو با Code)
- **نوع**: React-based Video Generation
- **قیمت**: رایگان (Personal)
- **قابلیت**: تولید ویدیو با React/TypeScript
- **کیفیت**: حرفه‌ای
- **مزایا**:
  - ✅ تولید ویدیو با کد
  - ✅ کنترل کامل روی انیمیشن
  - ✅ مناسب برای ویدیوهای تبلیغاتی

**لینک**: https://www.remotion.dev/

---

### 5. **MoviePy** (Python Library)
- **نوع**: Python Library برای ویرایش ویدیو
- **قیمت**: کاملاً رایگان
- **قابلیت**: ویرایش، ترکیب، اضافه کردن متن
- **مثال کد**:
  ```python
  from moviepy.editor import *
  
  # ساخت ویدیو از تصاویر
  clips = [ImageClip(img).set_duration(2) for img in images]
  video = concatenate_videoclips(clips)
  video.write_videofile("output.mp4", fps=24)
  ```
- **مزایا**:
  - ✅ برنامه‌نویسی با Python
  - ✅ کنترل کامل
  - ✅ رایگان

**لینک**: https://github.com/Zulko/moviepy

---

### 6. **CapCut** (ساده‌ترین - بدون نیاز به نصب)
- **نوع**: نرم‌افزار ویرایش ویدیو
- **قیمت**: کاملاً رایگان
- **قابلیت**: ویرایش حرفه‌ای، AI features
- **مزایا**:
  - ✅ رابط کاربری ساده
  - ✅ AI features (حذف پس‌زمینه، زیرنویس خودکار)
  - ✅ قالب‌های آماده
  - ✅ مناسب برای اینستاگرام

**لینک**: https://www.capcut.com/

---

## 🎯 پیشنهاد ترکیبی (Best Workflow)

### گزینه 1: **ComfyUI + Stable Video Diffusion** (برای تولید AI)
```
1. نصب ComfyUI
2. دانلود Stable Video Diffusion model
3. آپلود تصاویر فروشگاه
4. تولید ویدیو با AI
5. ویرایش با CapCut (اضافه کردن متن، موسیقی)
```

### گزینه 2: **MoviePy + Python Script** (برای تولید خودکار)
```python
# ساخت ویدیو تبلیغاتی با MoviePy
from moviepy.editor import *
import os

def create_instagram_video():
    # 1. تصاویر فروشگاه
    images = ['store1.jpg', 'store2.jpg', 'store3.jpg']
    
    # 2. ساخت clip از تصاویر
    clips = []
    for img in images:
        clip = ImageClip(img).set_duration(2)
        # اضافه کردن متن
        txt_clip = TextClip("چیدمانو", 
                          fontsize=50, 
                          color='white',
                          font='Vazir').set_duration(2)
        clip = CompositeVideoClip([clip, txt_clip])
        clips.append(clip)
    
    # 3. ترکیب clips
    video = concatenate_videoclips(clips, method="compose")
    
    # 4. اضافه کردن موسیقی
    audio = AudioFileClip("music.mp3")
    video = video.set_audio(audio)
    
    # 5. تنظیم برای اینستاگرام (9:16)
    video = video.resize(height=1920)
    
    # 6. ذخیره
    video.write_videofile("instagram_video.mp4", fps=24, codec='libx264')
```

---

## 🚀 راهنمای سریع نصب (ComfyUI + Stable Video Diffusion)

### مرحله 1: نصب ComfyUI
```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

### مرحله 2: دانلود مدل Stable Video Diffusion
```bash
# از Hugging Face
huggingface-cli download stabilityai/stable-video-diffusion-img2vid-xt
```

### مرحله 3: اجرا
```bash
python main.py
```

### مرحله 4: استفاده
1. باز کردن http://127.0.0.1:8188
2. آپلود تصویر فروشگاه
3. تنظیمات (duration, fps)
4. Generate

---

## 📊 مقایسه سریع

| ابزار | نصب | کیفیت | سرعت | پیچیدگی | هزینه |
|-------|-----|-------|------|---------|-------|
| **Stable Video Diffusion** | متوسط | ⭐⭐⭐⭐⭐ | متوسط | متوسط | رایگان |
| **AnimateDiff** | متوسط | ⭐⭐⭐⭐ | سریع | متوسط | رایگان |
| **ComfyUI** | آسان | ⭐⭐⭐⭐⭐ | متوسط | آسان | رایگان |
| **Remotion** | آسان | ⭐⭐⭐⭐ | سریع | متوسط | رایگان |
| **MoviePy** | آسان | ⭐⭐⭐ | سریع | آسان | رایگان |
| **CapCut** | آسان | ⭐⭐⭐⭐ | سریع | خیلی آسان | رایگان |

---

## 💡 توصیه نهایی

### برای چیدمانو، بهترین گزینه:

**ترکیب ComfyUI + CapCut**

**چرا؟**
1. ✅ ComfyUI: تولید ویدیو با AI از تصاویر فروشگاه
2. ✅ CapCut: ویرایش نهایی، اضافه کردن متن فارسی، موسیقی
3. ✅ هر دو رایگان هستند
4. ✅ نتیجه حرفه‌ای

**Workflow پیشنهادی:**
```
1. تصاویر فروشگاه → ComfyUI → ویدیو AI
2. ویدیو AI → CapCut → ویرایش + متن + موسیقی
3. Export برای اینستاگرام (9:16)
```

---

## 🔧 Integration با Pipedream

اگر می‌خواهید خودکارسازی کنید:

```javascript
// Pipedream Workflow
export default defineComponent({
  async run({ $ }) {
    // 1. دریافت تصاویر از فروشگاه
    const images = await fetchStoreImages();
    
    // 2. فراخوانی Stable Video Diffusion API
    const video = await axios.post('http://localhost:8188/api/v1/run', {
      prompt: "فروشگاه مدرن با چیدمان بهینه",
      images: images,
      duration: 60,
      fps: 24
    });
    
    // 3. دانلود ویدیو
    const videoFile = await downloadVideo(video.url);
    
    // 4. آپلود به اینستاگرام
    await uploadToInstagram(videoFile);
  }
});
```

---

## 📝 منابع مفید

- [ComfyUI Documentation](https://github.com/comfyanonymous/ComfyUI)
- [Stable Video Diffusion Guide](https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt)
- [MoviePy Tutorial](https://zulko.github.io/moviepy/)
- [CapCut Tutorial](https://www.capcut.com/help)

---

## ✅ Checklist

- [ ] نصب ComfyUI
- [ ] دانلود Stable Video Diffusion model
- [ ] آماده کردن تصاویر فروشگاه
- [ ] تولید ویدیو اولیه
- [ ] ویرایش با CapCut
- [ ] تست روی اینستاگرام
- [ ] بهینه‌سازی بر اساس نتایج

