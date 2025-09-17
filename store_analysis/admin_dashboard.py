"""
Dashboard سفارشی برای پنل ادمین
"""

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import (
    StoreAnalysis, SupportTicket, Payment, AIConsultantSession,
    DiscountCode, FAQ, EmailVerification, Wallet, Transaction, Order
)
from django.contrib.auth.models import User

class AdminDashboard:
    """کلاس مدیریت dashboard ادمین"""
    
    @staticmethod
    def get_dashboard_stats():
        """دریافت آمار کلی dashboard"""
        now = timezone.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        # محاسبه زمان پردازش متوسط
        completed_analyses = StoreAnalysis.objects.filter(status='completed')
        avg_processing_time = 0
        if completed_analyses.exists():
            total_time = 0
            count = 0
            for analysis in completed_analyses:
                if analysis.updated_at and analysis.created_at:
                    processing_time = (analysis.updated_at - analysis.created_at).total_seconds() / 60
                    total_time += processing_time
                    count += 1
            if count > 0:
                avg_processing_time = round(total_time / count, 1)
        
        stats = {
            # آمار کلی
            'total_users': User.objects.count(),
            'new_users_today': User.objects.filter(date_joined__date=today).count(),
            'total_analyses': StoreAnalysis.objects.count(),
            'analyses_today': StoreAnalysis.objects.filter(created_at__date=today).count(),
            'completed_analyses': StoreAnalysis.objects.filter(status='completed').count(),
            'pending_analyses': StoreAnalysis.objects.filter(status='pending').count(),
            'processing_analyses': StoreAnalysis.objects.filter(status='processing').count(),
            'avg_processing_time': avg_processing_time,
            
            # آمار تیکت‌ها
            'open_tickets': SupportTicket.objects.filter(status__in=['open', 'in_progress']).count(),
            'new_tickets_today': SupportTicket.objects.filter(created_at__date=today).count(),
            
            # آمار مالی
            'total_revenue': Payment.objects.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0,
            'revenue_today': Payment.objects.filter(created_at__date=today, status='completed').aggregate(total=Sum('amount'))['total'] or 0,
            'successful_payments': Payment.objects.filter(status='completed').count(),
            'pending_payments': Payment.objects.filter(status='pending').count(),
            'cancelled_payments': Payment.objects.filter(status='cancelled').count(),
            
            # آمار کیف پول
            'total_wallets': Wallet.objects.count(),
            'active_wallets': Wallet.objects.filter(is_active=True).count(),
            
            # آمار فضای ذخیره‌سازی (شبیه‌سازی)
            'storage_usage': 65,  # درصد استفاده از فضای ذخیره‌سازی
            
            # آمار ماه
            'month_analyses': StoreAnalysis.objects.filter(created_at__gte=month_ago).count(),
            'month_tickets': SupportTicket.objects.filter(created_at__gte=month_ago).count(),
            'month_revenue': Payment.objects.filter(
                created_at__gte=month_ago, 
                status='completed'
            ).aggregate(total=Sum('amount'))['total'] or 0,
            
            # آمار تیکت‌ها
            'open_tickets': SupportTicket.objects.filter(status='open').count(),
            'in_progress_tickets': SupportTicket.objects.filter(status='in_progress').count(),
            'resolved_tickets': SupportTicket.objects.filter(status='resolved').count(),
            
            # آمار کدهای تخفیف
            'active_discounts': DiscountCode.objects.filter(is_active=True).count(),
            'expired_discounts': DiscountCode.objects.filter(valid_until__lt=now).count(),
            
            # آمار FAQ
            'total_faqs': FAQ.objects.count(),
            'active_faqs': FAQ.objects.filter(is_active=True).count(),
            
            # آمار تاییدیه ایمیل
            'pending_verifications': EmailVerification.objects.filter(is_verified=False).count(),
            'verified_today': EmailVerification.objects.filter(
                is_verified=True, 
                updated_at__date=today
            ).count(),
        }
        
        return stats
    
    @staticmethod
    def get_chart_data():
        """دریافت داده‌های نمودارها"""
        now = timezone.now()
        labels = []
        users_data = []
        analyses_data = []
        
        # داده‌های 7 روز گذشته
        for i in range(7):
            date = now - timedelta(days=6-i)
            date_str = date.strftime('%Y-%m-%d')
            labels.append(date.strftime('%m/%d'))
            
            users_count = User.objects.filter(date_joined__date=date.date()).count()
            analyses_count = StoreAnalysis.objects.filter(created_at__date=date.date()).count()
            
            users_data.append(users_count)
            analyses_data.append(analyses_count)
        
        return {
            'labels': labels,
            'users_data': users_data,
            'analyses_data': analyses_data
        }
    
    @staticmethod
    def get_recent_activities():
        """دریافت فعالیت‌های اخیر"""
        activities = []
        
        # تحلیل‌های اخیر
        recent_analyses = StoreAnalysis.objects.select_related('user', 'store_info').order_by('-created_at')[:5]
        for analysis in recent_analyses:
            store_name = analysis.store_info.store_name if analysis.store_info else 'نامشخص'
            activities.append({
                'type': 'analysis',
                'title': f'تحلیل جدید: {store_name}',
                'description': f'کاربر {analysis.user.username} - وضعیت: {analysis.get_status_display()}',
                'time': analysis.created_at,
                'status': analysis.status,
                'icon': '📊'
            })
        
        # تیکت‌های اخیر
        recent_tickets = SupportTicket.objects.select_related('user').order_by('-created_at')[:5]
        for ticket in recent_tickets:
            activities.append({
                'type': 'ticket',
                'title': f'تیکت جدید: {ticket.subject}',
                'description': f'کاربر {ticket.user.username} - اولویت: {ticket.get_priority_display()}',
                'time': ticket.created_at,
                'status': ticket.status,
                'icon': '🎫'
            })
        
        # پرداخت‌های اخیر
        recent_payments = Payment.objects.select_related('user').order_by('-created_at')[:5]
        for payment in recent_payments:
            activities.append({
                'type': 'payment',
                'title': f'پرداخت جدید: {payment.amount:,} تومان',
                'description': f'کاربر {payment.user.username} - روش: {payment.get_payment_method_display()}',
                'time': payment.created_at,
                'status': payment.status,
                'icon': '💳'
            })
        
        # کاربران جدید
        recent_users = User.objects.order_by('-date_joined')[:3]
        for user in recent_users:
            activities.append({
                'type': 'user',
                'title': f'کاربر جدید: {user.username}',
                'description': f'ایمیل: {user.email} - وضعیت: {"فعال" if user.is_active else "غیرفعال"}',
                'time': user.date_joined,
                'status': 'active' if user.is_active else 'inactive',
                'icon': '👤'
            })
        
        # مرتب‌سازی بر اساس زمان
        activities.sort(key=lambda x: x['time'], reverse=True)
        return activities[:10]
    
    @staticmethod
    def get_chart_data():
        """دریافت داده‌های نمودار"""
        now = timezone.now()
        days = []
        analysis_data = []
        ticket_data = []
        payment_data = []
        
        # داده‌های 7 روز گذشته
        for i in range(7):
            date = (now - timedelta(days=i)).date()
            days.append(date.strftime('%m/%d'))
            
            # تعداد تحلیل‌ها
            analyses = StoreAnalysis.objects.filter(created_at__date=date).count()
            analysis_data.append(analyses)
            
            # تعداد تیکت‌ها
            tickets = SupportTicket.objects.filter(created_at__date=date).count()
            ticket_data.append(tickets)
            
            # درآمد
            revenue = Payment.objects.filter(
                created_at__date=date, 
                status='completed'
            ).aggregate(total=Sum('amount'))['total'] or 0
            payment_data.append(revenue)
        
        return {
            'days': list(reversed(days)),
            'analyses': list(reversed(analysis_data)),
            'tickets': list(reversed(ticket_data)),
            'payments': list(reversed(payment_data))
        }

def admin_dashboard_view(request):
    """نمایش dashboard ادمین"""
    if not request.user.is_superuser:
        return render(request, 'admin/access_denied.html')
    
    stats = AdminDashboard.get_dashboard_stats()
    activities = AdminDashboard.get_recent_activities()
    chart_data = AdminDashboard.get_chart_data()
    
    context = {
        'stats': stats,
        'recent_activities': activities,
        'chart_labels': chart_data['days'],
        'chart_users_data': chart_data['analyses'],
        'chart_analyses_data': chart_data['tickets'],
        'title': 'Dashboard ادمین',
        'has_permission': True,
    }
    
    return render(request, 'admin/custom_dashboard.html', context)

# اضافه کردن URL به admin
def get_admin_urls():
    """دریافت URL های admin با dashboard"""
    from django.contrib.admin.sites import AdminSite
    
    # فقط یک بار اضافه کردن
    if not hasattr(AdminSite, '_custom_urls_added'):
        original_get_urls = AdminSite.get_urls
        
        def custom_get_urls(self):
            """URL های سفارشی admin"""
            urls = original_get_urls(self)
            custom_urls = [
                path('dashboard/', self.admin_view(admin_dashboard_view), name='admin_dashboard'),
            ]
            return custom_urls + urls
        
        AdminSite.get_urls = custom_get_urls
        AdminSite._custom_urls_added = True

# فعال کردن URL های سفارشی
get_admin_urls()