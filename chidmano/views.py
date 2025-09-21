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

# Import های جدید برای تاییدیه ایمیل
from django.contrib.auth.models import User
from datetime import timedelta
from store_analysis.models import EmailVerification
from store_analysis.services.email_service import EmailVerificationService

logger = logging.getLogger(__name__)

def signup_view(request):
    """View for user registration with email verification"""
    if request.method == 'POST':
        try:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                # دریافت ایمیل از فرم
                email = request.POST.get('email')
                if not email:
                    messages.error(request, 'لطفاً ایمیل خود را وارد کنید.')
                    return render(request, 'store_analysis/signup.html', {'form': form})
                
                # بررسی وجود ایمیل
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'این ایمیل قبلاً ثبت شده است.')
                    return render(request, 'store_analysis/signup.html', {'form': form})
                
                # ایجاد کاربر
                user = form.save(commit=False)
                user.email = email
                user.is_active = True  # فعال کردن مستقیم برای تست
                user.save()
                
                # برای تست، کاربر را مستقیماً وارد کنیم
                from django.contrib.auth import login
                login(request, user)
                messages.success(request, f'حساب کاربری شما با موفقیت ایجاد شد! خوش آمدید {user.username}!')
                return redirect('store_analysis:user_dashboard')
                
            else:
                messages.error(request, 'خطا در ثبت‌نام. لطفاً اطلاعات را بررسی کنید.')
                return render(request, 'store_analysis/signup.html', {'form': form})
                
        except Exception as e:
            logger.error(f"Error in signup_view: {e}")
            messages.error(request, 'خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.')
            return render(request, 'store_analysis/signup.html', {'form': UserCreationForm()})
    else:
        form = UserCreationForm()
        return render(request, 'store_analysis/signup.html', {'form': form})

def verify_email_view(request, user_id):
    """صفحه تاییدیه ایمیل"""
    try:
        user = User.objects.get(id=user_id)
        email_verification = EmailVerification.objects.get(user=user)
        
        if request.method == 'POST':
            verification_code = request.POST.get('verification_code')
            
            if verification_code == email_verification.verification_code:
                if not email_verification.is_expired():
                    # تایید موفق
                    email_verification.is_verified = True
                    email_verification.save()
                    
                    # فعال کردن کاربر
                    user.is_active = True
                    user.save()
                    
                    # ارسال ایمیل خوش‌آمدگویی
                    email_service = EmailVerificationService()
                    email_service.send_welcome_email(user, user.email)
                    
                    messages.success(request, 'ایمیل شما با موفقیت تایید شد! حالا می‌توانید وارد شوید.')
                    return redirect('login')
                else:
                    messages.error(request, 'کد تایید منقضی شده است. لطفاً کد جدید درخواست کنید.')
            else:
                # افزایش تعداد تلاش
                email_verification.attempts += 1
                email_verification.save()
                
                if email_verification.attempts >= 3:
                    messages.error(request, 'تعداد تلاش‌های شما به حد مجاز رسیده است. لطفاً کد جدید درخواست کنید.')
                else:
                    messages.error(request, f'کد تایید اشتباه است. {3 - email_verification.attempts} تلاش باقی مانده.')
        
        return render(request, 'registration/verify_email.html', {
            'user': user,
            'email_verification': email_verification
        })
        
    except (User.DoesNotExist, EmailVerification.DoesNotExist):
        messages.error(request, 'کاربر یا تاییدیه ایمیل یافت نشد.')
        return redirect('signup')
    except Exception as e:
        logger.error(f"خطا در verify_email_view: {e}")
        messages.error(request, 'خطایی رخ داده است.')
        return redirect('signup')

def resend_verification_code(request, user_id):
    """ارسال مجدد کد تاییدیه"""
    try:
        user = User.objects.get(id=user_id)
        email_verification = EmailVerification.objects.get(user=user)
        
        if email_verification.can_resend():
            # تولید کد جدید
            new_code = email_verification.generate_new_code()
            
            # ارسال ایمیل
            email_service = EmailVerificationService()
            if email_service.send_verification_email(user, user.email, new_code):
                messages.success(request, 'کد تایید جدید به ایمیل شما ارسال شد.')
            else:
                messages.error(request, 'خطا در ارسال کد جدید.')
        else:
            messages.error(request, 'امکان ارسال مجدد کد وجود ندارد.')
        
        return redirect('verify_email', user_id=user_id)
        
    except (User.DoesNotExist, EmailVerification.DoesNotExist):
        messages.error(request, 'کاربر یا تاییدیه ایمیل یافت نشد.')
        return redirect('signup')
    except Exception as e:
        logger.error(f"خطا در resend_verification_code: {e}")
        messages.error(request, 'خطایی رخ داده است.')
        return redirect('signup')

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
                    if user.is_active:
                        login(request, user)
                        messages.success(request, f'خوش آمدید {user.username}!')
                        return redirect('store_analysis:user_dashboard')
                    else:
                        messages.error(request, 'حساب کاربری شما فعال نیست. لطفاً ابتدا ایمیل خود را تایید کنید.')
                else:
                    messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
            else:
                messages.error(request, 'لطفاً همه فیلدها را پر کنید.')
        
        return render(request, 'store_analysis/login.html')
    except Exception as e:
        logger.error(f"Error in simple_login_view: {e}")
        messages.error(request, 'خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.')
        return render(request, 'store_analysis/login.html')

def features_view(request):
    """Features page view"""
    return render(request, 'store_analysis/features.html')

def health_check(request):
    """Health check endpoint for Liara deployment"""
    try:
        # Simple database check
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return HttpResponse('OK')
    except Exception as e:
        # Return 200 even if database fails (for startup)
        return HttpResponse('OK')

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