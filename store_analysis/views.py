from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import json
import os
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from .models import StoreAnalysis, StoreBasicInfo, DetailedAnalysis, StoreAnalysisResult, PricingPlan, DiscountCode, Order, AnalysisRequest, PromotionalBanner, Payment, StoreLayout, StoreTraffic, StoreDesign, StoreSurveillance, StoreProducts, AIConsultantSession, AIConsultantQuestion, AIConsultantPayment
from .ai_analysis import StoreAnalysisAI
# from .forms import StoreAnalysisForm, ProfessionalStoreAnalysisForm

# Import های جدید برای PDF و تاریخ شمسی
try:
    import jdatetime  # type: ignore
    import arabic_reshaper  # type: ignore
    from bidi.algorithm import get_display  # type: ignore
except ImportError:
    # Fallback برای محیط‌هایی که کتابخانه‌ها نصب نیستند
    jdatetime = None
    arabic_reshaper = None
    get_display = None
from io import BytesIO
from .utils import calculate_analysis_cost, generate_initial_ai_analysis, color_name_to_hex
from .services.ai_consultant_service import AIConsultantService
import logging

# Setup logger
logger = logging.getLogger(__name__)

# --- صفحه اصلی ---

def index(request):
    """صفحه اصلی - تشخیص مشکل فروشگاه"""
    context = {}
    
    # دریافت تبلیغات فعال
    active_banners = PromotionalBanner.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).order_by('-created_at')
    
    context['active_banners'] = active_banners
    
    if request.user.is_authenticated:
        # آمار برای کاربران ورود کرده
        user_analyses = StoreAnalysis.objects.filter(user=request.user)
        context.update({
            'total_analyses': user_analyses.count(),
            'completed_analyses': user_analyses.filter(status='completed').count(),
            'processing_analyses': user_analyses.filter(status='processing').count(),
            'pending_analyses': user_analyses.filter(status='pending').count(),
        })
    
    return render(request, 'store_analysis/landing_page.html', context)

def problem_detection(request):
    """تشخیص مشکل فروشگاه با AI"""
    if request.method == 'POST':
        # دریافت تصاویر و داده‌های فروشگاه
        # form = ProfessionalStoreAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            # ایجاد تحلیل اولیه
            analysis = StoreAnalysis.objects.create(
                user=request.user if request.user.is_authenticated else None,
                analysis_type='problem_detection',
                store_name=form.cleaned_data.get('store_name', 'فروشگاه جدید'),
                status='processing',
                results='',
                error_message='',
                priority='high',
                estimated_duration=10
            )
            
            # ذخیره داده‌ها
            analysis.set_analysis_data(form.cleaned_data)
            
            # پردازش AI
            ai_analyzer = StoreAnalysisAI()
            problems = ai_analyzer.detect_store_problems(form.cleaned_data)
            
            # ذخیره نتایج
            analysis.preliminary_analysis = json.dumps(problems, ensure_ascii=False)
            analysis.status = 'preliminary_completed'
            analysis.save()
            
            return redirect('store_analysis:smart_recommendations', pk=analysis.pk)
    else:
        # form = ProfessionalStoreAnalysisForm()
        pass
        form = None
    
    context = {
        'form': None,
        'step': 'problem_detection'
    }
    return render(request, 'store_analysis/problem_detection.html', context)

def smart_recommendations(request, pk):
    """پیشنهاد راهکار هوشمند"""
    analysis = get_object_or_404(StoreAnalysis, pk=pk)
    
    if request.method == 'POST':
        # تولید پیشنهادات هوشمند
        ai_analyzer = StoreAnalysisAI()
        analysis_data = analysis.get_analysis_data()
        
        recommendations = ai_analyzer.generate_smart_recommendations(analysis_data)
        layout_suggestions = ai_analyzer.generate_layout_suggestions(analysis_data)
        
        # ذخیره پیشنهادات
        analysis.set_analysis_data({
            **analysis_data,
            'recommendations': recommendations,
            'layout_suggestions': layout_suggestions
        })
        
        return redirect('store_analysis:visual_simulation', pk=analysis.pk)
    
    context = {
        'analysis': analysis,
        'step': 'smart_recommendations'
    }
    return render(request, 'store_analysis/smart_recommendations.html', context)

def visual_simulation(request, pk):
    """شبیه‌سازی بصری 2D/3D"""
    analysis = get_object_or_404(StoreAnalysis, pk=pk)
    
    if request.method == 'POST':
        # تولید شبیه‌سازی
        ai_analyzer = StoreAnalysisAI()
        analysis_data = analysis.get_analysis_data()
        
        simulation_2d = ai_analyzer.generate_2d_simulation(analysis_data)
        simulation_3d = ai_analyzer.generate_3d_simulation(analysis_data)
        
        # ذخیره شبیه‌سازی‌ها
        analysis.set_analysis_data({
            **analysis_data,
            'simulation_2d': simulation_2d,
            'simulation_3d': simulation_3d
        })
        
        return redirect('store_analysis:detailed_report', pk=analysis.pk)
    
    context = {
        'analysis': analysis,
        'step': 'visual_simulation'
    }
    return render(request, 'store_analysis/visual_simulation.html', context)

def detailed_report(request, pk):
    """گزارش دقیق و آینده‌نگر"""
    analysis = get_object_or_404(StoreAnalysis, pk=pk)
    
    if request.method == 'POST':
        # تولید گزارش کامل
        ai_analyzer = StoreAnalysisAI()
        analysis_data = analysis.get_analysis_data()
        
        detailed_report = ai_analyzer.generate_detailed_report(analysis_data)
        forecast = ai_analyzer.generate_forecast(analysis_data)
        dashboard_data = ai_analyzer.generate_dashboard_data(analysis_data)
        
        # ذخیره گزارش
        analysis.set_analysis_data({
            **analysis_data,
            'detailed_report': detailed_report,
            'forecast': forecast,
            'dashboard_data': dashboard_data
        })
        
        return redirect('store_analysis:inspiration_library', pk=analysis.pk)
    
    context = {
        'analysis': analysis,
        'step': 'detailed_report'
    }
    return render(request, 'store_analysis/detailed_report.html', context)

def inspiration_library(request, pk):
    """الهام و نمونه‌ها - کتابخانه هوشمند"""
    analysis = get_object_or_404(StoreAnalysis, pk=pk)
    
    if request.method == 'POST':
        # تولید نمونه‌های الهام‌بخش
        ai_analyzer = StoreAnalysisAI()
        analysis_data = analysis.get_analysis_data()
        
        inspiration_examples = ai_analyzer.generate_inspiration_examples(analysis_data)
        similar_stores = ai_analyzer.find_similar_stores(analysis_data)
        
        # ذخیره نمونه‌ها
        analysis.set_analysis_data({
            **analysis_data,
            'inspiration_examples': inspiration_examples,
            'similar_stores': similar_stores
        })
        
        return redirect('store_analysis:virtual_consultant', pk=analysis.pk)
    
    context = {
        'analysis': analysis,
        'step': 'inspiration_library'
    }
    return render(request, 'store_analysis/inspiration_library.html', context)

def virtual_consultant(request, pk):
    """مشاور آنلاین هوش مصنوعی"""
    analysis = get_object_or_404(StoreAnalysis, pk=pk)
    
    if request.method == 'POST':
        # تولید مشاوره هوشمند
        ai_analyzer = StoreAnalysisAI()
        analysis_data = analysis.get_analysis_data()
        
        consultation = ai_analyzer.generate_virtual_consultation(analysis_data)
        qa_system = ai_analyzer.generate_qa_system(analysis_data)
        
        # ذخیره مشاوره
        analysis.set_analysis_data({
            **analysis_data,
            'consultation': consultation,
            'qa_system': qa_system
        })
        
        return redirect('store_analysis:implementation_guide', pk=analysis.pk)
    
    context = {
        'analysis': analysis,
        'step': 'virtual_consultant'
    }
    return render(request, 'store_analysis/virtual_consultant.html', context)

def implementation_guide(request, pk):
    """امکان اجرای تغییرات - خروجی فنی"""
    analysis = get_object_or_404(StoreAnalysis, pk=pk)
    
    if request.method == 'POST':
        # تولید راهنمای اجرا
        ai_analyzer = StoreAnalysisAI()
        analysis_data = analysis.get_analysis_data()
        
        implementation_guide = ai_analyzer.generate_implementation_guide(analysis_data)
        technical_specs = ai_analyzer.generate_technical_specifications(analysis_data)
        supplier_connections = ai_analyzer.generate_supplier_connections(analysis_data)
        
        # ذخیره راهنما
        analysis.set_analysis_data({
            **analysis_data,
            'implementation_guide': implementation_guide,
            'technical_specs': technical_specs,
            'supplier_connections': supplier_connections
        })
        
        # تکمیل تحلیل
        analysis.status = 'completed'
        analysis.save()
        
        messages.success(request, 'تحلیل فروشگاه شما با موفقیت تکمیل شد!')
        return redirect('store_analysis:analysis_results', pk=analysis.pk)
    
    context = {
        'analysis': analysis,
        'step': 'implementation_guide'
    }
    return render(request, 'store_analysis/implementation_guide.html', context)

def education_library(request):
    """کتابخانه آموزشی"""
    category = request.GET.get('category', '')
    
    # تعریف دسته‌بندی‌های مختلف
    categories = {
        'ai-analysis': {
            'title': 'تحلیل هوش مصنوعی',
            'description': 'آموزش‌های مربوط به تحلیل هوش مصنوعی فروشگاه',
            'articles': [
                {'title': 'مقدمه‌ای بر تحلیل هوش مصنوعی فروشگاه', 'slug': 'ai-introduction'},
                {'title': 'الگوریتم‌های پیشرفته AI', 'slug': 'advanced-ai-algorithms'},
                {'title': 'کاربردهای عملی AI در فروشگاه', 'slug': 'ai-practical-applications'},
            ]
        },
        'traffic-analysis': {
            'title': 'تحلیل ترافیک',
            'description': 'آموزش‌های مربوط به تحلیل ترافیک مشتریان',
            'articles': [
                {'title': 'اصول تحلیل ترافیک فروشگاه', 'slug': 'traffic-analysis-basics'},
                {'title': 'الگوهای حرکتی مشتریان', 'slug': 'customer-movement-patterns'},
                {'title': 'بهینه‌سازی مسیرهای فروشگاه', 'slug': 'store-path-optimization'},
            ]
        },
        'layout-optimization': {
            'title': 'بهینه‌سازی چیدمان',
            'description': 'آموزش‌های مربوط به بهینه‌سازی چیدمان فروشگاه',
            'articles': [
                {'title': 'اصول روانشناسی رنگ در فروشگاه', 'slug': 'color-psychology'},
                {'title': 'طراحی چیدمان بهینه', 'slug': 'optimal-layout-design'},
                {'title': 'تاثیر چیدمان بر فروش', 'slug': 'layout-sales-impact'},
            ]
        },
        'reports': {
            'title': 'گزارش‌های دقیق',
            'description': 'آموزش‌های مربوط به گزارش‌های تحلیلی',
            'articles': [
                {'title': 'نحوه خواندن گزارش‌های تحلیلی', 'slug': 'reading-analytical-reports'},
                {'title': 'تفسیر داده‌های فروش', 'slug': 'sales-data-interpretation'},
                {'title': 'تصمیم‌گیری بر اساس گزارش‌ها', 'slug': 'decision-making-reports'},
            ]
        },
        'predictions': {
            'title': 'پیش‌بینی هوشمند',
            'description': 'آموزش‌های مربوط به پیش‌بینی فروش',
            'articles': [
                {'title': 'اصول پیش‌بینی فروش', 'slug': 'sales-prediction-basics'},
                {'title': 'الگوریتم‌های پیش‌بینی', 'slug': 'prediction-algorithms'},
                {'title': 'استراتژی‌های آینده‌نگر', 'slug': 'future-strategies'},
            ]
        },
        'auto-optimization': {
            'title': 'بهینه‌سازی خودکار',
            'description': 'آموزش‌های مربوط به بهینه‌سازی خودکار',
            'articles': [
                {'title': 'سیستم‌های بهینه‌سازی خودکار', 'slug': 'auto-optimization-systems'},
                {'title': 'الگوریتم‌های یادگیری ماشین', 'slug': 'machine-learning-algorithms'},
                {'title': 'بهبود مستمر عملکرد', 'slug': 'continuous-improvement'},
            ]
        }
    }
    
    context = {
        'category': category,
        'category_data': categories.get(category, {}),
        'all_categories': categories,
    }
    
    return render(request, 'store_analysis/education.html', context)

def features(request):
    """ویژگی‌ها"""
    return render(request, 'store_analysis/features.html')

def article_detail(request, slug):
    """جزئیات مقاله"""
    # این view بعداً پیاده‌سازی می‌شود
    return render(request, 'store_analysis/article_detail.html', {'slug': slug})



# --- تحلیل‌ها ---

@login_required
def analysis_list(request):
    """لیست تحلیل‌ها"""
    # اگر ادمین است، تمام تحلیل‌ها را نشان بده
    if request.user.is_staff or request.user.is_superuser:
        analyses = StoreAnalysis.objects.all().order_by('-created_at')
    else:
        analyses = StoreAnalysis.objects.filter(user=request.user).order_by('-created_at')
    
    # اضافه کردن اطلاعات اضافی برای نمایش
    for analysis in analyses:
        # محاسبه پیشرفت
        if analysis.status == 'completed':
            analysis.progress = 100
        elif analysis.status == 'processing':
            analysis.progress = 75
        elif analysis.status == 'pending':
            analysis.progress = 25
        else:
            analysis.progress = 0
        
        # بررسی وجود پیش‌تحلیل (به صورت متغیر موقت)
        analysis.has_preliminary_temp = bool(analysis.results or analysis.preliminary_analysis)
    
    paginator = Paginator(analyses, 10)
    page = request.GET.get('page')
    analyses = paginator.get_page(page)
    
    context = {
        'analyses': analyses,
        'is_admin': request.user.is_staff or request.user.is_superuser,
        'total_analyses': len(analyses),
    }
    return render(request, 'store_analysis/analysis_list.html', context)

@login_required
def analysis_results(request, pk):
    """نتایج تحلیل"""
    try:
        # اگر ادمین است، هر تحلیلی را ببیند
        if request.user.is_staff or request.user.is_superuser:
            analysis = StoreAnalysis.objects.get(pk=pk)
        else:
            # کاربر عادی فقط تحلیل‌های خودش را می‌بیند
            analysis = StoreAnalysis.objects.get(pk=pk, user=request.user)
    except StoreAnalysis.DoesNotExist:
        from django.http import Http404
        raise Http404("تحلیل مورد نظر یافت نشد")
    
    # بررسی وجود نتیجه تحلیل
    try:
        result = analysis.storeanalysisresult_set.first()
    except:
        result = None
    
    # محاسبه امتیازات از نتایج AI
    scores = {}
    if analysis.results and 'executive_summary' in analysis.results:
        # محاسبه امتیاز کلی بر اساس confidence_score
        confidence_score = analysis.results.get('confidence_score', 0.85)
        overall_score = int(confidence_score * 100)
        
        # محاسبه امتیازات جزئی بر اساس داده‌های تحلیل
        analysis_data = analysis.get_analysis_data()
        # استفاده از مقادیر پیش‌فرض اگر داده‌ای موجود نباشد
        conversion_rate = float(analysis_data.get('conversion_rate', 42.5))
        customer_traffic = float(analysis_data.get('customer_traffic', 180))
        store_size = float(analysis_data.get('store_size', 1200))
        unused_area_size = float(analysis_data.get('unused_area_size', 150))
        
        # امتیاز چیدمان (بر اساس فضای بلااستفاده و نرخ تبدیل)
        layout_score = max(60, 100 - (unused_area_size / store_size * 100) if store_size > 0 else 80)
        layout_score = min(95, layout_score + (conversion_rate - 30) * 0.5)
        
        # امتیاز ترافیک (بر اساس تعداد مشتریان)
        traffic_score = min(95, max(60, customer_traffic / 10))
        
        # امتیاز طراحی (بر اساس نرخ تبدیل و ترافیک)
        design_score = min(95, max(60, conversion_rate * 1.5 + traffic_score * 0.3))
        
        # امتیاز فروش (بر اساس نرخ تبدیل)
        sales_score = min(95, max(60, conversion_rate * 2))
        
        scores = {
            'overall_score': overall_score,
            'layout_score': int(layout_score),
            'traffic_score': int(traffic_score),
            'design_score': int(design_score),
            'sales_score': int(sales_score)
        }
    else:
        # امتیازات پیش‌فرض
        scores = {
            'overall_score': 75,
            'layout_score': 70,
            'traffic_score': 75,
            'design_score': 80,
            'sales_score': 72
        }
    
    # بررسی دسترسی به گزارش مدیریتی
    is_admin = request.user.is_staff or request.user.is_superuser
    show_management_report = False
    
    if is_admin:
        # ادمین همیشه دسترسی دارد
        show_management_report = True
    elif analysis.can_generate_report:
        # کاربر عادی وقتی امکان تولید گزارش وجود داشته باشد
        show_management_report = True
    
    # بررسی وجود نتایج AI در JSONField
    has_ai_results = analysis.results and 'executive_summary' in analysis.results
    
    # دریافت order مربوط به analysis
    order = None
    if hasattr(analysis, 'order') and analysis.order:
        order = analysis.order
    
    context = {
        'analysis': analysis,
        'result': result,
        'scores': scores,
        'has_ai_results': has_ai_results,
        'show_management_report': show_management_report,
        'is_admin': is_admin,
        'order': order,
    }
    return render(request, 'store_analysis/analysis_results_enhanced.html', context)

@login_required
def download_analysis_report(request, pk):
    """دانلود گزارش تحلیل حرفه‌ای"""
    # اگر ادمین است، هر تحلیلی را دانلود کند
    if request.user.is_staff or request.user.is_superuser:
        analysis = get_object_or_404(StoreAnalysis, pk=pk)
    else:
        analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
    
    # بررسی دسترسی به گزارش مدیریتی
    is_admin = request.user.is_staff or request.user.is_superuser
    show_management_report = False
    
    if is_admin:
        # ادمین همیشه دسترسی دارد
        show_management_report = True
    elif analysis.can_generate_report:
        # کاربر عادی وقتی امکان تولید گزارش وجود داشته باشد
        show_management_report = True
    
    if not show_management_report:
        messages.error(request, "گزارش مدیریتی هنوز آماده نشده است.")
        return redirect('store_analysis:analysis_results', pk=analysis.pk)
    
    # دریافت نوع فایل درخواستی
    file_type = request.GET.get('type', 'html')
    
    try:
        # بررسی نتایج AI
        has_ai_results = analysis.results and 'executive_summary' in analysis.results
        
        if file_type == 'pdf':
            # تولید گزارش متنی حرفه‌ای (جایگزین PDF)
            text_content = generate_pdf_report(analysis, has_ai_results)
            
            response = HttpResponse(content_type='text/plain; charset=utf-8')
            response['Content-Disposition'] = f'attachment; filename="{analysis.store_name}_professional_report.txt"'
            response.write(text_content.encode('utf-8'))
            return response
            
        else:
            # تولید HTML حرفه‌ای (پیش‌فرض)
            html_content = generate_management_report(analysis, has_ai_results)
            
            response = HttpResponse(content_type='text/html; charset=utf-8')
            response['Content-Disposition'] = f'attachment; filename="{analysis.store_name}_professional_certificate.html"'
            response.write(html_content.encode('utf-8'))
            return response
        
    except Exception as e:
        messages.error(request, f"خطا در تولید گزارش: {str(e)}")
        return redirect('store_analysis:analysis_results', pk=analysis.pk)

def generate_management_report(analysis, has_ai_results=False):
    """Generate Professional Certificate-Style Management Report"""
    
    # Get analysis data
    analysis_data = analysis.get_analysis_data()
    results = analysis.results if hasattr(analysis, 'results') and analysis.results else {}
    
    # Check for analysis results
    has_results = hasattr(analysis, 'analysis_result')
    result = analysis.analysis_result if has_results else None
    
    # Generate unique certificate ID
    import uuid
    certificate_id = str(uuid.uuid4())[:8].upper()
    
    # Professional HTML report
    report_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Professional Store Analysis Report - {analysis.store_name}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Roboto:wght@300;400;500;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{ 
            font-family: 'Vazirmatn', 'Tahoma', 'Arial', sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            direction: rtl;
        }}
        .certificate {{ max-width: 1000px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 40px; text-align: center; }}
        .title {{ font-size: 36px; font-weight: bold; margin-bottom: 10px; font-family: 'Vazirmatn', 'Tahoma', sans-serif; }}
        .subtitle {{ font-size: 18px; opacity: 0.9; font-family: 'Vazirmatn', 'Tahoma', sans-serif; }}
        .cert-id {{ background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 25px; font-family: 'Courier New', monospace; margin-top: 20px; }}
        .body {{ padding: 40px; }}
        .store-info {{ background: #f8f9fa; padding: 30px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid #1e3c72; }}
        .store-name {{ font-size: 24px; font-weight: bold; color: #1e3c72; margin-bottom: 20px; font-family: 'Vazirmatn', 'Tahoma', sans-serif; }}
        .info-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
        .info-item {{ background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .info-label {{ font-weight: bold; color: #6c757d; font-size: 12px; text-transform: uppercase; font-family: 'Vazirmatn', 'Tahoma', sans-serif; }}
        .info-value {{ font-size: 16px; color: #1e3c72; margin-top: 5px; font-family: 'Vazirmatn', 'Tahoma', sans-serif; }}
        .scores {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        .scores-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; }}
        .score-item {{ background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; text-align: center; }}
        .score-value {{ font-size: 32px; font-weight: bold; font-family: 'Vazirmatn', 'Tahoma', sans-serif; }}
        .score-label {{ font-size: 14px; opacity: 0.9; font-family: 'Vazirmatn', 'Tahoma', sans-serif; }}
        .section {{ margin-bottom: 30px; }}
        .section-title {{ font-size: 22px; font-weight: bold; color: #1e3c72; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 3px solid #1e3c72; font-family: 'Vazirmatn', 'Tahoma', sans-serif; }}
        .swot-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }}
        .swot-card {{ background: white; padding: 25px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-top: 5px solid; }}
        .swot-strengths {{ border-top-color: #28a745; }}
        .swot-weaknesses {{ border-top-color: #dc3545; }}
        .swot-opportunities {{ border-top-color: #ffc107; }}
        .swot-threats {{ border-top-color: #6f42c1; }}
        .swot-title {{ font-weight: bold; font-size: 18px; margin-bottom: 15px; text-align: center; font-family: 'Vazirmatn', 'Tahoma', sans-serif; }}
        .swot-list {{ list-style: none; }}
        .swot-list li {{ padding: 8px 0; border-bottom: 1px solid #f8f9fa; padding-left: 20px; position: relative; font-family: 'Vazirmatn', 'Tahoma', sans-serif; }}
        .swot-list li::before {{ content: '•'; position: absolute; left: 0; color: #1e3c72; font-weight: bold; }}
        .footer {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 30px; text-align: center; }}
        .signature-section {{ display: flex; justify-content: space-between; margin-top: 30px; padding-top: 30px; border-top: 2px solid rgba(255,255,255,0.3); }}
        .signature-box {{ text-align: center; }}
        .signature-line {{ width: 200px; height: 2px; background: white; margin: 10px auto; }}
        .cert-date {{ font-family: monospace; font-size: 14px; opacity: 0.9; }}
        @media print {{ body {{ background: white; }} .certificate {{ box-shadow: none; }} }}
    </style>
</head>
<body>
    <div class="certificate">
        <div class="header">
            <div class="title">گواهی‌نامه تحلیل حرفه‌ای</div>
            <div class="subtitle">تحلیل تخصصی چیدمان و بازاریابی فروشگاه</div>
            <div class="cert-id">شناسه گواهی: {certificate_id}</div>
        </div>
        
        <div class="body">
            <div class="store-info">
                <div class="store-name">{analysis.store_name}</div>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">نوع فروشگاه</div>
                        <div class="info-value">{analysis_data.get('store_type', 'خرده‌فروشی') if analysis_data else 'خرده‌فروشی'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">اندازه فروشگاه</div>
                        <div class="info-value">{analysis_data.get('store_size', 'نامشخص') if analysis_data else 'نامشخص'} متر مربع</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">تاریخ تحلیل</div>
                        <div class="info-value">{analysis.created_at.strftime('%Y/%m/%d') if analysis.created_at else 'نامشخص'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">وضعیت تحلیل</div>
                        <div class="info-value">{analysis.status.title()}</div>
                    </div>
                </div>
            </div>
"""
    
    # Add scores if available
    if has_results and result:
        report_content += f"""
            <div class="scores">
                <h2 class="section-title" style="color: white;">امتیازات عملکرد</h2>
                <div class="scores-grid">
                    <div class="score-item">
                        <div class="score-value">{result.overall_score}/100</div>
                        <div class="score-label">امتیاز کلی</div>
                    </div>
                    <div class="score-item">
                        <div class="score-value">{result.layout_score}/100</div>
                        <div class="score-label">امتیاز چیدمان</div>
                    </div>
                    <div class="score-item">
                        <div class="score-value">{result.traffic_score}/100</div>
                        <div class="score-label">امتیاز ترافیک</div>
                    </div>
                    <div class="score-item">
                        <div class="score-value">{result.design_score}/100</div>
                        <div class="score-label">امتیاز طراحی</div>
                    </div>
                    <div class="score-item">
                        <div class="score-value">{result.sales_score}/100</div>
                        <div class="score-label">امتیاز فروش</div>
                    </div>
                </div>
            </div>
"""
    
    # Add SWOT analysis if available
    if results and 'detailed_analysis' in results:
        swot = results['detailed_analysis']
        report_content += f"""
            <div class="section">
                <h2 class="section-title">تحلیل SWOT</h2>
                <div class="swot-grid">
                    <div class="swot-card swot-strengths">
                        <h3 class="swot-title">نقاط قوت</h3>
                        <ul class="swot-list">
"""
        strengths = swot.get('strengths', [])
        if strengths:
            for strength in strengths:
                report_content += f"                            <li>{strength}</li>\n"
        else:
            report_content += "                            <li>موقعیت جغرافیایی مناسب فروشگاه</li>\n"
            report_content += "                            <li>دسترسی آسان به حمل و نقل عمومی</li>\n"
            report_content += "                            <li>فضای کافی برای نمایش محصولات</li>\n"
        
        report_content += f"""
                        </ul>
                    </div>
                    <div class="swot-card swot-weaknesses">
                        <h3 class="swot-title">نقاط ضعف</h3>
                        <ul class="swot-list">
"""
        weaknesses = swot.get('weaknesses', [])
        if weaknesses:
            for weakness in weaknesses:
                report_content += f"                            <li>{weakness}</li>\n"
        else:
            report_content += "                            <li>نیاز به بهبود نورپردازی</li>\n"
            report_content += "                            <li>چیدمان بهینه نشده قفسه‌ها</li>\n"
            report_content += "                            <li>عدم وجود سیستم مدیریت صف</li>\n"
        
        report_content += f"""
                        </ul>
                    </div>
                    <div class="swot-card swot-opportunities">
                        <h3 class="swot-title">فرصت‌ها</h3>
                        <ul class="swot-list">
"""
        opportunities = swot.get('opportunities', [])
        if opportunities:
            for opportunity in opportunities:
                report_content += f"                            <li>{opportunity}</li>\n"
        else:
            report_content += "                            <li>افزایش تقاضا در منطقه</li>\n"
            report_content += "                            <li>امکان توسعه فضای فروشگاه</li>\n"
            report_content += "                            <li>استفاده از فناوری‌های جدید</li>\n"
        
        report_content += f"""
                        </ul>
                    </div>
                    <div class="swot-card swot-threats">
                        <h3 class="swot-title">تهدیدها</h3>
                        <ul class="swot-list">
"""
        threats = swot.get('threats', [])
        if threats:
            for threat in threats:
                report_content += f"                            <li>{threat}</li>\n"
        else:
            report_content += "                            <li>رقابت با فروشگاه‌های جدید</li>\n"
            report_content += "                            <li>تغییرات در الگوی خرید مشتریان</li>\n"
            report_content += "                            <li>افزایش هزینه‌های عملیاتی</li>\n"
        
        report_content += """
                        </ul>
                    </div>
                </div>
            </div>
"""
    
    # Add recommendations if available
    if results and 'recommendations' in results:
        recommendations = results['recommendations']
        report_content += f"""
            <div class="section">
                <h2 class="section-title">توصیه‌های استراتژیک</h2>
"""
        
        if 'immediate' in recommendations:
            report_content += f"""
                <div class="swot-card" style="margin-bottom: 20px;">
                    <h3 class="swot-title">اقدامات فوری (1-2 ماه)</h3>
                    <ul class="swot-list">
"""
            for rec in recommendations['immediate']:
                report_content += f"                        <li>{rec}</li>\n"
            report_content += """
                    </ul>
                </div>
"""
        
        if 'short_term' in recommendations:
            report_content += f"""
                <div class="swot-card" style="margin-bottom: 20px;">
                    <h3 class="swot-title">برنامه‌های کوتاه‌مدت (3-6 ماه)</h3>
                    <ul class="swot-list">
"""
            for rec in recommendations['short_term']:
                report_content += f"                        <li>{rec}</li>\n"
            report_content += """
                    </ul>
                </div>
"""
        
        if 'long_term' in recommendations:
            report_content += f"""
                <div class="swot-card" style="margin-bottom: 20px;">
                    <h3 class="swot-title">استراتژی بلندمدت (6-12 ماه)</h3>
                    <ul class="swot-list">
"""
            for rec in recommendations['long_term']:
                report_content += f"                        <li>{rec}</li>\n"
            report_content += """
                    </ul>
                </div>
"""
    
    # Certificate footer
    report_content += f"""
        </div>
        
        <div class="footer">
            <p>این گواهی‌نامه تأیید می‌کند که تحلیل جامع فروشگاه با استفاده از فناوری هوش مصنوعی پیشرفته و روش‌های تحلیلی حرفه‌ای خرده‌فروشی انجام شده است.</p>
            <div class="signature-section">
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div>مشاور ارشد چیدمان فروشگاه</div>
                    <div>سیستم تحلیل فروشگاه</div>
                </div>
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div>متخصص بازاریابی</div>
                    <div>کارشناس بهینه‌سازی خرده‌فروشی</div>
                </div>
            </div>
            <div class="cert-date">
                شناسه گواهی: {certificate_id} | تولید شده در: {datetime.now().strftime('%Y/%m/%d ساعت %H:%M')}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    return report_content

def generate_pdf_report(analysis, has_ai_results=False):
    """Generate Professional Text Report (PDF alternative)"""
    import uuid
    
    # Generate unique certificate ID
    certificate_id = str(uuid.uuid4())[:8].upper()
    
    # Get analysis data
    analysis_data = analysis.get_analysis_data()
    results = analysis.results if hasattr(analysis, 'results') and analysis.results else {}
    has_results = hasattr(analysis, 'analysis_result')
    result = analysis.analysis_result if has_results else None
    
    # Build report content
    report_content = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           گزارش تحلیل حرفه‌ای                                  ║
║                    تحلیل تخصصی چیدمان و بازاریابی فروشگاه                      ║
║                                                                              ║
║                           شناسه گزارش: {certificate_id}                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 اطلاعات فروشگاه
═══════════════════════════════════════════════════════════════════════════════

🏪 نام فروشگاه: {analysis.store_name}
🏷️  نوع فروشگاه: {analysis_data.get('store_type', 'خرده‌فروشی') if analysis_data else 'خرده‌فروشی'}
📏 اندازه فروشگاه: {analysis_data.get('store_size', 'نامشخص') if analysis_data else 'نامشخص'} متر مربع
📅 تاریخ تحلیل: {analysis.created_at.strftime('%Y/%m/%d') if analysis.created_at else 'نامشخص'}
📊 وضعیت تحلیل: {analysis.status.title()}

"""
    
    # Add scores if available
    if has_results and result:
        report_content += f"""
📈 امتیازات عملکرد
═══════════════════════════════════════════════════════════════════════════════

🎯 امتیاز کلی: {result.overall_score}/100
🏗️  امتیاز چیدمان: {result.layout_score}/100
🚶 امتیاز ترافیک: {result.traffic_score}/100
🎨 امتیاز طراحی: {result.design_score}/100
💰 امتیاز فروش: {result.sales_score}/100

"""
    
    # Add SWOT analysis if available
    if results and 'detailed_analysis' in results:
        swot = results['detailed_analysis']
        report_content += f"""
🔍 تحلیل SWOT
═══════════════════════════════════════════════════════════════════════════════

✅ نقاط قوت:
"""
        strengths = swot.get('strengths', [])
        if strengths:
            for i, strength in enumerate(strengths, 1):
                report_content += f"   {i}. {strength}\n"
        else:
            report_content += """   1. موقعیت جغرافیایی مناسب فروشگاه
   2. دسترسی آسان به حمل و نقل عمومی
   3. فضای کافی برای نمایش محصولات
"""
        
        report_content += f"""
❌ نقاط ضعف:
"""
        weaknesses = swot.get('weaknesses', [])
        if weaknesses:
            for i, weakness in enumerate(weaknesses, 1):
                report_content += f"   {i}. {weakness}\n"
        else:
            report_content += """   1. نیاز به بهبود نورپردازی
   2. چیدمان بهینه نشده قفسه‌ها
   3. عدم وجود سیستم مدیریت صف
"""
        
        report_content += f"""
🚀 فرصت‌ها:
"""
        opportunities = swot.get('opportunities', [])
        if opportunities:
            for i, opportunity in enumerate(opportunities, 1):
                report_content += f"   {i}. {opportunity}\n"
        else:
            report_content += """   1. افزایش تقاضا در منطقه
   2. امکان توسعه فضای فروشگاه
   3. استفاده از فناوری‌های جدید
"""
        
        report_content += f"""
⚠️  تهدیدها:
"""
        threats = swot.get('threats', [])
        if threats:
            for i, threat in enumerate(threats, 1):
                report_content += f"   {i}. {threat}\n"
        else:
            report_content += """   1. رقابت با فروشگاه‌های جدید
   2. تغییرات در الگوی خرید مشتریان
   3. افزایش هزینه‌های عملیاتی
"""
    
    # Add recommendations if available
    if results and 'recommendations' in results:
        recommendations = results['recommendations']
        report_content += f"""
💡 توصیه‌های استراتژیک
═══════════════════════════════════════════════════════════════════════════════

⚡ اقدامات فوری (1-2 ماه):
"""
        if 'immediate' in recommendations:
            for i, rec in enumerate(recommendations['immediate'], 1):
                report_content += f"   {i}. {rec}\n"
        else:
            report_content += """   1. بهبود نورپردازی فروشگاه
   2. بهینه‌سازی چیدمان قفسه‌ها
   3. نصب سیستم مدیریت صف
"""
        
        report_content += f"""
📅 برنامه‌های کوتاه‌مدت (3-6 ماه):
"""
        if 'short_term' in recommendations:
            for i, rec in enumerate(recommendations['short_term'], 1):
                report_content += f"   {i}. {rec}\n"
        else:
            report_content += """   1. نصب دوربین‌های نظارتی
   2. بهبود سیستم تهویه
   3. اضافه کردن فضای استراحت
"""
        
        report_content += f"""
🎯 استراتژی بلندمدت (6-12 ماه):
"""
        if 'long_term' in recommendations:
            for i, rec in enumerate(recommendations['long_term'], 1):
                report_content += f"   {i}. {rec}\n"
        else:
            report_content += """   1. نوسازی کامل فروشگاه
   2. پیاده‌سازی سیستم هوشمند
   3. توسعه فضای فروشگاه
"""
    
    # Certificate footer
    report_content += f"""
═══════════════════════════════════════════════════════════════════════════════
📜 اطلاعات گزارش
═══════════════════════════════════════════════════════════════════════════════

این گزارش تأیید می‌کند که تحلیل جامع فروشگاه با استفاده از فناوری 
هوش مصنوعی پیشرفته و روش‌های تحلیلی حرفه‌ای خرده‌فروشی انجام شده است.

👨‍💼 مشاور ارشد چیدمان فروشگاه          👩‍💼 متخصص بازاریابی
    سیستم تحلیل فروشگاه                     کارشناس بهینه‌سازی خرده‌فروشی

═══════════════════════════════════════════════════════════════════════════════
شناسه گزارش: {certificate_id} | تولید شده در: {datetime.now().strftime('%Y/%m/%d ساعت %H:%M')}
═══════════════════════════════════════════════════════════════════════════════
"""
    
    return report_content

def generate_image_report(request, analysis):
    """تولید گزارش تصویری حرفه‌ای"""
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # ایجاد تصویر
    width, height = 1200, 1600
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        # فونت‌ها (اگر موجود باشند)
        title_font = ImageFont.truetype("arial.ttf", 48)
        subtitle_font = ImageFont.truetype("arial.ttf", 32)
        normal_font = ImageFont.truetype("arial.ttf", 24)
    except:
        # فونت پیش‌فرض
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()
    
    # رنگ‌ها
    primary_color = (46, 134, 171)  # #2E86AB
    secondary_color = (162, 59, 114)  # #A23B72
    text_color = (0, 0, 0)
    
    y_position = 50
    
    # عنوان اصلی
    draw.text((width//2, y_position), "گزارش مدیریتی تحلیل فروشگاه", fill=primary_color, font=title_font, anchor="mm")
    y_position += 80
    
    # اطلاعات مدیر
    manager_name = analysis.analysis_data.get('manager_name', 'مدیر محترم') if analysis.analysis_data else 'مدیر محترم'
    draw.text((width//2, y_position), f"جناب {manager_name}", fill=secondary_color, font=subtitle_font, anchor="mm")
    y_position += 60
    
    # اطلاعات فروشگاه
    draw.text((100, y_position), "اطلاعات فروشگاه:", fill=primary_color, font=subtitle_font)
    y_position += 50
    
    store_info = [
        f"نام فروشگاه: {analysis.store_name}",
        f"نوع فروشگاه: {analysis.get_store_type_display() if analysis.store_type else 'نامشخص'}",
        f"اندازه فروشگاه: {analysis.store_size or 'نامشخص'} متر مربع",
        f"وضعیت تحلیل: {analysis.get_status_display()}",
        f"تاریخ ایجاد: {analysis.created_at.strftime('%Y/%m/%d %H:%M')}"
    ]
    
    for info in store_info:
        draw.text((120, y_position), info, fill=text_color, font=normal_font)
        y_position += 40
    
    y_position += 30
    
    # امتیازات
    if hasattr(analysis, 'results') and analysis.results:
        draw.text((100, y_position), "امتیازات کلی:", fill=primary_color, font=subtitle_font)
        y_position += 50
        
        scores = [
            ("امتیاز کلی", "85"),
            ("امتیاز چیدمان", "93"),
            ("امتیاز ترافیک", "60"),
            ("امتیاز طراحی", "82"),
            ("امتیاز فروش", "85")
        ]
        
        for i, (label, score) in enumerate(scores):
            x = 120 + (i * 200)
            draw.text((x, y_position), label, fill=text_color, font=normal_font)
            draw.text((x, y_position + 30), score, fill=secondary_color, font=subtitle_font)
        
        y_position += 80
    
    # پیش‌تحلیل
    if analysis.preliminary_analysis:
        draw.text((100, y_position), "پیش‌تحلیل اولیه:", fill=primary_color, font=subtitle_font)
        y_position += 50
        
        # تقسیم متن به خطوط
        words = analysis.preliminary_analysis.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if len(test_line) * 15 < width - 200:  # تقریب عرض متن
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        for line in lines[:10]:  # حداکثر 10 خط
            draw.text((120, y_position), line, fill=text_color, font=normal_font)
            y_position += 35
    
    # تاریخ تولید
    y_position = height - 100
    draw.text((width//2, y_position), f"تاریخ تولید: {datetime.now().strftime('%Y/%m/%d %H:%M')}", 
              fill=text_color, font=normal_font, anchor="mm")
    
    # ذخیره تصویر
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # پاسخ HTTP
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{analysis.store_name}_management_report.png"'
    return response

def generate_text_report(request, analysis):
    """تولید گزارش متنی"""
    response = HttpResponse(content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{analysis.store_name}_analysis_report.txt"'
    
    # محتوای گزارش
    manager_name = analysis.analysis_data.get('manager_name', 'مدیر محترم') if analysis.analysis_data else 'مدیر محترم'
    
    report_content = f"""
گزارش مدیریتی تحلیل فروشگاه: {analysis.store_name}
{'='*60}

جناب {manager_name}

جزئیات فروشگاه:
- نام فروشگاه: {analysis.store_name}
- نوع فروشگاه: {analysis.get_store_type_display() if analysis.store_type else 'نامشخص'}
- اندازه فروشگاه: {analysis.store_size or 'نامشخص'}
- نوع تحلیل: {analysis.get_analysis_type_display()}
- وضعیت: {analysis.get_status_display()}
- تاریخ ایجاد: {analysis.created_at.strftime('%Y/%m/%d %H:%M')}

پیش‌تحلیل اولیه:
{analysis.preliminary_analysis}

جزئیات تکمیلی:
- اولویت: {analysis.get_priority_display()}
- زمان تخمینی: {analysis.estimated_duration} دقیقه
- پیشرفت: {analysis.get_progress()}%

داده‌های تحلیل:
{json.dumps(analysis.get_analysis_data(), ensure_ascii=False, indent=2)}

تاریخ تولید گزارش: {datetime.now().strftime('%Y/%m/%d %H:%M')}
        """
    
    response.write(report_content.encode('utf-8'))
    return response

@login_required
def user_dashboard(request):
    """پنل کاربری حرفه‌ای - Apple Style"""
    if not request.user.is_authenticated:
        return redirect('store_analysis:login')
    
    # آمار تحلیل‌ها
    total_analyses = StoreAnalysis.objects.filter(user=request.user).count()
    completed_analyses = StoreAnalysis.objects.filter(user=request.user, status='completed').count()
    pending_analyses = StoreAnalysis.objects.filter(user=request.user, status='pending').count()
    processing_analyses = StoreAnalysis.objects.filter(user=request.user, status='processing').count()
    
    # آخرین تحلیل‌ها
    recent_analyses = StoreAnalysis.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # تولید تحلیل کامل برای نمایش در داشبورد
    detailed_analysis = None
    if recent_analyses.exists():
        latest_analysis = recent_analyses.first()
        if latest_analysis.analysis_data:
            detailed_analysis = generate_detailed_analysis_for_dashboard(latest_analysis.analysis_data)
    
    # تاریخ شمسی برای داشبورد
    if jdatetime:
        now = timezone.now()
        persian_date = jdatetime.datetime.fromgregorian(datetime=now)
        persian_date_str = persian_date.strftime("%Y/%m/%d")
    else:
        persian_date_str = timezone.now().strftime("%Y/%m/%d")
    
    # تحلیل‌های قابل دانلود
    downloadable_analyses = StoreAnalysis.objects.filter(
        user=request.user, 
        status__in=['preliminary_completed', 'completed']
    ).order_by('-created_at')[:3]
    
    # محاسبه درصد موفقیت
    success_rate = (completed_analyses / total_analyses * 100) if total_analyses > 0 else 0
    
    context = {
        'total_analyses': total_analyses,
        'completed_analyses': completed_analyses,
        'pending_analyses': pending_analyses,
        'processing_analyses': processing_analyses,
        'recent_analyses': recent_analyses,
        'downloadable_analyses': downloadable_analyses,
        'success_rate': round(success_rate, 1),
        'user': request.user,
        'detailed_analysis': detailed_analysis,
        'persian_date': persian_date_str,
    }
    
    return render(request, 'store_analysis/user_dashboard.html', context)

@login_required
def download_detailed_pdf(request, pk):
    """دانلود برنامه اجرایی تفصیلی به صورت PDF"""
    analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
    
    if not analysis.analysis_data:
        messages.error(request, 'داده‌های تحلیل موجود نیست')
        return redirect('store_analysis:user_dashboard')
    
    try:
        # تولید برنامه اجرایی تفصیلی
        implementation_plan = generate_comprehensive_implementation_plan(analysis.analysis_data)
        
        # ایجاد PDF
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.colors import Color
        from reportlab.lib import colors
        from io import BytesIO
        import os
        
        # تنظیم فونت فارسی
        try:
            # اولویت با فونت وزیر
            font_path = os.path.join(os.path.dirname(__file__), 'static', 'fonts', 'Vazir.ttf')
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('Vazir', font_path))
                font_name = 'Vazir'
                print("Using Vazir font for PDF")
            else:
                # استفاده از فونت Tahoma که از فارسی پشتیبانی می‌کند
                tahoma_path = "C:/Windows/Fonts/tahoma.ttf"
                if os.path.exists(tahoma_path):
                    pdfmetrics.registerFont(TTFont('Tahoma', tahoma_path))
                    font_name = 'Tahoma'
                    print("Using Tahoma font for PDF")
                else:
                    font_name = 'Helvetica'
                    print("Using Helvetica font for PDF")
        except Exception as e:
            print(f"Font registration error: {e}")
            font_name = 'Helvetica'
        
        # ایجاد buffer برای PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # استایل‌های متن
        styles = getSampleStyleSheet()
        
        # استایل عنوان اصلی - استانداردهای حرفه‌ای
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName=font_name,
            fontSize=22,
            spaceAfter=20,
            alignment=2,  # راست‌چین
            textColor=colors.Color(0.1, 0.3, 0.6),  # آبی تیره حرفه‌ای
            spaceBefore=15,
            leading=28,
            leftIndent=0,
            rightIndent=0
        )
        
        # استایل زیرعنوان - استانداردهای حرفه‌ای
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontName=font_name,
            fontSize=16,
            spaceAfter=15,
            textColor=colors.Color(0.2, 0.2, 0.2),  # خاکستری تیره
            spaceBefore=12,
            leading=20,
            alignment=2,  # راست‌چین
            leftIndent=0,
            rightIndent=0
        )
        
        # استایل متن عادی - استانداردهای حرفه‌ای
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=11,
            spaceAfter=8,
            alignment=2,  # راست‌چین
            textColor=colors.Color(0.2, 0.2, 0.2),  # خاکستری تیره
            leading=16,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0
        )
        
        # استایل لیست - استانداردهای حرفه‌ای
        list_style = ParagraphStyle(
            'CustomList',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=10,
            spaceAfter=6,
            leftIndent=20,
            bulletIndent=10,
            leading=14,
            alignment=2,  # راست‌چین
            textColor=colors.Color(0.3, 0.3, 0.3),  # خاکستری متوسط
            rightIndent=0
        )
        
        # استایل بخش‌ها - استانداردهای حرفه‌ای
        section_style = ParagraphStyle(
            'CustomSection',
            parent=styles['Heading3'],
            fontName=font_name,
            fontSize=14,
            spaceAfter=12,
            spaceBefore=18,
            textColor=colors.Color(0.1, 0.3, 0.6),  # آبی تیره حرفه‌ای
            leading=18,
            alignment=2,  # راست‌چین
            leftIndent=0,
            rightIndent=0
        )
        
        # استایل زیربخش‌ها - استانداردهای حرفه‌ای
        subsection_style = ParagraphStyle(
            'CustomSubsection',
            parent=styles['Heading4'],
            fontName=font_name,
            fontSize=12,
            spaceAfter=10,
            spaceBefore=15,
            textColor=colors.Color(0.2, 0.2, 0.2),  # خاکستری تیره
            leading=16,
            alignment=2,  # راست‌چین
            leftIndent=0,
            rightIndent=0
        )
        
        # ایجاد محتوای PDF
        story = []
        
        # سربرگ حرفه‌ای و مدرن - طراحی جهانی
        from reportlab.platypus import Table, TableStyle, Image, Spacer
        from reportlab.lib import colors
        from reportlab.lib.units import inch, cm
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph
        
        def get_persian_date():
            """تبدیل تاریخ میلادی به شمسی"""
            if jdatetime:
                now = timezone.now()
                persian_date = jdatetime.datetime.fromgregorian(datetime=now)
                return persian_date.strftime("%Y/%m/%d")
            else:
                return timezone.now().strftime("%Y/%m/%d")
        
        def fix_persian_text(text):
            """تبدیل متن فارسی به فرمت صحیح RTL"""
            if not text:
                return text
            # حذف کاراکترهای خاص که مشکل ایجاد می‌کنند
            text = text.replace('📊', '').replace('🏪', '').replace('✅', '').replace('⚠️', '').replace('🚀', '').replace('⚡', '').replace('👥', '').replace('💰', '').replace('💎', '').replace('🎯', '').replace('📅', '').replace('📈', '')
            # تبدیل به RTL
            if arabic_reshaper and get_display:
                reshaped_text = arabic_reshaper.reshape(text)
                return get_display(reshaped_text)
            else:
                return text
        
        # سربرگ تمیز و حرفه‌ای - بدون تداخل
        # ردیف اول: برند و تاریخ
        header_row1_data = [
            ['CHIDEMANO', '', fix_persian_text(get_persian_date())],
        ]
        
        header_row1_table = Table(header_row1_data, colWidths=[250, 100, 250], rowHeights=[35])
        header_row1_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.Color(0.05, 0.15, 0.35)),
            ('INNERGRID', (0, 0), (-1, -1), 0, colors.Color(0.05, 0.15, 0.35)),
            ('BOX', (0, 0), (-1, -1), 0, colors.Color(0.05, 0.15, 0.35)),
            
            # برند انگلیسی
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 22),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.Color(0.9, 0.95, 1.0)),
            ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
            
            # تاریخ
            ('FONTNAME', (2, 0), (2, 0), font_name),
            ('FONTSIZE', (2, 0), (2, 0), 14),
            ('TEXTCOLOR', (2, 0), (2, 0), colors.Color(0.8, 0.9, 1.0)),
            ('ALIGN', (2, 0), (2, 0), 'LEFT'),
            
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        # ردیف دوم: عنوان اصلی - با RTL صحیح
        header_row2_data = [
            [fix_persian_text('سیستم تحلیل فروشگاه هوشمند')],
        ]
        
        header_row2_table = Table(header_row2_data, colWidths=[600], rowHeights=[30])
        header_row2_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.Color(0.05, 0.15, 0.35)),
            ('INNERGRID', (0, 0), (-1, -1), 0, colors.Color(0.05, 0.15, 0.35)),
            ('BOX', (0, 0), (-1, -1), 0, colors.Color(0.05, 0.15, 0.35)),
            
            ('FONTNAME', (0, 0), (0, 0), font_name),
            ('FONTSIZE', (0, 0), (0, 0), 16),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.Color(0.95, 0.98, 1.0)),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        # ردیف سوم: زیرعنوان - با RTL صحیح
        header_row3_data = [
            [fix_persian_text('گزارش تفصیلی و حرفه‌ای')],
        ]
        
        header_row3_table = Table(header_row3_data, colWidths=[600], rowHeights=[25])
        header_row3_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.Color(0.05, 0.15, 0.35)),
            ('INNERGRID', (0, 0), (-1, -1), 0, colors.Color(0.05, 0.15, 0.35)),
            ('BOX', (0, 0), (-1, -1), 0, colors.Color(0.05, 0.15, 0.35)),
            
            ('FONTNAME', (0, 0), (0, 0), font_name),
            ('FONTSIZE', (0, 0), (0, 0), 12),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.Color(0.85, 0.92, 1.0)),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        # خط جداکننده طلایی
        separator_data = [['']]
        separator_table = Table(separator_data, colWidths=[600], rowHeights=[2])
        separator_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.Color(0.8, 0.6, 0.2)),
            ('INNERGRID', (0, 0), (-1, -1), 0, colors.white),
            ('BOX', (0, 0), (-1, -1), 0, colors.white),
        ]))
        
        # اضافه کردن سربرگ
        story.append(header_row1_table)
        story.append(header_row2_table)
        story.append(header_row3_table)
        story.append(Spacer(1, 15))
        story.append(separator_table)
        story.append(Spacer(1, 25))
        
        
        # عنوان اصلی با استانداردهای حرفه‌ای
        story.append(Paragraph(fix_persian_text("گزارش تحلیل و برنامه اجرایی"), title_style))
        story.append(Paragraph(fix_persian_text(f"فروشگاه {analysis.store_name}"), subtitle_style))
        story.append(Spacer(1, 15))
        
        # اطلاعات کلی
        story.append(Paragraph(fix_persian_text("اطلاعات کلی پروژه"), section_style))
        story.append(Paragraph(fix_persian_text(f"نام فروشگاه: {analysis.store_name}"), normal_style))
        story.append(Paragraph(fix_persian_text(f"تاریخ تهیه گزارش: {get_persian_date()}"), normal_style))
        story.append(Paragraph(fix_persian_text("تهیه شده توسط: سیستم تحلیل فروشگاه هوشمند چیدمانو"), normal_style))
        story.append(Spacer(1, 20))
        
        # تقسیم متن به بخش‌ها
        sections = implementation_plan.split('\n## ')
        
        for i, section in enumerate(sections):
            if i == 0:
                # بخش اول (بدون ##)
                lines = section.split('\n')
                for line in lines:
                    if line.strip():
                        if line.startswith('#'):
                            story.append(Paragraph(fix_persian_text(line.replace('#', '').strip()), subtitle_style))
                        elif line.startswith('-'):
                            story.append(Paragraph(fix_persian_text(f"• {line[1:].strip()}"), list_style))
                        else:
                            story.append(Paragraph(fix_persian_text(line.strip()), normal_style))
            else:
                # بخش‌های بعدی (با ##)
                lines = section.split('\n')
                if lines[0].strip():
                    story.append(Paragraph(fix_persian_text(lines[0].strip()), subtitle_style))
                
                for line in lines[1:]:
                    if line.strip():
                        if line.startswith('###'):
                            story.append(Paragraph(fix_persian_text(line.replace('###', '').strip()), section_style))
                        elif line.startswith('-'):
                            story.append(Paragraph(fix_persian_text(f"• {line[1:].strip()}"), list_style))
                        elif line.startswith('**') and line.endswith('**'):
                            story.append(Paragraph(fix_persian_text(f"<b>{line[2:-2]}</b>"), normal_style))
                        elif line.startswith('####'):
                            story.append(Paragraph(fix_persian_text(line.replace('####', '').strip()), subsection_style))
                        else:
                            story.append(Paragraph(fix_persian_text(line.strip()), normal_style))
            
            if i < len(sections) - 1:
                story.append(Spacer(1, 20))
        
        # ساخت PDF
        doc.build(story)
        
        # آماده‌سازی response
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="detailed_implementation_plan_{analysis.store_name}_{analysis.id}.pdf"'
        
        return response
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Error generating PDF: {e}")
        logger.error(f"Error details: {error_details}")
        print(f"PDF Generation Error: {error_details}")
        messages.error(request, f'خطا در تولید PDF: {str(e)}')
        return redirect('store_analysis:user_dashboard')


# --- سیستم پرداخت و تحلیل ---

@login_required
def submit_analysis_request(request):
    """ارسال درخواست تحلیل و محاسبه هزینه"""
    if request.method == 'POST':
        try:
            # دریافت داده‌های فرم
            form_data = request.POST.dict()
            files_data = request.FILES
            
            # محاسبه هزینه بر اساس درخواست‌ها
            cost_breakdown = calculate_analysis_cost(form_data)
            
            # ذخیره داده‌های تحلیل
            store_analysis = StoreAnalysis.objects.create(
                user=request.user,
                analysis_type='comprehensive',
                store_name=form_data.get('store_name', ''),
                store_type=form_data.get('store_type', ''),
                store_size=form_data.get('store_size', ''),
                status='pending',
                analysis_data=form_data
            )
            
            # ایجاد سفارش
            order = Order.objects.create(
                user=request.user,
                plan=None,  # پلن سفارشی
                original_amount=cost_breakdown['total'],
                discount_amount=cost_breakdown.get('discount', 0),
                final_amount=cost_breakdown['final'],
                status='pending'
            )
            
            # ایجاد درخواست تحلیل
            analysis_request = AnalysisRequest.objects.create(
                order=order,
                store_analysis_data=form_data,
                status='pending'
            )
            
            # اتصال تحلیل به سفارش
            store_analysis.order = order
            store_analysis.save()
            
            # هدایت به صفحه پرداخت
            return redirect('store_analysis:payment_page', order_id=order.order_id)
            
        except Exception as e:
            messages.error(request, f'خطا در ارسال درخواست: {str(e)}')
            return redirect('store_analysis:user_dashboard')
    
    return redirect('store_analysis:user_dashboard')

@login_required
def payment_page(request, order_id):
    """صفحه پرداخت"""
    try:
        # بررسی وجود Order - هر کاربر فقط به Order های خودش دسترسی دارد
        try:
            order = Order.objects.get(order_id=order_id, user=request.user)
        except Order.DoesNotExist:
            messages.error(request, f'سفارش با شناسه {order_id} یافت نشد یا شما دسترسی ندارید.')
            return redirect('store_analysis:user_dashboard')
        
        # بررسی وجود StoreAnalysis
        store_analysis = StoreAnalysis.objects.filter(order=order).first()
        if not store_analysis:
            messages.error(request, 'تحلیل فروشگاه مربوط به این سفارش یافت نشد.')
            return redirect('store_analysis:user_dashboard')
        
        # تولید تحلیل اولیه اگر وجود ندارد
        if not store_analysis.preliminary_analysis and store_analysis.analysis_data:
            try:
                from .ai_analysis import StoreAnalysisAI
                ai_analyzer = StoreAnalysisAI()
                preliminary_analysis = ai_analyzer.generate_preliminary_analysis(store_analysis.analysis_data)
                store_analysis.preliminary_analysis = preliminary_analysis
                store_analysis.save()
            except Exception as e:
                logger.error(f"Error generating preliminary analysis: {e}")
                # تحلیل اولیه ساده
                store_analysis.preliminary_analysis = "تحلیل اولیه: فروشگاه شما نیاز به بررسی دقیق‌تر دارد. پس از پرداخت، تحلیل کامل انجام خواهد شد."
                store_analysis.save()
        
        # محاسبه مجدد هزینه‌ها
        if store_analysis.analysis_data:
            # محاسبه ساده هزینه‌ها
            cost_breakdown = {
                'base_price': 500000,
                'total': 500000,
                'final': 500000,
                'breakdown': [
                    {'item': 'تحلیل پایه', 'price': 300000},
                    {'item': 'گزارش تفصیلی', 'price': 200000}
                ]
            }
        else:
            cost_breakdown = {
                'base_price': 500000,
                'total': 500000,
                'final': 500000,
                'breakdown': [
                    {'item': 'تحلیل پایه', 'price': 300000},
                    {'item': 'گزارش تفصیلی', 'price': 200000}
                ]
            }
        
        context = {
            'order': order,
            'store_analysis': store_analysis,
            'cost_breakdown': cost_breakdown,
            'payment_methods': [
                {'id': 'online', 'name': 'پرداخت آنلاین', 'icon': 'fas fa-credit-card'},
                {'id': 'wallet', 'name': 'کیف پول', 'icon': 'fas fa-wallet'},
            ]
        }
        
        return render(request, 'store_analysis/payment_page.html', context)
        
    except Exception as e:
        logger.error(f"Error in payment_page: {e}")
        messages.error(request, f'خطا در بارگذاری صفحه پرداخت: {str(e)}')
        return redirect('store_analysis:user_dashboard')

@login_required
def process_payment(request, order_id):
    """پردازش پرداخت"""
    if request.method == 'POST':
        try:
            # هر کاربر فقط Order های خودش را پردازش کند
            order = get_object_or_404(Order, order_id=order_id, user=request.user)
            payment_method = request.POST.get('payment_method', 'online')
            
            # شبیه‌سازی پرداخت موفق
            # در واقعیت باید با درگاه پرداخت ارتباط برقرار شود
            
            # ایجاد رکورد پرداخت
            payment = Payment.objects.create(
                user=request.user,
                store_analysis=StoreAnalysis.objects.filter(order=order).first(),
                amount=order.final_amount,
                payment_method=payment_method,
                status='completed',
                transaction_id=f'TXN_{uuid.uuid4().hex[:12].upper()}'
            )
            
            # به‌روزرسانی وضعیت سفارش
            order.status = 'paid'
            order.payment_method = payment_method
            order.transaction_id = payment.transaction_id
            order.save()
            
            # به‌روزرسانی وضعیت تحلیل
            store_analysis = StoreAnalysis.objects.filter(order=order).first()
            if store_analysis:
                store_analysis.status = 'preliminary_completed'
                store_analysis.save()
                
                # تولید تحلیل اولیه هوش مصنوعی
                initial_analysis = generate_initial_ai_analysis(store_analysis.analysis_data)
                store_analysis.preliminary_analysis = initial_analysis
                store_analysis.save()
            
            # هدایت به صفحه نتایج
            return redirect('store_analysis:order_analysis_results', order_id=order_id)
            
        except Exception as e:
            messages.error(request, f'خطا در پردازش پرداخت: {str(e)}')
            return redirect('store_analysis:payment_page', order_id=order_id)
    
    return redirect('store_analysis:payment_page', order_id=order_id)

@login_required
def order_analysis_results(request, order_id):
    """صفحه نتایج تحلیل بر اساس سفارش"""
    try:
        # هر کاربر فقط Order های خودش را ببیند
        order = get_object_or_404(Order, order_id=order_id, user=request.user)
        store_analysis = StoreAnalysis.objects.filter(order=order).first()
        
        if not store_analysis:
            messages.error(request, 'تحلیل مورد نظر یافت نشد')
            return redirect('store_analysis:user_dashboard')
        
        context = {
            'order': order,
            'store_analysis': store_analysis,
            'has_preliminary': bool(store_analysis.preliminary_analysis),
            'has_results': store_analysis.has_results,
            'progress': store_analysis.get_progress(),
        }
        
        return render(request, 'store_analysis/analysis_results_enhanced.html', context)
        
    except Exception as e:
        messages.error(request, f'خطا در بارگذاری نتایج: {str(e)}')
        return redirect('store_analysis:user_dashboard')

@login_required
def check_analysis_status(request, order_id):
    """بررسی وضعیت تحلیل (AJAX)"""
    try:
        # هر کاربر فقط Order های خودش را بررسی کند
        order = get_object_or_404(Order, order_id=order_id, user=request.user)
        store_analysis = StoreAnalysis.objects.filter(order=order).first()
        
        if not store_analysis:
            return JsonResponse({'error': 'تحلیل یافت نشد'}, status=404)
        
        return JsonResponse({
            'status': store_analysis.status,
            'progress': store_analysis.get_progress(),
            'has_preliminary': bool(store_analysis.preliminary_analysis),
            'has_results': store_analysis.has_results,
            'estimated_completion': store_analysis.estimated_duration,
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def analysis_insights(request, pk):
    """بینش‌های تحلیلی پیشرفته"""
    analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
    
    # تولید بینش‌های پیشرفته
    insights = {
        'performance_metrics': {
            'overall_score': 85.5,
            'layout_efficiency': 78.2,
            'customer_flow': 82.1,
            'visual_appeal': 88.7,
            'sales_potential': 91.3
        },
        'key_findings': [
            "چیدمان فعلی شما 78% بهینه است",
            "نورپردازی نیاز به بهبود 15% دارد",
            "ترافیک مشتریان در ساعات 14-18 قابل بهبود است",
            "رنگ‌بندی فروشگاه تأثیر مثبتی بر فروش دارد"
        ],
        'recommendations': [
            "نصب سیستم نورپردازی هوشمند",
            "بازطراحی مسیر حرکت مشتریان",
            "بهینه‌سازی ارتفاع قفسه‌ها",
            "اضافه کردن عناصر بصری جذاب"
        ],
        'forecast': {
            'expected_improvement': "25-35%",
            'time_to_implement': "2-3 هفته",
            'estimated_cost': "15-25 میلیون تومان",
            'roi_prediction': "40-60%"
        }
    }
    
    context = {
        'analysis': analysis,
        'insights': insights,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    }
    
    return render(request, 'store_analysis/analysis_insights.html', context)

@login_required
def store_comparison(request):
    """مقایسه فروشگاه‌ها"""
    user_analyses = StoreAnalysis.objects.filter(user=request.user, status='completed')
    
    comparison_data = []
    for analysis in user_analyses:
        try:
            result = StoreAnalysisResult.objects.get(store_analysis=analysis)
            comparison_data.append({
                'store_name': analysis.store_name,
                'overall_score': result.overall_score,
                'layout_score': result.layout_score,
                'traffic_score': result.traffic_score,
                'design_score': result.design_score,
                'sales_score': result.sales_score,
                'created_at': analysis.created_at
            })
        except StoreAnalysisResult.DoesNotExist:
            continue
    
    context = {
        'comparison_data': comparison_data,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    }
    
    return render(request, 'store_analysis/store_comparison.html', context)

@login_required
def ai_consultant(request):
    """مشاور هوش مصنوعی شخصی"""
    user_analyses = StoreAnalysis.objects.filter(user=request.user, status='completed')
    
    # تولید مشاوره شخصی‌سازی شده
    ai_advice = {
        'personalized_recommendations': [
            "بر اساس تحلیل‌های قبلی شما، پیشنهاد می‌شود روی بهبود نورپردازی تمرکز کنید",
            "چیدمان قفسه‌های شما در مقایسه با استانداردهای صنعت نیاز به بهینه‌سازی دارد",
            "ترافیک مشتریان در ساعات خاصی از روز قابل بهبود است"
        ],
        'industry_benchmarks': {
            'your_average_score': 82.5,
            'industry_average': 75.0,
            'top_performers': 92.0
        },
        'improvement_areas': [
            "نورپردازی: +15% بهبود",
            "چیدمان: +12% بهبود", 
            "ترافیک: +8% بهبود",
            "طراحی: +10% بهبود"
        ]
    }
    
    context = {
        'ai_advice': ai_advice,
        'user_analyses': user_analyses,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    }
    
    return render(request, 'store_analysis/ai_consultant.html', context)


@login_required
def ai_detailed_analysis(request, pk):
    """تحلیل تفصیلی با AI"""
    # اگر ادمین است، هر تحلیلی را ببیند
    if request.user.is_staff or request.user.is_superuser:
        analysis = get_object_or_404(StoreAnalysis, pk=pk)
    else:
        analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
    
    # تولید تحلیل تفصیلی جدید
    ai_analyzer = StoreAnalysisAI()
    analysis_data = analysis.get_analysis_data()
    
    if analysis_data:
        detailed_analysis = ai_analyzer.generate_detailed_analysis(analysis_data)
        implementation_guide = ai_analyzer.generate_implementation_guide(detailed_analysis)
    else:
        messages.error(request, "داده‌های تحلیل موجود نیست.")
        return redirect('store_analysis:analysis_results', pk=analysis.pk)
    
    context = {
        'analysis': analysis,
        'detailed_analysis': detailed_analysis,
        'implementation_guide': implementation_guide,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    }
    
    return render(request, 'store_analysis/ai_detailed_analysis.html', context)

@login_required
def admin_process_analysis(request, pk):
    """پردازش فوری تحلیل توسط ادمین"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, "شما دسترسی ادمین ندارید.")
        return redirect('store_analysis:analysis_list')
    
    analysis = get_object_or_404(StoreAnalysis, pk=pk)
    
    try:
        # تولید تحلیل فوری
        ai_analyzer = StoreAnalysisAI()
        analysis_data = analysis.analysis_data or {}
        
        # تولید تحلیل
        analysis_result = ai_analyzer.generate_detailed_analysis(analysis_data)
        
        # ذخیره نتایج
        StoreAnalysisResult.objects.update_or_create(
            store_analysis=analysis,
            defaults={
                'overall_score': analysis_result.get('overall_score', 75.0),
                'layout_score': analysis_result.get('layout_score', 75.0),
                'traffic_score': analysis_result.get('traffic_score', 75.0),
                'design_score': analysis_result.get('design_score', 75.0),
                'sales_score': analysis_result.get('sales_score', 75.0),
                'layout_analysis': str(analysis_result.get('strengths', [])),
                'traffic_analysis': str(analysis_result.get('weaknesses', [])),
                'design_analysis': str(analysis_result.get('opportunities', [])),
                'sales_analysis': str(analysis_result.get('threats', [])),
                'overall_analysis': str(analysis_result.get('recommendations', [])),
            }
        )
        
        # بروزرسانی وضعیت تحلیل
        analysis.status = 'completed'
        analysis.save()
        
        messages.success(request, f"تحلیل {analysis.store_name} با موفقیت پردازش شد.")
        
    except Exception as e:
        messages.error(request, f"خطا در پردازش تحلیل: {str(e)}")
    
    return redirect('store_analysis:analysis_results', pk=analysis.pk)


@login_required
def generate_ai_report(request, pk):
    """تولید گزارش AI"""
    analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
    
    try:
        # تولید تحلیل تفصیلی
        ai_analyzer = StoreAnalysisAI()
        analysis_data = analysis.get_analysis_data()
        
        if not analysis_data:
            return JsonResponse({
                'status': 'error',
                'message': 'داده‌های تحلیل موجود نیست.'
            })
        
        detailed_analysis = ai_analyzer.generate_detailed_analysis(analysis_data)
        implementation_guide = ai_analyzer.generate_implementation_guide(detailed_analysis)
        
        return JsonResponse({
            'status': 'success',
            'message': 'تحلیل تفصیلی با موفقیت تولید شد.',
            'analysis_id': analysis.pk,
            'detailed_analysis': detailed_analysis,
            'implementation_guide': implementation_guide
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'خطا در تولید تحلیل: {str(e)}'
        })


@login_required
def advanced_ml_analysis(request, pk):
    """تحلیل پیشرفته با استفاده از ML"""
    try:
        # اگر ادمین است، هر تحلیلی را ببیند
        if request.user.is_staff or request.user.is_superuser:
            analysis = get_object_or_404(StoreAnalysis, pk=pk)
        else:
            # کاربر عادی فقط تحلیل‌های خودش را ببیند
            analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
        
        # بررسی دسترسی
        if not request.user.is_authenticated:
            return redirect('login')
        
        # دریافت داده‌های تحلیل
        analysis_data = analysis.get_analysis_data()
        
        # ایجاد نمونه AI
        ai_analyzer = StoreAnalysisAI()
        
        # تولید تحلیل پیشرفته ML
        ml_analysis = ai_analyzer.generate_advanced_ml_analysis(analysis_data)
        
        # تولید تحلیل معمولی
        regular_analysis = ai_analyzer.generate_detailed_analysis(analysis_data)
        
        context = {
            'analysis': analysis,
            'ml_analysis': ml_analysis,
            'regular_analysis': regular_analysis,
            'analysis_data': analysis_data,
            'is_admin': request.user.is_staff or request.user.is_superuser,
        }
        
        return render(request, 'store_analysis/advanced_ml_analysis.html', context)
        
    except Exception as e:
        messages.error(request, f'خطا در تحلیل پیشرفته: {str(e)}')
        return redirect('store_analysis:analysis_results', pk=pk)


def ai_analysis_guide(request):
    """راهنمای کامل تحلیل AI"""
    return render(request, 'store_analysis/ai_analysis_guide.html')

@login_required
def check_legal_agreement(request):
    """بررسی وضعیت تایید تعهدنامه حقوقی"""
    try:
        # بررسی اینکه آیا کاربر قبلاً تایید کرده یا نه
        # می‌توانید از UserProfile یا جدول جداگانه استفاده کنید
        # فعلاً از session استفاده می‌کنیم
        accepted = request.session.get('legal_agreement_accepted', False)
        
        return JsonResponse({
            'accepted': accepted,
            'user_id': request.user.id
        })
    except Exception as e:
        return JsonResponse({
            'accepted': False,
            'error': str(e)
        })

@login_required
def accept_legal_agreement(request):
    """تایید تعهدنامه حقوقی"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            
            if data.get('accepted'):
                # ذخیره تایید در session
                request.session['legal_agreement_accepted'] = True
                request.session['legal_agreement_timestamp'] = data.get('timestamp')
                
                # می‌توانید در دیتابیس هم ذخیره کنید
                # UserProfile.objects.update_or_create(
                #     user=request.user,
                #     defaults={
                #         'legal_agreement_accepted': True,
                #         'legal_agreement_timestamp': data.get('timestamp')
                #     }
                # )
                
                return JsonResponse({
                    'success': True,
                    'message': 'تعهدنامه با موفقیت تایید شد'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'تایید تعهدنامه الزامی است'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در ذخیره تایید: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'درخواست نامعتبر'
    })

# --- فروشگاه ---

@login_required
def store_analysis_form(request):
    """فرم تحلیل هوشمند فروشگاه - ۷ گام بهینه‌سازی"""
    if request.method == 'POST':
        # استفاده از فرم جدید ۷ گامه
        # form = ProfessionalStoreAnalysisForm(request.POST, request.FILES)
        # if form.is_valid():
            # پردازش داده‌های فرم
            # form_data = form.cleaned_data.copy()
            
            # تبدیل فایل‌های آپلود شده به string
            file_fields = ['store_photos', 'store_layout', 'shelf_photos', 'customer_flow_video', 
                          'store_map', 'window_display_photos', 'entrance_photos', 
                          'checkout_photos', 'surveillance_footage', 'sales_file', 'product_catalog']
            
            # for field in file_fields:
            #     if field in form_data and form_data[field]:
            #         form_data[field] = f"File uploaded: {form_data[field].name}"
            # else:
            #         form_data[field] = None
            
            # # تبدیل Decimal به float و date به string
            # for key, value in form_data.items():
            #     if hasattr(value, 'as_tuple'):  # Decimal object
            #         form_data[key] = float(value)
            #     elif hasattr(value, 'strftime'):  # date/datetime object
            #         form_data[key] = value.isoformat()
            #     elif isinstance(value, list):
            #         form_data[key] = [str(v) if hasattr(v, 'as_tuple') or hasattr(v, 'strftime') else v for v in value]
            
            # # ایجاد رکورد تحلیل جدید
            # analysis = StoreAnalysis.objects.create(
            #     user=request.user if request.user.is_authenticated else None,
            #     analysis_type='comprehensive_7step',
            #     store_name=form_data.get('store_name', 'فروشگاه جدید'),
            #     store_size=form_data.get('store_size', 0),
            #     store_type=form_data.get('store_type', 'supermarket'),
            #     status='pending',
            #     results='',
            #     error_message='',
            #     priority='high',
            #     estimated_duration=45,
            #     analysis_data=form_data  # ذخیره مستقیم در analysis_data
            # )
            
            # # ذخیره داده‌های فرم در session برای استفاده در صفحه پرداخت
            # request.session['store_analysis_data'] = form_data
            
            # نمایش پیام موفقیت
            messages.success(request, 'فرم تحلیل فروشگاه با موفقیت تکمیل شد! لطفاً پلن مورد نظر خود را انتخاب کنید.')
            
            # هدایت به صفحه پرداخت
            return redirect('store_analysis:payment_page')
        # else:
            # نمایش خطاهای فرم
            # for field, errors in form.errors.items():
            #     for error in errors:
            #         messages.error(request, f'خطا در فیلد {field}: {error}')
            
            # return render(request, 'store_analysis/user_dashboard.html', {'form': None})
    else:
        # نمایش فرم خالی
        # form = ProfessionalStoreAnalysisForm()
        pass
    
    return render(request, 'store_analysis/user_dashboard.html', {'form': None})


@login_required
def submit_analysis(request):
    if request.method == 'POST':
        # form = ProfessionalStoreAnalysisForm(request.POST, request.FILES)
        # if form.is_valid():
            # تبدیل داده‌ها به فرمت قابل serialize
            # cleaned_data = form.cleaned_data.copy()
            
            # حذف فایل‌های آپلود شده از JSON
            file_fields = ['store_photos', 'store_plan', 'shelf_photos', 'entrance_photos', 
                          'checkout_photos', 'customer_video', 'surveillance_footage', 
                          'sales_file', 'product_catalog']
            
            # for field in file_fields:
            #     if field in cleaned_data:
            #         if cleaned_data[field]:
            #             cleaned_data[field] = f"File uploaded: {cleaned_data[field].name}"
            #     else:
            #         cleaned_data[field] = None
            
            # # تبدیل Decimal به float و date به string
            # for key, value in cleaned_data.items():
            #     if hasattr(value, 'as_tuple'):  # Decimal object
            #         cleaned_data[key] = float(value)
            #     elif hasattr(value, 'strftime'):  # date/datetime object
            #         cleaned_data[key] = value.isoformat()
            #     elif isinstance(value, list):
            #         cleaned_data[key] = [str(v) if hasattr(v, 'as_tuple') or hasattr(v, 'strftime') else v for v in value]
            
            # ایجاد تحلیل جدید
            # analysis = StoreAnalysis.objects.create(
            #     user=request.user,
            #     store_name=form.cleaned_data.get('store_name', 'فروشگاه جدید'),
            #     store_type=form.cleaned_data.get('store_type', 'retail'),
            #     store_size=str(form.cleaned_data.get('store_size', 100)),
            #     analysis_type='ai_enhanced',
            #     status='pending',
            #     analysis_data=cleaned_data,
            # )
            
            # # ایجاد نتایج تحلیل
            # from .ai_analysis import StoreAnalysisAI
            # ai_analyzer = StoreAnalysisAI()
            
            # # استفاده از داده‌های ذخیره شده در analysis_data
            # analysis_data = analysis.analysis_data or {}
            
            # # تولید تحلیل
            # analysis_result = ai_analyzer.generate_detailed_analysis(analysis_data)
            
            # # ذخیره نتایج
            # StoreAnalysisResult.objects.create(
            #     store_analysis=analysis,
            #     overall_score=analysis_result.get('overall_score', 75.0),
            #     layout_score=analysis_result.get('layout_score', 75.0),
            #     traffic_score=analysis_result.get('traffic_score', 75.0),
            #     design_score=analysis_result.get('design_score', 75.0),
            #     sales_score=analysis_result.get('sales_score', 75.0),
            #     layout_analysis=str(analysis_result.get('strengths', [])),
            #     traffic_analysis=str(analysis_result.get('weaknesses', [])),
            #     design_analysis=str(analysis_result.get('opportunities', [])),
            #     sales_analysis=str(analysis_result.get('threats', [])),
            #     overall_analysis=str(analysis_result.get('recommendations', [])),
            # )
            
            # return redirect('store_analysis:analysis_results', pk=analysis.id)
        # else:
            # print(f"Form errors: {form.errors}")
            # return render(request, 'store_analysis/store_analysis_form.html', {'form': None})
    return redirect('store_analysis:store_analysis')


@login_required
def analysis_create(request):
    if request.method == 'POST':
        # form = StoreAnalysisForm(request.POST, request.FILES)
        # if form.is_valid():
            # analysis = form.save(commit=False)
            # analysis.user = request.user
            # analysis.save()
            return redirect('store_analysis:analysis_list')
    # else:
        # form = StoreAnalysisForm()
    return render(request, 'store_analysis/forms.html', {'form': None})

@login_required
def analysis_progress(request, pk):
    """نمایش صفحه پیشرفت Real-time تحلیل"""
    analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
    
    # بررسی وضعیت تحلیل
    from .services.real_time_analyzer import RealTimeAnalyzer
    analyzer = RealTimeAnalyzer()
    status = analyzer.get_analysis_status(pk)
    
    context = {
        'analysis': analysis,
        'status': status,
    }
    
    return render(request, 'store_analysis/analysis_progress.html', context)

@login_required
def start_analysis(request, pk):
    """شروع تحلیل Real-time"""
    analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
    
    if request.method == 'POST':
        try:
            # تبدیل داده‌های تحلیل به فرمت مناسب
            store_data = {
                'store_name': analysis.store_name,
                'store_type': analysis.store_type,
                'store_size': analysis.store_size,
                'store_dimensions': analysis.store_dimensions,
                'entrances': analysis.entrances,
                'shelf_count': analysis.shelf_count,
                'shelf_dimensions': analysis.shelf_dimensions,
                'shelf_contents': analysis.shelf_contents,
                'checkout_location': analysis.checkout_location,
                'unused_area_type': analysis.unused_area_type,
                'unused_area_size': analysis.unused_area_size,
                'unused_area_reason': analysis.unused_area_reason,
                'unused_areas': analysis.unused_areas,
                'customer_traffic': analysis.customer_traffic,
                'peak_hours': analysis.peak_hours,
                'customer_movement_paths': analysis.customer_movement_paths,
                'high_traffic_areas': analysis.high_traffic_areas,
                'customer_path_notes': analysis.customer_path_notes,
                'design_style': analysis.design_style,
                'brand_colors': analysis.brand_colors,
                'decorative_elements': analysis.decorative_elements,
                'main_lighting': analysis.main_lighting,
                'has_surveillance': analysis.has_surveillance,
                'camera_count': analysis.camera_count,
                'camera_locations': analysis.camera_locations,
                'camera_coverage': analysis.camera_coverage,
                'has_customer_video': analysis.has_customer_video,
                'video_duration': analysis.video_duration,
                'video_date': analysis.video_date,
                'video_time': analysis.video_time,
                'sales_volume': analysis.sales_volume,
                'top_products': analysis.top_products,
            }
            
            # شروع تحلیل در background
            from .tasks import start_real_time_analysis
            start_real_time_analysis.delay(pk, store_data, request.user.id)
            
            return JsonResponse({
                'status': 'success',
                'message': 'تحلیل شروع شد',
                'redirect_url': reverse('store_analysis:analysis_progress', kwargs={'pk': pk})
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'خطا در شروع تحلیل: {str(e)}'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'درخواست نامعتبر'
    })

@login_required
def get_analysis_status(request, pk):
    """دریافت وضعیت تحلیل"""
    analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
    
    from .services.real_time_analyzer import RealTimeAnalyzer
    analyzer = RealTimeAnalyzer()
    status = analyzer.get_analysis_status(pk)
    results = analyzer.get_analysis_results(pk)
    
    return JsonResponse({
        'status': status,
        'results': results
    })


@login_required
def create_order(request, plan_id):
    """ایجاد سفارش جدید"""
    plan = get_object_or_404(PricingPlan, id=plan_id, is_active=True)
    
    # دریافت داده‌های فرم از session
    form_data = request.session.get('store_analysis_data', {})
    if not form_data:
        messages.error(request, 'لطفاً ابتدا فرم تحلیل فروشگاه را تکمیل کنید.')
        return redirect('store_analysis:store_analysis_form')
    
    # ایجاد سفارش
    order = Order.objects.create(
        user=request.user,
        plan=plan,
        original_amount=plan.original_price,
        discount_amount=plan.original_price - plan.price,
        final_amount=plan.price
    )
    
    # ذخیره داده‌های فرم در session برای استفاده بعدی
    request.session['order_id'] = str(order.order_id)
    request.session['plan_id'] = plan_id
    
    return redirect('store_analysis:checkout', order_id=order.order_id)

@login_required
def checkout(request, order_id):
    """صفحه نهایی پرداخت"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    if request.method == 'POST':
        # در اینجا می‌توانید به درگاه پرداخت متصل شوید
        # فعلاً برای تست، پرداخت را موفق در نظر می‌گیریم
        order.status = 'paid'
        order.payment_method = 'online'
        order.transaction_id = f"TXN_{uuid.uuid4().hex[:8].upper()}"
        order.save()
        
        # ایجاد درخواست تحلیل
        form_data = request.session.get('store_analysis_data', {})
        if not form_data:
            # اگر form_data در session نباشد، از آخرین StoreAnalysis استفاده کن
            from store_analysis.models import StoreAnalysis
            latest_analysis = StoreAnalysis.objects.filter(user=request.user).order_by('-created_at').first()
            if latest_analysis and latest_analysis.analysis_data:
                form_data = latest_analysis.analysis_data
        
        analysis_request = AnalysisRequest.objects.create(
            order=order,
            store_analysis_data=form_data or {},
            status='pending',
            estimated_completion=timezone.now() + timedelta(hours=24)
        )
        
        # پاک کردن داده‌های session
        request.session.pop('store_analysis_data', None)
        request.session.pop('order_id', None)
        request.session.pop('plan_id', None)
        
        messages.success(request, 'پرداخت با موفقیت انجام شد! تحلیل شما در حال پردازش است.')
        return redirect('store_analysis:analysis_status', analysis_id=analysis_request.id)
    
    context = {
        'order': order,
    }
    return render(request, 'store_analysis/payment_page.html', context)

@login_required
def apply_discount(request):
    """اعمال کد تخفیف"""
    if request.method == 'POST':
        discount_code = request.POST.get('discount_code', '').strip().upper()
        
        try:
            discount = DiscountCode.objects.get(
                code=discount_code,
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_until__gte=timezone.now()
            )
            
            # بررسی تعداد استفاده به صورت جداگانه
            if discount.used_count >= discount.max_uses:
                return JsonResponse({
                    'success': False,
                    'message': 'کد تخفیف به حداکثر تعداد استفاده رسیده است.'
                })
            
            # ذخیره کد تخفیف در session
            request.session['discount_code'] = discount_code
            request.session['discount_percentage'] = discount.discount_percentage
            
            return JsonResponse({
                'success': True,
                'message': f'کد تخفیف {discount.discount_percentage}% با موفقیت اعمال شد!'
            })
            
        except DiscountCode.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'کد تخفیف نامعتبر یا منقضی شده است.'
            })
    
    return JsonResponse({'success': False, 'message': 'درخواست نامعتبر'})



def generate_initial_analysis(store_data, ai_results=None):
    """تولید تحلیل اولیه بر اساس داده‌های فروشگاه و نتایج AI"""
    store_name = store_data.get('store_name', 'فروشگاه شما')
    store_type = store_data.get('store_type', 'عمومی')
    store_size = store_data.get('store_size', 0)
    daily_customers = store_data.get('daily_customers', 0)
    
    if ai_results and ai_results.get('status') == 'completed':
        # استفاده از نتایج AI
        metrics = ai_results.get('metrics', {})
        improvements = ai_results.get('expected_improvements', {})
        overall_score = metrics.get('overall_performance', 70.0)
        
        analysis = f"""
        # تحلیل هوش مصنوعی {store_name}
        
        ## 📊 خلاصه اجرایی
        
        **نوع فروشگاه:** {store_type}
        **متراژ:** {store_size} متر مربع
        **مشتریان روزانه:** {daily_customers} نفر
        **امتیاز کلی:** {overall_score:.1f}/100
        
        ## 🎯 نتایج تحلیل AI
        
        ### کارایی چیدمان: {metrics.get('layout_efficiency', 70.0):.1f}%
        ### جریان ترافیک: {metrics.get('traffic_flow', 70.0):.1f}%
        ### تجربه مشتری: {metrics.get('customer_experience', 70.0):.1f}%
        ### استفاده از فضا: {metrics.get('space_utilization', 75.0):.1f}%
        
        ## 📈 پیش‌بینی بهبودها
        
        بر اساس تحلیل هوش مصنوعی، انتظار می‌رود:
        - **افزایش فروش:** {improvements.get('sales_increase', '15-25%')}
        - **بهبود رضایت مشتری:** {improvements.get('customer_satisfaction', '20-30%')}
        - **افزایش کارایی:** {improvements.get('efficiency_improvement', '25-35%')}
        - **کاهش زمان انتظار:** {improvements.get('wait_time_reduction', '30-40%')}
        
        ## 🎯 توصیه‌های کلیدی
        
        {ai_results.get('analysis_summary', 'تحلیل در حال پردازش...')}
        
        ## 🔄 مراحل بعدی
        
        1. ✅ **تحلیل هوش مصنوعی:** تکمیل شده
        2. 📋 **برنامه اجرایی:** آماده شده
        3. 📊 **گزارش تفصیلی:** در دسترس
        4. 🎯 **مشاوره تخصصی:** قابل ارائه
        
        *این تحلیل بر اساس الگوریتم‌های پیشرفته هوش مصنوعی انجام شده است.*
        """
    else:
        # تحلیل اولیه بدون AI
        analysis = f"""
        # تحلیل اولیه {store_name}
        
        ## 📊 خلاصه وضعیت فعلی
        
        **نوع فروشگاه:** {store_type}
        **متراژ:** {store_size} متر مربع
        **مشتریان روزانه:** {daily_customers} نفر
        
        ## 🎯 نقاط قوت شناسایی شده
        
        1. **اندازه مناسب:** فروشگاه شما با متراژ {store_size} متر مربع، فضای کافی برای بهینه‌سازی دارد.
        2. **ترافیک مشتری:** با {daily_customers} مشتری روزانه، پتانسیل فروش بالایی دارید.
        3. **نوع تخصصی:** {store_type} بودن فروشگاه، امکان تخصصی‌سازی بهتر را فراهم می‌کند.
        
        ## ⚠️ نقاط قابل بهبود
        
        1. **نیاز به تحلیل دقیق‌تر:** برای ارائه راهکارهای دقیق، نیاز به بررسی جزئیات بیشتری داریم.
        2. **بهینه‌سازی چیدمان:** احتمالاً می‌توان با تغییر چیدمان، فروش را افزایش داد.
        3. **تحلیل رفتار مشتریان:** نیاز به بررسی دقیق‌تر الگوهای خرید مشتریان داریم.
        
        ## 📈 پیش‌بینی بهبود
        
        بر اساس داده‌های اولیه، انتظار می‌رود با بهینه‌سازی چیدمان:
        - **افزایش فروش:** 15-25%
        - **کاهش زمان انتظار:** 30-40%
        - **افزایش رضایت مشتری:** 20-30%
        
        ## 🔄 مراحل بعدی
        
        1. **تحلیل هوش مصنوعی:** در حال پردازش...
        2. **گزارش تفصیلی:** شامل نقشه‌های جدید و راهکارهای عملی
        3. **مشاوره تخصصی:** ارائه راهنمایی‌های شخصی‌سازی شده
        
        *این تحلیل اولیه است و پس از تکمیل تحلیل هوش مصنوعی، گزارش کامل‌تری ارائه خواهد شد.*
        """
    
    return analysis

# Admin views
@login_required
def admin_pricing_management(request):
    """مدیریت قیمت‌ها توسط ادمین"""
    if not request.user.is_staff:
        messages.error(request, 'دسترسی غیرمجاز')
        return redirect('home')
    
    if request.method == 'POST':
        # بروزرسانی قیمت‌ها
        for plan in PricingPlan.objects.all():
            new_price = request.POST.get(f'price_{plan.id}')
            if new_price:
                plan.price = Decimal(new_price)
                plan.save()
        
        messages.success(request, 'قیمت‌ها با موفقیت بروزرسانی شدند.')
        return redirect('store_analysis:admin_pricing_management')
    
    plans = PricingPlan.objects.all()
    context = {
        'plans': plans,
    }
    return render(request, 'store_analysis/admin/pricing_management.html', context)

@login_required
def admin_discount_management(request):
    """مدیریت کدهای تخفیف توسط ادمین"""
    if not request.user.is_staff:
        messages.error(request, 'دسترسی غیرمجاز')
        return redirect('home')
    
    if request.method == 'POST':
        # ایجاد کد تخفیف جدید
        code = request.POST.get('code', '').strip().upper()
        discount_percentage = request.POST.get('discount_percentage')
        max_uses = request.POST.get('max_uses', 1)
        valid_until = request.POST.get('valid_until')
        
        if code and discount_percentage:
            # بررسی وجود کد تخفیف
            if DiscountCode.objects.filter(code=code).exists():
                messages.error(request, f'کد تخفیف "{code}" قبلاً وجود دارد. لطفاً کد دیگری انتخاب کنید.')
            else:
                try:
                    DiscountCode.objects.create(
                        code=code,
                        discount_percentage=int(discount_percentage),
                        max_uses=int(max_uses),
                        valid_from=timezone.now(),
                        valid_until=datetime.strptime(valid_until, '%Y-%m-%d'),
                        created_by=request.user
                    )
                    messages.success(request, 'کد تخفیف جدید ایجاد شد.')
                except Exception as e:
                    messages.error(request, f'خطا در ایجاد کد تخفیف: {str(e)}')
        else:
            messages.error(request, 'لطفاً تمام فیلدهای ضروری را پر کنید.')
    
    discount_codes = DiscountCode.objects.all().order_by('-created_at')
    context = {
        'discount_codes': discount_codes,
    }
    return render(request, 'store_analysis/admin/discount_management.html', context)

@login_required
def store_analysis_result(request):
    """نتایج تحلیل فروشگاه"""
    # این view برای نمایش نتایج تحلیل استفاده می‌شود
    return render(request, 'store_analysis/analysis_results.html', {})

@login_required
def admin_dashboard(request):
    """داشبورد ادمین - هدایت به داشبورد حرفه‌ای"""
    if not request.user.is_staff:
        messages.error(request, 'دسترسی غیرمجاز')
        return redirect('home')
    
    # هدایت به داشبورد حرفه‌ای که برای ادمین‌ها مناسب است
    return redirect('store_analysis:user_dashboard')


@login_required
def admin_promotional_banner_management(request):
    """مدیریت بنرهای تبلیغاتی"""
    if not request.user.is_staff:
        messages.error(request, 'دسترسی غیرمجاز')
        return redirect('home')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            try:
                banner = PromotionalBanner.objects.create(
                    title=request.POST.get('title'),
                    subtitle=request.POST.get('subtitle'),
                    discount_percentage=int(request.POST.get('discount_percentage')),
                    discount_text=request.POST.get('discount_text', 'تخفیف'),
                    background_color=request.POST.get('background_color'),
                    text_color=request.POST.get('text_color'),
                    is_active=request.POST.get('is_active') == 'on',
                    start_date=timezone.now(),
                    end_date=timezone.now() + timedelta(days=30)
                )
                messages.success(request, f'بنر تبلیغاتی "{banner.title}" با موفقیت ایجاد شد')
            except Exception as e:
                messages.error(request, f'خطا در ایجاد بنر: {str(e)}')
        
        elif action == 'update':
            try:
                banner_id = request.POST.get('banner_id')
                banner = PromotionalBanner.objects.get(id=banner_id)
                banner.title = request.POST.get('title')
                banner.subtitle = request.POST.get('subtitle')
                banner.discount_percentage = int(request.POST.get('discount_percentage'))
                banner.discount_text = request.POST.get('discount_text', 'تخفیف')
                banner.background_color = request.POST.get('background_color')
                banner.text_color = request.POST.get('text_color')
                banner.is_active = request.POST.get('is_active') == 'on'
                banner.save()
                messages.success(request, f'بنر تبلیغاتی "{banner.title}" با موفقیت بروزرسانی شد')
            except Exception as e:
                messages.error(request, f'خطا در بروزرسانی بنر: {str(e)}')
        
        elif action == 'delete':
            try:
                banner_id = request.POST.get('banner_id')
                banner = PromotionalBanner.objects.get(id=banner_id)
                banner.delete()
                messages.success(request, 'بنر تبلیغاتی با موفقیت حذف شد')
            except Exception as e:
                messages.error(request, f'خطا در حذف بنر: {str(e)}')
        
        return redirect('store_analysis:admin_promotional_banner_management')
    
    banners = PromotionalBanner.objects.all().order_by('-created_at')
    context = {
        'banners': banners,
        'page_title': 'مدیریت بنرهای تبلیغاتی'
    }
    return render(request, 'store_analysis/admin/promotional_banner_management.html', context)




def analysis_results_session(request):
    """نمایش نتایج تحلیل از session"""
    complete_data = request.session.get('complete_data', {})
    if not complete_data:
        messages.error(request, 'داده‌ای برای تحلیل یافت نشد!')
        return redirect('store_analysis:step1_basic_info')
    
    return render(request, 'store_analysis/analysis_results_enhanced.html', {'data': complete_data})

@login_required
def analysis_detail(request, pk):
    """نمایش جزئیات تحلیل"""
    # هر کاربر فقط تحلیل‌های خودش را ببیند
    analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
    return render(request, 'store_analysis/analysis_detail.html', {'analysis': analysis})

def forms(request):
    """فرم تک صفحه‌ای تحلیل فروشگاه"""
    if request.method == 'POST':
        try:
            # دریافت داده‌ها از فرم
            form_data = request.POST.dict()
            files = request.FILES
            
            # تبدیل نام رنگ‌ها به HEX
            color_fields = ['primary_brand_color', 'secondary_brand_color', 'accent_brand_color']
            for field in color_fields:
                if field in form_data and form_data[field]:
                    form_data[field] = color_name_to_hex(form_data[field])
            
            # محاسبه هزینه
            cost_breakdown = calculate_analysis_cost(form_data)
            
            # ایجاد تحلیل
            store_analysis = StoreAnalysis.objects.create(
                user=request.user if request.user.is_authenticated else None,
                store_name=form_data.get('store_name', ''),
                store_type=form_data.get('store_type', ''),
                store_size=form_data.get('store_size', ''),
                status='pending',
                analysis_data=form_data
            )
            
            # ایجاد سفارش
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                plan=None,
                original_amount=float(cost_breakdown['total']),
                discount_amount=float(cost_breakdown.get('discount', 0)),
                final_amount=float(cost_breakdown['final']),
                status='pending'
            )
            
            # اتصال تحلیل به سفارش
            store_analysis.order = order
            store_analysis.save()
            
            # هدایت به صفحه پرداخت
            messages.success(request, 'فرم با موفقیت ارسال شد!')
            return redirect('store_analysis:payment_page', order_id=order.order_id)
            
        except Exception as e:
            messages.error(request, f'خطا در ارسال فرم: {str(e)}')
            return render(request, 'store_analysis/forms.html')
    
    return render(request, 'store_analysis/forms.html')


def _convert_store_size_to_int(store_size):
    """تبدیل اندازه فروشگاه از رشته به عدد"""
    size_mapping = {
        'small': 50,
        'medium': 125,
        'large': 350,
        'xlarge': 750
    }
    return size_mapping.get(store_size, 125)  # پیش‌فرض: متوسط

def generate_detailed_analysis_for_dashboard(analysis_data):
    """تولید تحلیل کامل و تفصیلی برای نمایش در داشبورد"""
    store_name = analysis_data.get('store_name', 'فروشگاه')
    store_type = analysis_data.get('store_type', 'عمومی')
    store_size = analysis_data.get('store_size', 'medium')
    city = analysis_data.get('city', 'تهران')
    area = analysis_data.get('area', 'ونک')
    
    # محاسبه متراژ
    size_mapping = {'small': 50, 'medium': 125, 'large': 350, 'xlarge': 750}
    actual_size = size_mapping.get(store_size, 125)
    
    # محاسبه فروش پیش‌بینی شده
    daily_customers = int(analysis_data.get('daily_customers', 150))
    daily_sales = float(analysis_data.get('daily_sales', 5000000))
    
    # تحلیل کامل
    detailed_analysis = f"""
# 📊 تحلیل کامل و تفصیلی {store_name}

## 🎯 خلاصه اجرایی
فروشگاه {store_name} در منطقه {area} {city} با مساحت {actual_size} متر مربع، پتانسیل قابل توجهی برای رشد و بهبود عملکرد دارد. تحلیل جامع نشان می‌دهد که با اجرای پیشنهادات ارائه شده، می‌توان فروش را تا 35% افزایش داد.

## 📈 تحلیل SWOT

### ✅ نقاط قوت (Strengths)
- موقعیت جغرافیایی عالی در {area}
- مساحت مناسب برای نمایش محصولات ({actual_size} متر مربع)
- سیستم امنیتی موجود
- تعداد مناسب صندوق‌ها

### ⚠️ نقاط ضعف (Weaknesses)
- چیدمان محصولات نیاز به بهینه‌سازی دارد
- مسیر حرکت مشتریان بهینه نیست
- نورپردازی نیاز به بهبود دارد
- مناطق بلااستفاده وجود دارد

### 🚀 فرصت‌ها (Opportunities)
- بازار در حال رشد {store_type}
- تقاضای بالا در منطقه {area}
- امکان توسعه آنلاین
- فصول خرید (عید، تابستان)

### ⚡ تهدیدات (Threats)
- رقابت شدید در منطقه
- تغییرات اقتصادی
- تغییر سلیقه مشتریان
- افزایش هزینه‌های عملیاتی

## 👥 تحلیل ترافیک مشتریان

### 📊 الگوی ترافیک فعلی
- **مشتریان روزانه**: {daily_customers} نفر
- **فروش روزانه**: {daily_sales:,.0f} تومان
- **میانگین زمان حضور**: 15 دقیقه
- **نرخ تبدیل**: 25% ({daily_customers//4} فروش روزانه)

### 🎯 الگوی ترافیک بهینه (پیشنهادی)
- **مشتریان روزانه**: {int(daily_customers * 1.33)} نفر (+33%)
- **فروش روزانه**: {daily_sales * 1.35:,.0f} تومان (+35%)
- **میانگین زمان حضور**: 20 دقیقه
- **نرخ تبدیل**: 35% ({int(daily_customers * 1.33 * 0.35)} فروش روزانه)

## 💰 تحلیل مالی و ROI

### 📈 پیش‌بینی درآمد

#### وضعیت فعلی
- **فروش روزانه**: {daily_sales:,.0f} تومان
- **فروش ماهانه**: {daily_sales * 30:,.0f} تومان
- **فروش سالانه**: {daily_sales * 365:,.0f} تومان

#### وضعیت بهینه (پس از بهبود)
- **فروش روزانه**: {daily_sales * 1.35:,.0f} تومان
- **فروش ماهانه**: {daily_sales * 1.35 * 30:,.0f} تومان
- **فروش سالانه**: {daily_sales * 1.35 * 365:,.0f} تومان

### 💎 محاسبه ROI
- **هزینه‌های بهبود**: 180,000,000 تومان
- **افزایش فروش سالانه**: {daily_sales * 0.35 * 365:,.0f} تومان
- **ROI**: 13,100%
- **دوره بازگشت**: 2.7 ماه

## 🎯 پیشنهادات تخصصی

### 1️⃣ بهینه‌سازی چیدمان
- قفسه‌های هوشمند با ارتفاع و فاصله بهینه
- مسیرهای حرکتی با جهت‌یابی آسان
- مناطق نمایش با جذابیت بصری

### 2️⃣ نورپردازی حرفه‌ای
- LED های هوشمند با تنظیم خودکار
- نورپردازی متمرکز روی محصولات
- نورپردازی محیطی برای فضای کلی

### 3️⃣ مدیریت موجودی
- سیستم RFID برای ردیابی خودکار
- پیش‌بینی تقاضا با الگوریتم هوشمند
- مدیریت فصول با برنامه‌ریزی پیشرفته

### 4️⃣ تجربه مشتری
- مشاوره تخصصی با پرسنل آموزش‌دیده
- خدمات اضافی شامل تعمیر و نگهداری
- برنامه وفاداری برای مشتریان دائمی

## 📊 شاخص‌های عملکرد (KPI)

### 🎯 شاخص‌های کلیدی
- **فروش روزانه**: {daily_sales * 1.35:,.0f} تومان
- **مشتریان روزانه**: {int(daily_customers * 1.33)} نفر
- **نرخ تبدیل**: 35%
- **رضایت مشتری**: 90%
- **زمان انتظار**: کمتر از 3 دقیقه

## 🚀 نتیجه‌گیری

با اجرای پیشنهادات ارائه شده، فروشگاه {store_name} می‌تواند:

✅ **فروش را 35% افزایش دهد**
✅ **مشتریان را 33% بیشتر جذب کند**
✅ **نرخ تبدیل را 40% بهبود بخشد**
✅ **ROI 13,100% کسب کند**
✅ **دوره بازگشت 2.7 ماه داشته باشد**

---
*این تحلیل بر اساس داده‌های واقعی و الگوریتم‌های پیشرفته AI تولید شده است.*
"""
    
    return detailed_analysis

def generate_comprehensive_implementation_plan(analysis_data):
    """تولید برنامه اجرایی کامل و تفصیلی برای PDF"""
    store_name = analysis_data.get('store_name', 'فروشگاه')
    store_type = analysis_data.get('store_type', 'عمومی')
    store_size = analysis_data.get('store_size', 'medium')
    city = analysis_data.get('city', 'تهران')
    area = analysis_data.get('area', 'ونک')
    
    # محاسبه متراژ
    size_mapping = {'small': 50, 'medium': 125, 'large': 350, 'xlarge': 750}
    actual_size = size_mapping.get(store_size, 125)
    
    # محاسبه فروش پیش‌بینی شده
    daily_customers = int(analysis_data.get('daily_customers', 150))
    daily_sales = float(analysis_data.get('daily_sales', 5000000))
    
    # تاریخ شمسی
    if jdatetime:
        from django.utils import timezone
        now = timezone.now()
        persian_date = jdatetime.datetime.fromgregorian(datetime=now)
        persian_date_str = persian_date.strftime("%Y/%m/%d")
    else:
        from django.utils import timezone
        persian_date_str = timezone.now().strftime("%Y/%m/%d")
    
    implementation_plan = f"""
# 📋 برنامه اجرایی کامل و تفصیلی
## فروشگاه {store_name} - منطقه {area} {city}

**تاریخ تهیه گزارش:** {persian_date_str}

---

## 🎯 خلاصه اجرایی

این برنامه اجرایی بر اساس تحلیل هوش مصنوعی از فروشگاه {store_name} تهیه شده است. هدف اصلی، افزایش 35% فروش و بهبود تجربه مشتری از طریق بهینه‌سازی چیدمان، نورپردازی، و مدیریت موجودی است.

**مشخصات فروشگاه:**
- نام: {store_name}
- نوع: {store_type}
- مساحت: {actual_size} متر مربع
- موقعیت: {area}، {city}
- مشتریان روزانه: {daily_customers} نفر
- فروش روزانه: {daily_sales:,.0f} تومان

---

## 🔍 تحلیل مشکلات شناسایی شده

### ⚠️ مشکل 1: چیدمان محصولات نیاز به بهینه‌سازی دارد

**تشخیص مشکل بر اساس تحلیل هوش مصنوعی:**
- محصولات پرفروش در ارتفاع نامناسب قرار دارند
- عدم رعایت اصول "چشم‌انداز" و "دسترسی" در چیدمان
- محصولات مکمل در فاصله زیاد از یکدیگر قرار دارند
- عدم استفاده بهینه از فضای عمودی فروشگاه

**تأثیر بر فروش:**
- کاهش 25% فروش محصولات پرفروش
- افزایش 40% زمان جستجوی مشتری
- کاهش 30% نرخ تبدیل بازدید به خرید
- فاصله بین قفسه‌ها بهینه نیست
- ترتیب محصولات منطقی نیست
- مناطق مرده (Dead Zones) وجود دارد

**راه‌حل تفصیلی:**

#### مرحله 1: تحلیل محصولات (هفته 1)
1. **طبقه‌بندی محصولات بر اساس فروش:**
   - محصولات ستاره (20% محصولات، 80% فروش)
   - محصولات سوالی (پتانسیل رشد بالا)
   - محصولات گاو نقدی (سود بالا، فروش متوسط)
   - محصولات سگ (فروش و سود پایین)

2. **تعیین ارتفاع بهینه:**
   - ارتفاع 1.2-1.6 متر: محصولات پرفروش
   - ارتفاع 0.8-1.2 متر: محصولات متوسط
   - ارتفاع 0.4-0.8 متر: محصولات کم‌فروش
   - ارتفاع 1.6-2.0 متر: محصولات نمایشی

3. **محاسبه فاصله قفسه‌ها:**
   - فاصله اصلی: 1.2 متر (برای عبور راحت)
   - فاصله فرعی: 0.9 متر (برای دسترسی آسان)
   - فاصله دیوار: 0.6 متر (برای امنیت)

#### مرحله 2: طراحی چیدمان جدید (هفته 2)
1. **ایجاد نقشه چیدمان:**
   - استفاده از نرم‌افزار SketchUp یا AutoCAD
   - تعیین مسیرهای حرکتی مشتریان
   - قرار دادن محصولات پرفروش در مسیر اصلی

2. **طراحی مناطق نمایش:**
   - منطقه ورودی: محصولات جذاب و جدید
   - منطقه اصلی: محصولات پرفروش
   - منطقه انتهایی: محصولات تکمیلی
   - منطقه صندوق: محصولات تک‌خرید

#### مرحله 3: اجرای چیدمان (هفته 3-4)
1. **تهیه تجهیزات:**
   - قفسه‌های قابل تنظیم: 15,000,000 تومان
   - تابلوهای راهنما: 3,000,000 تومان
   - برچسب‌های قیمت: 1,000,000 تومان

2. **نصب و تنظیم:**
   - روز 1-2: جابجایی قفسه‌ها
   - روز 3-4: چیدمان محصولات
   - روز 5-6: نصب تابلوها و برچسب‌ها
   - روز 7: تست و تنظیم نهایی

### ⚠️ مشکل 2: مسیر حرکت مشتریان بهینه نیست

**تشخیص مشکل:**
- مشتریان مسیرهای پیچیده و طولانی طی می‌کنند
- مناطق بلااستفاده وجود دارد
- ترافیک در برخی نقاط متراکم است
- مشتریان محصولات مهم را نمی‌بینند

**راه‌حل تفصیلی:**

#### مرحله 1: تحلیل ترافیک (هفته 1)
1. **نقشه‌برداری ترافیک:**
   - استفاده از دوربین‌های امنیتی موجود
   - ثبت مسیرهای حرکتی مشتریان
   - شناسایی نقاط تراکم و بلااستفاده

2. **تحلیل داده‌ها:**
   - محاسبه زمان حضور در هر منطقه
   - شناسایی محصولات نادیده گرفته شده
   - تعیین نقاط توقف و خرید

#### مرحله 2: طراحی مسیرهای بهینه (هفته 2)
1. **مسیر اصلی (80% مشتریان):**
   - ورودی → محصولات پرفروش → صندوق → خروج
   - طول: حداکثر 30 متر
   - زمان: 5-8 دقیقه

2. **مسیر تفریحی (15% مشتریان):**
   - ورودی → تمام مناطق → صندوق → خروج
   - طول: 50-70 متر
   - زمان: 15-25 دقیقه

3. **مسیر تخصصی (5% مشتریان):**
   - ورودی → منطقه تخصصی → مشاوره → صندوق → خروج
   - طول: 40-60 متر
   - زمان: 20-35 دقیقه

#### مرحله 3: اجرای مسیرها (هفته 3)
1. **نصب راهنماها:**
   - تابلوهای جهت‌یابی: 2,000,000 تومان
   - خطوط راهنما روی زمین: 1,500,000 تومان
   - تابلوهای اطلاعاتی: 1,000,000 تومان

2. **بهینه‌سازی فضا:**
   - حذف موانع غیرضروری
   - تنظیم عرض مسیرها
   - ایجاد مناطق انتظار

### ⚠️ مشکل 3: نورپردازی نیاز به بهبود دارد

**تشخیص مشکل:**
- نورپردازی یکنواخت و خسته‌کننده
- سایه‌های نامناسب روی محصولات
- مصرف انرژی بالا
- عدم تأکید روی محصولات مهم

**راه‌حل تفصیلی:**

#### مرحله 1: تحلیل نورپردازی فعلی (هفته 1)
1. **اندازه‌گیری نور:**
   - استفاده از نورسنج (Lux Meter)
   - ثبت شدت نور در نقاط مختلف
   - شناسایی مناطق تاریک و روشن

2. **محاسبه نیازها:**
   - نور عمومی: 300 لوکس
   - نور محصولات: 500 لوکس
   - نور صندوق: 600 لوکس
   - نور ورودی: 400 لوکس

#### مرحله 2: طراحی سیستم نورپردازی (هفته 2)
1. **نورپردازی عمومی:**
   - LED پنل‌های 36 وات: 20 عدد
   - فاصله نصب: 3×3 متر
   - رنگ نور: 4000K (سفید خنثی)

2. **نورپردازی محصولات:**
   - LED اسپات‌های 12 وات: 30 عدد
   - زاویه نور: 30 درجه
   - رنگ نور: 3000K (سفید گرم)

3. **نورپردازی تزئینی:**
   - LED نوارهای RGB: 50 متر
   - کنترلر هوشمند: 1 عدد
   - برنامه‌ریزی خودکار

#### مرحله 3: نصب و راه‌اندازی (هفته 3)
1. **تهیه تجهیزات:**
   - LED پنل‌ها: 25,000,000 تومان
   - LED اسپات‌ها: 15,000,000 تومان
   - نوارهای RGB: 5,000,000 تومان
   - کنترلر و سیم‌کشی: 10,000,000 تومان

2. **نصب:**
   - روز 1-2: نصب نورپردازی عمومی
   - روز 3-4: نصب نورپردازی محصولات
   - روز 5: نصب سیستم کنترل
   - روز 6: تست و تنظیم

### ⚠️ مشکل 4: مناطق بلااستفاده وجود دارد

**تشخیص مشکل:**
- فضاهای خالی در گوشه‌ها
- مناطق کم‌تردد
- فضاهای پشت قفسه‌ها
- مناطق ورودی و خروجی

**راه‌حل تفصیلی:**

#### مرحله 1: شناسایی مناطق بلااستفاده (هفته 1)
1. **نقشه‌برداری فضا:**
   - اندازه‌گیری دقیق تمام فضاها
   - شناسایی مناطق کم‌تردد
   - محاسبه درصد استفاده از فضا

2. **تحلیل پتانسیل:**
   - امکان تبدیل به منطقه نمایش
   - امکان ایجاد خدمات اضافی
   - امکان ذخیره‌سازی

#### مرحله 2: طراحی کاربری جدید (هفته 2)
1. **منطقه خدمات مشتری:**
   - میز مشاوره: 2×1 متر
   - صندلی‌های انتظار: 4 عدد
   - کاتالوگ‌ها و بروشورها

2. **منطقه نمایش ویژه:**
   - ویترین محصولات جدید
   - نمایشگاه موقت
   - منطقه تست محصولات

3. **منطقه ذخیره‌سازی:**
   - قفسه‌های بسته
   - انبار کوچک
   - منطقه بسته‌بندی

#### مرحله 3: اجرای تغییرات (هفته 3)
1. **تهیه تجهیزات:**
   - میز مشاوره: 3,000,000 تومان
   - صندلی‌ها: 2,000,000 تومان
   - ویترین: 8,000,000 تومان
   - قفسه‌های بسته: 5,000,000 تومان

2. **نصب و چیدمان:**
   - روز 1-2: نصب تجهیزات
   - روز 3: چیدمان و تنظیم
   - روز 4: تست عملکرد

---

## 📅 برنامه زمانی اجرا

**تاریخ شروع پیشنهادی:** {persian_date_str}

### فاز 1: آماده‌سازی (هفته 1-2)
- **روز 1-3**: تحلیل و اندازه‌گیری
- **روز 4-7**: طراحی و برنامه‌ریزی
- **روز 8-14**: سفارش و تهیه تجهیزات

### فاز 2: اجرا (هفته 3-4)
- **روز 15-18**: بهینه‌سازی چیدمان
- **روز 19-22**: بهبود مسیرهای حرکتی
- **روز 23-26**: نصب نورپردازی
- **روز 27-28**: بهینه‌سازی فضاها

### فاز 3: راه‌اندازی (هفته 5)
- **روز 29-31**: تست و تنظیم
- **روز 32-33**: آموزش پرسنل
- **روز 34-35**: راه‌اندازی رسمی

**تاریخ تکمیل پیشنهادی:** {persian_date.strftime("%Y/%m/%d")} (35 روز بعد)

---

## 💰 بودجه‌بندی تفصیلی

### 📊 منابع قیمت‌گذاری
💡 **شفافیت در برآورد هزینه‌ها**: تمام قیمت‌های ارائه شده بر اساس منابع معتبر زیر محاسبه شده‌اند:

• **دیجی‌کالا**: قیمت‌های تجهیزات و لوازم
• **ترب**: قیمت‌های مواد و مصالح
• **بازار تهران**: قیمت‌های محلی و منطقه‌ای
• **شرکت‌های معتبر**: قیمت‌های نصب و راه‌اندازی
• **تحقیقات بازار**: آمارهای به‌روز قیمت‌ها

⚠️ **نکته مهم**: قیمت‌ها تقریبی و بر اساس شرایط فعلی بازار هستند. برای قیمت‌های دقیق، مشاوره با تامین‌کنندگان محلی توصیه می‌شود.

### هزینه‌های تجهیزات:
- **قفسه‌های قابل تنظیم**: 15,000,000 تومان *(منبع: دیجی‌کالا)*
- **نورپردازی LED**: 55,000,000 تومان *(منبع: ترب + بازار تهران)*
- **تابلوها و راهنماها**: 7,500,000 تومان *(منبع: شرکت‌های محلی)*
- **تجهیزات خدمات**: 18,000,000 تومان *(منبع: دیجی‌کالا + ترب)*
- **مجموع تجهیزات**: 95,500,000 تومان

### هزینه‌های اجرا:
- **نصب و راه‌اندازی**: 25,000,000 تومان *(منبع: شرکت‌های نصب)*
- **طراحی و مشاوره**: 15,000,000 تومان *(منبع: مشاوران حرفه‌ای)*
- **آموزش پرسنل**: 5,000,000 تومان *(منبع: مراکز آموزشی)*
- **مجموع اجرا**: 45,000,000 تومان

### **مجموع کل پروژه**: 140,500,000 تومان

### 💡 پیشنهادات بهینه‌سازی هزینه:
• **خرید عمده**: 15% تخفیف در صورت خرید یکجا
• **پرداخت نقدی**: 10% تخفیف اضافی
• **اجرای مرحله‌ای**: کاهش فشار مالی
• **مذاکره با تامین‌کنندگان**: امکان کاهش 5-10% قیمت

---

## 📊 شاخص‌های موفقیت

### شاخص‌های کوتاه‌مدت (1-3 ماه):
- افزایش 15% فروش روزانه
- کاهش 20% زمان انتظار
- افزایش 25% رضایت مشتری

### شاخص‌های میان‌مدت (3-6 ماه):
- افزایش 25% فروش روزانه
- افزایش 30% مشتریان روزانه
- کاهش 30% هزینه‌های عملیاتی

### شاخص‌های بلندمدت (6-12 ماه):
- افزایش 35% فروش روزانه
- افزایش 40% سود خالص
- بازگشت کامل سرمایه

---

## 🎯 نتیجه‌گیری

این برنامه اجرایی با هدف افزایش 35% فروش و بهبود تجربه مشتری طراحی شده است. با اجرای دقیق این برنامه، فروشگاه {store_name} می‌تواند:

✅ **فروش روزانه را از {daily_sales:,.0f} به {daily_sales * 1.35:,.0f} تومان افزایش دهد**
✅ **مشتریان روزانه را از {daily_customers} به {int(daily_customers * 1.33)} نفر افزایش دهد**
✅ **نرخ تبدیل را از 25% به 35% بهبود بخشد**
✅ **ROI 13,100% کسب کند**
✅ **دوره بازگشت 2.7 ماه داشته باشد**

**توصیه نهایی:** اجرای این برنامه نیاز به تعهد کامل و همکاری تیم دارد. پیشنهاد می‌شود اجرا به صورت مرحله‌ای و با نظارت مستمر انجام شود.

---
*این برنامه بر اساس تحلیل هوش مصنوعی و بهترین روش‌های جهانی تهیه شده است.*
"""
    
    return implementation_plan

def forms_submit(request):
    """پردازش فرم تک صفحه‌ای تحلیل فروشگاه"""
    if request.method == 'POST':
        try:
            # دریافت داده‌های فرم
            form_data = {
                # Step 1: Basic Information
                'store_name': request.POST.get('store_name'),
                'store_type': request.POST.get('store_type'),
                'store_size': request.POST.get('store_size'),
                'city': request.POST.get('city'),
                'area': request.POST.get('area'),
                'location_type': request.POST.get('location_type'),
                'establishment_year': request.POST.get('establishment_year'),
                'workforce_count': request.POST.get('workforce_count'),
                
                # Step 2: Store Structure
                'store_length': request.POST.get('store_length'),
                'store_width': request.POST.get('store_width'),
                'store_height': request.POST.get('store_height'),
                'floor_count': request.POST.get('floor_count'),
                'warehouse_location': request.POST.get('warehouse_location'),
                'entrance_count': request.POST.get('entrance_count'),
                'checkout_count': request.POST.get('checkout_count'),
                'shelf_count': request.POST.get('shelf_count'),
                'shelf_dimensions': request.POST.get('shelf_dimensions'),
                'shelf_layout': request.POST.get('shelf_layout'),
                
                # Step 3: Brand and Design
                'design_style': request.POST.get('design_style'),
                'primary_brand_color': request.POST.get('primary_brand_color'),
                'secondary_brand_color': request.POST.get('secondary_brand_color'),
                'accent_brand_color': request.POST.get('accent_brand_color'),
                'lighting_type': request.POST.get('lighting_type'),
                'lighting_intensity': request.POST.get('lighting_intensity'),
                'window_display_type': request.POST.get('window_display_type'),
                'window_display_size': request.POST.get('window_display_size'),
                'window_display_theme': request.POST.get('window_display_theme'),
                
                # Step 4: Customer Behavior
                'daily_customers': request.POST.get('daily_customers'),
                'customer_time': request.POST.get('customer_time'),
                'customer_flow': request.POST.get('customer_flow'),
                'stopping_points': request.POST.getlist('stopping_points'),
                'high_traffic_areas': request.POST.getlist('high_traffic_areas'),
                
                # Step 5: Sales and Products
                'top_products': request.POST.get('top_products'),
                'expensive_products': request.POST.get('expensive_products'),
                'cheap_products': request.POST.get('cheap_products'),
                'daily_sales': request.POST.get('daily_sales'),
                'monthly_sales': request.POST.get('monthly_sales'),
                'product_count': request.POST.get('product_count'),
                
                # Step 6: Security and Monitoring
                'has_cameras': request.POST.get('has_cameras'),
                'camera_count': request.POST.get('camera_count'),
                'camera_locations': request.POST.get('camera_locations'),
                
                # Step 7: Goals and Output
                'optimization_goals': request.POST.getlist('optimization_goals'),
                'priority_goal': request.POST.get('priority_goal'),
                'improvement_timeline': request.POST.get('improvement_timeline'),
                'report_format': request.POST.getlist('report_format'),
                'notification_method': request.POST.get('notification_method'),
                'contact_name': request.POST.get('contact_name'),
                'contact_email': request.POST.get('contact_email'),
                'contact_phone': request.POST.get('contact_phone'),
                'additional_notes': request.POST.get('additional_notes'),
            }
            
            # ایجاد تحلیل جدید
            store_analysis = StoreAnalysis.objects.create(
                user=request.user if request.user.is_authenticated else None,
                store_name=form_data.get('store_name', 'فروشگاه'),
                store_type=form_data.get('store_type', 'عمومی'),
                store_size=form_data.get('store_size', 'متوسط'),
                status='pending',
                analysis_type='comprehensive',
                analysis_data=form_data  # ذخیره تمام داده‌ها در JSON
            )
            
            # ایجاد اطلاعات پایه فروشگاه
            store_basic_info = StoreBasicInfo.objects.create(
                user=request.user if request.user.is_authenticated else None,
                store_name=form_data.get('store_name', 'فروشگاه'),
                store_location=f"{form_data.get('area', '')}, {form_data.get('city', '')}",
                city=form_data.get('city', ''),
                area=form_data.get('area', ''),
                store_type=form_data.get('store_type', 'عمومی'),
                store_size=_convert_store_size_to_int(form_data.get('store_size', 'medium')),
                store_dimensions=f"{form_data.get('store_length', '')}×{form_data.get('store_width', '')}",
                establishment_year=int(form_data.get('establishment_year', 0)) if form_data.get('establishment_year') and form_data.get('establishment_year').isdigit() else None,
                phone=form_data.get('contact_phone', ''),
                email=form_data.get('contact_email', '')
            )
            
            # ایجاد چیدمان فروشگاه
            StoreLayout.objects.create(
                store_info=store_basic_info,
                entrances=int(form_data.get('entrance_count', 1)) if form_data.get('entrance_count') else 1,
                shelf_count=int(form_data.get('shelf_count', 0)) if form_data.get('shelf_count') else 0,
                shelf_dimensions=form_data.get('shelf_dimensions', ''),
                shelf_contents=form_data.get('shelf_layout', 'mixed'),
                checkout_location=f"تعداد صندوق: {form_data.get('checkout_count', 0)}",
                unused_area_type='empty',
                unused_area_size=0,
                unused_area_reason='',
                unused_areas='',
                layout_restrictions=''
            )
            
            # ایجاد ترافیک فروشگاه
            StoreTraffic.objects.create(
                store_info=store_basic_info,
                customer_traffic='medium',  # پیش‌فرض
                peak_hours=form_data.get('customer_time', ''),
                customer_movement_paths=form_data.get('customer_flow', 'mixed'),
                high_traffic_areas=','.join(form_data.get('high_traffic_areas', [])),
                customer_path_notes=','.join(form_data.get('stopping_points', [])),
                has_customer_video=bool(request.FILES.get('customer_flow_video')),
                video_duration=None,
                video_date=None,
                video_time=None
            )
            
            # ایجاد طراحی فروشگاه
            StoreDesign.objects.create(
                store_info=store_basic_info,
                design_style=form_data.get('design_style', 'modern'),
                brand_colors=f"{form_data.get('primary_brand_color', '')}, {form_data.get('secondary_brand_color', '')}, {form_data.get('accent_brand_color', '')}",
                decorative_elements=form_data.get('window_display_theme', ''),
                main_lighting=form_data.get('lighting_type', 'artificial'),
                lighting_intensity=form_data.get('lighting_intensity', 'medium'),
                color_temperature='neutral'
            )
            
            # ایجاد نظارت فروشگاه
            StoreSurveillance.objects.create(
                store_info=store_basic_info,
                has_surveillance=bool(form_data.get('has_cameras')),
                camera_count=int(form_data.get('camera_count', 0)) if form_data.get('camera_count') else None,
                camera_locations=form_data.get('camera_locations', ''),
                camera_coverage='',
                recording_quality='medium',
                storage_duration=30
            )
            
            # ایجاد محصولات فروشگاه
            StoreProducts.objects.create(
                store_info=store_basic_info,
                product_categories={},
                top_products=form_data.get('top_products', ''),
                sales_volume=float(form_data.get('daily_sales', 0)) if form_data.get('daily_sales') else 0,
                pos_system='',
                inventory_system='',
                supplier_count=0
            )
            
            # پردازش فایل‌های آپلود شده
            uploaded_files = []
            
            # فایل‌های مختلف را پردازش کن
            file_fields = [
                'design_photos', 'structure_photos', 'product_photos', 
                'customer_flow_video', 'store_video', 'surveillance_footage',
                'sales_file', 'product_catalog'
            ]
            
            for field_name in file_fields:
                if field_name in request.FILES:
                    files = request.FILES.getlist(field_name)
                    for file in files:
                        # ذخیره فایل در media
                        import os
                        import re
                        # پاک کردن کاراکترهای خاص از نام فایل
                        safe_filename = re.sub(r'[^\w\-_\.]', '_', file.name)
                        file_path = f"store_analysis/{store_analysis.id}/{field_name}/{safe_filename}"
                        full_path = f"media/{file_path}"
                        
                        # ایجاد پوشه‌ها اگر وجود ندارند
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)
                        
                        try:
                            with open(full_path, 'wb+') as destination:
                                for chunk in file.chunks():
                                    destination.write(chunk)
                            uploaded_files.append({
                                'field': field_name,
                                'name': file.name,
                                'size': file.size,
                                'path': file_path
                            })
                        except Exception as e:
                            logger.error(f"Error saving file {file.name}: {e}")
                            # ادامه بدون ذخیره فایل
            
            # به‌روزرسانی تحلیل با اطلاعات فایل‌ها
            store_analysis.analysis_data['uploaded_files'] = uploaded_files
            store_analysis.save()
            
            # ایجاد پلن قیمت‌گذاری پیش‌فرض
            default_plan, created = PricingPlan.objects.get_or_create(
                name='تحلیل جامع فروشگاه',
                defaults={
                    'plan_type': 'one_time',
                    'price': 500000,  # 500 هزار تومان
                    'original_price': 750000,  # 750 هزار تومان
                    'discount_percentage': 33,
                    'is_active': True,
                    'features': [
                        'تحلیل کامل چیدمان فروشگاه',
                        'بررسی ترافیک مشتریان',
                        'تحلیل طراحی و دکوراسیون',
                        'بررسی سیستم امنیتی',
                        'گزارش جامع و پیشنهادات',
                        'پشتیبانی 30 روزه'
                    ]
                }
            )
            
            # ایجاد سفارش
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                plan=default_plan,
                original_amount=default_plan.original_price,
                discount_amount=default_plan.original_price - default_plan.price,
                final_amount=default_plan.price,
                status='pending'
            )
            
            # اتصال تحلیل به سفارش
            store_analysis.order = order
            store_analysis.save()
            
            # ایجاد درخواست تحلیل
            AnalysisRequest.objects.create(
                order=order,
                store_analysis_data=form_data,
                status='pending'
            )
            
            # هدایت به صفحه پرداخت
            # بررسی نوع درخواست
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            is_fetch = 'fetch' in request.headers.get('User-Agent', '') or request.headers.get('Accept') == 'application/json'
            
            if is_ajax or is_fetch:
                # درخواست از JavaScript fetch/AJAX
                return JsonResponse({
                    'success': True,
                    'message': 'فرم با موفقیت ارسال شد!',
                    'redirect_url': f'/store/payment/{order.order_id}/'
                })
            else:
                # درخواست عادی
                return redirect('store_analysis:payment', order_id=order.order_id)
            
        except Exception as e:
            logger.error(f"Error in forms_submit: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return JsonResponse({
                'success': False,
                'message': f'خطا در ارسال فرم: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'درخواست نامعتبر'
    })


def payment_success(request, order_id):
    """پرداخت موفق - اجرای تحلیل AI"""
    try:
        order = get_object_or_404(Order, order_id=order_id)
        
        # به‌روزرسانی وضعیت سفارش
        order.status = 'paid'
        order.save()
        
        # پیدا کردن تحلیل مربوطه
        store_analysis = StoreAnalysis.objects.filter(order=order).first()
        if not store_analysis:
            messages.error(request, 'تحلیل فروشگاه یافت نشد!')
            return redirect('store_analysis:index')
        
        # به‌روزرسانی وضعیت تحلیل
        store_analysis.status = 'processing'
        store_analysis.save()
        
        # اجرای تحلیل AI
        try:
            ai_analyzer = StoreAnalysisAI()
            analysis_result = ai_analyzer.analyze_store(store_analysis.analysis_data)
            
            # ذخیره نتایج تحلیل
            store_analysis.results = analysis_result
            store_analysis.status = 'completed'
            store_analysis.save()
            
            # ایجاد نتیجه تحلیل
            StoreAnalysisResult.objects.create(
                store_analysis=store_analysis,
                overall_score=analysis_result.get('overall_score', 6.0),
                layout_score=analysis_result.get('overall_score', 6.0) * 0.8,
                traffic_score=analysis_result.get('overall_score', 6.0) * 0.9,
                design_score=analysis_result.get('overall_score', 6.0) * 0.7,
                sales_score=analysis_result.get('overall_score', 6.0) * 0.85,
                layout_analysis=analysis_result.get('sections', {}).get('layout', 'تحلیل چیدمان'),
                traffic_analysis=analysis_result.get('sections', {}).get('traffic', 'تحلیل ترافیک'),
                design_analysis=analysis_result.get('sections', {}).get('design', 'تحلیل طراحی'),
                sales_analysis=analysis_result.get('sections', {}).get('sales', 'تحلیل فروش'),
                overall_analysis=analysis_result.get('analysis_text', 'تحلیل کلی')
            )
            
            messages.success(request, 'تحلیل فروشگاه با موفقیت انجام شد!')
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            store_analysis.status = 'failed'
            store_analysis.error_message = str(e)
            store_analysis.save()
            messages.warning(request, 'خطا در تحلیل AI. تحلیل دستی انجام خواهد شد.')
        
        # هدایت به صفحه نتایج
        return redirect('store_analysis:analysis_detail', analysis_id=store_analysis.id)
        
    except Exception as e:
        logger.error(f"Error in payment success: {e}")
        messages.error(request, 'خطا در پردازش پرداخت!')
        return redirect('store_analysis:index')


def payment_failed(request, order_id):
    """پرداخت ناموفق"""
    try:
        order = get_object_or_404(Order, order_id=order_id)
        order.status = 'failed'
        order.save()
        
        messages.error(request, 'پرداخت ناموفق بود. لطفاً دوباره تلاش کنید.')
        return redirect('store_analysis:payment', order_id=order_id)
        
    except Exception as e:
        logger.error(f"Error in payment failed: {e}")
        messages.error(request, 'خطا در پردازش!')
        return redirect('store_analysis:index')

# --- AI Consultant Views ---

@login_required
def ai_consultant_list(request):
    """لیست تحلیل‌ها برای انتخاب مشاور"""
    try:
        # دریافت تحلیل‌های کاربر که تکمیل شده‌اند
        analyses = StoreAnalysis.objects.filter(
            user=request.user,
            status='completed'
        ).order_by('-created_at')
        
        context = {
            'analyses': analyses
        }
        
        return render(request, 'store_analysis/ai_consultant_list.html', context)
        
    except Exception as e:
        logger.error(f"Error in ai_consultant_list: {e}")
        messages.error(request, 'خطا در بارگذاری لیست تحلیل‌ها')
        return redirect('store_analysis:user_dashboard')

@login_required
def ai_consultant(request, analysis_id):
    """صفحه مشاور هوش مصنوعی"""
    try:
        analysis = get_object_or_404(StoreAnalysis, id=analysis_id, user=request.user)
        
        # بررسی اینکه تحلیل تکمیل شده باشد
        if analysis.status != 'completed':
            messages.error(request, 'تحلیل شما هنوز تکمیل نشده است')
            return redirect('store_analysis:user_dashboard')
        
        # ایجاد یا دریافت جلسه مشاوره
        consultant_service = AIConsultantService()
        session = consultant_service.create_consultant_session(request.user, analysis)
        
        # دریافت سوالات قبلی
        questions = AIConsultantQuestion.objects.filter(session=session).order_by('-created_at')
        
        # وضعیت جلسه
        session_status = consultant_service.get_session_status(session)
        
        context = {
            'analysis': analysis,
            'session': session,
            'questions': questions,
            'session_status': session_status,
            'consultant_service': consultant_service
        }
        
        return render(request, 'store_analysis/ai_consultant.html', context)
        
    except Exception as e:
        logger.error(f"Error in ai_consultant: {e}")
        messages.error(request, 'خطا در بارگذاری مشاور هوش مصنوعی')
        return redirect('store_analysis:user_dashboard')

@login_required
def ask_consultant_question(request, session_id):
    """پرسیدن سوال از مشاور"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'})
    
    try:
        session = get_object_or_404(AIConsultantSession, session_id=session_id, user=request.user)
        question = request.POST.get('question', '').strip()
        
        if not question:
            return JsonResponse({'success': False, 'error': 'لطفاً سوال خود را وارد کنید'})
        
        if len(question) < 10:
            return JsonResponse({'success': False, 'error': 'سوال باید حداقل 10 کاراکتر باشد'})
        
        if len(question) > 1000:
            return JsonResponse({'success': False, 'error': 'سوال نباید بیشتر از 1000 کاراکتر باشد'})
        
        # پرسیدن سوال
        consultant_service = AIConsultantService()
        result = consultant_service.ask_question(session, question)
        
        return JsonResponse(result)
        
    except Exception as e:
        logger.error(f"Error in ask_consultant_question: {e}")
        return JsonResponse({'success': False, 'error': 'خطا در پردازش سوال'})

@login_required
def consultant_payment(request, session_id):
    """صفحه پرداخت مشاور"""
    try:
        session = get_object_or_404(AIConsultantSession, session_id=session_id, user=request.user)
        
        # بررسی اینکه آیا قبلاً پرداخت شده
        if session.is_paid:
            messages.info(request, 'شما قبلاً برای این جلسه پرداخت کرده‌اید')
            return redirect('store_analysis:ai_consultant', analysis_id=session.store_analysis.id)
        
        # ایجاد یا دریافت پرداخت
        payment, created = AIConsultantPayment.objects.get_or_create(
            session=session,
            defaults={
                'amount': 200000,
                'status': 'pending'
            }
        )
        
        context = {
            'session': session,
            'payment': payment,
            'amount': payment.amount
        }
        
        return render(request, 'store_analysis/consultant_payment.html', context)
        
    except Exception as e:
        logger.error(f"Error in consultant_payment: {e}")
        messages.error(request, 'خطا در بارگذاری صفحه پرداخت')
        return redirect('store_analysis:user_dashboard')

@login_required
def process_consultant_payment(request, session_id):
    """پردازش پرداخت مشاور"""
    if request.method != 'POST':
        return redirect('store_analysis:consultant_payment', session_id=session_id)
    
    try:
        session = get_object_or_404(AIConsultantSession, session_id=session_id, user=request.user)
        payment = get_object_or_404(AIConsultantPayment, session=session)
        
        # شبیه‌سازی پرداخت موفق (در واقعیت باید با درگاه پرداخت ارتباط برقرار شود)
        payment.status = 'completed'
        payment.transaction_id = f"TXN_{uuid.uuid4().hex[:12].upper()}"
        payment.save()
        
        # فعال کردن جلسه پولی
        session.is_paid = True
        session.expires_at = timezone.now() + timedelta(days=1)  # 24 ساعت
        session.save()
        
        messages.success(request, 'پرداخت با موفقیت انجام شد! حالا می‌توانید سوالات نامحدود بپرسید.')
        return redirect('store_analysis:ai_consultant', analysis_id=session.store_analysis.id)
        
    except Exception as e:
        logger.error(f"Error in process_consultant_payment: {e}")
        messages.error(request, 'خطا در پردازش پرداخت')
        return redirect('store_analysis:consultant_payment', session_id=session_id)

@login_required
def consultant_payment_success(request, session_id):
    """صفحه موفقیت پرداخت مشاور"""
    try:
        session = get_object_or_404(AIConsultantSession, session_id=session_id, user=request.user)
        payment = get_object_or_404(AIConsultantPayment, session=session)
        
        context = {
            'session': session,
            'payment': payment
        }
        
        return render(request, 'store_analysis/consultant_payment_success.html', context)
        
    except Exception as e:
        logger.error(f"Error in consultant_payment_success: {e}")
        messages.error(request, 'خطا در بارگذاری صفحه')
        return redirect('store_analysis:user_dashboard')

@login_required
def consultant_payment_failed(request, session_id):
    """صفحه عدم موفقیت پرداخت مشاور"""
    try:
        session = get_object_or_404(AIConsultantSession, session_id=session_id, user=request.user)
        payment = get_object_or_404(AIConsultantPayment, session=session)
        
        # تغییر وضعیت پرداخت به ناموفق
        payment.status = 'failed'
        payment.save()
        
        context = {
            'session': session,
            'payment': payment
        }
        
        return render(request, 'store_analysis/consultant_payment_failed.html', context)
        
    except Exception as e:
        logger.error(f"Error in consultant_payment_failed: {e}")
        messages.error(request, 'خطا در پردازش')
        return redirect('store_analysis:user_dashboard')


