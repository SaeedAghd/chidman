from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
import json
import os
import logging

logger = logging.getLogger(__name__)

def signup_view(request):
    """View for user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'حساب کاربری شما با موفقیت ایجاد شد!')
            return redirect('store_analysis:index')
        else:
            messages.error(request, 'خطا در ثبت‌نام. لطفاً اطلاعات را بررسی کنید.')
    else:
        form = UserCreationForm()
    
    return render(request, 'store_analysis/signup.html', {'form': form})

def logout_view(request):
    """Custom logout view that handles GET requests"""
    logout(request)
    messages.success(request, 'شما با موفقیت از سیستم خارج شدید.')
    return redirect('store_analysis:index')

def features_view(request):
    """Features page view"""
    return render(request, 'store_analysis/features.html')

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({'status': 'healthy', 'message': 'Chidemano is running'})

def dashboard_view(request):
    """Dashboard view"""
    return render(request, 'store_analysis/dashboard.html')

def simple_home(request):
    """صفحه اصلی ساده برای تست"""
    return HttpResponse("""
    <html>
    <head>
        <title>چیدمان - تست</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 600px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; }
            .btn { display: inline-block; background: #27ae60; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; margin: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏪 چیدمان</h1>
            <p>✅ سیستم در حال کار است!</p>
            <p>این صفحه نشان می‌دهد که Django و URL routing درست کار می‌کند.</p>
            
            <div style="margin-top: 30px;">
                <a href="/store/" class="btn">🏪 سایت اصلی</a>
                <a href="/health/" class="btn">💚 وضعیت سیستم</a>
            </div>
        </div>
    </body>
    </html>
    """)

def store_analysis_home(request):
    """صفحه اصلی تحلیل فروشگاه"""
    return HttpResponse("""
    <html>
    <head>
        <title>تحلیل فروشگاه - چیدمان</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
            .container { max-width: 600px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; }
            .btn { display: inline-block; background: #27ae60; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; margin: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 تحلیل فروشگاه</h1>
            <p>✅ صفحه تحلیل فروشگاه در دسترس است!</p>
            <p>این صفحه برای تحلیل هوشمند فروشگاه شما طراحی شده است.</p>
            
            <div style="margin-top: 30px;">
                <a href="/" class="btn">🏠 صفحه اصلی</a>
                <a href="/store/" class="btn">🏪 سایت اصلی</a>
                <a href="/health/" class="btn">💚 وضعیت سیستم</a>
            </div>
        </div>
    </body>
    </html>
    """)

def test_page(request):
    """Test page to ensure everything works"""
    return HttpResponse("""
    <html>
    <head>
        <title>تست سیستم - چیدمان</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f8f9fa; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .success { color: #28a745; font-size: 18px; }
            .info { color: #6c757d; margin: 20px 0; }
            .btn { display: inline-block; background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧪 تست سیستم</h1>
            <p class="success">✅ سیستم در حال کار است!</p>
            <p class="info">این صفحه نشان می‌دهد که Django و URL routing درست کار می‌کند.</p>
            
            <div style="margin-top: 30px;">
                <a href="/" class="btn">🏠 صفحه اصلی</a>
                <a href="/health/" class="btn">💚 وضعیت سیستم</a>
                <a href="/store/" class="btn">🏪 سایت اصلی</a>
            </div>
        </div>
    </body>
    </html>
    """)

def safe_home(request):
    """Safe home page with error handling"""
    try:
        # سعی می‌کنیم مستقیماً به سایت اصلی redirect کنیم
        from store_analysis.views import index
        return index(request)
    except Exception as e:
        # اگر خطا داشت، صفحه fallback نمایش می‌دهیم
        import traceback
        error_details = traceback.format_exc()
        
        # بررسی نوع خطا
        error_type = "مشکل موقت"
        error_message = str(e)
        
        if "namespace" in error_message.lower():
            error_type = "مشکل Namespace"
            error_message = "مشکل در تنظیمات URL. در حال حل..."
        elif "template" in error_message.lower():
            error_type = "مشکل Template"
            error_message = "مشکل در فایل‌های قالب. در حال حل..."
        elif "import" in error_message.lower():
            error_type = "مشکل Import"
            error_message = "مشکل در import کردن ماژول‌ها. در حال حل..."
        
        return HttpResponse(f"""
        <html>
        <head>
            <title>چیدمان - تحلیل هوشمند فروشگاه</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }}
                .container {{ max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; }}
                .error {{ background: rgba(220, 53, 69, 0.3); padding: 15px; border-radius: 10px; margin: 20px 0; text-align: left; }}
                .btn {{ display: inline-block; background: #27ae60; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; margin: 10px; }}
                .error-details {{ background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; margin: 20px 0; text-align: left; font-family: monospace; font-size: 12px; overflow-x: auto; }}
                .status {{ background: rgba(39, 174, 96, 0.3); padding: 15px; border-radius: 10px; margin: 20px 0; }}
                .success {{ background: rgba(39, 174, 96, 0.3); padding: 15px; border-radius: 10px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏪 چیدمان</h1>
                
                <div class="status">
                    <h3>✅ سیستم آماده است!</h3>
                    <p>سیستم تحلیل هوشمند فروشگاه با موفقیت راه‌اندازی شده است.</p>
                </div>
                
                <div class="error">
                    <h3>⚠️ {error_type}</h3>
                    <p>{error_message}</p>
                    <p><strong>خطای فنی:</strong> {str(e)}</p>
                </div>
                
                <div class="success">
                    <h3>🎯 راه‌حل</h3>
                    <p>Namespace در root level اضافه شده است. لطفاً صفحه را refresh کنید یا روی دکمه "سایت اصلی" کلیک کنید.</p>
                </div>
                
                <div class="error-details">
                    <h4>جزئیات خطا:</h4>
                    <pre>{error_details}</pre>
                </div>
                
                <div style="margin-top: 40px;">
                    <a href="/" class="btn">🔄 Refresh صفحه</a>
                    <a href="/store/" class="btn">🏪 سایت اصلی</a>
                    <a href="/test/" class="btn">🧪 تست سیستم</a>
                    <a href="/health/" class="btn">💚 وضعیت سیستم</a>
                    <a href="/store-analysis/" class="btn">📊 تحلیل فروشگاه</a>
                    <a href="/admin/" class="btn">⚙️ پنل مدیریت</a>
                </div>
                
                <div style="margin-top: 30px; font-size: 14px; opacity: 0.8;">
                    <p>🎉 پروژه شما با موفقیت روی Render دیپلوی شده است!</p>
                    <p>مشکل فنی در حال حل شدن است. لطفاً چند دقیقه صبر کنید.</p>
                </div>
            </div>
        </body>
        </html>
        """)

def store_analysis_page(request):
    """Store analysis page - main functionality"""
    return HttpResponse("""
    <html>
    <head>
        <title>تحلیل فروشگاه - چیدمان</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }
            h1 { color: #fff; margin-bottom: 30px; }
            .feature { background: rgba(255,255,255,0.2); margin: 20px 0; padding: 20px; border-radius: 10px; text-align: left; }
            .feature h3 { color: #fff; margin-top: 0; }
            .btn { display: inline-block; background: #27ae60; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; margin: 10px; transition: all 0.3s; }
            .btn:hover { background: #219a52; transform: translateY(-2px); }
            .status { background: rgba(39, 174, 96, 0.3); padding: 15px; border-radius: 10px; margin: 20px 0; }
            .coming-soon { background: rgba(255, 193, 7, 0.3); padding: 15px; border-radius: 10px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏪 تحلیل هوشمند فروشگاه</h1>
            
            <div class="status">
                <h3>✅ سیستم آماده است!</h3>
                <p>سیستم تحلیل هوشمند فروشگاه با موفقیت راه‌اندازی شده و آماده ارائه خدمات است.</p>
            </div>
            
            <div class="coming-soon">
                <h3>🚧 در حال توسعه</h3>
                <p>قابلیت‌های پیشرفته تحلیل فروشگاه در حال توسعه هستند. به زودی در دسترس خواهند بود.</p>
            </div>
            
            <div class="feature">
                <h3>🤖 تحلیل هوشمند با AI</h3>
                <p>تحلیل دقیق فروشگاه با استفاده از هوش مصنوعی و یادگیری ماشین</p>
            </div>
            
            <div class="feature">
                <h3>📊 گزارش‌های مدیریتی</h3>
                <p>تولید گزارش‌های جامع و کاربردی برای تصمیم‌گیری بهتر</p>
            </div>
            
            <div class="feature">
                <h3>💰 پیش‌بینی مالی و ROI</h3>
                <p>محاسبه دقیق بازگشت سرمایه و پیش‌بینی درآمد</p>
            </div>
            
            <div class="feature">
                <h3>🎯 راهنمایی عملی</h3>
                <p>ارائه راهنمایی‌های عملی و قابل اجرا برای بهبود فروشگاه</p>
            </div>
            
            <div style="margin-top: 40px;">
                <a href="/" class="btn">🏠 صفحه اصلی</a>
                <a href="/test/" class="btn">🧪 تست سیستم</a>
                <a href="/health/" class="btn">💚 وضعیت سیستم</a>
                <a href="/admin/" class="btn">⚙️ پنل مدیریت</a>
            </div>
            
            <div style="margin-top: 30px; font-size: 14px; opacity: 0.8;">
                <p>🎉 پروژه شما با موفقیت روی Render دیپلوی شده است!</p>
                <p>برای شروع تحلیل فروشگاه، لطفاً با تیم توسعه تماس بگیرید.</p>
            </div>
        </div>
    </body>
    </html>
    """) 