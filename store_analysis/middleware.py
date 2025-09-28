"""
Middleware for tracking page views and analytics
"""

import uuid
from django.utils.deprecation import MiddlewareMixin
from django.db import transaction
from django.utils import timezone
from .models import PageView, SiteStats
from django.contrib.auth.models import User
from datetime import date


class AnalyticsMiddleware(MiddlewareMixin):
    """Middleware to track page views and user analytics"""
    
    def process_request(self, request):
        """Process incoming request and track analytics"""
        try:
            # Skip tracking for certain paths
            skip_paths = [
                '/admin/',
                '/static/',
                '/media/',
                '/favicon.ico',
                '/robots.txt',
                '/sitemap.xml',
            ]
            
            if any(request.path.startswith(path) for path in skip_paths):
                return None
            
            # Get or create session ID
            if 'analytics_session_id' not in request.session:
                request.session['analytics_session_id'] = str(uuid.uuid4())
            
            # Track page view
            self.track_page_view(request)
            
        except Exception as e:
            # Log error but don't break the request
            print(f"Analytics middleware error: {e}")
        
        return None
    
    def track_page_view(self, request):
        """Track individual page view"""
        try:
            with transaction.atomic():
                # Get user info
                user = request.user if request.user.is_authenticated else None
                
                # Get IP address
                ip_address = self.get_client_ip(request)
                
                # Get referrer
                referrer = request.META.get('HTTP_REFERER', '')
                if referrer and len(referrer) > 500:  # Limit referrer length
                    referrer = referrer[:500]
                
                # Create page view record
                PageView.objects.create(
                    page_url=request.build_absolute_uri(),
                    page_title=self.get_page_title(request),
                    user=user,
                    ip_address=ip_address,
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                    referrer=referrer if referrer else None,
                    session_id=request.session.get('analytics_session_id', ''),
                )
                
                # Update daily stats
                self.update_daily_stats(request, user)
                
        except Exception as e:
            print(f"Error tracking page view: {e}")
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_page_title(self, request):
        """Get page title from request"""
        # This is a simplified version - in real implementation,
        # you might want to get the actual page title
        path = request.path
        if path == '/':
            return 'صفحه اصلی - چیدمانو'
        elif '/store/' in path:
            return 'فروشگاه - چیدمانو'
        elif '/dashboard/' in path:
            return 'داشبورد - چیدمانو'
        elif '/support/' in path:
            return 'پشتیبانی - چیدمانو'
        else:
            return f'صفحه {path} - چیدمانو'
    
    def update_daily_stats(self, request, user):
        """Update daily statistics"""
        try:
            today = date.today()
            stats, created = SiteStats.objects.get_or_create(
                date=today,
                defaults={
                    'total_views': 0,
                    'unique_visitors': 0,
                    'new_users': 0,
                    'page_views': 0,
                }
            )
            
            # Update stats
            stats.total_views += 1
            stats.page_views += 1
            
            # Check if this is a unique visitor (by session)
            session_id = request.session.get('analytics_session_id', '')
            if not PageView.objects.filter(
                session_id=session_id,
                created_at__date=today
            ).exists():
                stats.unique_visitors += 1
            
            # Check if this is a new user
            if user and not User.objects.filter(
                id=user.id,
                date_joined__date=today
            ).exists():
                stats.new_users += 1
            
            stats.save()
            
        except Exception as e:
            print(f"Error updating daily stats: {e}")