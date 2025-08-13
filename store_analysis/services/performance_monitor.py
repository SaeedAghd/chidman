"""
Performance monitoring service for store analysis application.
"""

import time
import psutil
import logging
from django.core.cache import cache
from django.db import connection
from django.conf import settings

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor application performance metrics."""
    
    def __init__(self):
        self.metrics = {}
        self.start_time = time.time()
    
    def start_monitoring(self):
        """Start performance monitoring."""
        self.start_time = time.time()
        logger.info("Performance monitoring started")
    
    def measure_query_performance(self, query_name):
        """Measure database query performance."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Log slow queries
                if execution_time > getattr(settings, 'SLOW_QUERY_THRESHOLD', 1.0):
                    logger.warning(f"Slow query detected: {query_name} took {execution_time:.2f}s")
                
                # Store metrics
                self.metrics[f"query_{query_name}"] = execution_time
                return result
            return wrapper
        return decorator
    
    def get_memory_usage(self):
        """Get current memory usage."""
        process = psutil.Process()
        memory_info = process.memory_info()
        return {
            'rss': memory_info.rss / 1024 / 1024,  # MB
            'vms': memory_info.vms / 1024 / 1024,  # MB
            'percent': process.memory_percent()
        }
    
    def get_cpu_usage(self):
        """Get current CPU usage."""
        return psutil.cpu_percent(interval=1)
    
    def get_cache_stats(self):
        """Get cache statistics."""
        try:
            # This is a simplified version - in production you'd want more detailed stats
            cache_stats = {
                'hit_rate': 0.0,
                'miss_rate': 0.0,
                'total_requests': 0
            }
            return cache_stats
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {}
    
    def get_database_stats(self):
        """Get database connection statistics."""
        try:
            db_stats = {
                'connections': len(connection.queries),
                'total_time': sum(float(q['time']) for q in connection.queries),
                'slow_queries': len([q for q in connection.queries if float(q['time']) > 1.0])
            }
            return db_stats
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
    
    def generate_report(self):
        """Generate performance report."""
        report = {
            'uptime': time.time() - self.start_time,
            'memory_usage': self.get_memory_usage(),
            'cpu_usage': self.get_cpu_usage(),
            'cache_stats': self.get_cache_stats(),
            'database_stats': self.get_database_stats(),
            'custom_metrics': self.metrics
        }
        
        logger.info(f"Performance report generated: {report}")
        return report
    
    def check_alerts(self):
        """Check for performance alerts."""
        alerts = []
        
        # Memory usage alert
        memory_usage = self.get_memory_usage()
        if memory_usage['percent'] > 90:
            alerts.append(f"High memory usage: {memory_usage['percent']:.1f}%")
        
        # CPU usage alert
        cpu_usage = self.get_cpu_usage()
        if cpu_usage > 90:
            alerts.append(f"High CPU usage: {cpu_usage:.1f}%")
        
        # Slow query alert
        db_stats = self.get_database_stats()
        if db_stats.get('slow_queries', 0) > 10:
            alerts.append(f"Too many slow queries: {db_stats['slow_queries']}")
        
        if alerts:
            logger.warning(f"Performance alerts: {alerts}")
        
        return alerts 