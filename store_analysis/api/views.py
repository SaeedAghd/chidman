from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import timedelta
import logging

from ..models import StoreAnalysis, Payment
from ..serializers import (
    StoreAnalysisSerializer, 
    StoreAnalysisDetailSerializer,
    PaymentSerializer,
    AnalysisStatsSerializer
)
from ..services.security_service import SecurityService
from ..decorators import require_secure_headers, log_user_activity

logger = logging.getLogger(__name__)

class StoreAnalysisPagination(PageNumberPagination):
    """کلاس صفحه‌بندی برای API"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class StoreAnalysisViewSet(viewsets.ModelViewSet):
    """ViewSet برای تحلیل فروشگاه"""
    serializer_class = StoreAnalysisSerializer
    pagination_class = StoreAnalysisPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'store_type', 'city', 'area', 'has_surveillance', 'has_customer_video']
    search_fields = ['store_name', 'store_location', 'description']
    ordering_fields = ['created_at', 'updated_at', 'store_name', 'store_size']
    ordering = ['-created_at']

    def get_queryset(self):
        """فیلتر کردن queryset بر اساس کاربر"""
        return StoreAnalysis.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """انتخاب serializer مناسب"""
        if self.action == 'retrieve':
            return StoreAnalysisDetailSerializer
        return StoreAnalysisSerializer

    @require_secure_headers
    @log_user_activity('api_list_analyses')
    def list(self, request, *args, **kwargs):
        """لیست تحلیل‌ها با فیلترهای پیشرفته"""
        try:
            # فیلترهای اضافی
            store_size_min = request.query_params.get('store_size_min')
            store_size_max = request.query_params.get('store_size_max')
            date_from = request.query_params.get('date_from')
            date_to = request.query_params.get('date_to')
            
            queryset = self.get_queryset()
            
            # اعمال فیلترهای اضافی
            if store_size_min:
                queryset = queryset.filter(store_size__gte=store_size_min)
            if store_size_max:
                queryset = queryset.filter(store_size__lte=store_size_max)
            if date_from:
                queryset = queryset.filter(created_at__gte=date_from)
            if date_to:
                queryset = queryset.filter(created_at__lte=date_to)
            
            # صفحه‌بندی
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"API list error: {str(e)}")
            return Response(
                {'error': 'خطا در دریافت لیست تحلیل‌ها'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @require_secure_headers
    @log_user_activity('api_create_analysis')
    def create(self, request, *args, **kwargs):
        """ایجاد تحلیل جدید"""
        try:
            # اعتبارسنجی ورودی
            data = request.data.copy()
            data['user'] = request.user.id
            
            # پاکسازی ورودی
            security_service = SecurityService()
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = security_service.sanitize_input(value)
            
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                analysis = serializer.save(user=request.user)
                
                # ثبت در کش
                try:
                    from ..utils.cache_manager import CacheManager
                    CacheManager.invalidate_user_cache(request.user.id)
                except Exception as cache_error:
                    logger.warning(f"Cache invalidation failed: {cache_error}")
                
                return Response(
                    serializer.data, 
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            logger.error(f"API create error: {str(e)}")
            return Response(
                {'error': 'خطا در ایجاد تحلیل'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @require_secure_headers
    @log_user_activity('api_retrieve_analysis')
    def retrieve(self, request, *args, **kwargs):
        """دریافت جزئیات تحلیل"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            
            # اضافه کردن اطلاعات اضافی
            data = serializer.data
            data['analysis_duration'] = instance.get_analysis_duration()
            data['is_completed'] = instance.is_completed
            data['is_processing'] = instance.is_processing
            data['is_failed'] = instance.is_failed
            
            return Response(data)
            
        except Exception as e:
            logger.error(f"API retrieve error: {str(e)}")
            return Response(
                {'error': 'خطا در دریافت تحلیل'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @require_secure_headers
    @log_user_activity('api_update_analysis')
    def update(self, request, *args, **kwargs):
        """به‌روزرسانی تحلیل"""
        try:
            instance = self.get_object()
            
            # بررسی وضعیت تحلیل
            if instance.status in ['completed', 'processing']:
                return Response(
                    {'error': 'تحلیل در حال پردازش یا تکمیل شده است'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # پاکسازی ورودی
            data = request.data.copy()
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = SecurityService.sanitize_input(value)
            
            serializer = self.get_serializer(instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                # پاک کردن کش
                from ..utils.cache_manager import CacheManager
                CacheManager.invalidate_analysis_cache(instance.id)
                
                return Response(serializer.data)
            else:
                return Response(
                    serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            logger.error(f"API update error: {str(e)}")
            return Response(
                {'error': 'خطا در به‌روزرسانی تحلیل'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @require_secure_headers
    @log_user_activity('api_delete_analysis')
    def destroy(self, request, *args, **kwargs):
        """حذف تحلیل"""
        try:
            instance = self.get_object()
            
            # بررسی وضعیت تحلیل
            if instance.status == 'processing':
                return Response(
                    {'error': 'تحلیل در حال پردازش است و قابل حذف نیست'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # پاک کردن کش
            from ..utils.cache_manager import CacheManager
            CacheManager.invalidate_analysis_cache(instance.id)
            CacheManager.invalidate_user_cache(request.user.id)
            
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            logger.error(f"API delete error: {str(e)}")
            return Response(
                {'error': 'خطا در حذف تحلیل'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    @require_secure_headers
    @log_user_activity('api_start_analysis')
    def start_analysis(self, request, pk=None):
        """شروع تحلیل"""
        try:
            analysis = self.get_object()
            
            if analysis.status != 'pending':
                return Response(
                    {'error': 'تحلیل در وضعیت مناسب برای شروع نیست'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # بررسی پرداخت
            last_payment = Payment.objects.filter(
                user=request.user,
                status='completed'
            ).order_by('-created_at').first()
            
            if not last_payment:
                return Response(
                    {'error': 'ابتدا باید هزینه تحلیل را پرداخت کنید'},
                    status=status.HTTP_402_PAYMENT_REQUIRED
                )
            
            # شروع تحلیل
            analysis.status = 'processing'
            analysis.save()
            
            # ارسال به Celery
            from ..tasks import analyze_store_task
            analyze_store_task.delay(analysis.id)
            
            return Response({
                'message': 'تحلیل شروع شد',
                'analysis_id': analysis.id
            })
            
        except Exception as e:
            logger.error(f"API start analysis error: {str(e)}")
            return Response(
                {'error': 'خطا در شروع تحلیل'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    @require_secure_headers
    @log_user_activity('api_get_analysis_status')
    def status(self, request, pk=None):
        """دریافت وضعیت تحلیل"""
        try:
            analysis = self.get_object()
            
            return Response({
                'id': analysis.id,
                'status': analysis.status,
                'progress': analysis.get_progress(),
                'created_at': analysis.created_at,
                'updated_at': analysis.updated_at,
                'is_completed': analysis.is_completed,
                'is_processing': analysis.is_processing,
                'is_failed': analysis.is_failed
            })
            
        except Exception as e:
            logger.error(f"API status error: {str(e)}")
            return Response(
                {'error': 'خطا در دریافت وضعیت'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    @require_secure_headers
    @log_user_activity('api_get_statistics')
    def statistics(self, request):
        """دریافت آمار تحلیل‌ها"""
        try:
            user = request.user
            
            # آمار کلی
            total_analyses = StoreAnalysis.objects.filter(user=user).count()
            completed_analyses = StoreAnalysis.objects.filter(
                user=user, 
                status='completed'
            ).count()
            processing_analyses = StoreAnalysis.objects.filter(
                user=user, 
                status='processing'
            ).count()
            failed_analyses = StoreAnalysis.objects.filter(
                user=user, 
                status='failed'
            ).count()
            
            # آمار بر اساس نوع فروشگاه
            store_type_stats = StoreAnalysis.objects.filter(
                user=user
            ).values('store_type').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # آمار بر اساس شهر
            city_stats = StoreAnalysis.objects.filter(
                user=user
            ).values('city').annotate(
                count=Count('id')
            ).order_by('-count')[:10]
            
            # آمار ماهانه
            monthly_stats = StoreAnalysis.objects.filter(
                user=user,
                created_at__gte=timezone.now() - timedelta(days=365)
            ).extra(
                select={'month': "strftime('%Y-%m', created_at)"}
            ).values('month').annotate(
                count=Count('id')
            ).order_by('month')
            
            return Response({
                'total_analyses': total_analyses,
                'completed_analyses': completed_analyses,
                'processing_analyses': processing_analyses,
                'failed_analyses': failed_analyses,
                'success_rate': (completed_analyses / total_analyses * 100) if total_analyses > 0 else 0,
                'store_type_stats': store_type_stats,
                'city_stats': city_stats,
                'monthly_stats': monthly_stats
            })
            
        except Exception as e:
            logger.error(f"API statistics error: {str(e)}")
            return Response(
                {'error': 'خطا در دریافت آمار'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    @require_secure_headers
    @log_user_activity('api_search_analyses')
    def search(self, request):
        """جستجوی پیشرفته تحلیل‌ها"""
        try:
            query = request.query_params.get('q', '')
            if not query:
                return Response(
                    {'error': 'پارامتر جستجو الزامی است'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            queryset = self.get_queryset().filter(
                Q(store_name__icontains=query) |
                Q(store_location__icontains=query) |
                Q(description__icontains=query) |
                Q(city__icontains=query) |
                Q(area__icontains=query)
            )
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"API search error: {str(e)}")
            return Response(
                {'error': 'خطا در جستجو'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet برای پرداخت‌ها"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StoreAnalysisPagination

    def get_queryset(self):
        """فیلتر کردن queryset بر اساس کاربر"""
        return Payment.objects.filter(user=self.request.user)

    @require_secure_headers
    @log_user_activity('api_get_payment_history')
    def list(self, request, *args, **kwargs):
        """لیست پرداخت‌ها"""
        try:
            queryset = self.get_queryset().order_by('-created_at')
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"API payment list error: {str(e)}")
            return Response(
                {'error': 'خطا در دریافت لیست پرداخت‌ها'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 