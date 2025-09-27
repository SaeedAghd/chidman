from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from . import views
# from .seo_views import sitemap_xml, robots_txt
from django.views.generic import TemplateView, RedirectView
from django.urls import re_path

urlpatterns = [
    # صفحه اصلی
    path('', views.simple_home, name='home'),
    path('landing/', views.simple_home, name='landing'),
    
    # اپ تحلیل فروشگاه
    path('store/', include('store_analysis.urls', namespace='store_analysis')),
    
    # احراز هویت
    path('accounts/', include([
        path('signup/', views.signup_view, name='signup'),
        path('verify-email/<int:user_id>/', views.verify_email_view, name='verify_email'),
        path('resend-code/<int:user_id>/', views.resend_verification_code, name='resend_verification_code'),
        path('login/', views.simple_login_view, name='login'),
        path('logout/', views.logout_view, name='logout'),
        path('password_change/', auth_views.PasswordChangeView.as_view(
            template_name='store_analysis/password_change.html',
            success_url='store_analysis:password_change_done'
        ), name='password_change'),
        path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
            template_name='store_analysis/password_change_done.html'
        ), name='password_change_done'),
        path('password_reset/', lambda request: HttpResponse('بازیابی رمز عبور فعال نیست.'), name='password_reset'),
    ])),
    
    # ویژگی‌ها
    path('features/', views.features_view, name='features'),
    
    # راهنماهای SEO
    path('guide/', include([
        path('store-layout/', views.store_layout_guide, name='store_layout_guide'),
        path('supermarket-layout/', views.supermarket_layout_guide, name='supermarket_layout_guide'),
        path('storefront-lighting/', views.storefront_lighting_guide, name='storefront_lighting_guide'),
        path('color-psychology/', views.color_psychology_guide, name='color_psychology_guide'),
        path('customer-journey/', views.customer_journey_guide, name='customer_journey_guide'),
        path('lighting-design/', views.lighting_design_guide, name='lighting_design_guide'),
    ])),
    
    # صفحات محتوا
    path('چیدمان-فروشگاه/', views.store_layout_pillar, name='store_layout_pillar'),
    path('case-studies/', views.case_studies, name='case_studies'),
    path('partnership/', views.partnership, name='partnership'),
    # path('seo-dashboard/', views.seo_dashboard, name='seo_dashboard'),
    
    # ادمین
    path('admin/', include([
        path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
        path('', admin.site.urls),
    ])),
    
    # سیستم و دیباگ
    path('test/', views.test_page, name='test_page'),
    path('debug/db/', views.debug_db_status, name='debug_db_status'),
    re_path(r'^bootstrap-admin/(?P<token>[^/]+)/$', views.bootstrap_admin, name='bootstrap_admin'),
    
    # فایل‌های SEO
    # path('sitemap.xml', sitemap_xml, name='sitemap'),
    # path('robots.txt', robots_txt, name='robots'),
    path('37797489.txt', TemplateView.as_view(template_name='verification/37797489.txt', content_type='text/plain'), name='enamad_37797489'),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)