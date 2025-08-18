import logging
from typing import Any, Optional, Dict
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)

class CacheManager:
    """مدیر کش برای بهینه‌سازی عملکرد"""
    
    # کلیدهای کش
    USER_ANALYSES_KEY = "user_analyses_{user_id}"
    ANALYSIS_DETAIL_KEY = "analysis_detail_{analysis_id}"
    STATISTICS_KEY = "statistics_{user_id}"
    SEARCH_RESULTS_KEY = "search_results_{query_hash}"
    
    # زمان انقضا (ثانیه)
    DEFAULT_TIMEOUT = 300  # 5 دقیقه
    USER_ANALYSES_TIMEOUT = 600  # 10 دقیقه
    ANALYSIS_DETAIL_TIMEOUT = 1800  # 30 دقیقه
    STATISTICS_TIMEOUT = 3600  # 1 ساعت
    
    @classmethod
    def get_user_analyses(cls, user_id: int) -> Optional[list]:
        """دریافت تحلیل‌های کاربر از کش"""
        try:
            key = cls.USER_ANALYSES_KEY.format(user_id=user_id)
            return cache.get(key)
        except Exception as e:
            logger.error(f"Error getting user analyses from cache: {e}")
            return None
    
    @classmethod
    def set_user_analyses(cls, user_id: int, analyses: list) -> bool:
        """ذخیره تحلیل‌های کاربر در کش"""
        try:
            key = cls.USER_ANALYSES_KEY.format(user_id=user_id)
            cache.set(key, analyses, cls.USER_ANALYSES_TIMEOUT)
            return True
        except Exception as e:
            logger.error(f"Error setting user analyses in cache: {e}")
            return False
    
    @classmethod
    def get_analysis_detail(cls, analysis_id: int) -> Optional[Dict]:
        """دریافت جزئیات تحلیل از کش"""
        try:
            key = cls.ANALYSIS_DETAIL_KEY.format(analysis_id=analysis_id)
            return cache.get(key)
        except Exception as e:
            logger.error(f"Error getting analysis detail from cache: {e}")
            return None
    
    @classmethod
    def set_analysis_detail(cls, analysis_id: int, detail: Dict) -> bool:
        """ذخیره جزئیات تحلیل در کش"""
        try:
            key = cls.ANALYSIS_DETAIL_KEY.format(analysis_id=analysis_id)
            cache.set(key, detail, cls.ANALYSIS_DETAIL_TIMEOUT)
            return True
        except Exception as e:
            logger.error(f"Error setting analysis detail in cache: {e}")
            return False
    
    @classmethod
    def get_statistics(cls, user_id: int) -> Optional[Dict]:
        """دریافت آمار از کش"""
        try:
            key = cls.STATISTICS_KEY.format(user_id=user_id)
            return cache.get(key)
        except Exception as e:
            logger.error(f"Error getting statistics from cache: {e}")
            return None
    
    @classmethod
    def set_statistics(cls, user_id: int, stats: Dict) -> bool:
        """ذخیره آمار در کش"""
        try:
            key = cls.STATISTICS_KEY.format(user_id=user_id)
            cache.set(key, stats, cls.STATISTICS_TIMEOUT)
            return True
        except Exception as e:
            logger.error(f"Error setting statistics in cache: {e}")
            return False
    
    @classmethod
    def get_search_results(cls, query: str) -> Optional[list]:
        """دریافت نتایج جستجو از کش"""
        try:
            import hashlib
            query_hash = hashlib.md5(query.encode()).hexdigest()
            key = cls.SEARCH_RESULTS_KEY.format(query_hash=query_hash)
            return cache.get(key)
        except Exception as e:
            logger.error(f"Error getting search results from cache: {e}")
            return None
    
    @classmethod
    def set_search_results(cls, query: str, results: list) -> bool:
        """ذخیره نتایج جستجو در کش"""
        try:
            import hashlib
            query_hash = hashlib.md5(query.encode()).hexdigest()
            key = cls.SEARCH_RESULTS_KEY.format(query_hash=query_hash)
            cache.set(key, results, cls.DEFAULT_TIMEOUT)
            return True
        except Exception as e:
            logger.error(f"Error setting search results in cache: {e}")
            return False
    
    @classmethod
    def invalidate_user_cache(cls, user_id: int) -> bool:
        """پاک کردن کش کاربر"""
        try:
            # پاک کردن تحلیل‌های کاربر
            analyses_key = cls.USER_ANALYSES_KEY.format(user_id=user_id)
            cache.delete(analyses_key)
            
            # پاک کردن آمار کاربر
            stats_key = cls.STATISTICS_KEY.format(user_id=user_id)
            cache.delete(stats_key)
            
            logger.info(f"User cache invalidated for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error invalidating user cache: {e}")
            return False
    
    @classmethod
    def invalidate_analysis_cache(cls, analysis_id: int) -> bool:
        """پاک کردن کش تحلیل"""
        try:
            # پاک کردن جزئیات تحلیل
            detail_key = cls.ANALYSIS_DETAIL_KEY.format(analysis_id=analysis_id)
            cache.delete(detail_key)
            
            logger.info(f"Analysis cache invalidated for analysis {analysis_id}")
            return True
        except Exception as e:
            logger.error(f"Error invalidating analysis cache: {e}")
            return False
    
    @classmethod
    def clear_all_cache(cls) -> bool:
        """پاک کردن تمام کش"""
        try:
            cache.clear()
            logger.info("All cache cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing all cache: {e}")
            return False
    
    @classmethod
    def get_cache_info(cls) -> Dict[str, Any]:
        """دریافت اطلاعات کش"""
        try:
            # این اطلاعات بستگی به نوع کش دارد
            # برای Redis می‌توان اطلاعات بیشتری دریافت کرد
            return {
                'cache_backend': getattr(settings, 'CACHES', {}).get('default', {}).get('BACKEND', 'Unknown'),
                'timestamp': timezone.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error getting cache info: {e}")
            return {}
    
    @classmethod
    def optimize_cache(cls) -> bool:
        """بهینه‌سازی کش"""
        try:
            # پاک کردن کش‌های منقضی شده
            # این کار معمولاً توسط خود سیستم کش انجام می‌شود
            logger.info("Cache optimization completed")
            return True
        except Exception as e:
            logger.error(f"Error optimizing cache: {e}")
            return False 