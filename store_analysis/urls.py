from django.urls import path, include
from . import views

app_name = 'store_analysis'

urlpatterns = [
    # صفحات وب اصلی
    path('', views.index, name='index'),
    path('education/', views.education_library, name='education_library'),
    path('education/article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('features/', views.features, name='features'),

    # مسیرهای آنالیز فروشگاه
    path('store-analysis/', views.store_analysis_form, name='store_analysis'),
    path('store-analysis/submit/', views.submit_analysis, name='submit_analysis'),
    path('analyses/', views.StoreAnalysisListView.as_view(), name='analysis_list'),
    path('analyses/<int:pk>/', views.StoreAnalysisDetailView.as_view(), name='analysis_detail'),
    path('analyses/<int:pk>/edit/', views.StoreAnalysisUpdateView.as_view(), name='analysis_update'),
    path('analyses/<int:pk>/delete/', views.StoreAnalysisDeleteView.as_view(), name='analysis_delete'),
    path('analyses/<int:pk>/results/', views.analysis_results, name='analysis_results'),
    path('analyses/<int:pk>/status/', views.check_analysis_status, name='check_analysis_status'),

    # پرداخت و ایجاد آنالیز
    path('payment/', views.payment_view, name='payment'),
    path('analysis/<int:pk>/result/', views.analysis_result, name='analysis_result'),
    path('analysis/create/', views.analysis_create, name='analysis_create'),
    path('analysis/<int:pk>/results/', views.analysis_results, name='analysis_results'),

    # داشبورد ادمین
    path('admin-dashboard/', include('store_analysis.admin_dashboard_urls')),

    # مسیرهای API
    path('api/', include('store_analysis.api.urls')),
]
