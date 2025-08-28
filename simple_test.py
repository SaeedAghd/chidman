#!/usr/bin/env python
import requests
import urllib3

# Disable SSL warnings and verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_simple():
    """Simple test to check if Django server is running"""
    print("🔍 تست ساده سرور Django...")
    
    try:
        # Create session with SSL verification disabled
        session = requests.Session()
        session.verify = False
        
        # Test main page
        response = session.get('http://localhost:8000/', timeout=5)
        print(f"✅ سرور در حال اجرا است! کد وضعیت: {response.status_code}")
        print(f"📄 طول پاسخ: {len(response.text)} کاراکتر")
        
        if "Django" in response.text or "chidman" in response.text.lower():
            print("✅ محتوای Django شناسایی شد!")
        else:
            print("⚠️ محتوای Django شناسایی نشد")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ سرور در دسترس نیست")
        return False
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False

if __name__ == "__main__":
    test_simple()
