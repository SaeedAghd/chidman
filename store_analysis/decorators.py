import logging
import functools
from django.http import JsonResponse
from django.conf import settings
from .services.security_service import SecurityService

logger = logging.getLogger(__name__)

def require_secure_headers(view_func):
    """Decorator برای بررسی هدرهای امنیتی"""
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # بررسی هدرهای امنیتی
        if not _check_secure_headers(request):
            return JsonResponse({
                'error': 'هدرهای امنیتی نامعتبر',
                'message': 'درخواست شما از نظر امنیتی نامعتبر است.'
            }, status=400)
        
        return view_func(request, *args, **kwargs)
    return wrapper

def log_user_activity(activity_type):
    """Decorator برای ثبت فعالیت‌های کاربر"""
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # ثبت فعالیت
            user_id = request.user.id if request.user.is_authenticated else 'anonymous'
            logger.info(f"User activity: {activity_type} by user {user_id} on {request.path}")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_payment(view_func):
    """Decorator برای بررسی وضعیت پرداخت کاربر"""
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        from .models import Payment
        
        # بررسی وجود پرداخت موفق
        last_payment = Payment.objects.filter(
            user=request.user, 
            status='completed'
        ).order_by('-created_at').first()
        
        if not last_payment:
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.warning(request, 'لطفاً ابتدا هزینه تحلیل را پرداخت کنید.')
            return redirect('store_analysis:payment')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def require_analysis_owner(view_func):
    """Decorator برای بررسی مالکیت تحلیل"""
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        from .models import StoreAnalysis
        from django.contrib import messages
        from django.shortcuts import redirect
        
        analysis_id = kwargs.get('pk') or kwargs.get('analysis_id')
        if analysis_id:
            try:
                analysis = StoreAnalysis.objects.get(
                    id=analysis_id, 
                    user=request.user
                )
                request.analysis = analysis
            except StoreAnalysis.DoesNotExist:
                messages.error(request, 'تحلیل مورد نظر یافت نشد.')
                return redirect('store_analysis:analysis_list')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def _check_secure_headers(request):
    """بررسی هدرهای امنیتی"""
    # بررسی CSRF token برای درخواست‌های POST
    if request.method == 'POST':
        if not request.headers.get('X-CSRFToken'):
            return False
    
    # بررسی Origin header
    origin = request.headers.get('Origin')
    if origin and hasattr(settings, 'CORS_ALLOWED_ORIGINS'):
        if origin not in settings.CORS_ALLOWED_ORIGINS:
            return False
    
    return True 