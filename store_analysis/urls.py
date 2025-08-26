from django.urls import path, include
from . import views
from . import consumers

app_name = 'store_analysis'

urlpatterns = [
    # تغییر زبان

    
    # صفحات وب اصلی
    path('', views.index, name='index'),
    path('education/', views.education_library, name='education_library'),
    path('education/article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('features/', views.features, name='features'),

    # مسیرهای آنالیز فروشگاه
    path('store-analysis/', views.store_analysis_form, name='store_analysis'),
    path('store-analysis/submit/', views.submit_analysis, name='submit_analysis'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    
    # مسیرهای تحلیل‌ها
    path('analyses/', views.analysis_list, name='analysis_list'),
    path('analyses/<int:pk>/results/', views.analysis_results, name='analysis_results'),
    path('analyses/<int:pk>/download/', views.download_analysis_report, name='download_analysis'),

    # مسیرهای تحلیل AI
    path('analysis/<int:pk>/ai-detailed/', views.ai_detailed_analysis, name='ai_detailed_analysis'),
    path('analyses/<int:pk>/advanced-ml/', views.advanced_ml_analysis, name='advanced_ml_analysis'),
    path('api/generate-ai-report/', views.generate_ai_report, name='generate_ai_report'),
    
    # مسیرهای ادمین
    path('admin/analyses/<int:pk>/process/', views.admin_process_analysis, name='admin_process_analysis'),
    
    # مسیرهای پنل کاربری فوق حرفه‌ای
    path('professional-dashboard/', views.professional_dashboard, name='professional_dashboard'),
    path('analyses/<int:pk>/insights/', views.analysis_insights, name='analysis_insights'),
    path('store-comparison/', views.store_comparison, name='store_comparison'),
    path('ai-consultant/', views.ai_consultant, name='ai_consultant'),
    
    # مسیرهای راهنما
    path('ai-analysis-guide/', views.ai_analysis_guide, name='ai_analysis_guide'),
]
