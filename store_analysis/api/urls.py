from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from .views import StoreAnalysisViewSet, PaymentViewSet

# تنظیمات router
router = DefaultRouter()
router.register(r'analyses', StoreAnalysisViewSet, basename='analysis')
router.register(r'payments', PaymentViewSet, basename='payment')

# URL patterns
urlpatterns = [
    # API endpoints version 1
    path('v1/', include(router.urls)),
    
    # API documentation
    path('v1/docs/', include_docs_urls(title='چیدمانو API')),
    
    # Authentication
    path('v1/auth/', include('rest_framework.urls')),
    
    # API root - default to latest version
    path('', include(router.urls)),
] 