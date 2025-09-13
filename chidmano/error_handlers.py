"""
Custom error handlers for production deployment
"""
import logging
from django.http import HttpResponseServerError, HttpResponse
from django.template import Context, Template
from django.conf import settings

logger = logging.getLogger(__name__)

def custom_500_handler(request):
    """
    Custom 500 error handler for production
    """
    logger.error(f"500 Error occurred for {request.path}")
    
    # Simple error page template
    error_template = """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>خطای سرور - چیدمان</title>
        <style>
            body {
                font-family: 'Vazirmatn', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px;
                margin: 0;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }
            h1 { font-size: 3rem; margin-bottom: 20px; }
            p { font-size: 1.2rem; margin-bottom: 30px; opacity: 0.9; }
            .btn {
                display: inline-block;
                background: rgba(255,255,255,0.2);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 25px;
                margin: 10px;
                transition: all 0.3s ease;
            }
            .btn:hover {
                background: rgba(255,255,255,0.3);
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚠️ خطای سرور</h1>
            <p>متأسفانه خطایی در سرور رخ داده است. لطفاً چند دقیقه صبر کنید و دوباره تلاش کنید.</p>
            <a href="/" class="btn">🏠 صفحه اصلی</a>
            <a href="/admin/" class="btn">⚙️ پنل مدیریت</a>
        </div>
    </body>
    </html>
    """
    
    template = Template(error_template)
    context = Context({'request': request})
    return HttpResponse(template.render(context), status=500)

def custom_404_handler(request, exception):
    """
    Custom 404 error handler
    """
    logger.warning(f"404 Error: {request.path}")
    
    error_template = """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>صفحه یافت نشد - چیدمان</title>
        <style>
            body {
                font-family: 'Vazirmatn', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px;
                margin: 0;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }
            h1 { font-size: 3rem; margin-bottom: 20px; }
            p { font-size: 1.2rem; margin-bottom: 30px; opacity: 0.9; }
            .btn {
                display: inline-block;
                background: rgba(255,255,255,0.2);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 25px;
                margin: 10px;
                transition: all 0.3s ease;
            }
            .btn:hover {
                background: rgba(255,255,255,0.3);
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 صفحه یافت نشد</h1>
            <p>صفحه‌ای که دنبال آن می‌گردید وجود ندارد یا حذف شده است.</p>
            <a href="/" class="btn">🏠 صفحه اصلی</a>
            <a href="/store/" class="btn">🏪 سایت اصلی</a>
        </div>
    </body>
    </html>
    """
    
    template = Template(error_template)
    context = Context({'request': request, 'exception': exception})
    return HttpResponse(template.render(context), status=404)
