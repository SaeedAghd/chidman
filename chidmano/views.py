from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store_analysis.models import StoreAnalysis, Payment
from store_analysis.services.performance_monitor import PerformanceMonitor
import logging

logger = logging.getLogger(__name__)

def features_view(request):
    """نمایش ویژگی‌های سیستم"""
    return render(request, 'store_analysis/features.html')

@login_required
def dashboard_view(request):
    """نمایش داشبورد کاربر"""
    try:
        user = request.user
        analyses = StoreAnalysis.objects.filter(user=user).order_by('-created_at')[:5]
        payments = Payment.objects.filter(user=user).order_by('-created_at')[:5]
        
        context = {
            'recent_analyses': analyses,
            'recent_payments': payments,
            'total_analyses': StoreAnalysis.objects.filter(user=user).count(),
            'completed_analyses': StoreAnalysis.objects.filter(user=user, status='completed').count(),
        }
        return render(request, 'store_analysis/dashboard.html', context)
    except Exception as e:
        logger.error(f"Error in dashboard view: {e}")
        return render(request, 'store_analysis/error.html', {'error': str(e)})

def health_check(request):
    """بررسی سلامت سیستم"""
    try:
        monitor = PerformanceMonitor()
        health_data = {
            'status': 'healthy',
            'memory_usage': monitor.get_memory_usage(),
            'cpu_usage': monitor.get_cpu_usage(),
            'alerts': monitor.check_alerts()
        }
        return JsonResponse(health_data)
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=500) 