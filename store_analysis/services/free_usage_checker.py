#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
🛡️ Free Usage Checker Service
سیستم بررسی استفاده رایگان - جلوگیری از سوء استفاده
"""

import hashlib
import logging
from typing import Dict, Optional, List
from django.utils import timezone
from django.db.models import Q
from store_analysis.models import FreeUsageTracking

logger = logging.getLogger(__name__)


class FreeUsageChecker:
    """سرویس بررسی و مدیریت استفاده از پلن رایگان"""
    
    @staticmethod
    def hash_ip(ip_address: str) -> str:
        """Hash کردن IP Address برای حفظ حریم خصوصی"""
        return hashlib.sha256(ip_address.encode()).hexdigest()
    
    @staticmethod
    def get_user_ip(request) -> str:
        """دریافت IP Address کاربر"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        return ip
    
    @staticmethod
    def check_free_usage(
        username: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        ip_address: Optional[str] = None,
        request=None
    ) -> Dict:
        """
        بررسی اینکه آیا کاربر قبلاً از پلن رایگان استفاده کرده است
        
        Returns:
            dict: {
                'can_use': bool,
                'reason': str,
                'tracking': FreeUsageTracking or None,
                'days_used_ago': int,
                'suggested_action': str
            }
        """
        try:
            # دریافت IP از request
            if request and not ip_address:
                ip_address = FreeUsageChecker.get_user_ip(request)
            
            # Hash کردن IP
            ip_hash = FreeUsageChecker.hash_ip(ip_address) if ip_address else None
            
            # جستجوی رکوردهای موجود
            filters = Q()
            
            if username:
                filters |= Q(username=username)
            
            if email:
                filters |= Q(email=email)
            
            if phone:
                filters |= Q(phone=phone)
            
            if ip_hash:
                filters |= Q(ip_address=ip_hash)
            
            # جستجوی رکوردها
            existing_tracks = FreeUsageTracking.objects.filter(filters).first()
            
            if not existing_tracks:
                # کاربر قبلاً استفاده نکرده - مجاز است
                return {
                    'can_use': True,
                    'reason': 'این اولین بار است که از پلن رایگان استفاده می‌شود',
                    'tracking': None,
                    'days_used_ago': 0,
                    'suggested_action': 'allow'
                }
            
            # کاربر قبلاً استفاده کرده
            days_ago = existing_tracks.get_usage_age_days()
            
            # بررسی مسدودیت
            if existing_tracks.is_blocked:
                return {
                    'can_use': False,
                    'reason': f'شما از پلن رایگان استفاده کرده‌اید. {existing_tracks.block_reason}',
                    'tracking': existing_tracks,
                    'days_used_ago': days_ago,
                    'suggested_action': 'blocked',
                    'message': '🚫 شما قبلاً از پلن رایگان استفاده کرده‌اید. لطفاً از پلن‌های پولی استفاده کنید.'
                }
            
            # بررسی امکان استفاده مجدد (بعد از 30 روز)
            if days_ago < 30:
                return {
                    'can_use': False,
                    'reason': f'شما {days_ago} روز پیش از پلن رایگان استفاده کردید. حداقل 30 روز باید بگذرد.',
                    'tracking': existing_tracks,
                    'days_used_ago': days_ago,
                    'suggested_action': 'cooldown',
                    'remaining_days': 30 - days_ago,
                    'message': f'⏳ شما {days_ago} روز پیش از پلن رایگان استفاده کردید. {30 - days_ago} روز دیگر صبر کنید یا از پلن‌های پولی استفاده کنید.'
                }
            else:
                # بیش از 30 روز گذشته - امکان استفاده مجدد
                return {
                    'can_use': True,
                    'reason': f'بیش از {days_ago} روز گذشته - امکان استفاده مجدد',
                    'tracking': existing_tracks,
                    'days_used_ago': days_ago,
                    'suggested_action': 'allow_with_reset'
                }
        
        except Exception as e:
            logger.error(f"❌ خطا در بررسی استفاده رایگان: {e}")
            # در صورت خطا، اجازه استفاده می‌دهیم (fail-open)
            return {
                'can_use': True,
                'reason': f'خطا در بررسی: {str(e)}',
                'tracking': None,
                'days_used_ago': 0,
                'suggested_action': 'error_allow'
            }
    
    @staticmethod
    def track_free_usage(
        username: str,
        analysis_id: int,
        store_name: str = '',
        email: str = '',
        phone: str = '',
        ip_address: str = None,
        request=None,
        user_agent: str = '',
        **kwargs
    ) -> FreeUsageTracking:
        """
        ثبت استفاده از پلن رایگان
        
        Returns:
            FreeUsageTracking: رکورد ایجاد شده
        """
        try:
            # دریافت IP
            if request and not ip_address:
                ip_address = FreeUsageChecker.get_user_ip(request)
            
            # Hash کردن IP
            ip_hash = FreeUsageChecker.hash_ip(ip_address) if ip_address else 'unknown'
            
            # دریافت User Agent
            if request and not user_agent:
                user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # ایجاد یا بروزرسانی رکورد
            tracking, created = FreeUsageTracking.objects.update_or_create(
                username=username,
                defaults={
                    'email': email if email else tracking.email if not created else '',
                    'phone': phone if phone else tracking.phone if not created else '',
                    'ip_address': ip_hash,
                    'analysis_id': analysis_id,
                    'store_name': store_name,
                    'user_agent': user_agent[:500],  # محدود کردن طول
                    'additional_info': kwargs
                }
            )
            
            logger.info(f"{'📝 ثبت جدید' if created else '🔄 بروزرسانی'} استفاده رایگان: {username}")
            
            return tracking
        
        except Exception as e:
            logger.error(f"❌ خطا در ثبت استفاده رایگان: {e}")
            raise
    
    @staticmethod
    def check_multiple_identifiers(request, username=None, email=None, phone=None) -> Dict:
        """بررسی با چندین شناسه به صورت همزمان"""
        ip = FreeUsageChecker.get_user_ip(request)
        
        return FreeUsageChecker.check_free_usage(
            username=username,
            email=email,
            phone=phone,
            ip_address=ip,
            request=request
        )

