from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import os
import logging

logger = logging.getLogger(__name__)

def signup_view(request):
    """View for user registration"""
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'حساب کاربری شما با موفقیت ایجاد شد!')
                return redirect('store_analysis:user_dashboard')
            else:
                messages.error(request, 'خطا در ثبت‌نام. لطفاً اطلاعات را بررسی کنید.')
        else:
            form = UserCreationForm()
        
        return render(request, 'store_analysis/signup.html', {'form': form})
    except Exception as e:
        logger.error(f"Error in signup_view: {e}")
        messages.error(request, 'خطا در سیستم. لطفاً دوباره تلاش کنید.')
        return render(request, 'store_analysis/signup.html', {'form': UserCreationForm()})

def logout_view(request):
    """Custom logout view that handles GET requests"""
    logout(request)
    messages.success(request, 'شما با موفقیت از سیستم خارج شدید.')
    return redirect('home')

def simple_login_view(request):
    """Simple login view for testing"""
    try:
        if request.method == 'POST':
            from django.contrib.auth import authenticate, login
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if username and password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('store_analysis:user_dashboard')
                else:
                    messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
            else:
                messages.error(request, 'لطفاً همه فیلدها را پر کنید.')
        
        return render(request, 'store_analysis/login.html')
    except Exception as e:
        logger.error(f"Error in simple_login_view: {e}")
        return HttpResponse(f"Login error: {str(e)}", status=500)

def features_view(request):
    """Features page view"""
    return render(request, 'store_analysis/features.html')

def health_check(request):
    """Health check endpoint for Render deployment"""
    try:
        from django.db import connection
        from django.core.cache import cache
        
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Test cache
        cache.set('health_check', 'ok', 30)
        cache_status = cache.get('health_check') == 'ok'
        
        return JsonResponse({
            'status': 'healthy',
            'message': 'Chidemano is running',
            'database': 'connected',
            'cache': 'working' if cache_status else 'error',
            'timestamp': str(timezone.now())
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'message': f'Error: {str(e)}',
            'timestamp': str(timezone.now())
        }, status=500)

def dashboard_view(request):
    """Dashboard view"""
    return render(request, 'store_analysis/dashboard.html')

def simple_home(request):
    """صفحه اصلی فوق‌العاده جذاب و حرفه‌ای"""
    context = {
        'hero_title': 'تحلیل هوشمند فروشگاه شما',
        'hero_subtitle': 'با هوش مصنوعی پیشرفته، فروشگاه خود را به سطح جهانی برسانید',
        'features': [
            {
                'icon': '🚀',
                'title': 'تحلیل هوشمند',
                'description': 'با استفاده از هوش مصنوعی پیشرفته، فروشگاه شما را تحلیل می‌کنیم'
            },
            {
                'icon': '📊',
                'title': 'گزارش‌های جامع',
                'description': 'گزارش‌های کامل و دقیق از وضعیت فروشگاه شما'
            },
            {
                'icon': '💡',
                'title': 'توصیه‌های عملی',
                'description': 'راهکارهای عملی برای بهبود فروش و جذب مشتری'
            },
            {
                'icon': '🎯',
                'title': 'بهینه‌سازی',
                'description': 'بهینه‌سازی چیدمان و استراتژی فروش'
            }
        ],
        'stats': [
            {'number': '1000+', 'label': 'فروشگاه تحلیل شده'},
            {'number': '95%', 'label': 'رضایت مشتریان'},
            {'number': '50%', 'label': 'افزایش فروش'},
            {'number': '24/7', 'label': 'پشتیبانی'}
        ],
        'testimonials': [
            {
                'name': 'احمد محمدی',
                'role': 'مدیر فروشگاه',
                'text': 'بعد از تحلیل، فروش ما 60% افزایش یافت!',
                'rating': 5
            },
            {
                'name': 'فاطمه احمدی',
                'role': 'صاحب فروشگاه',
                'text': 'توصیه‌هایشان واقعاً عملی و مؤثر بود.',
                'rating': 5
            }
        ]
    }
    return render(request, 'chidmano/landing.html', context)

def store_analysis_home(request):
    """صفحه اصلی تحلیل فروشگاه - حذف شده و به صفحه اصلی جدید منتقل شده"""
    return redirect('home')

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
    """Safe home page - redirect to new professional home page"""
    return redirect('home')

def store_analysis_page(request):
    """Store analysis page - redirect to main store analysis form"""
    return redirect('store_analysis:forms') 