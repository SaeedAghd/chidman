"""
Views مخصوص ادمین برای مدیریت قیمت‌گذاری و تخفیف‌ها
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from .models import DiscountCode, Payment, StoreAnalysis
import json

@staff_member_required
def pricing_management(request):
    """مدیریت قیمت‌گذاری"""
    # آمار قیمت‌گذاری
    pricing_stats = {
        'total_revenue': Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0,
        'monthly_revenue': Payment.objects.filter(
            status='completed',
            created_at__gte=timezone.now() - timedelta(days=30)
        ).aggregate(total=Sum('amount'))['total'] or 0,
        'total_analyses': StoreAnalysis.objects.count(),
        'paid_analyses': StoreAnalysis.objects.filter(
            payments__status='completed'
        ).count(),
    }
    
    # آمار نوع فروشگاه
    store_type_stats = StoreAnalysis.objects.values('store_info__store_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'pricing_stats': pricing_stats,
        'store_type_stats': store_type_stats,
        'title': 'مدیریت قیمت‌گذاری'
    }
    
    return render(request, 'store_analysis/admin/pricing_management.html', context)

@staff_member_required
def discount_management(request):
    """مدیریت تخفیف‌ها"""
    discounts = DiscountCode.objects.all().order_by('-created_at')
    
    # آمار تخفیف‌ها
    discount_stats = {
        'total_discounts': discounts.count(),
        'active_discounts': discounts.filter(is_active=True).count(),
        'expired_discounts': discounts.filter(valid_until__lt=timezone.now()).count(),
        'total_usage': discounts.aggregate(total=Sum('used_count'))['total'] or 0,
    }
    
    context = {
        'discounts': discounts,
        'discount_stats': discount_stats,
        'title': 'مدیریت تخفیف‌ها'
    }
    
    return render(request, 'store_analysis/admin/discount_management.html', context)

@staff_member_required
@require_http_methods(["POST"])
def create_discount_code(request):
    """ایجاد کد تخفیف جدید"""
    try:
        data = json.loads(request.body)
        
        discount = DiscountCode.objects.create(
            code=data['code'],
            description=data.get('description', ''),
            discount_type=data['discount_type'],
            percentage=data.get('percentage', 0),
            fixed_amount=data.get('fixed_amount', 0),
            event_type=data.get('event_type', 'general'),
            max_usage=data.get('max_usage', 100),
            min_order_amount=data.get('min_order_amount', 0),
            valid_from=datetime.fromisoformat(data['valid_from']) if data.get('valid_from') else timezone.now(),
            valid_until=datetime.fromisoformat(data['valid_until']) if data.get('valid_until') else timezone.now() + timedelta(days=30),
            is_active=data.get('is_active', True)
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'کد تخفیف با موفقیت ایجاد شد',
            'discount_id': discount.id
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'خطا در ایجاد کد تخفیف: {str(e)}'
        })

@staff_member_required
@require_http_methods(["POST"])
def toggle_discount_status(request, discount_id):
    """تغییر وضعیت کد تخفیف"""
    try:
        discount = get_object_or_404(DiscountCode, id=discount_id)
        discount.is_active = not discount.is_active
        discount.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'وضعیت کد تخفیف {discount.code} تغییر کرد',
            'is_active': discount.is_active
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'خطا در تغییر وضعیت: {str(e)}'
        })

@staff_member_required
def support_ticket_management(request):
    """مدیریت تیکت‌های پشتیبانی"""
    from .models import SupportTicket, TicketMessage
    
    # فیلترها
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    category_filter = request.GET.get('category', '')
    
    tickets = SupportTicket.objects.select_related('user', 'assigned_to').order_by('-created_at')
    
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)
    if category_filter:
        tickets = tickets.filter(category=category_filter)
    
    # آمار تیکت‌ها
    ticket_stats = {
        'total_tickets': SupportTicket.objects.count(),
        'open_tickets': SupportTicket.objects.filter(status='open').count(),
        'in_progress_tickets': SupportTicket.objects.filter(status='in_progress').count(),
        'resolved_tickets': SupportTicket.objects.filter(status='resolved').count(),
        'urgent_tickets': SupportTicket.objects.filter(priority='urgent').count(),
    }
    
    context = {
        'tickets': tickets,
        'ticket_stats': ticket_stats,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'category_filter': category_filter,
        'title': 'مدیریت تیکت‌های پشتیبانی'
    }
    
    return render(request, 'store_analysis/admin/support_ticket_management.html', context)

@staff_member_required
@require_http_methods(["POST"])
def assign_ticket(request, ticket_id):
    """واگذاری تیکت به ادمین"""
    try:
        from .models import SupportTicket
        from django.contrib.auth.models import User
        
        ticket = get_object_or_404(SupportTicket, id=ticket_id)
        data = json.loads(request.body)
        
        if data.get('assigned_to'):
            assigned_user = get_object_or_404(User, id=data['assigned_to'])
            ticket.assigned_to = assigned_user
        else:
            ticket.assigned_to = None
            
        ticket.status = data.get('status', ticket.status)
        ticket.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'تیکت با موفقیت به‌روزرسانی شد'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'خطا در به‌روزرسانی تیکت: {str(e)}'
        })

@staff_member_required
def system_analytics(request):
    """تحلیل‌های سیستم"""
    # آمار کلی
    analytics = {
        'user_growth': [],
        'revenue_trend': [],
        'analysis_completion_rate': 0,
        'popular_store_types': [],
        'peak_hours': [],
    }
    
    # رشد کاربران (7 روز گذشته)
    for i in range(7):
        date = timezone.now() - timedelta(days=i)
        user_count = User.objects.filter(date_joined__date=date.date()).count()
        analytics['user_growth'].append({
            'date': date.strftime('%Y-%m-%d'),
            'count': user_count
        })
    
    # روند درآمد (7 روز گذشته)
    for i in range(7):
        date = timezone.now() - timedelta(days=i)
        revenue = Payment.objects.filter(
            created_at__date=date.date(),
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        analytics['revenue_trend'].append({
            'date': date.strftime('%Y-%m-%d'),
            'amount': revenue
        })
    
    # نرخ تکمیل تحلیل‌ها
    total_analyses = StoreAnalysis.objects.count()
    completed_analyses = StoreAnalysis.objects.filter(status='completed').count()
    if total_analyses > 0:
        analytics['analysis_completion_rate'] = (completed_analyses / total_analyses) * 100
    
    # محبوب‌ترین نوع فروشگاه
    analytics['popular_store_types'] = list(
        StoreAnalysis.objects.values('store_info__store_type').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
    )
    
    context = {
        'analytics': analytics,
        'title': 'تحلیل‌های سیستم'
    }
    
    return render(request, 'store_analysis/admin/system_analytics.html', context)
