from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import render
from store_analysis.models import StoreAnalysis

@staff_member_required
def admin_dashboard(request):
    # آمار کلیدی
    total_analyses = StoreAnalysis.objects.count()
    pending = StoreAnalysis.objects.filter(status='pending').count()
    processing = StoreAnalysis.objects.filter(status='processing').count()
    completed = StoreAnalysis.objects.filter(status='completed').count()
    failed = StoreAnalysis.objects.filter(status='failed').count()
    users = StoreAnalysis.objects.values('user').distinct().count()
    
    context = {
        'total_analyses': total_analyses,
        'pending': pending,
        'processing': processing,
        'completed': completed,
        'failed': failed,
        'users': users,
    }
    return render(request, 'admin/custom_dashboard.html', context)
