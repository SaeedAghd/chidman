#!/usr/bin/env python3
"""
اسکریپت راه‌اندازی HTTPS با uvicorn
"""

import os
import sys
import django
from pathlib import Path

# اضافه کردن مسیر پروژه به sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# تنظیم متغیر محیطی Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')

# راه‌اندازی Django
django.setup()

if __name__ == "__main__":
    import uvicorn
    from django.core.management import execute_from_command_line
    
    # بررسی وجود فایل‌های SSL
    cert_file = "ssl/cert.pem"
    key_file = "ssl/key.pem"
    
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("❌ فایل‌های SSL یافت نشدند!")
        print("💡 ابتدا اسکریپت create_ssl_cert.py را اجرا کنید")
        sys.exit(1)
    
    print("🚀 راه‌اندازی سرور HTTPS...")
    print("🌐 آدرس: https://127.0.0.1:8443")
    print("📁 فایل‌های SSL:")
    print(f"   - Certificate: {cert_file}")
    print(f"   - Private Key: {key_file}")
    print("\n⏹️ برای توقف سرور، Ctrl+C را فشار دهید")
    
    try:
        # راه‌اندازی سرور HTTPS با uvicorn
        uvicorn.run(
            "chidmano.asgi:application",
            host="127.0.0.1",
            port=8443,
            ssl_keyfile=key_file,
            ssl_certfile=cert_file,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 سرور متوقف شد")
    except Exception as e:
        print(f"❌ خطا در راه‌اندازی سرور: {e}")
        sys.exit(1)
