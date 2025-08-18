#!/usr/bin/env python3
"""
اسکریپت تست HTTPS
"""

import urllib.request
import ssl
import sys

def test_https():
    """تست اتصال HTTPS"""
    
    # ایجاد context برای نادیده گرفتن certificate warnings
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        # تست اتصال به HTTPS
        url = "https://127.0.0.1:8443/store-analysis/"
        print(f"🔍 تست اتصال به: {url}")
        
        with urllib.request.urlopen(url, context=context) as response:
            print(f"✅ اتصال موفق!")
            print(f"📊 Status Code: {response.status}")
            print(f"📄 Content Type: {response.headers.get('Content-Type', 'Unknown')}")
            print(f"📏 Content Length: {response.headers.get('Content-Length', 'Unknown')}")
            
            # خواندن بخشی از محتوا
            content = response.read(500).decode('utf-8')
            if "فرم تحلیل رایگان فروشگاه" in content:
                print("✅ محتوای صحیح یافت شد!")
            else:
                print("⚠️ محتوای مورد انتظار یافت نشد")
                
    except urllib.error.URLError as e:
        print(f"❌ خطا در اتصال: {e}")
        return False
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 شروع تست HTTPS...")
    success = test_https()
    
    if success:
        print("\n🎉 تست HTTPS موفق بود!")
        print("🌐 حالا می‌توانید از https://127.0.0.1:8443 استفاده کنید")
    else:
        print("\n💥 تست HTTPS ناموفق بود!")
        sys.exit(1)
