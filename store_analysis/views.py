from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from .models import StoreAnalysis, StoreAnalysisResult, DetailedAnalysis, Payment, Article, ArticleCategory
from .forms import StoreAnalysisForm, PaymentForm  # فرم‌های خودت را بساز یا اصلاح کن
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
    return render(request, 'store_analysis/education_library.html')

def features(request):
    return render(request, 'store_analysis/features.html')

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'store_analysis/article_detail.html', {'article': article})

from .forms import StoreAnalysisForm

def store_analysis_form(request):
    if request.method == 'POST':
        form = StoreAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store_analysis:index')
    else:
        form = StoreAnalysisForm()
    return render(request, 'store_analysis/store_analysis_form.html', {'form': form})

def submit_analysis(request):
    if request.method == 'POST':
        form = StoreAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
