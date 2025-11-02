#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(__name__)

class ServiceManager:
    """مدیریت سرویس‌های تحلیل"""
    
    def __init__(self):
        self.services = {
            'free': None,
            'professional': None,
            'enterprise': None
        }
        self._initialize_services()
    
    def _initialize_services(self):
        """مقداردهی اولیه سرویس‌ها"""
        try:
            from .free_analysis_service import FreeAnalysisService
            from .professional_analysis_service import ProfessionalAnalysisService
            from .enterprise_analysis_service import EnterpriseAnalysisService
            
            self.services['free'] = FreeAnalysisService()
            self.services['professional'] = ProfessionalAnalysisService()
            self.services['enterprise'] = EnterpriseAnalysisService()
            
            logger.info("✅ سرویس‌های تحلیل با موفقیت مقداردهی شدند")
            
        except Exception as e:
            logger.error(f"❌ خطا در مقداردهی سرویس‌ها: {e}")
    
    def get_service(self, service_type: str) -> Optional[Any]:
        """دریافت سرویس بر اساس نوع"""
        try:
            if service_type in self.services:
                return self.services[service_type]
            else:
                logger.warning(f"⚠️ سرویس {service_type} یافت نشد")
                return None
                
        except Exception as e:
            logger.error(f"❌ خطا در دریافت سرویس {service_type}: {e}")
            return None
    
    def analyze_store(self, store_data: Dict[str, Any], service_type: str = 'free') -> Dict[str, Any]:
        """تحلیل فروشگاه با سرویس مشخص"""
        try:
            service = self.get_service(service_type)
            if service:
                logger.info(f"🔍 شروع تحلیل با سرویس {service_type}")
                return service.analyze_store(store_data)
            else:
                logger.error(f"❌ سرویس {service_type} در دسترس نیست")
                return self._fallback_analysis(store_data, service_type)
                
        except Exception as e:
            logger.error(f"❌ خطا در تحلیل با سرویس {service_type}: {e}")
            return self._fallback_analysis(store_data, service_type)
    
    def get_service_info(self, service_type: str = None) -> Dict[str, Any]:
        """دریافت اطلاعات سرویس‌ها"""
        try:
            if service_type:
                # اطلاعات یک سرویس خاص
                service = self.get_service(service_type)
                if service:
                    return {
                        'service_type': service_type,
                        'service_info': service.get_service_info()
                    }
                else:
                    return {
                        'service_type': service_type,
                        'error': 'سرویس یافت نشد'
                    }
            else:
                # اطلاعات تمام سرویس‌ها
                all_services_info = {}
                for service_name, service in self.services.items():
                    if service:
                        all_services_info[service_name] = service.get_service_info()
                    else:
                        all_services_info[service_name] = {'error': 'سرویس در دسترس نیست'}
                
                return {
                    'all_services': all_services_info,
                    'total_services': len(self.services),
                    'available_services': len([s for s in self.services.values() if s is not None])
                }
                
        except Exception as e:
            logger.error(f"❌ خطا در دریافت اطلاعات سرویس‌ها: {e}")
            return {
                'error': f'خطا در دریافت اطلاعات: {str(e)}'
            }
    
    def compare_services(self) -> Dict[str, Any]:
        """مقایسه سرویس‌ها"""
        try:
            comparison = {
                'free': {
                    'ai_engine': 'Ollama (Maximum Capacity)',
                    'max_analyses': 1,
                    'report_pages': 50,
                    'quality_level': 'Professional',
                    'features': [
                        'تحلیل جامع با Ollama',
                        '25 توصیه تخصصی',
                        'گزارش 50 صفحه‌ای حرفه‌ای',
                        'تحلیل در حد مشاوره‌های رقیب',
                        'قالب استاندارد جهانی',
                        'تحلیل مالی و ROI',
                        'برنامه اجرایی 3 فازی'
                    ],
                    'limitations': [
                        '1 تحلیل در ماه',
                        'بدون پشتیبانی تخصصی',
                        'بدون تحلیل تصاویر پیشرفته'
                    ],
                    'price': 'رایگان'
                },
                'professional': {
                    'ai_engine': 'GPT-4.1 + Ollama',
                    'max_analyses': 5,
                    'report_pages': 75,
                    'quality_level': 'Advanced',
                    'features': [
                        'تحلیل با GPT-4.1 + Ollama',
                        '35 توصیه تخصصی پیشرفته',
                        'گزارش 75 صفحه‌ای جامع',
                        'تحلیل مقایسه‌ای و تطبیقی',
                        'قالب استاندارد جهانی + ویژگی‌های اضافی',
                        'تحلیل مالی پیشرفته',
                        'برنامه اجرایی 4 فازی',
                        'پشتیبانی تخصصی'
                    ],
                    'limitations': [
                        '5 تحلیل در ماه',
                        'بدون تحلیل تصاویر پیشرفته',
                        'بدون مشاوره حضوری'
                    ],
                    'price': 'پولی'
                },
                'enterprise': {
                    'ai_engine': 'GPT-4.1 + Claude-3 + Image Analysis',
                    'max_analyses': 20,
                    'report_pages': 100,
                    'quality_level': 'Enterprise',
                    'features': [
                        'تحلیل با GPT-4.1 + Claude-3 + تحلیل تصاویر',
                        '50 توصیه تخصصی جامع',
                        'گزارش 100 صفحه‌ای کامل',
                        'تحلیل مقایسه‌ای و تطبیقی پیشرفته',
                        'قالب استاندارد جهانی + ویژگی‌های اضافی + تحلیل تصاویر',
                        'تحلیل مالی پیشرفته + تحلیل تصاویر',
                        'برنامه اجرایی 5 فازی',
                        'پشتیبانی تخصصی + مشاوره حضوری',
                        'تحلیل تصاویر پیشرفته',
                        'مشاوره حضوری'
                    ],
                    'limitations': [
                        '20 تحلیل در ماه',
                        'بدون محدودیت'
                    ],
                    'price': 'پولی (بالا)'
                }
            }
            
            return {
                'comparison': comparison,
                'summary': {
                    'free': 'تحلیل حرفه‌ای رایگان با Ollama',
                    'professional': 'تحلیل پیشرفته با GPT-4.1 + Ollama',
                    'enterprise': 'تحلیل جامع با GPT-4.1 + Claude-3 + تحلیل تصاویر'
                },
                'recommendations': {
                    'start_with': 'free',
                    'upgrade_to': 'professional',
                    'enterprise_for': 'سازمان‌های بزرگ'
                }
            }
            
        except Exception as e:
            logger.error(f"❌ خطا در مقایسه سرویس‌ها: {e}")
            return {
                'error': f'خطا در مقایسه: {str(e)}'
            }
    
    def get_service_recommendation(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """توصیه سرویس بر اساس پروفایل کاربر"""
        try:
            # تحلیل پروفایل کاربر
            user_type = user_profile.get('user_type', 'individual')
            business_size = user_profile.get('business_size', 'small')
            budget = user_profile.get('budget', 'low')
            analysis_frequency = user_profile.get('analysis_frequency', 'low')
            support_needed = user_profile.get('support_needed', False)
            image_analysis_needed = user_profile.get('image_analysis_needed', False)
            
            # منطق توصیه
            if user_type == 'enterprise' or business_size == 'large':
                recommended_service = 'enterprise'
                reason = 'سازمان بزرگ با نیازهای پیچیده'
            elif budget == 'high' or analysis_frequency == 'high' or support_needed:
                recommended_service = 'professional'
                reason = 'نیاز به تحلیل پیشرفته و پشتیبانی'
            elif image_analysis_needed:
                recommended_service = 'enterprise'
                reason = 'نیاز به تحلیل تصاویر'
            else:
                recommended_service = 'free'
                reason = 'تحلیل حرفه‌ای رایگان کافی است'
            
            return {
                'recommended_service': recommended_service,
                'reason': reason,
                'user_profile': user_profile,
                'service_info': self.get_service_info(recommended_service),
                'alternatives': self._get_alternatives(recommended_service, user_profile)
            }
            
        except Exception as e:
            logger.error(f"❌ خطا در توصیه سرویس: {e}")
            return {
                'error': f'خطا در توصیه: {str(e)}',
                'fallback': 'free'
            }
    
    def _get_alternatives(self, recommended_service: str, user_profile: Dict[str, Any]) -> List[str]:
        """دریافت گزینه‌های جایگزین"""
        try:
            alternatives = []
            
            if recommended_service == 'free':
                alternatives = ['professional', 'enterprise']
            elif recommended_service == 'professional':
                alternatives = ['free', 'enterprise']
            elif recommended_service == 'enterprise':
                alternatives = ['professional', 'free']
            
            return alternatives
            
        except Exception as e:
            logger.error(f"❌ خطا در دریافت گزینه‌های جایگزین: {e}")
            return []
    
    def _fallback_analysis(self, store_data: Dict[str, Any], service_type: str) -> Dict[str, Any]:
        """تحلیل جایگزین در صورت خطا"""
        return {
            'status': 'error',
            'service_type': service_type,
            'analysis_text': f'خطا در تحلیل با سرویس {service_type}. لطفاً دوباره تلاش کنید.',
            'confidence_score': 0.1,
            'limitations': ['خطا در تحلیل'],
            'generated_at': timezone.now().isoformat()
        }
    
    def get_service_statistics(self) -> Dict[str, Any]:
        """آمار سرویس‌ها"""
        try:
            stats = {
                'total_services': len(self.services),
                'available_services': len([s for s in self.services.values() if s is not None]),
                'service_types': list(self.services.keys()),
                'service_status': {
                    'free': 'available' if self.services['free'] else 'unavailable',
                    'professional': 'available' if self.services['professional'] else 'unavailable',
                    'enterprise': 'available' if self.services['enterprise'] else 'unavailable'
                },
                'last_updated': timezone.now().isoformat()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ خطا در دریافت آمار سرویس‌ها: {e}")
            return {
                'error': f'خطا در آمار: {str(e)}'
            }
    
    def validate_service_request(self, service_type: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """اعتبارسنجی درخواست سرویس"""
        try:
            validation_result = {
                'valid': True,
                'service_type': service_type,
                'errors': [],
                'warnings': []
            }
            
            # بررسی وجود سرویس
            if service_type not in self.services:
                validation_result['valid'] = False
                validation_result['errors'].append(f'سرویس {service_type} وجود ندارد')
            
            # بررسی در دسترس بودن سرویس
            if service_type in self.services and self.services[service_type] is None:
                validation_result['valid'] = False
                validation_result['errors'].append(f'سرویس {service_type} در دسترس نیست')
            
            # بررسی محدودیت‌های کاربر
            if service_type == 'free':
                # بررسی محدودیت تحلیل رایگان
                user_id = user_data.get('user_id')
                if user_id:
                    # اینجا می‌توانید محدودیت‌های کاربر را بررسی کنید
                    pass
            
            # بررسی داده‌های ورودی
            required_fields = ['store_name', 'store_type']
            for field in required_fields:
                if field not in user_data:
                    validation_result['valid'] = False
                    validation_result['errors'].append(f'فیلد {field} الزامی است')
            
            return validation_result
            
        except Exception as e:
            logger.error(f"❌ خطا در اعتبارسنجی درخواست: {e}")
            return {
                'valid': False,
                'service_type': service_type,
                'errors': [f'خطا در اعتبارسنجی: {str(e)}'],
                'warnings': []
            }
