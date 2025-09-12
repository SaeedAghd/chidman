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
    path('form/', views.store_analysis_form, name='store_analysis_form'),
    path('store-analysis/', views.store_analysis_form, name='store_analysis'),
    path('professional-form/', views.store_analysis_form, name='professional_form'),
    path('submit/', views.submit_analysis, name='submit_analysis'),
    path('analysis/create/', views.analysis_create, name='analysis_create'),
    path('analysis/list/', views.analysis_list, name='analysis_list'),
    path('analysis/<int:pk>/', views.analysis_detail, name='analysis_detail'),
    path('analysis/<int:pk>/download/', views.download_analysis_report, name='download_analysis'),
    path('analysis/<int:pk>/progress/', views.analysis_progress, name='analysis_progress'),
    path('analysis/<int:pk>/start/', views.start_analysis, name='start_analysis'),
    path('analysis/<int:pk>/status/', views.get_analysis_status, name='get_analysis_status'),
    path('analysis/<int:pk>/insights/', views.analysis_insights, name='analysis_insights'),
    path('analysis/<int:pk>/ml/', views.advanced_ml_analysis, name='advanced_ml_analysis'),
    path('analysis/<int:pk>/ai/', views.ai_detailed_analysis, name='ai_detailed_analysis'),
    path('analysis/<int:pk>/process/', views.admin_process_analysis, name='admin_process_analysis'),
    path('analysis/<int:pk>/generate-ai/', views.generate_ai_report, name='generate_ai_report'),
    
    # Dashboard URLs
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('analysis/<int:pk>/download-detailed-pdf/', views.download_detailed_pdf, name='download_detailed_pdf'),
    path('store-comparison/', views.store_comparison, name='store_comparison'),
    
    # Result URLs
    path('result/', views.store_analysis_result, name='store_analysis_result'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/pricing/', views.admin_pricing_management, name='admin_pricing_management'),
    path('admin/discounts/', views.admin_discount_management, name='admin_discount_management'),
    path('admin/banners/', views.admin_promotional_banner_management, name='admin_promotional_banner_management'),
    
    # Payment and Analysis URLs
    path('submit-request/', views.submit_analysis_request, name='submit_analysis_request'),
    path('payment/<uuid:order_id>/', views.payment_page, name='payment'),
    path('process-payment/<uuid:order_id>/', views.process_payment, name='process_payment'),
    path('payment-success/<uuid:order_id>/', views.payment_success, name='payment_success'),
    path('payment-failed/<uuid:order_id>/', views.payment_failed, name='payment_failed'),
    path('order-results/<uuid:order_id>/', views.order_analysis_results, name='order_analysis_results'),
    path('check-status/<uuid:order_id>/', views.check_analysis_status, name='check_analysis_status'),
    path('create-order/<int:plan_id>/', views.create_order, name='create_order'),
    path('checkout/<uuid:order_id>/', views.checkout, name='checkout'),
    path('apply-discount/', views.apply_discount, name='apply_discount'),

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
]
