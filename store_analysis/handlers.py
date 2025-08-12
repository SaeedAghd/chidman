import logging
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)

def security_exception_handler(request, exception=None):
    """
    Handler برای خطاهای 404 و 500 با تمرکز بر امنیت
    """
    if exception:
        logger.error(f"Exception occurred: {str(exception)}")
    
    # تعیین نوع خطا
    if hasattr(request, 'resolver_match') and request.resolver_match is None:
        status_code = 404
        error_title = "صفحه یافت نشد"
        error_message = "صفحه مورد نظر شما یافت نشد."
    else:
        status_code = 500
        error_title = "خطای سرور"
        error_message = "خطایی در سرور رخ داده است. لطفاً دوباره تلاش کنید."
    
    # بررسی نوع درخواست
    if request.headers.get('Accept', '').startswith('application/json'):
        return JsonResponse({
            'error': error_title,
            'message': error_message,
            'status_code': status_code
        }, status=status_code)
    
    # رندر قالب خطا
    context = {
        'error_title': error_title,
        'error_message': error_message,
        'status_code': status_code
    }
    
    # انتخاب قالب مناسب
    if status_code == 404:
        template = 'store_analysis/404.html'
    else:
        template = 'store_analysis/500.html'
    
    try:
        html = render_to_string(template, context, request=request)
        return HttpResponse(html, status=status_code)
    except Exception as e:
        logger.error(f"Error rendering error template: {str(e)}")
        # پاسخ ساده در صورت خطا در رندر قالب
        return HttpResponse(
            f"<h1>{error_title}</h1><p>{error_message}</p>",
            status=status_code,
            content_type='text/html'
        ) 