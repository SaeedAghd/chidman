"""
Query optimization service for store analysis application.
"""

import logging
from django.db import connection
from django.core.cache import cache
from django.db.models import Q, Prefetch, Count, Sum
from django.conf import settings

logger = logging.getLogger(__name__)

class QueryOptimizer:
    """Optimize database queries for better performance."""
    
    def __init__(self):
        self.query_count = 0
        self.slow_queries = []
    
    def optimize_store_analysis_queryset(self, queryset, user=None):
        """Optimize StoreAnalysis queryset."""
        if user:
            queryset = queryset.filter(user=user)
        
        # Select related fields to avoid N+1 queries
        queryset = queryset.select_related(
            'user',
            'analysis_result'
        ).prefetch_related(
            'product_categories'
        )
        
        # Only fetch necessary fields
        queryset = queryset.only(
            'id', 'store_name', 'store_type', 'status', 'created_at',
            'user__username', 'user__email'
        )
        
        return queryset
    
    def optimize_payment_queryset(self, queryset, user=None):
        """Optimize Payment queryset."""
        if user:
            queryset = queryset.filter(user=user)
        
        queryset = queryset.select_related('user').only(
            'id', 'amount', 'payment_method', 'status', 'created_at',
            'user__username'
        )
        
        return queryset
    
    def optimize_article_queryset(self, queryset):
        """Optimize Article queryset."""
        queryset = queryset.select_related('category').only(
            'id', 'title', 'summary', 'slug', 'is_featured',
            'category__title', 'category__slug'
        )
        
        return queryset
    
    def batch_update_analyses(self, analysis_ids, updates):
        """Batch update multiple analyses efficiently."""
        try:
            from ..models import StoreAnalysis
            
            # Use bulk_update for efficiency
            analyses = StoreAnalysis.objects.filter(id__in=analysis_ids)
            for analysis in analyses:
                for field, value in updates.items():
                    setattr(analysis, field, value)
            
            StoreAnalysis.objects.bulk_update(analyses, list(updates.keys()))
            logger.info(f"Batch updated {len(analyses)} analyses")
            
        except Exception as e:
            logger.error(f"Error in batch update: {e}")
            raise
    
    def get_analytics_data(self, user=None, date_range=None):
        """Get analytics data with optimized queries."""
        from ..models import StoreAnalysis, Payment
        
        # Base queryset
        base_qs = StoreAnalysis.objects.all()
        if user:
            base_qs = base_qs.filter(user=user)
        
        if date_range:
            base_qs = base_qs.filter(created_at__range=date_range)
        
        # Get counts efficiently
        analytics = {
            'total_analyses': base_qs.count(),
            'completed_analyses': base_qs.filter(status='completed').count(),
            'pending_analyses': base_qs.filter(status='pending').count(),
            'processing_analyses': base_qs.filter(status='processing').count(),
            'failed_analyses': base_qs.filter(status='failed').count(),
        }
        
        # Get store type distribution
        store_type_stats = base_qs.values('store_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        analytics['store_type_distribution'] = list(store_type_stats)
        
        # Get payment statistics
        payment_qs = Payment.objects.all()
        if user:
            payment_qs = payment_qs.filter(user=user)
        
        analytics['total_payments'] = payment_qs.count()
        analytics['total_revenue'] = payment_qs.filter(
            status='completed'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        return analytics
    
    def search_analyses(self, query, user=None, filters=None):
        """Search analyses with optimized queries."""
        from ..models import StoreAnalysis
        
        # Build search query
        search_q = Q(store_name__icontains=query) | \
                   Q(store_location__icontains=query) | \
                   Q(description__icontains=query)
        
        queryset = StoreAnalysis.objects.filter(search_q)
        
        # Apply user filter
        if user:
            queryset = queryset.filter(user=user)
        
        # Apply additional filters
        if filters:
            for field, value in filters.items():
                if value and hasattr(StoreAnalysis, field):
                    queryset = queryset.filter(**{field: value})
        
        # Optimize queryset
        queryset = self.optimize_store_analysis_queryset(queryset)
        
        return queryset
    
    def get_user_dashboard_data(self, user):
        """Get user dashboard data efficiently."""
        from ..models import StoreAnalysis, Payment
        
        # Get recent analyses
        recent_analyses = StoreAnalysis.objects.filter(
            user=user
        ).select_related('analysis_result').order_by('-created_at')[:5]
        
        # Get recent payments
        recent_payments = Payment.objects.filter(
            user=user
        ).order_by('-created_at')[:5]
        
        # Get statistics
        stats = self.get_analytics_data(user=user)
        
        return {
            'recent_analyses': recent_analyses,
            'recent_payments': recent_payments,
            'statistics': stats
        }
    
    def monitor_query_performance(self):
        """Monitor and log query performance."""
        if hasattr(settings, 'DEBUG') and settings.DEBUG:
            queries = connection.queries
            total_time = sum(float(q['time']) for q in queries)
            
            logger.info(f"Total queries: {len(queries)}, Total time: {total_time:.3f}s")
            
            # Log slow queries
            slow_queries = [q for q in queries if float(q['time']) > 1.0]
            if slow_queries:
                logger.warning(f"Found {len(slow_queries)} slow queries")
                for q in slow_queries:
                    logger.warning(f"Slow query: {q['sql'][:100]}... ({q['time']}s)")
    
    def clear_query_log(self):
        """Clear the query log."""
        if hasattr(connection, 'queries'):
            connection.queries = []
            logger.info("Query log cleared") 