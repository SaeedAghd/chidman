from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from . import views
from django.http import HttpResponse
from store_analysis.admin_dashboard import admin_dashboard

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # اضافه شده برای تغییر زبان
    
    # صفحه تست برای اطمینان از کارکرد
    path('test/', views.test_page, name='test_page'),
    
    # مسیر اصلی با error handling
    path('', views.safe_home, name='safe_home'),
    
    # مسیرهای store_analysis با error handling
    path('store/', include('store_analysis.urls')),  # مسیر اصلی - با prefix
    
    path('admin/', admin.site.urls),
    path('accounts/signup/', views.signup_view, name='signup'),  # اضافه شده
    path('accounts/login/', auth_views.LoginView.as_view(template_name='store_analysis/login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='store_analysis/password_change.html',
        success_url='store_analysis:password_change_done'
    ), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='store_analysis/password_change_done.html'
    ), name='password_change_done'),
    path('accounts/password_reset/', lambda request: HttpResponse('بازیابی رمز عبور فعال نیست.'), name='password_reset'),
    path('store-analysis/features/', views.features_view, name='features'),
    path('health/', views.health_check, name='health_check'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)