#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 Chidmano Video Generator - نسخه ساده و کاربردی
تولید ویدیوی تبلیغاتی 30 ثانیه‌ای با MoviePy

نصب کتابخانه‌ها:
pip install moviepy pillow numpy gtts pydub
"""

import os
import sys
from pathlib import Path
import numpy as np
from moviepy.editor import (
    VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip,
    concatenate_videoclips, ColorClip, ImageClip, vfx
)
from moviepy.video.fx.all import fadein, fadeout, speedx
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import warnings
warnings.filterwarnings('ignore')

print("🎬 Chidmano Video Generator")
print("=" * 60)

# ========================================
# تنظیمات اولیه
# ========================================

class Config:
    """تنظیمات پروژه"""
    BASE_DIR = Path(__file__).parent
    ASSETS_DIR = BASE_DIR / "video_assets"
    OUTPUT_DIR = BASE_DIR / "video_output"
    
    # رنگ‌ها
    COLOR_TEAL = (26, 188, 156)  # RGB
    COLOR_WHITE = (255, 255, 255)
    COLOR_GOLD = (243, 156, 18)
    COLOR_GRAY = (44, 62, 80)
    COLOR_DARK = (30, 30, 30)
    
    # مشخصات ویدیو
    WIDTH = 1080
    HEIGHT = 1920  # Portrait برای استوری
    FPS = 30
    DURATION = 30

# ایجاد پوشه‌ها
config = Config()
config.ASSETS_DIR.mkdir(exist_ok=True)
config.OUTPUT_DIR.mkdir(exist_ok=True)

# ========================================
# 1. تولید Voice Overs
# ========================================

print("\n📢 مرحله 1: تولید صداهای گوینده...")

narrations = {
    'scene1': "هر فروشگاه، با رؤیای نظم شروع میشه... اما با گذر زمان، آشفتگی جاشو می‌گیره.",
    'scene2': "چیدمانو با تحلیل هوشمند مسیر مشتری، هر سانتی‌متر فروشگاهت رو به سود تبدیل می‌کنه.",
    'scene3': "از ورودی تا صندوق، هر جزئی تحلیل و بهینه‌سازی شده. چون فروشگاه مرتب، فروش بیشتر یعنی.",
    'scene4': "چیدمانو، شریک هوشمند رشد فروش تو."
}

audio_files = {}

for scene_name, text in narrations.items():
    audio_path = config.ASSETS_DIR / f"vo_{scene_name}.mp3"
    
    if not audio_path.exists():
        print(f"  🎙️ تولید صدا برای {scene_name}...")
        tts = gTTS(text=text, lang='fa', slow=False)
        tts.save(str(audio_path))
        print(f"     ✓ ذخیره شد")
    else:
        print(f"  ✓ صدا برای {scene_name} قبلاً تولید شده")
    
    audio_files[scene_name] = str(audio_path)

print("✅ تولید صداها کامل شد!")

# ========================================
# 2. تولید تصاویر Background
# ========================================

print("\n🎨 مرحله 2: تولید تصاویر پس‌زمینه...")

def create_gradient_image(width, height, color1, color2, filename):
    """تولید تصویر گرادیانت"""
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    img.save(filename)
    return filename

def create_chaos_image(width, height, filename):
    """تصویر بی‌نظمی"""
    img = Image.new('RGB', (width, height), config.COLOR_DARK)
    draw = ImageDraw.Draw(img)
    
    # خطوط تصادفی برای نمایش بی‌نظمی
    for _ in range(100):
        x1, y1 = np.random.randint(0, width), np.random.randint(0, height)
        x2, y2 = np.random.randint(0, width), np.random.randint(0, height)
        color = tuple(np.random.randint(50, 150, 3))
        draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
    
    img.save(filename)
    return filename

def create_ai_image(width, height, filename):
    """تصویر هوش مصنوعی با grid"""
    img = Image.new('RGB', (width, height), (20, 30, 40))
    draw = ImageDraw.Draw(img)
    
    # Grid lines
    for x in range(0, width, 60):
        draw.line([(x, 0), (x, height)], fill=config.COLOR_TEAL, width=1)
    for y in range(0, height, 60):
        draw.line([(0, y), (width, y)], fill=config.COLOR_TEAL, width=1)
    
    # نقاط روشن (data points)
    for _ in range(50):
        x, y = np.random.randint(0, width), np.random.randint(0, height)
        r = np.random.randint(5, 15)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=config.COLOR_TEAL)
    
    img.save(filename)
    return filename

def create_order_image(width, height, filename):
    """تصویر نظم و زیبایی"""
    create_gradient_image(
        width, height,
        config.COLOR_WHITE,
        (240, 248, 255),  # آبی خیلی روشن
        filename
    )
    return filename

# تولید تصاویر
print("  🖼️ تولید background scene 1 (chaos)...")
chaos_img = create_chaos_image(config.WIDTH, config.HEIGHT, 
                                 config.ASSETS_DIR / "bg_chaos.png")

print("  🖼️ تولید background scene 2 (AI)...")
ai_img = create_ai_image(config.WIDTH, config.HEIGHT, 
                          config.ASSETS_DIR / "bg_ai.png")

print("  🖼️ تولید background scene 3 (order)...")
order_img = create_order_image(config.WIDTH, config.HEIGHT, 
                                config.ASSETS_DIR / "bg_order.png")

print("  🖼️ تولید background scene 4 (CTA)...")
cta_img = create_gradient_image(
    config.WIDTH, config.HEIGHT,
    config.COLOR_WHITE,
    (248, 249, 250),
    config.ASSETS_DIR / "bg_cta.png"
)

print("✅ تولید تصاویر کامل شد!")

# ========================================
# 3. ساخت صحنه‌ها
# ========================================

print("\n🎬 مرحله 3: ساخت صحنه‌های ویدیو...")

def create_text_clip(text, fontsize, color, position, duration, **kwargs):
    """تولید TextClip با تنظیمات بهتر"""
    try:
        # استفاده از فونت پیش‌فرض
        txt = TextClip(
            text,
            fontsize=fontsize,
            color=color,
            method='caption',
            size=(config.WIDTH - 100, None),
            align='center',
            **kwargs
        )
    except:
        # fallback اگر فونت نبود
        txt = TextClip(
            text,
            fontsize=fontsize,
            color=color,
            method='label'
        )
    
    txt = txt.set_position(position).set_duration(duration)
    return txt

# ========================================
# صحنه 1: بی‌نظمی (0-6 ثانیه)
# ========================================

print("  📹 ساخت Scene 1: بی‌نظمی...")

# Background
scene1_bg = ImageClip(str(chaos_img)).set_duration(6)
scene1_bg = scene1_bg.fx(vfx.colorx, 0.6)  # تیره‌تر

# متن
scene1_text = create_text_clip(
    "مشکل واقعی:\n۷۵٪ فروشگاه‌ها فضای خود را\nاشتباه چیدمان می‌کنند",
    fontsize=50,
    color='white',
    position=('center', config.HEIGHT - 400),
    duration=6
)
scene1_text = scene1_text.fx(fadein, 0.5).fx(fadeout, 0.5)

# صدا
scene1_audio = AudioFileClip(audio_files['scene1'])

# ترکیب
scene1 = CompositeVideoClip([scene1_bg, scene1_text])
scene1 = scene1.set_audio(scene1_audio)
scene1 = scene1.subclip(0, min(6, scene1_audio.duration))

print("     ✓ Scene 1 آماده شد")

# ========================================
# صحنه 2: هوش مصنوعی (6-14 ثانیه = 8 ثانیه)
# ========================================

print("  📹 ساخت Scene 2: هوش مصنوعی...")

# Background
scene2_bg = ImageClip(str(ai_img)).set_duration(8)

# متن اصلی
scene2_text_main = create_text_clip(
    "تحلیل چیدمان با\nهوش مصنوعی 🧠",
    fontsize=70,
    color='white',
    position=('center', 600),
    duration=8
)
scene2_text_main = scene2_text_main.fx(fadein, 0.5)

# زیرنویس
scene2_text_sub = create_text_clip(
    "GPT-4 • Claude • Computer Vision",
    fontsize=38,
    color='lightblue',
    position=('center', 850),
    duration=8
)
scene2_text_sub = scene2_text_sub.fx(fadein, 1)

# صدا
scene2_audio = AudioFileClip(audio_files['scene2'])

# ترکیب
scene2 = CompositeVideoClip([scene2_bg, scene2_text_main, scene2_text_sub])
scene2 = scene2.set_audio(scene2_audio)
scene2 = scene2.subclip(0, min(8, scene2_audio.duration))

print("     ✓ Scene 2 آماده شد")

# ========================================
# صحنه 3: نظم (14-22 ثانیه = 8 ثانیه)
# ========================================

print("  📹 ساخت Scene 3: نظم و موفقیت...")

# Background
scene3_bg = ImageClip(str(order_img)).set_duration(8)

# Stats
stats_text = [
    "↑ 47% افزایش فروش",
    "↑ 32% رضایت مشتری",
    "↑ 28% زمان ماندگاری"
]

stat_clips = []
for i, stat in enumerate(stats_text):
    stat_clip = TextClip(
        stat,
        fontsize=42,
        color='darkgreen',
        bg_color='white',
        method='label'
    ).set_position((100, 300 + i * 100)).set_duration(8)
    stat_clip = stat_clip.fx(fadein, 0.5 + i * 0.2)
    stat_clips.append(stat_clip)

# صدا
scene3_audio = AudioFileClip(audio_files['scene3'])

# ترکیب
scene3 = CompositeVideoClip([scene3_bg] + stat_clips)
scene3 = scene3.set_audio(scene3_audio)
scene3 = scene3.subclip(0, min(8, scene3_audio.duration))

print("     ✓ Scene 3 آماده شد")

# ========================================
# صحنه 4: CTA (22-30 ثانیه = 8 ثانیه)
# ========================================

print("  📹 ساخت Scene 4: دعوت به اقدام...")

# Background
scene4_bg = ImageClip(str(cta_img)).set_duration(8)

# لوگو (متن)
scene4_logo = create_text_clip(
    "چیدمانو",
    fontsize=90,
    color='#1ABC9C',
    position=('center', 500),
    duration=8
)
scene4_logo = scene4_logo.fx(fadein, 0.5)

# شعار
scene4_slogan = create_text_clip(
    "نظم · فروش · آرامش",
    fontsize=55,
    color='#2C3E50',
    position=('center', 700),
    duration=8
)
scene4_slogan = scene4_slogan.fx(fadein, 1)

# URL
scene4_url = create_text_clip(
    "www.chidmano.ir",
    fontsize=50,
    color='#1ABC9C',
    position=('center', 900),
    duration=8
)
scene4_url = scene4_url.fx(fadein, 1.5)

# CTA Button
scene4_cta = TextClip(
    "ثبت رایگان فروشگاه 🚀",
    fontsize=48,
    color='white',
    bg_color='#1ABC9C',
    method='label'
).set_position(('center', 1200)).set_duration(8)
scene4_cta = scene4_cta.fx(fadein, 2)

# صدا
scene4_audio = AudioFileClip(audio_files['scene4'])

# ترکیب
scene4 = CompositeVideoClip([
    scene4_bg,
    scene4_logo,
    scene4_slogan,
    scene4_url,
    scene4_cta
])
scene4 = scene4.set_audio(scene4_audio)
scene4 = scene4.subclip(0, min(8, scene4_audio.duration))

print("     ✓ Scene 4 آماده شد")

print("✅ تمام صحنه‌ها آماده شدند!")

# ========================================
# 4. ترکیب نهایی
# ========================================

print("\n🔗 مرحله 4: ترکیب صحنه‌ها و ایجاد ویدیو نهایی...")

# ترکیب همه صحنه‌ها
final_video = concatenate_videoclips([scene1, scene2, scene3, scene4])

# خروجی
output_path = config.OUTPUT_DIR / "chidmano_ad_30s.mp4"

print(f"\n💾 در حال ذخیره ویدیو...")
print(f"   📁 مسیر: {output_path}")
print(f"   ⏱️  مدت زمان: {final_video.duration:.1f} ثانیه")
print(f"   📐 رزولوشن: {config.WIDTH}x{config.HEIGHT}")
print(f"\n⏳ لطفاً صبر کنید... (ممکن است چند دقیقه طول بکشد)")

final_video.write_videofile(
    str(output_path),
    fps=config.FPS,
    codec='libx264',
    audio_codec='aac',
    preset='medium',
    threads=4,
    logger=None  # حذف لاگ‌های verbose
)

print("\n" + "=" * 60)
print("🎉 ویدیو با موفقیت تولید شد!")
print("=" * 60)
print(f"\n📂 فایل خروجی: {output_path}")
print(f"📊 حجم: {output_path.stat().st_size / (1024*1024):.1f} MB")
print(f"⏱️  مدت زمان: {final_video.duration:.1f} ثانیه")
print(f"\n✨ ویدیو آماده برای انتشار در:")
print("   • Instagram Story")
print("   • YouTube Shorts")
print("   • WhatsApp Status")
print("\n💡 نکته: برای تولید نسخه landscape (YouTube):")
print("   config.WIDTH = 1920")
print("   config.HEIGHT = 1080")
print("\n🚀 موفق باشید!")

