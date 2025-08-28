#!/usr/bin/env python
"""
Test script to verify Django server connection
"""
import requests
import sys

def test_connection():
    """Test connection to Django server"""
    try:
        # Test HTTP connection
        response = requests.get('http://127.0.0.1:8000', timeout=5)
        print(f"✅ سرور Django در حال اجرا است!")
        print(f"📊 کد وضعیت: {response.status_code}")
        print(f"🌐 آدرس: http://127.0.0.1:8000")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ سرور Django در دسترس نیست")
        print("💡 لطفاً سرور را راه‌اندازی کنید:")
        print("   python manage.py runserver 127.0.0.1:8000")
        return False
    except requests.exceptions.Timeout:
        print("⏰ درخواست timeout شد")
        return False
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False

if __name__ == "__main__":
    print("🔍 تست اتصال به سرور Django...")
    success = test_connection()
    sys.exit(0 if success else 1)
