"""
اسکریپت دانلود فونت‌های سالم Vazir
"""
import urllib.request
import os

# آدرس فونت‌های سالم از GitHub رسمی Vazir
fonts = {
    'Vazir.ttf': 'https://github.com/rastikerdar/vazir-font/raw/master/dist/Vazir-Regular.ttf',
    'Vazir-Bold.ttf': 'https://github.com/rastikerdar/vazir-font/raw/master/dist/Vazir-Bold.ttf'
}

# دایرکتوری static/fonts
fonts_dir = 'static/fonts'
os.makedirs(fonts_dir, exist_ok=True)

print("🔽 شروع دانلود فونت‌های Vazir...")

for filename, url in fonts.items():
    filepath = os.path.join(fonts_dir, filename)
    
    try:
        print(f"📥 دانلود {filename}...")
        urllib.request.urlretrieve(url, filepath)
        
        # بررسی اندازه فایل
        size = os.path.getsize(filepath)
        print(f"✅ {filename} دانلود شد ({size:,} bytes)")
        
    except Exception as e:
        print(f"❌ خطا در دانلود {filename}: {e}")

print("\n✅ تمام فونت‌ها دانلود شدند!")
print(f"📂 محل ذخیره: {os.path.abspath(fonts_dir)}")

