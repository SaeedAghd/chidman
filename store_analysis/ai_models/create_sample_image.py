import cv2
import numpy as np
import os
from django.conf import settings

def create_sample_layout():
    # ایجاد تصویر خالی
    width, height = 800, 600
    image = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # رسم دیوارها
    cv2.rectangle(image, (50, 50), (750, 550), (0, 0, 0), 2)
    
    # رسم در ورودی
    cv2.rectangle(image, (400, 50), (450, 80), (0, 255, 0), -1)
    
    # رسم قفسه‌ها
    shelves = [
        ((100, 100), (300, 200)),  # قفسه 1
        ((400, 100), (600, 200)),  # قفسه 2
        ((100, 300), (300, 400)),  # قفسه 3
        ((400, 300), (600, 400)),  # قفسه 4
    ]
    
    for shelf in shelves:
        cv2.rectangle(image, shelf[0], shelf[1], (0, 0, 255), -1)
    
    # رسم میز صندوق
    cv2.rectangle(image, (350, 450), (450, 500), (255, 0, 0), -1)
    
    # رسم مسیرهای اصلی
    paths = [
        ((400, 80), (400, 450)),   # مسیر اصلی
        ((200, 200), (200, 400)),  # مسیر فرعی 1
        ((500, 200), (500, 400)),  # مسیر فرعی 2
    ]
    
    for path in paths:
        cv2.line(image, path[0], path[1], (128, 128, 128), 3)
    
    # ذخیره تصویر
    output_dir = os.path.join(settings.MEDIA_ROOT, 'store_analysis', 'sample')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'layout.jpg')
    cv2.imwrite(output_path, image)
    
    print(f"تصویر نمونه در مسیر {output_path} ذخیره شد.")

if __name__ == "__main__":
    create_sample_layout() 