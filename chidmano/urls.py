from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from . import views
from django.http import HttpResponse
from django.views.generic import TemplateView

urlpatterns = [
    # صفحه اصلی حرفه‌ای
    path('', views.simple_home, name='home'),
    
    # مسیرهای اصلی store_analysis
    path('store/', include('store_analysis.urls', namespace='store_analysis')),
    
    # مسیرهای احراز هویت
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/verify-email/<int:user_id>/', views.verify_email_view, name='verify_email'),
    path('accounts/resend-code/<int:user_id>/', views.resend_verification_code, name='resend_verification_code'),
    path('accounts/login/', views.simple_login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='store_analysis/password_change.html',
        success_url='store_analysis:password_change_done'
    ), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='store_analysis/password_change_done.html'
    ), name='password_change_done'),
    path('accounts/password_reset/', lambda request: HttpResponse('بازیابی رمز عبور فعال نیست.'), name='password_reset'),
    
    # مسیرهای اضافی
    path('features/', views.features_view, name='features'),
    
    # مسیرهای ادمین
    path('admin/', admin.site.urls),
    
    # مسیرهای سیستم
    path('health/', views.health_check, name='health_check'),
    path('test/', views.test_page, name='test_page'),
    
    # SEO فایل‌ها
    path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml'), name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)