from django import template
from django.utils import timezone
import jdatetime

register = template.Library()

@register.filter
def persian_date(value):
    """تبدیل تاریخ میلادی به شمسی"""
    if not value:
        return '-'
    
    try:
        # تبدیل به تاریخ شمسی
        persian_date = jdatetime.datetime.fromgregorian(datetime=value)
        return persian_date.strftime('%Y/%m/%d %H:%M')
    except:
        return value

@register.filter
def persian_date_only(value):
    """تبدیل تاریخ میلادی به شمسی (فقط تاریخ)"""
    if not value:
        return '-'
    
    try:
        persian_date = jdatetime.datetime.fromgregorian(datetime=value)
        return persian_date.strftime('%Y/%m/%d')
    except:
        return value

@register.filter
def persian_time_only(value):
    """تبدیل تاریخ میلادی به شمسی (فقط زمان)"""
    if not value:
        return '-'
    
    try:
        persian_date = jdatetime.datetime.fromgregorian(datetime=value)
        return persian_date.strftime('%H:%M')
    except:
        return value

@register.filter
def get_status_text(status):
    """تبدیل وضعیت انگلیسی به فارسی"""
    status_map = {
        'pending': 'در انتظار',
        'processing': 'در حال پردازش',
        'completed': 'تکمیل شده',
        'failed': 'ناموفق',
        'draft': 'پیش‌نویس',
        'preliminary_completed': 'تحلیل اولیه تکمیل شده',
    }
    return status_map.get(status, status)

@register.filter
def get_store_type_text(store_type):
    """تبدیل نوع فروشگاه انگلیسی به فارسی"""
    type_map = {
        'clothing': 'پوشاک',
        'electronics': 'الکترونیک',
        'grocery': 'مواد غذایی',
        'cosmetics': 'آرایشی و بهداشتی',
        'books': 'کتاب و لوازم التحریر',
        'home_appliances': 'لوازم خانگی',
        'jewelry': 'جواهرات',
        'sports': 'ورزشی',
        'toys': 'اسباب بازی',
        'other': 'سایر',
    }
    return type_map.get(store_type, store_type)

@register.filter
def get_store_size_text(size):
    """تبدیل اندازه فروشگاه انگلیسی به فارسی"""
    size_map = {
        'small': 'کوچک (کمتر از 50 متر)',
        'medium': 'متوسط (50-150 متر)',
        'large': 'بزرگ (150-300 متر)',
        'xlarge': 'خیلی بزرگ (بیش از 300 متر)',
    }
    return size_map.get(size, size)

@register.filter
def format_unknown(value):
    """فرمت کردن مقادیر نامشخص"""
    if not value or value in ['نامشخص', 'unknown', 'null', 'None', '']:
        return 'نامشخص'
    return value
