#!/usr/bin/env python
"""
اسکریپت راه‌اندازی کامل سیستم تحلیل AI فروشگاه
"""

import os
import sys
import subprocess
import platform
import requests
import time
from pathlib import Path

def print_header():
    """نمایش هدر"""
    print("🚀 راه‌اندازی سیستم تحلیل AI فروشگاه")
    print("=" * 50)
    print("این اسکریپت سیستم تحلیل AI را با Ollama راه‌اندازی می‌کند")
    print("Ollama یک سیستم AI رایگان و محلی است")
    print("=" * 50)

def check_system_requirements():
    """بررسی نیازمندی‌های سیستم"""
    print("🔍 بررسی نیازمندی‌های سیستم...")
    
    # بررسی Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8 یا بالاتر مورد نیاز است")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # بررسی Django
    try:
        import django
        print(f"✅ Django {django.get_version()}")
    except ImportError:
        print("❌ Django نصب نشده است")
        return False
    
    # بررسی requests
    try:
        import requests
        print("✅ requests")
    except ImportError:
        print("❌ requests نصب نشده است")
        return False
    
    return True

def install_ollama():
    """نصب Ollama"""
    print("\n📥 نصب Ollama...")
    
    system = platform.system().lower()
    
    if system == "windows":
        print("🪟 نصب برای Windows...")
        try:
            # استفاده از winget
            result = subprocess.run(['winget', 'install', 'Ollama.Ollama'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ Ollama نصب شد")
                return True
            else:
                print("❌ خطا در نصب با winget")
                print("💡 لطفاً دستی نصب کنید: https://ollama.ai/download")
                return False
        except:
            print("❌ خطا در نصب")
            print("💡 لطفاً دستی نصب کنید: https://ollama.ai/download")
            return False
    
    elif system == "linux":
        print("🐧 نصب برای Linux...")
        try:
            result = subprocess.run([
                'curl', '-fsSL', 'https://ollama.ai/install.sh'
            ], capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ Ollama نصب شد")
                return True
            else:
                print("❌ خطا در نصب")
                return False
        except:
            print("❌ خطا در نصب")
            return False
    
    elif system == "darwin":  # macOS
        print("🍎 نصب برای macOS...")
        try:
            result = subprocess.run(['brew', 'install', 'ollama'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ Ollama نصب شد")
                return True
            else:
                print("❌ خطا در نصب")
                return False
        except:
            print("❌ خطا در نصب")
            return False
    
    else:
        print(f"❌ سیستم عامل {system} پشتیبانی نمی‌شود")
        return False

def start_ollama_service():
    """راه‌اندازی سرویس Ollama"""
    print("\n🔄 راه‌اندازی سرویس Ollama...")
    
    try:
        # شروع سرویس
        subprocess.Popen(['ollama', 'serve'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # انتظار برای راه‌اندازی
        print("⏳ منتظر راه‌اندازی سرویس...")
        for i in range(15):
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
    print("\n📥 دانلود مدل Llama 3.2...")
    print("⏳ این فرآیند ممکن است چند دقیقه طول بکشد...")
    
    try:
        result = subprocess.run([
            'ollama', 'pull', 'llama3.2'
        ], capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ مدل Llama 3.2 دانلود شد!")
            return True
        else:
            print(f"❌ خطا در دانلود مدل: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ زمان دانلود مدل تمام شد")
        return False
    except Exception as e:
        print(f"❌ خطا در دانلود مدل: {e}")
        return False

def test_ollama():
    """تست Ollama"""
    print("\n🧪 تست Ollama...")
    
    try:
        # تست ساده
        result = subprocess.run([
            'ollama', 'run', 'llama3.2', 'سلام، چطوری؟'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Ollama به درستی کار می‌کند!")
            return True
        else:
            print(f"❌ خطا در تست: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ خطا در تست: {e}")
        return False

def run_django_tests():
    """اجرای تست‌های Django"""
    print("\n🧪 اجرای تست‌های Django...")
    
    try:
        # اجرای تست سیستم
        result = subprocess.run([
            sys.executable, 'test_ollama_system.py'
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ تست‌های Django موفق بودند!")
            return True
        else:
            print(f"❌ خطا در تست‌های Django: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ خطا در اجرای تست‌ها: {e}")
        return False

def main():
    """تابع اصلی"""
    print_header()
    
    # بررسی نیازمندی‌ها
    if not check_system_requirements():
        print("❌ نیازمندی‌های سیستم برآورده نشده‌اند")
        return False
    
    # بررسی نصب بودن Ollama
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ollama قبلاً نصب شده است")
        else:
            print("❌ Ollama نصب نشده است")
            if not install_ollama():
                print("❌ نصب Ollama ناموفق بود")
                return False
    except:
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
    
    # تست‌های Django
    if not run_django_tests():
        print("❌ تست‌های Django ناموفق بودند")
        return False
    
    print("\n🎉 سیستم تحلیل AI با موفقیت راه‌اندازی شد!")
    print("\n📋 دستورات مفید:")
    print("   ollama serve          # راه‌اندازی سرویس")
    print("   ollama list           # لیست مدل‌ها")
    print("   ollama run llama3.2   # اجرای مدل")
    print("   ollama stop           # توقف سرویس")
    print("\n🚀 سیستم آماده استفاده است!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
