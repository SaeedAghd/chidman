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
    """Simple home page for testing"""
    return HttpResponse("""
    <html>
    <head>
        <title>چیدمان - تحلیل هوشمند فروشگاه</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            h1 { color: #2c3e50; }
            p { color: #7f8c8d; }
            .success { color: #27ae60; }
        </style>
    </head>
    <body>
        <h1>🏪 چیدمان</h1>
        <p class="success">✅ سیستم تحلیل هوشمند فروشگاه با موفقیت راه‌اندازی شد!</p>
        <p>🎉 پروژه شما روی Render دیپلوی شده و آماده استفاده است.</p>
        <p>📊 قابلیت‌های موجود:</p>
        <ul style="text-align: left; display: inline-block;">
            <li>تحلیل هوشمند فروشگاه با AI</li>
            <li>تولید گزارش‌های مدیریتی</li>
            <li>پیش‌بینی مالی و ROI</li>
            <li>راهنمایی عملی برای بهبود</li>
            <li>ربات مشاور هوش مصنوعی</li>
        </ul>
        <p><a href="/store-analysis/">شروع تحلیل فروشگاه</a></p>
    </body>
    </html>
    """) 