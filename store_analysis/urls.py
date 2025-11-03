from django.urls import path, include
from . import views
from . import payment_views
from . import chat_views
from django.http import HttpResponse
from django.views.generic import RedirectView

app_name = 'store_analysis'

def health(request):
    return HttpResponse("OK")

urlpatterns = [
    # صفحه اصلی
    path('', views.index, name='index'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/cleanup/', views.delete_incomplete_analyses, name='delete_incomplete_analyses'),
    
    # محصولات و خرید
    path('products/', views.products_page, name='products'),
    path('buy/basic/', views.buy_basic, name='buy_basic'),
    path('buy/complete/', views.buy_complete, name='buy_complete'),
    path('buy/advanced/', views.buy_advanced, name='buy_advanced'),
    
    # فرم‌ها و تحلیل
    path('forms/', views.store_analysis_form, name='forms'),
    path('forms/<int:analysis_id>/', views.store_analysis_form, name='forms'),
    path('forms/submit/', views.forms_submit, name='forms_submit'),
    path('check-legal-agreement/', views.check_legal_agreement, name='check_legal_agreement'),
    path('accept-legal-agreement/', views.accept_legal_agreement, name='accept_legal_agreement'),
    
    # مدیریت تحلیل‌ها - فقط توابع اصلی
    path('analysis/', include([
        path('create/', views.analysis_create, name='analysis_create'),
        path('list/', views.analysis_list, name='analysis_list'),
        path('<int:pk>/results/', views.analysis_results, name='analysis_results'),
        path('<int:pk>/download/', views.download_analysis_report, name='download_analysis'),
        path('<int:pk>/view-report/', views.view_analysis_report, name='view_analysis_report'),
        path('<int:pk>/progress/', views.analysis_progress, name='analysis_progress'),
        path('<int:pk>/start/', views.start_analysis, name='start_analysis'),
        path('<int:pk>/status/', views.get_analysis_status, name='get_analysis_status'),
        path('<int:pk>/process/', views.admin_process_analysis, name='admin_process_analysis'),
        
        # AI Consultant (چت‌بات هوشمند)
        path('<str:analysis_id>/chat/', chat_views.ai_consultant_chat, name='ai_consultant_chat'),
        path('<str:analysis_id>/chat/send/', chat_views.ai_consultant_send, name='ai_consultant_send'),
    ])),
    
    # پشتیبانی - فقط توابع اصلی
        path('support/', include([
        path('', views.support_center, name='support_center'),
        path('ticket/create/', views.create_ticket, name='create_ticket'),
        path('tickets/', views.ticket_list, name='ticket_list'),
        path('tickets/<str:ticket_id>/', views.ticket_detail, name='ticket_detail'),
        path('faq/search/', views.faq_search, name='faq_search'),
    ])),
    
    # آموزش - فقط توابع اصلی
    path('education/', include([
        path('', views.education_library, name='education_library'),
        path('ai-guide/', views.ai_analysis_guide, name='ai_analysis_guide'),
    ])),
    
    # ویژگی‌ها
    path('features/', views.features, name='features'),
    
    # URL های اصلی
    path('payment/<str:order_id>/', views.payment_page, name='payment_page'),
    path('payment/<str:order_id>/payping/', views.payping_payment, name='payping_payment'),
    path('payment/<str:order_id>/process/', views.process_payment, name='process_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('store-comparison/', views.store_comparison, name='store_comparison'),
    path('ai-consultant/', views.ai_consultant_list, name='ai_consultant_list'),
    path('ai-consultant/<int:analysis_id>/', views.ai_consultant, name='ai_consultant'),
    
    # مدیریت ادمین - فقط توابع اصلی
    path('admin/', include([
        path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
        path('users/', views.admin_users, name='admin_users'),
        path('users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
        path('analyses/', views.admin_analyses, name='admin_analyses'),
        path('analyses/<str:analysis_id>/', views.admin_analysis_detail, name='admin_analysis_detail'),
        path('analyses/<str:analysis_id>/delete/', views.admin_delete_analysis, name='admin_delete_analysis'),
        path('orders/', views.admin_orders, name='admin_orders'),
        path('orders/<str:order_id>/', views.admin_order_detail, name='admin_order_detail'),
        path('tickets/', views.admin_tickets, name='admin_tickets'),
        path('tickets/<str:ticket_id>/', views.admin_ticket_detail, name='admin_ticket_detail'),
        path('pricing/', views.admin_pricing_management, name='admin_pricing'),
        path('discounts/', views.admin_discounts, name='admin_discounts'),
        path('reports/', views.admin_reports, name='admin_reports'),
        path('settings/', views.admin_settings, name='admin_settings'),
        path('analytics/', views.admin_analytics, name='admin_analytics'),
    ])),
    
    # Payment URLs
    path('payment/packages/', payment_views.payment_packages, name='payment_packages'),
    path('payment/create/<int:package_id>/', payment_views.create_payment, name='create_payment'),
    path('payment/callback/', payment_views.payment_callback, name='payment_callback'),
    path('payment/return/', payment_views.payment_return, name='payment_return'),
    path('payment/history/', payment_views.payment_history, name='payment_history'),
    path('payment/detail/<int:payment_id>/', payment_views.payment_detail, name='payment_detail'),
    path('subscriptions/', payment_views.user_subscriptions, name='user_subscriptions'),
        path('mock/payment/success/<str:authority>/', views.mock_payment_success, name='mock_payment_success'),
    
    # PayPing Callback URLs
    path('payment/<str:order_id>/payping/callback/', views.payping_callback, name='payping_callback'),
    
    # Wallet redirect (wallet functionality removed)
    path('wallet/', RedirectView.as_view(url='/store/dashboard/', permanent=True), name='wallet_redirect'),
]
