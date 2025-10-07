from django.urls import path, include
from . import views
from . import payment_views
from django.http import HttpResponse

app_name = 'store_analysis'

def health(request):
    return HttpResponse("OK")

urlpatterns = [
    # صفحه اصلی
    path('', views.index, name='index'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('check-legal-agreement/', views.check_legal_agreement, name='check_legal_agreement'),
    path('accept-legal-agreement/', views.accept_legal_agreement, name='accept_legal_agreement'),
    
    # فرم‌ها و تحلیل
    path('forms/', views.store_analysis_form, name='forms'),
    path('forms/submit/', views.forms_submit, name='forms_submit'),
    path('forms/professional/', views.store_analysis_form, name='professional_form'),
    
    # مدیریت تحلیل‌ها
    path('analysis/', include([
        path('create/', views.analysis_create, name='analysis_create'),
        path('list/', views.analysis_list, name='analysis_list'),
        path('<int:pk>/results/', views.analysis_results, name='analysis_results'),
        # analysis_detail حذف شد - مستقیماً به نتایج مدرن هدایت می‌شود
        # path('<uuid:pk>/edit/', views.edit_analysis, name='edit_analysis'),  # Function removed
        # path('<uuid:pk>/delete/', views.delete_analysis, name='delete_analysis'),  # Function removed  
        # path('<uuid:pk>/payment/', views.analysis_payment_page, name='analysis_payment'),  # Function removed
        path('<int:pk>/download/', views.download_analysis_report, name='download_analysis'),
        path('<int:pk>/progress/', views.analysis_progress, name='analysis_progress'),
        path('<int:pk>/start/', views.start_analysis, name='start_analysis'),
        path('<int:pk>/status/', views.get_analysis_status, name='get_analysis_status'),
        path('<int:pk>/insights/', views.analysis_insights, name='analysis_insights'),
        path('<int:pk>/ml/', views.advanced_ml_analysis, name='advanced_ml_analysis'),
        path('<int:pk>/ai/', views.ai_detailed_analysis, name='ai_detailed_analysis'),
        path('<int:pk>/process/', views.admin_process_analysis, name='admin_process_analysis'),
        path('<int:pk>/generate-ai/', views.generate_ai_report, name='generate_ai_report'),
        path('<int:pk>/reprocess-ollama/', views.reprocess_analysis_with_ollama, name='reprocess_analysis_with_ollama'),
        path('<int:pk>/processing-status/', views.processing_status, name='processing_status'),
        path('<int:pk>/start-ollama-processing/', views.start_ollama_processing, name='start_ollama_processing'),
        path('<int:pk>/start-advanced-ai-processing/', views.start_advanced_ai_processing, name='start_advanced_ai_processing'),
        path('<int:pk>/check-processing-status/', views.check_processing_status, name='check_processing_status'),
    ])),
    
    # پشتیبانی
    path('support/', include([
        path('', views.support_center, name='support_center'),
        path('faq/search/', views.faq_search, name='faq_search'),
        path('faq/<int:faq_id>/', views.faq_detail, name='faq_detail'),
        path('ticket/create/', views.create_ticket, name='create_ticket'),
        path('tickets/', views.ticket_list, name='ticket_list'),
        path('ticket/<str:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    ])),
    
    # کیف پول و پرداخت
    path('wallet/', include([
        path('', views.wallet_dashboard, name='wallet_dashboard'),
        path('deposit/', views.deposit_to_wallet, name='deposit_to_wallet'),
        path('payment/<str:order_id>/', views.wallet_payment, name='wallet_payment'),
        path('withdraw/', views.withdraw_from_wallet, name='withdraw_from_wallet'),
        path('transactions/', views.wallet_transactions, name='wallet_transactions'),
    ])),
    
    # آموزش و مقالات
    path('education/', include([
        path('', views.education_library, name='education_library'),
        path('article/<slug:slug>/', views.article_detail, name='article_detail'),
        path('ai-guide/', views.ai_analysis_guide, name='ai_analysis_guide'),
    ])),
    
    # ویژگی‌ها
    path('features/', views.features, name='features'),
    
    # نتایج سفارش
    path('order/<str:order_id>/results/', views.order_analysis_results, name='order_analysis_results'),
    path('order/<str:order_id>/status/', views.check_analysis_status, name='check_analysis_status'),
    
    # URL های موجود (حذف شد چون در بالا تعریف شده)
    path('payment/<str:order_id>/', views.payment_page, name='payment_page'),
    # path('payment/<str:order_id>/activate-wallet/', views.activate_launch_wallet, name='activate_launch_wallet'),  # Function removed
    path('payment/<str:order_id>/payping/', views.payping_payment, name='payping_payment'),
    path('payment/<str:order_id>/process/', views.process_payment, name='process_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('analysis/<int:pk>/pdf/', views.view_analysis_pdf_inline, name='view_analysis_pdf_inline'),
    path('analysis/<int:pk>/pdf-detailed/', views.download_detailed_pdf, name='download_detailed_pdf'),
    path('store-comparison/', views.store_comparison, name='store_comparison'),
    path('ai-consultant/', views.ai_consultant_list, name='ai_consultant_list'),
    path('ai-consultant/<int:analysis_id>/', views.ai_consultant, name='ai_consultant'),
    # مدیریت ادمین کامل
    path('admin/', include([
        path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
        path('users/', views.admin_users, name='admin_users'),
        path('users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
        path('analyses/', views.admin_analyses, name='admin_analyses'),
        path('analyses/<int:analysis_id>/', views.admin_analysis_detail, name='admin_analysis_detail'),
        path('orders/', views.admin_orders, name='admin_orders'),
        path('orders/<str:order_id>/', views.admin_order_detail, name='admin_order_detail'),
        path('tickets/', views.admin_tickets, name='admin_tickets'),
        path('tickets/<str:ticket_id>/', views.admin_ticket_detail, name='admin_ticket_detail'),
        path('wallets/', views.admin_wallets, name='admin_wallets'),
        path('wallets/<int:wallet_id>/', views.admin_wallet_detail, name='admin_wallet_detail'),
        path('pricing/', views.admin_pricing_management, name='admin_pricing'),
        path('discounts/', views.admin_discounts, name='admin_discounts'),
        path('settings/', views.admin_settings, name='admin_settings'),
        path('analytics/', views.admin_analytics, name='admin_analytics'),
        path('reports/', views.admin_reports, name='admin_reports'),
    ])),
    
    # دیباگ
    path('debug/payping/', views.debug_payping, name='debug_payping'),
    path('test/payping/', views.test_payping_connection, name='test_payping'),
    
    # Payment URLs
    path('payment/packages/', payment_views.payment_packages, name='payment_packages'),
    path('payment/create/<int:package_id>/', payment_views.create_payment, name='create_payment'),
    path('payment/callback/', payment_views.payment_callback, name='payment_callback'),
    path('payment/return/', payment_views.payment_return, name='payment_return'),
    path('payment/history/', payment_views.payment_history, name='payment_history'),
    path('payment/detail/<int:payment_id>/', payment_views.payment_detail, name='payment_detail'),
    path('subscriptions/', payment_views.user_subscriptions, name='user_subscriptions'),
    
    # PayPing Callback URL
    path('payment/<str:order_id>/payping/callback/', views.payping_callback, name='payping_callback'),
]