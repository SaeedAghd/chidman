from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings
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
# from store_analysis.models import EmailVerification
# from store_analysis.services.email_service import EmailVerificationService

logger = logging.getLogger(__name__)

def signup_view(request):
    """View for user registration with phone number requirement"""
    from store_analysis.forms import CustomUserCreationForm
    
    try:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            
            # لاگ کردن داده‌های دریافتی برای دیباگ
            logger.info(f"📥 Signup POST data: {request.POST}")
            
            if form.is_valid():
                try:
                    # فرم خودش UserProfile رو با شماره موبایل ایجاد می‌کنه
                    user = form.save()
                    
                    # ورود مستقیم
                    login(request, user)
                    messages.success(request, f'✅ حساب کاربری شما با موفقیت ایجاد شد! خوش آمدید {user.get_full_name() or user.username}!')
                    
                    # redirect به صفحه محصولات
                    return redirect('store_analysis:products')
                except Exception as e:
                    logger.error(f"❌ Error during user creation: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    messages.error(request, f'خطا در ایجاد حساب کاربری: {str(e)}')
                    return render(request, 'store_analysis/signup.html', {'form': form})
            else:
                # لاگ کردن خطاهای فرم
                logger.error(f"❌ Form validation errors: {form.errors}")
                logger.error(f"❌ Form data: {form.data}")
                
                # نمایش خطاهای فرم
                for field, errors in form.errors.items():
                    field_label = form.fields.get(field).label if field in form.fields else field
                    for error in errors:
                        messages.error(request, f'{field_label}: {error}')
                return render(request, 'store_analysis/signup.html', {'form': form})
        else:
            form = CustomUserCreationForm()
            return render(request, 'store_analysis/signup.html', {'form': form})
    except Exception as e:
        logger.error(f"Error in signup_view: {e}")
        import traceback
        logger.error(traceback.format_exc())
        messages.error(request, 'خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.')
        return render(request, 'store_analysis/signup.html', {'form': CustomUserCreationForm()})

def verify_email_view(request, user_id):
    """Fallback view: email verification is disabled; prevent server error."""
    try:
        messages.info(request, 'تایید ایمیل در حال حاضر غیرفعال است.')
    except Exception:
        pass
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
                        # اگر قبلا در سشن تعهدنامه تایید شده بود، آن را به DB منتقل کن
                        try:
                            if request.session.get('legal_agreement_accepted', False):
                                from store_analysis.models import UserProfile
                                profile, created = UserProfile.objects.get_or_create(
                                    user=user,
                                    defaults={'legal_agreement_accepted': True}
                                )
                                if not created and not profile.legal_agreement_accepted:
                                    profile.legal_agreement_accepted = True
                                    profile.save()
                        except Exception:
                            pass
                        messages.success(request, f'خوش آمدید {user.username}!')
                        
                        # بررسی analysis_id در session (برای redirect بعد از پرداخت)
                        # اول pending_analysis_id را بررسی کن (backup)
                        analysis_id = request.session.get('pending_analysis_id') or request.session.get('analysis_id')
                        if analysis_id:
                            # اگر analysis_id در session موجود است، به forms redirect کن
                            from django.urls import reverse
                            # پاک کردن از session بعد از استفاده
                            if 'pending_analysis_id' in request.session:
                                del request.session['pending_analysis_id']
                            if 'analysis_id' in request.session:
                                del request.session['analysis_id']
                            logger.info(f"🔐 Redirecting to forms after login: analysis_id={analysis_id}")
                            return redirect('store_analysis:forms', analysis_id=analysis_id)
                        
                        # استفاده از next parameter اگر موجود باشد
                        next_url = request.GET.get('next') or request.POST.get('next')
                        if next_url:
                            # بررسی امنیت: مطمئن شو که URL به دامنه خودمان است
                            from django.urls import resolve
                            from django.http import HttpResponseRedirect
                            try:
                                # بررسی اینکه آیا URL به دامنه خودمان است
                                if next_url.startswith('/') or next_url.startswith(request.build_absolute_uri('/')):
                                    return HttpResponseRedirect(next_url)
                            except:
                                pass
                        
                        # اگر next موجود نبود یا نامعتبر بود، به dashboard برو
                        return redirect('store_analysis:user_dashboard')
                    else:
                        messages.error(request, 'حساب کاربری شما فعال نیست. لطفاً ابتدا ایمیل خود را تایید کنید.')
                else:
                    messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
            else:
                messages.error(request, 'لطفاً همه فیلدها را پر کنید.')

        return render(request, 'store_analysis/login.html', {'form': None})
    except Exception as e:
        logger.error(f"Error in simple_login_view: {e}")
        messages.error(request, 'خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.')
        return render(request, 'store_analysis/login.html', {'form': None})

def features_view(request):
    """Features page view"""
    return render(request, 'store_analysis/features.html')

# --- Diagnostics & Bootstrap (temporary, token-protected) ---
def debug_db_status(request):
    """Return minimal DB status for diagnostics."""
    try:
        from django.contrib.auth.models import User
        total_users = User.objects.count()
        engine = settings.DATABASES['default']['ENGINE']
        return JsonResponse({
            'ok': True,
            'engine': engine,
            'users': total_users,
            'session_key': request.session.session_key,
        })
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)})

def bootstrap_admin(request, token: str):
    """Create/reset admin user securely using a one-time token from env."""
    expected = os.getenv('SETUP_TOKEN')
    if not expected or token != expected:
        return JsonResponse({'ok': False, 'error': 'unauthorized'}, status=401)
    from django.contrib.auth.models import User
    username = os.getenv('SETUP_USERNAME', 'saeed')
    password = os.getenv('SETUP_PASSWORD', '123456')
    email = os.getenv('SETUP_EMAIL', 'admin@example.com')
    user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True, 'is_active': True})
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.email = email
    user.set_password(password)
    user.save()
    return JsonResponse({'ok': True, 'created': created, 'username': username})

def health_check(request):
    """Health check endpoint for Liara deployment - Ultra lightweight"""
    return HttpResponse('OK', content_type='text/plain')

def dashboard_view(request):
    """Dashboard view"""
    return render(request, 'store_analysis/dashboard.html')

def simple_home(request):
    """صفحه اصلی فوق‌العاده جذاب و حرفه‌ای"""
    import time
    from django.core.cache import cache
    from datetime import datetime
    
    # تخفیف افتتاحیه - هاردکد شده (بدون نیاز به دیتابیس)
    current_date = datetime.now()
    launch_end_date = datetime(2025, 12, 31)  # تا پایان سال 2025
    
    # محاسبه تخفیف افتتاحیه
    if current_date <= launch_end_date:
        discount_info = {
            'has_discount': True,
            'discount_percentage': 80,
            'discount_title': 'تخفیف ویژه افتتاحیه 80%',
            'discount_message': '🎉 فرصت طلایی! تحلیل فروشگاه شما با تخفیف ۸۰٪ افتتاحیه. همین حالا سفارش دهید!',
            'discount_type': 'opening',
            'discount_end_date': launch_end_date
        }
    else:
        discount_info = {
            'has_discount': False,
            'discount_percentage': 0,
            'discount_title': '',
            'discount_message': '',
            'discount_type': 'none',
            'discount_end_date': None
        }
    
    # دریافت تنظیمات سیستم از cache
    saved_settings = cache.get('admin_settings', {})
    
    # مقادیر واقعی - اطلاعات تماس چیدمانو
    site_name = saved_settings.get('site_name', 'چیدمانو')
    contact_phone = saved_settings.get('contact_phone', '0920-2658678')
    support_email = saved_settings.get('support_email', 'info@chidmano.ir')
    address = saved_settings.get('address', 'البرز - کرج - بلوار موذن')
    
    context = {
        'hero_title': 'تحلیل هوشمند فروشگاه شما',
        'hero_subtitle': 'با هوش مصنوعی پیشرفته، فروشگاه خود را به سطح جهانی برسانید',
        'discount_info': discount_info,
        'site_name': site_name,
        'contact_phone': contact_phone,
        'support_email': support_email,
        'address': address,
        'timestamp': int(time.time()),  # Cache busting timestamp
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
    # attach active service packages so templates use dynamic prices instead of hardcoded ones
    try:
        from store_analysis.models import ServicePackage
        packages = list(ServicePackage.objects.filter(is_active=True).order_by('sort_order', 'price'))
        context['packages'] = packages
        context['featured_package'] = packages[0] if packages else None
        if context.get('featured_package'):
            pkg = context['featured_package']
            discount_pct = context.get('discount_info', {}).get('discount_percentage', 0)
            try:
                discounted = float(pkg.price) * (1 - float(discount_pct) / 100.0)
            except Exception:
                discounted = float(pkg.price)
            context['featured_package_discounted_price'] = int(discounted)
    except Exception:
        context.setdefault('packages', [])
        context.setdefault('featured_package', None)
        context.setdefault('featured_package_discounted_price', None)

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

def store_layout_guide(request):
    """Store layout guide page"""
    return render(request, 'chidmano/store_layout_guide.html')

def supermarket_layout_guide(request):
    """Supermarket layout guide page"""
    return render(request, 'chidmano/supermarket_layout_guide.html')

def storefront_lighting_guide(request):
    """Storefront lighting guide page"""
    return render(request, 'chidmano/storefront_lighting_guide.html')

def store_layout_pillar(request):
    """Main pillar page for store layout - comprehensive guide"""
    return render(request, 'chidmano/store_layout_pillar.html')

def color_psychology_guide(request):
    """Color psychology guide page"""
    return render(request, 'chidmano/color_psychology_guide.html')

def customer_journey_guide(request):
    """Customer journey guide page"""
    return render(request, 'chidmano/customer_journey_guide.html')

def lighting_design_guide(request):
    """Lighting design guide page"""
    return render(request, 'chidmano/lighting_design_guide.html')

def home_appliances_guide(request):
    """Home appliances store layout guide page"""
    return render(request, 'chidmano/home_appliances_guide.html')

def fruit_store_guide(request):
    """Fruit store layout guide page"""
    return render(request, 'chidmano/fruit_store_guide.html')

def cosmetics_store_guide(request):
    """Cosmetics and beauty store layout guide page"""
    return render(request, 'chidmano/cosmetics_store_guide.html')

def case_studies(request):
    """Case studies page"""
    return render(request, 'chidmano/case_studies.html')

def partnership(request):
    """Partnership page"""
    return render(request, 'chidmano/partnership.html')

def admin_dashboard(request):
    """داشبورد یکپارچه و حرفه‌ای ادمین"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin:login')
    
    from .models import BlogPost, SEOKeyword, SEOMetrics
    from django.db.models import Count, Sum, Avg
    from django.utils import timezone
    from datetime import timedelta
    
    # تعیین تب فعال
    active_tab = request.GET.get('tab', 'overview')
    
    # آمار کلی
    total_posts = BlogPost.objects.filter(published=True).count()
    total_keywords = SEOKeyword.objects.filter(is_active=True).count()
    
    # آمار هفته گذشته
    week_ago = timezone.now() - timedelta(days=7)
    recent_posts = BlogPost.objects.filter(
        published=True, 
        created_at__gte=week_ago
    ).count()
    
    # آخرین متریک‌ها
    latest_metrics = SEOMetrics.objects.order_by('-date').first()
    
    # متریک‌های SEO
    avg_metrics = SEOMetrics.objects.aggregate(
        avg_traffic=Avg('organic_traffic'),
        avg_keywords=Avg('keyword_rankings'),
        avg_speed=Avg('page_speed_score'),
        avg_backlinks=Avg('backlinks_count'),
        avg_authority=Avg('domain_authority')
    )
    
    # کلمات کلیدی برتر
    top_keywords = SEOKeyword.objects.filter(
        is_active=True
    ).order_by('-search_volume')[:10]
    
    # مقالات اخیر
    recent_blog_posts = BlogPost.objects.filter(
        published=True
    ).order_by('-created_at')[:5]
    
    # گزارش هفته گذشته
    weekly_metrics = SEOMetrics.objects.filter(
        date__gte=week_ago
    ).aggregate(
        total_traffic=Sum('organic_traffic'),
        avg_speed=Avg('page_speed_score'),
        avg_keywords=Avg('keyword_rankings')
    )
    
    # گزارش ماه گذشته
    month_ago = timezone.now() - timedelta(days=30)
    monthly_metrics = SEOMetrics.objects.filter(
        date__gte=month_ago
    ).aggregate(
        total_traffic=Sum('organic_traffic'),
        avg_speed=Avg('page_speed_score'),
        avg_keywords=Avg('keyword_rankings')
    )
    
    context = {
        'active_tab': active_tab,
        'total_posts': total_posts,
        'total_keywords': total_keywords,
        'recent_posts': recent_posts,
        'latest_metrics': latest_metrics,
        'avg_metrics': avg_metrics,
        'top_keywords': top_keywords,
        'recent_blog_posts': recent_blog_posts,
        'weekly_metrics': weekly_metrics,
        'monthly_metrics': monthly_metrics,
        'user': request.user,
    }
    
    return render(request, 'chidmano/admin/dashboard.html', context)

