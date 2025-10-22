from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from . import views
from .seo_views import sitemap_xml, robots_txt, sitemap_images, seo_analysis, seo_home, seo_features, seo_analytics_dashboard
from django.views.generic import TemplateView, RedirectView
from django.urls import re_path
from django.views.generic import RedirectView
from django.shortcuts import redirect
from django.urls import reverse

# NOTE: Deployment cache-buster: 2025-10-05T22:58 - urls synced
# Fallback to prevent import-time errors if an old build references verify_email_view
if not hasattr(views, 'verify_email_view'):
    def verify_email_view(request, user_id):
        return redirect('signup')

# NOTE: Deployment cache-buster: 2025-10-05T22:58 - urls synced
urlpatterns = [
    # صفحات اصلی
    path('', views.simple_home, name='home'),
    path('landing/', views.simple_home, name='landing'),
    path('about/', TemplateView.as_view(template_name='chidmano/about_minimal.html'), name='about'),
    path('guide/store-layout/', TemplateView.as_view(template_name='chidmano/guide_minimal.html'), name='store_layout_guide'),
    
    # اپ تحلیل فروشگاه
    path('store/', include('store_analysis.urls', namespace='store_analysis')),
    
    # احراز هویت
    path('accounts/', include([
        path('signup/', views.signup_view, name='signup'),
        # Email verification view removed
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
    path('sitemap.xml', sitemap_xml, name='sitemap'),
    path('sitemap-index.xml', sitemap_xml, name='sitemap_index'),
    path('sitemap-images.xml', sitemap_images, name='sitemap_images'),
    path('robots.txt', robots_txt, name='robots'),
    
    # صفحات SEO
    path('seo/analysis/<int:analysis_id>/', seo_analysis, name='seo_analysis'),
    path('seo/home/', seo_home, name='seo_home'),
    path('seo/features/', seo_features, name='seo_features'),
    path('seo/analytics/', seo_analytics_dashboard, name='seo_analytics'),
    path('37797489.txt', TemplateView.as_view(template_name='verification/37797489.txt', content_type='text/plain'), name='enamad_37797489'),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
    # Serve service worker at root to avoid 404 in some browsers
    re_path(r'^sw\.js$', RedirectView.as_view(url='/static/sw.js', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)