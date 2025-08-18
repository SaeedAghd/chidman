from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from .models import StoreAnalysis, StoreAnalysisResult, DetailedAnalysis, Payment, Article, ArticleCategory
from .forms import StoreAnalysisForm, PaymentForm, AIStoreAnalysisForm
from django.db.models import Q

# --- فروشگاه ---

@method_decorator(login_required, name='dispatch')
class StoreAnalysisListView(ListView):
    """نمایش لیست تحلیل‌های فروشگاه کاربر"""
    model = StoreAnalysis
    template_name = 'store_analysis/analysis_list.html'
    context_object_name = 'analyses'
    paginate_by = 10

    def get_queryset(self):
        """فقط تحلیل‌های کاربر فعلی"""
        return StoreAnalysis.objects.filter(user=self.request.user).order_by('-created_at')


@method_decorator(login_required, name='dispatch')
class StoreAnalysisDetailView(DetailView):
    """نمایش جزئیات تحلیل فروشگاه"""
    model = StoreAnalysis
    template_name = 'store_analysis/analysis_detail.html'
    context_object_name = 'analysis'

    def get_queryset(self):
        """فقط تحلیل‌های کاربر فعلی"""
        return StoreAnalysis.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class StoreAnalysisCreateView(CreateView):
    """ایجاد تحلیل جدید فروشگاه"""
    model = StoreAnalysis
    form_class = StoreAnalysisForm
    template_name = 'store_analysis/analysis_form.html'

    def form_valid(self, form):
        """تنظیم کاربر برای تحلیل جدید"""
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class StoreAnalysisUpdateView(UpdateView):
    """ویرایش تحلیل فروشگاه"""
    model = StoreAnalysis
    form_class = StoreAnalysisForm
    template_name = 'store_analysis/analysis_form.html'

    def get_queryset(self):
        """فقط تحلیل‌های کاربر فعلی"""
        return StoreAnalysis.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class StoreAnalysisDeleteView(DeleteView):
    """حذف تحلیل فروشگاه"""
    model = StoreAnalysis
    template_name = 'store_analysis/analysis_confirm_delete.html'
    success_url = reverse_lazy('store_analysis:analysis_list')

    def get_queryset(self):
        """فقط تحلیل‌های کاربر فعلی"""
        return StoreAnalysis.objects.filter(user=self.request.user)


@login_required
def analysis_result(request, pk):
    analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
    try:
        result = analysis.analysis_result
    except StoreAnalysisResult.DoesNotExist:
        result = None
    return render(request, 'store_analysis/analysis_result.html', {
        'analysis': analysis,
        'result': result,
    })


@login_required
def detailed_analysis_view(request, pk):
    analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
    try:
        detailed = analysis.detailed_analysis_data
    except DetailedAnalysis.DoesNotExist:
        detailed = None
    return render(request, 'store_analysis/detailed_analysis.html', {
        'analysis': analysis,
        'detailed': detailed,
    })

@login_required
def check_analysis_status(request, pk):
    analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
    data = {
        'status': analysis.status,
        'error_message': analysis.error_message,
    }
    return JsonResponse(data)


# --- پرداخت ---

@method_decorator(login_required, name='dispatch')
class PaymentListView(ListView):
    model = Payment
    template_name = 'store_analysis/payment_list.html'
    context_object_name = 'payments'

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')

@login_required
def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            return redirect('store_analysis:payment_list')
    else:
        form = PaymentForm()
    return render(request, 'store_analysis/payment_form.html', {'form': form})

# --- مقالات ---

class ArticleListView(ListView):
    model = Article
    template_name = 'store_analysis/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = Article.objects.all().order_by('-created_at')
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(summary__icontains=search) |
                Q(tags__icontains=search)
            )
        return queryset

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'store_analysis/article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class ArticleCategoryListView(ListView):
    model = ArticleCategory
    template_name = 'store_analysis/article_category_list.html'
    context_object_name = 'categories'

class ArticlesByCategoryView(ListView):
    model = Article
    template_name = 'store_analysis/articles_by_category.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        category = get_object_or_404(ArticleCategory, slug=category_slug)
        return Article.objects.filter(category=category).order_by('-created_at')

# --- صفحه اصلی ---

def index(request):
    # می‌توانید داده‌ها را برای داشبورد یا صفحه اول آماده کنید
    return render(request, 'store_analysis/index.html')

def education_library(request):
    # می‌توانید بعداً این بخش را کامل‌تر کنید
    return render(request, 'store_analysis/education.html')

def features(request):
    return render(request, 'store_analysis/features.html')

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'store_analysis/article_detail.html', {'article': article})

from .forms import StoreAnalysisForm, AIStoreAnalysisForm

def store_analysis_form(request):
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
                request.session['quick_analysis_data'] = quick_data
                request.session['analysis_id'] = analysis.id
                
                # Show success message
                messages.success(request, 'درخواست تحلیل رایگان شما با موفقیت ثبت شد!')
                return redirect('store_analysis:analysis_results', pk=analysis.id)
            else:
                messages.error(request, 'لطفاً تمام فیلدهای الزامی را پر کنید.')
                return redirect('store_analysis:index')
        
        # Full AI form submission
        form = AIStoreAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data
            form_data = form.cleaned_data
            
            # Create a new analysis record
            analysis = StoreAnalysis.objects.create(
                user=request.user if request.user.is_authenticated else None,
                status='pending',
                results='',
                error_message='',
                priority='medium',
                estimated_duration=30
            )
            
            # Store form data in session for processing
            request.session['analysis_data'] = form_data
            request.session['analysis_id'] = analysis.id
            
            return redirect('store_analysis:analysis_results', pk=analysis.id)
        else:
            return render(request, 'store_analysis/store_analysis_form.html', {'form': form})
    else:
        form = AIStoreAnalysisForm()
    return render(request, 'store_analysis/store_analysis_form.html', {'form': form})

def submit_analysis(request):
    if request.method == 'POST':
        form = StoreAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            analysis = form.save(commit=False)
            if request.user.is_authenticated:
                analysis.user = request.user
            analysis.save()
            return redirect('store_analysis:analysis_list')
        else:
            return render(request, 'store_analysis/store_analysis_form.html', {'form': form})
    return redirect('store_analysis:store_analysis')

@login_required
def analysis_results(request, pk):
    analysis = get_object_or_404(StoreAnalysis, pk=pk, user=request.user)
    results = StoreAnalysisResult.objects.filter(store_analysis=analysis)
    return render(request, 'store_analysis/analysis_results.html', {
        'analysis': analysis,
        'results': results,
    })

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


