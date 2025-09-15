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
            return redirect('store_analysis:user_dashboard')
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

def landing_page(request):
    """Apple-style landing page"""
    return render(request, 'store_analysis/landing_page.html') 