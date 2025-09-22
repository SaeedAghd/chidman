from django.urls import path
from . import views

app_name = 'store_analysis'

urlpatterns = [
    # Main index page
    path('', views.index, name='index'),
    
    # Core URLs
    path('features/', views.features, name='features'),
    path('education/', views.education_library, name='education_library'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('ai-guide/', views.ai_analysis_guide, name='ai_analysis_guide'),
    
    # Analysis URLs
    path('store-analysis/', views.store_analysis_form, name='store_analysis'),
    path('professional-form/', views.store_analysis_form, name='professional_form'),
    path('submit/', views.submit_analysis, name='submit_analysis'),
    path('analysis/create/', views.analysis_create, name='analysis_create'),
    path('analysis/list/', views.analysis_list, name='analysis_list'),
    path('analysis/<int:pk>/', views.analysis_detail, name='analysis_detail'),
    path('analysis/<int:pk>/delete/', views.delete_analysis, name='delete_analysis'),
    path('analysis/<int:pk>/payment/', views.analysis_payment_page, name='analysis_payment'),
    path('analysis/<int:pk>/download/', views.download_analysis_report, name='download_analysis'),
    path('analysis/<int:pk>/progress/', views.analysis_progress, name='analysis_progress'),
    path('analysis/<int:pk>/start/', views.start_analysis, name='start_analysis'),
    path('analysis/<int:pk>/status/', views.get_analysis_status, name='get_analysis_status'),
    path('analysis/<int:pk>/insights/', views.analysis_insights, name='analysis_insights'),
    path('analysis/<int:pk>/ml/', views.advanced_ml_analysis, name='advanced_ml_analysis'),
    path('analysis/<int:pk>/ai/', views.ai_detailed_analysis, name='ai_detailed_analysis'),
    path('analysis/<int:pk>/process/', views.admin_process_analysis, name='admin_process_analysis'),
    path('analysis/<int:pk>/generate-ai/', views.generate_ai_report, name='generate_ai_report'),
    path('analysis/<int:pk>/reprocess-ollama/', views.reprocess_analysis_with_ollama, name='reprocess_analysis_with_ollama'),
    path('analysis/<int:pk>/processing-status/', views.processing_status, name='processing_status'),
    path('analysis/<int:pk>/start-ollama-processing/', views.start_ollama_processing, name='start_ollama_processing'),
    path('analysis/<int:pk>/start-advanced-ai-processing/', views.start_advanced_ai_processing, name='start_advanced_ai_processing'),
    path('analysis/<int:pk>/check-processing-status/', views.check_processing_status, name='check_processing_status'),
    
    # سیستم تیکت پشتیبانی
    path('support/', views.support_center, name='support_center'),
    path('support/faq/search/', views.faq_search, name='faq_search'),
    path('support/faq/<int:faq_id>/', views.faq_detail, name='faq_detail'),
    path('support/ticket/create/', views.create_ticket, name='create_ticket'),
    path('support/tickets/', views.ticket_list, name='ticket_list'),
    path('support/ticket/<str:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('api/suggest-faqs/', views.suggest_faqs_api, name='suggest_faqs_api'),
    
    # Dashboard URLs
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('analysis/<int:pk>/download-detailed-pdf/', views.download_detailed_pdf, name='download_detailed_pdf'),
    path('store-comparison/', views.store_comparison, name='store_comparison'),
    
    # Result URLs
    path('result/', views.store_analysis_result, name='store_analysis_result'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/pricing/', views.pricing_management, name='admin_pricing'),
    path('admin/discounts/', views.discount_management, name='admin_discounts'),
    path('admin/support-tickets/', views.support_ticket_management, name='admin_support_tickets'),
    path('admin/analytics/', views.system_analytics, name='admin_analytics'),
    path('admin/banners/', views.admin_promotional_banner_management, name='admin_promotional_banner_management'),
    path('admin/api/create-discount/', views.create_discount_code, name='admin_create_discount'),
    path('admin/api/toggle-discount/<int:discount_id>/', views.toggle_discount_status, name='admin_toggle_discount'),
    path('admin/api/assign-ticket/<int:ticket_id>/', views.assign_ticket, name='admin_assign_ticket'),
    
    # Payment and Analysis URLs
    path('submit-request/', views.submit_analysis_request, name='submit_analysis_request'),
    path('payment/<uuid:order_id>/', views.payment_page, name='payment_page'),
    path('process-payment/<uuid:order_id>/', views.process_payment, name='process_payment'),
    path('payment-success/<uuid:order_id>/', views.payment_success, name='payment_success'),
    path('payment-failed/<uuid:order_id>/', views.payment_failed, name='payment_failed'),
    path('order-results/<uuid:order_id>/', views.order_analysis_results, name='order_analysis_results'),
    path('check-status/<uuid:order_id>/', views.check_analysis_status, name='check_analysis_status'),
    path('create-order/<int:plan_id>/', views.create_order, name='create_order'),
    path('checkout/<uuid:order_id>/', views.checkout, name='checkout'),
    path('apply-discount/', views.apply_discount, name='apply_discount'),
    path('test-zarinpal/', views.test_zarinpal, name='test_zarinpal'),

    path('analysis-results/<int:pk>/', views.analysis_results, name='analysis_results'),
    path('analysis-results-session/', views.analysis_results_session, name='analysis_results_session'),
    
    # Forms
    path('forms/', views.forms, name='forms'),
    path('forms/submit/', views.forms_submit, name='forms_submit'),
    
    # Legal Agreement URLs
    path('check-legal-agreement/', views.check_legal_agreement, name='check_legal_agreement'),
    path('accept-legal-agreement/', views.accept_legal_agreement, name='accept_legal_agreement'),
    
    # AI Consultant URLs
    path('ai-consultant/', views.ai_consultant_list, name='ai_consultant_list'),
    path('ai-consultant/<int:analysis_id>/', views.ai_consultant, name='ai_consultant'),
    path('consultant/ask/<uuid:session_id>/', views.ask_consultant_question, name='ask_consultant_question'),
    path('consultant/payment/<uuid:session_id>/', views.consultant_payment, name='consultant_payment'),
    path('consultant/process-payment/<uuid:session_id>/', views.process_consultant_payment, name='process_consultant_payment'),
    path('consultant/payment-success/<uuid:session_id>/', views.consultant_payment_success, name='consultant_payment_success'),
    path('consultant/payment-failed/<uuid:session_id>/', views.consultant_payment_failed, name='consultant_payment_failed'),
    
    # سیستم کیف پول
    path('wallet/', views.wallet_dashboard, name='wallet_dashboard'),
    path('wallet/transactions/', views.wallet_transactions, name='wallet_transactions'),
    path('wallet/deposit/', views.deposit_to_wallet, name='deposit_to_wallet'),
    path('wallet/withdraw/', views.withdraw_from_wallet, name='withdraw_from_wallet'),
    path('wallet/payment/<str:order_id>/', views.wallet_payment, name='wallet_payment'),
    
    # مدیریت کیف پول برای ادمین
    path('admin/wallets/', views.admin_wallet_management, name='admin_wallet_management'),
    path('admin/wallet/<int:wallet_id>/', views.admin_wallet_detail, name='admin_wallet_detail'),
    path('admin/wallet/<int:wallet_id>/adjust/', views.admin_adjust_wallet, name='admin_adjust_wallet'),
    
    # پرداخت زرین‌پال
    path('payment/zarinpal/<str:order_id>/', views.zarinpal_payment, name='zarinpal_payment'),
    path('payment/zarinpal/callback/<str:order_id>/', views.zarinpal_callback, name='zarinpal_callback'),
]
