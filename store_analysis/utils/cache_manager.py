from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """مدیریت کش برای بهبود عملکرد"""
    
    @staticmethod
    def get_analysis_results(analysis_id, timeout=3600):
        """
        دریافت نتایج تحلیل از کش
        """
        cache_key = f'analysis_results_{analysis_id}'
        results = cache.get(cache_key)
        
        if results is None:
            logger.debug(f"Cache miss for analysis {analysis_id}")
        else:
            logger.debug(f"Cache hit for analysis {analysis_id}")
        
        return results
    
    @staticmethod
    def set_analysis_results(analysis_id, results, timeout=3600):
        """
        ذخیره نتایج تحلیل در کش
        """
        cache_key = f'analysis_results_{analysis_id}'
        cache.set(cache_key, results, timeout=timeout)
        logger.debug(f"Cached analysis results for {analysis_id}")
    
    @staticmethod
    def get_user_analyses(user_id, timeout=1800):
        """
        دریافت تحلیل‌های کاربر از کش
        """
        cache_key = f'user_analyses_{user_id}'
        analyses = cache.get(cache_key)
        
        if analyses is None:
            logger.debug(f"Cache miss for user analyses {user_id}")
        else:
            logger.debug(f"Cache hit for user analyses {user_id}")
        
        return analyses
    
    @staticmethod
    def set_user_analyses(user_id, analyses, timeout=1800):
        """
        ذخیره تحلیل‌های کاربر در کش
        """
        cache_key = f'user_analyses_{user_id}'
        cache.set(cache_key, analyses, timeout=timeout)
        logger.debug(f"Cached user analyses for {user_id}")
    
    @staticmethod
    def invalidate_analysis_cache(analysis_id):
        """
        پاک کردن کش تحلیل
        """
        cache_key = f'analysis_results_{analysis_id}'
        cache.delete(cache_key)
        logger.debug(f"Invalidated cache for analysis {analysis_id}")
    
    @staticmethod
    def invalidate_user_cache(user_id):
        """
        پاک کردن کش کاربر
        """
        cache_key = f'user_analyses_{user_id}'
        cache.delete(cache_key)
        logger.debug(f"Invalidated cache for user {user_id}")
    
    @staticmethod
    def clear_all_cache():
        """
        پاک کردن تمام کش
        """
        cache.clear()
        logger.info("Cleared all cache") 