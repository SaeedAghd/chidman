from PIL import Image
from pathlib import Path

base = Path('static/images')
base.mkdir(parents=True, exist_ok=True)
logo = base / 'logo_optimized.png'
if not logo.exists():
    logo = base / 'logo.png'
slider_bg = base / 'slider' / 'background.jpg'
slider_bg_opt = base / 'slider' / 'background_optimized.jpg'

# helper
def save_resized(src, dest, size):
    try:
        im = Image.open(src).convert('RGBA')
        im = im.resize(size, Image.LANCZOS)
        im.save(dest, format='PNG')
        print('wrote', dest)
    except Exception as e:
        print('failed', dest, e)

# icons
save_resized(logo, base / 'icon-192x192.png', (192,192))
save_resized(logo, base / 'icon-512x512.png', (512,512))
# shortcuts
save_resized(logo, base / 'shortcut-analysis.png', (96,96))
save_resized(logo, base / 'shortcut-dashboard.png', (96,96))
save_resized(logo, base / 'shortcut-guide.png', (96,96))
# screenshots
bg_src = slider_bg_opt if slider_bg_opt.exists() else slider_bg if slider_bg.exists() else logo
save_resized(bg_src, base / 'screenshot-desktop.png', (1280,720))
save_resized(bg_src, base / 'screenshot-mobile.png', (750,1334))

print('done')
