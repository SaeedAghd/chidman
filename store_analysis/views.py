from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse

from django.conf import settings
import json
import os
from datetime import datetime, timedelta
from .models import StoreAnalysis, StoreBasicInfo, DetailedAnalysis, StoreAnalysisResult
from .ai_analysis import StoreAnalysisAI
from .forms import StoreAnalysisForm, AIStoreAnalysisForm

# --- صفحه اصلی ---

def index(request):
    """صفحه اصلی - تشخیص مشکل فروشگاه"""
    context = {}
    
    if request.user.is_authenticated:
        # آمار برای کاربران ورود کرده
        user_analyses = StoreAnalysis.objects.filter(user=request.user)
        context.update({
            'total_analyses': user_analyses.count(),
            'completed_analyses': user_analyses.filter(status='completed').count(),
            'processing_analyses': user_analyses.filter(status='processing').count(),
            'pending_analyses': user_analyses.filter(status='pending').count(),
        })
    
    return render(request, 'store_analysis/index.html', context)

def problem_detection(request):
    """تشخیص مشکل فروشگاه با AI"""
    if request.method == 'POST':
        # دریافت تصاویر و داده‌های فروشگاه
        form = AIStoreAnalysisForm(request.POST, request.FILES)
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
        form = AIStoreAnalysisForm()
    
    context = {
        'form': form,
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
    
    paginator = Paginator(analyses, 10)
    page = request.GET.get('page')
    analyses = paginator.get_page(page)
    
    context = {
        'analyses': analyses,
        'is_admin': request.user.is_staff or request.user.is_superuser,
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
        conversion_rate = analysis_data.get('conversion_rate', 35)
        customer_traffic = analysis_data.get('customer_traffic', 150)
        store_size = analysis_data.get('store_size', 500)
        unused_area_size = analysis_data.get('unused_area_size', 0)
        
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
    
    context = {
        'analysis': analysis,
        'result': result,
        'scores': scores,
        'has_ai_results': has_ai_results,
        'show_management_report': show_management_report,
        'is_admin': is_admin,
    }
    return render(request, 'store_analysis/analysis_results.html', context)

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
    """داشبورد کاربری"""
    # آمار تحلیل‌ها
    total_analyses = StoreAnalysis.objects.filter(user=request.user).count()
    completed_analyses = StoreAnalysis.objects.filter(user=request.user, status='completed').count()
    pending_analyses = StoreAnalysis.objects.filter(user=request.user, status='pending').count()
    processing_analyses = StoreAnalysis.objects.filter(user=request.user, status='processing').count()
    
    # آخرین تحلیل‌ها
    recent_analyses = StoreAnalysis.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # تحلیل‌های قابل دانلود
    downloadable_analyses = StoreAnalysis.objects.filter(
        user=request.user, 
        status__in=['preliminary_completed', 'completed']
    ).order_by('-created_at')[:3]
    
    context = {
        'total_analyses': total_analyses,
        'completed_analyses': completed_analyses,
        'pending_analyses': pending_analyses,
        'processing_analyses': processing_analyses,
        'recent_analyses': recent_analyses,
        'downloadable_analyses': downloadable_analyses,
    }
    
    return render(request, 'store_analysis/user_dashboard.html', context)

@login_required
def professional_dashboard(request):
    """پنل کاربری فوق حرفه‌ای"""
    user = request.user
    
    # آمار کلی
    total_analyses = StoreAnalysis.objects.filter(user=user).count()
    completed_analyses = StoreAnalysis.objects.filter(user=user, status='completed').count()
    pending_analyses = StoreAnalysis.objects.filter(user=user, status='pending').count()
    processing_analyses = StoreAnalysis.objects.filter(user=user, status='processing').count()
    
    total_score = 0
    if completed_analyses > 0:
        results = StoreAnalysisResult.objects.filter(store_analysis__user=user)
        if results.exists():
            total_score = sum([r.overall_score for r in results]) / results.count()
    
    # تحلیل‌های اخیر با جزئیات
    recent_analyses = StoreAnalysis.objects.filter(user=user).order_by('-created_at')[:10]
    
    # پیشنهادات هوشمند
    smart_suggestions = []
    if completed_analyses > 0:
        # تولید پیشنهادات بر اساس تحلیل‌های قبلی
        smart_suggestions = [
            "بر اساس تحلیل‌های قبلی، پیشنهاد می‌شود روی بهبود نورپردازی تمرکز کنید",
            "چیدمان قفسه‌های شما نیاز به بهینه‌سازی دارد",
            "ترافیک مشتریان در ساعات خاصی از روز قابل بهبود است"
        ]
    
    # نمودار پیشرفت
    progress_data = {
        'labels': ['تحلیل‌های تکمیل شده', 'در حال پردازش', 'در انتظار'],
        'data': [completed_analyses, processing_analyses, pending_analyses],
        'colors': ['#28a745', '#ffc107', '#6c757d']
    }
    
    context = {
        'user': user,
        'total_analyses': total_analyses,
        'completed_analyses': completed_analyses,
        'total_score': round(total_score, 1),
        'recent_analyses': recent_analyses,
        'smart_suggestions': smart_suggestions,
        'progress_data': progress_data,
        'is_admin': user.is_staff or user.is_superuser,
    }
    
    return render(request, 'store_analysis/professional_dashboard.html', context)

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

# --- فروشگاه ---

@login_required
def store_analysis_form(request):
    """Smart Store Analysis Form"""
    if request.method == 'POST':
        # Check if it's a quick form submission
        if 'store_name' in request.POST and 'store_size' in request.POST:
            # Quick free form submission
            store_name = request.POST.get('store_name')
            store_size = request.POST.get('store_size')
            store_type = request.POST.get('store_type')
            email = request.POST.get('email')
            
            if store_name and store_size and store_type and email:
                # Create a new analysis record
                analysis = StoreAnalysis.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    analysis_type='quick_free',
                    store_name=store_name,
                    store_size=store_size,
                    store_type=store_type,
                    status='pending',
                    results='',
                    error_message='',
                    priority='medium',
                    estimated_duration=15
                )
                
                # Store quick form data
                quick_data = {
                    'store_name': store_name,
                    'store_size': store_size,
                    'store_type': store_type,
                    'email': email,
                    'analysis_type': 'quick_free'
                }
                analysis.set_analysis_data(quick_data)
                
                # Show success message
                messages.success(request, 'Your free analysis request has been successfully registered!')
                return redirect('store_analysis:analysis_results', pk=analysis.id)
            else:
                messages.error(request, 'Please fill in all required fields.')
                return redirect('store_analysis:index')
        
        # Full AI form submission
        form = StoreAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data
            form_data = form.cleaned_data
            
            # Create a new analysis record
            analysis = StoreAnalysis.objects.create(
                user=request.user if request.user.is_authenticated else None,
                analysis_type='comprehensive',
                store_name=form_data.get('store_name', 'Unknown'),
                store_size=form_data.get('store_size', 0),
                store_type=form_data.get('store_type', 'retail'),
                status='pending',
                results='',
                error_message='',
                priority='medium',
                estimated_duration=30
            )
            
            # Store form data
            analysis.set_analysis_data(form_data)
            
            # Redirect to analysis results page
            return redirect('store_analysis:analysis_results', pk=analysis.id)
        else:
            return render(request, 'store_analysis/store_analysis_form.html', {'form': form})
    else:
        form = StoreAnalysisForm()
    return render(request, 'store_analysis/store_analysis_form.html', {'form': form})


@login_required
def submit_analysis(request):
    if request.method == 'POST':
        form = AIStoreAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            # تبدیل داده‌ها به فرمت قابل serialize
            cleaned_data = form.cleaned_data.copy()
            
            # حذف فایل‌های آپلود شده از JSON
            file_fields = ['store_photos', 'store_plan', 'shelf_photos', 'entrance_photos', 
                          'checkout_photos', 'customer_video', 'surveillance_footage', 
                          'sales_file', 'product_catalog']
            
            for field in file_fields:
                if field in cleaned_data:
                    if cleaned_data[field]:
                        cleaned_data[field] = f"File uploaded: {cleaned_data[field].name}"
        else:
                        cleaned_data[field] = None
            
            # تبدیل Decimal به float و date به string
            for key, value in cleaned_data.items():
                if hasattr(value, 'as_tuple'):  # Decimal object
                    cleaned_data[key] = float(value)
                elif hasattr(value, 'strftime'):  # date/datetime object
                    cleaned_data[key] = value.isoformat()
                elif isinstance(value, list):
                    cleaned_data[key] = [str(v) if hasattr(v, 'as_tuple') or hasattr(v, 'strftime') else v for v in value]
            
            # ایجاد تحلیل جدید
            analysis = StoreAnalysis.objects.create(
                user=request.user,
                store_name=form.cleaned_data.get('store_name', 'فروشگاه جدید'),
                store_type=form.cleaned_data.get('store_type', 'retail'),
                store_size=str(form.cleaned_data.get('store_size', 100)),
                analysis_type='ai_enhanced',
                status='pending',
                analysis_data=cleaned_data,
            )
            
            # ایجاد نتایج تحلیل
            from .ai_analysis import StoreAnalysisAI
            ai_analyzer = StoreAnalysisAI()
            
            # استفاده از داده‌های ذخیره شده در analysis_data
            analysis_data = analysis.analysis_data or {}
            
            # تولید تحلیل
            analysis_result = ai_analyzer.generate_detailed_analysis(analysis_data)
            
            # ذخیره نتایج
            StoreAnalysisResult.objects.create(
                store_analysis=analysis,
                overall_score=analysis_result.get('overall_score', 75.0),
                layout_score=analysis_result.get('layout_score', 75.0),
                traffic_score=analysis_result.get('traffic_score', 75.0),
                design_score=analysis_result.get('design_score', 75.0),
                sales_score=analysis_result.get('sales_score', 75.0),
                layout_analysis=str(analysis_result.get('strengths', [])),
                traffic_analysis=str(analysis_result.get('weaknesses', [])),
                design_analysis=str(analysis_result.get('opportunities', [])),
                sales_analysis=str(analysis_result.get('threats', [])),
                overall_analysis=str(analysis_result.get('recommendations', [])),
            )
            
            return redirect('store_analysis:analysis_results', pk=analysis.id)
        else:
            print(f"Form errors: {form.errors}")
            return render(request, 'store_analysis/store_analysis_form.html', {'form': form})
    return redirect('store_analysis:store_analysis')


@login_required
def analysis_create(request):
    if request.method == 'POST':
        form = StoreAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.user = request.user
            analysis.save()
            return redirect('store_analysis:analysis_list')
    else:
        form = StoreAnalysisForm()
    return render(request, 'store_analysis/store_analysis_form.html', {'form': form})

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


