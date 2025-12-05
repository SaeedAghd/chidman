"""
سرویس جستجو و مدیریت سوالات متداول
"""

import logging
from typing import List, Dict, Any
from django.db.models import Q
from django.core.paginator import Paginator
from ..models import FAQ, FAQCategory

logger = logging.getLogger(__name__)

class FAQService:
    """سرویس مدیریت سوالات متداول"""
    
    def __init__(self):
        self.search_fields = ['question', 'answer', 'keywords']
    
    def search_faqs(self, query: str, category_id: int = None, limit: int = 10) -> List[Dict[str, Any]]:
        """جستجو در سوالات متداول"""
        try:
            # جستجوی پایه
            base_query = FAQ.objects.filter(is_active=True)
            
            if category_id:
                base_query = base_query.filter(category_id=category_id)
            
            if query:
                # جستجو در فیلدهای مختلف
                search_query = Q()
                for field in self.search_fields:
                    search_query |= Q(**{f"{field}__icontains": query})
                
                base_query = base_query.filter(search_query)
            
            # مرتب‌سازی بر اساس مرتبط بودن
            faqs = base_query.select_related('category').order_by('-view_count', 'order')[:limit]
            
            results = []
            for faq in faqs:
                results.append({
                    'id': faq.id,
                    'question': faq.question,
                    'answer': faq.answer,
                    'category': {
                        'id': faq.category.id,
                        'name': faq.category.name,
                        'icon': faq.category.icon
                    },
                    'view_count': faq.view_count,
                    'relevance_score': self._calculate_relevance(faq, query)
                })
            
            # مرتب‌سازی بر اساس امتیاز مرتبط بودن
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            return results
            
        except Exception as e:
            logger.error(f"خطا در جستجوی FAQ: {e}")
            return []
    
    def _calculate_relevance(self, faq: FAQ, query: str) -> float:
        """محاسبه امتیاز مرتبط بودن"""
        if not query:
            return 0.0
        
        query_lower = query.lower()
        score = 0.0
        
        # امتیاز برای تطبیق کامل سوال
        if query_lower in faq.question.lower():
            score += 10.0
        
        # امتیاز برای تطبیق کلمات کلیدی
        if faq.keywords:
            keywords = [kw.strip().lower() for kw in faq.keywords.split(',')]
            for keyword in keywords:
                if keyword in query_lower:
                    score += 5.0
        
        # امتیاز برای تطبیق در پاسخ
        if query_lower in faq.answer.lower():
            score += 2.0
        
        # امتیاز برای تعداد بازدید
        score += min(faq.view_count * 0.01, 2.0)
        
        return score
    
    def get_popular_faqs(self, limit: int = 5) -> List[Dict[str, Any]]:
        """دریافت سوالات محبوب"""
        try:
            faqs = FAQ.objects.filter(is_active=True).select_related('category').order_by('-view_count')[:limit]
            
            results = []
            for faq in faqs:
                results.append({
                    'id': faq.id,
                    'question': faq.question,
                    'answer': faq.answer,
                    'category': {
                        'id': faq.category.id,
                        'name': faq.category.name,
                        'icon': faq.category.icon
                    },
                    'view_count': faq.view_count
                })
            
            return results
            
        except Exception as e:
            logger.error(f"خطا در دریافت سوالات محبوب: {e}")
            return []
    
    def get_faq_categories(self) -> List[Dict[str, Any]]:
        """دریافت دسته‌بندی‌های FAQ"""
        try:
            # بررسی وجود مدل FAQCategory و FAQ
            try:
                from ..models import FAQCategory as FAQCategoryModel
                from ..models import FAQ as FAQModel
                categories = FAQCategoryModel.objects.filter(is_active=True).order_by('order', 'name')

                results = []
                for category in categories:
                    faq_count = FAQModel.objects.filter(category=category, is_active=True).count()
                    results.append({
                        'id': category.id,
                        'name': category.name,
                        'description': category.description,
                        'icon': category.icon,
                        'faq_count': faq_count
                    })

                return results

            except ImportError:
                # اگر مدل‌های FAQ وجود ندارند، لیست خالی برگردان
                logger.warning("FAQ models not available, returning empty categories")
                return []

        except Exception as e:
            logger.error(f"خطا در دریافت دسته‌بندی‌ها: {e}")
            return []
    
    def get_faq_by_id(self, faq_id: int) -> Dict[str, Any]:
        """دریافت FAQ بر اساس ID"""
        try:
            faq = FAQ.objects.select_related('category').get(id=faq_id, is_active=True)
            
            # افزایش تعداد بازدید
            faq.increment_view()
            
            return {
                'id': faq.id,
                'question': faq.question,
                'answer': faq.answer,
                'category': {
                    'id': faq.category.id,
                    'name': faq.category.name,
                    'icon': faq.category.icon
                },
                'keywords': faq.keywords,
                'view_count': faq.view_count + 1
            }
            
        except FAQ.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"خطا در دریافت FAQ: {e}")
            return None
    
    def get_related_faqs(self, faq_id: int, limit: int = 3) -> List[Dict[str, Any]]:
        """دریافت سوالات مرتبط"""
        try:
            current_faq = FAQ.objects.get(id=faq_id)
            
            # جستجو در همان دسته‌بندی
            related_faqs = FAQ.objects.filter(
                category=current_faq.category,
                is_active=True
            ).exclude(id=faq_id).order_by('-view_count')[:limit]
            
            results = []
            for faq in related_faqs:
                results.append({
                    'id': faq.id,
                    'question': faq.question,
                    'answer': faq.answer[:100] + '...' if len(faq.answer) > 100 else faq.answer,
                    'view_count': faq.view_count
                })
            
            return results
            
        except FAQ.DoesNotExist:
            return []
        except Exception as e:
            logger.error(f"خطا در دریافت سوالات مرتبط: {e}")
            return []
    
    def suggest_faqs(self, user_query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """پیشنهاد سوالات بر اساس جستجوی کاربر"""
        try:
            # جستجو در سوالات
            suggestions = self.search_faqs(user_query, limit=limit)
            
            # اگر نتیجه کمی پیدا شد، جستجوی گسترده‌تر
            if len(suggestions) < 3:
                # تقسیم کلمات و جستجو
                words = user_query.split()
                for word in words:
                    if len(word) > 2:  # فقط کلمات بیش از 2 حرف
                        additional = self.search_faqs(word, limit=2)
                        suggestions.extend(additional)
                
                # حذف تکراری‌ها
                seen_ids = set()
                unique_suggestions = []
                for suggestion in suggestions:
                    if suggestion['id'] not in seen_ids:
                        seen_ids.add(suggestion['id'])
                        unique_suggestions.append(suggestion)
                
                suggestions = unique_suggestions[:limit]
            
            return suggestions
            
        except Exception as e:
            logger.error(f"خطا در پیشنهاد سوالات: {e}")
            return []
