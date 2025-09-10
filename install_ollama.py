#!/usr/bin/env python
"""
اسکریپت نصب و راه‌اندازی Ollama برای تحلیل AI فروشگاه
"""

import os
import sys
import subprocess
import platform
import requests
import time

def check_ollama_installed():
    """بررسی نصب بودن Ollama"""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except:
        return False

def install_ollama():
    """نصب Ollama"""
    system = platform.system().lower()
    
    print("🚀 شروع نصب Ollama...")
    
    if system == "windows":
        print("📥 دانلود Ollama برای Windows...")
        # دانلود و نصب Ollama برای Windows
        try:
            # استفاده از winget برای نصب
            subprocess.run(['winget', 'install', 'Ollama.Ollama'], check=True)
            print("✅ Ollama با موفقیت نصب شد!")
            return True
        except:
            print("❌ خطا در نصب Ollama. لطفاً دستی نصب کنید:")
            print("   https://ollama.ai/download")
            return False
    
    elif system == "linux":
        print("📥 نصب Ollama برای Linux...")
        try:
            # نصب از طریق curl
            subprocess.run([
                'curl', '-fsSL', 'https://ollama.ai/install.sh'
            ], check=True, stdout=subprocess.PIPE)
            print("✅ Ollama با موفقیت نصب شد!")
            return True
        except:
            print("❌ خطا در نصب Ollama. لطفاً دستی نصب کنید:")
            print("   curl -fsSL https://ollama.ai/install.sh | sh")
            return False
    
    elif system == "darwin":  # macOS
        print("📥 نصب Ollama برای macOS...")
        try:
            # نصب از طریق Homebrew
            subprocess.run(['brew', 'install', 'ollama'], check=True)
            print("✅ Ollama با موفقیت نصب شد!")
            return True
        except:
            print("❌ خطا در نصب Ollama. لطفاً دستی نصب کنید:")
            print("   brew install ollama")
            return False
    
    else:
        print(f"❌ سیستم عامل {system} پشتیبانی نمی‌شود")
        return False

def start_ollama_service():
    """راه‌اندازی سرویس Ollama"""
    print("🔄 راه‌اندازی سرویس Ollama...")
    
    try:
        # شروع سرویس Ollama
        subprocess.Popen(['ollama', 'serve'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # انتظار برای راه‌اندازی
        print("⏳ منتظر راه‌اندازی سرویس...")
        time.sleep(5)
        
        # بررسی دسترسی
        for i in range(10):
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    print("✅ سرویس Ollama راه‌اندازی شد!")
                    return True
            except:
                time.sleep(2)
        
        print("❌ سرویس Ollama راه‌اندازی نشد")
        return False
        
    except Exception as e:
        print(f"❌ خطا در راه‌اندازی سرویس: {e}")
        return False

def download_model():
    """دانلود مدل Llama"""
    print("📥 دانلود مدل Llama 3.2...")
    
    try:
        # دانلود مدل
        result = subprocess.run([
            'ollama', 'pull', 'llama3.2'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ مدل Llama 3.2 دانلود شد!")
            return True
        else:
            print(f"❌ خطا در دانلود مدل: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ زمان دانلود مدل تمام شد. لطفاً دوباره تلاش کنید.")
        return False
    except Exception as e:
        print(f"❌ خطا در دانلود مدل: {e}")
        return False

def test_ollama():
    """تست Ollama"""
    print("🧪 تست Ollama...")
    
    try:
        # تست ساده
        result = subprocess.run([
            'ollama', 'run', 'llama3.2', 'سلام، چطوری؟'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Ollama به درستی کار می‌کند!")
            print(f"📝 پاسخ: {result.stdout[:100]}...")
            return True
        else:
            print(f"❌ خطا در تست: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ خطا در تست: {e}")
        return False

def main():
    """تابع اصلی"""
    print("🚀 راه‌اندازی Ollama برای تحلیل AI فروشگاه")
    print("=" * 50)
    
    # بررسی نصب بودن
    if check_ollama_installed():
        print("✅ Ollama قبلاً نصب شده است")
    else:
        print("❌ Ollama نصب نشده است")
        if not install_ollama():
            print("❌ نصب Ollama ناموفق بود")
            return False
    
    # راه‌اندازی سرویس
    if not start_ollama_service():
        print("❌ راه‌اندازی سرویس ناموفق بود")
        return False
    
    # دانلود مدل
    if not download_model():
        print("❌ دانلود مدل ناموفق بود")
        return False
    
    # تست
    if not test_ollama():
        print("❌ تست ناموفق بود")
        return False
    
    print("\n🎉 Ollama با موفقیت راه‌اندازی شد!")
    print("📋 دستورات مفید:")
    print("   ollama serve          # راه‌اندازی سرویس")
    print("   ollama list           # لیست مدل‌ها")
    print("   ollama run llama3.2   # اجرای مدل")
    print("   ollama stop           # توقف سرویس")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
