"""
ابزارهای کمکی برای محاسبه هزینه‌ها و تحلیل هوش مصنوعی
"""
from decimal import Decimal
import json
from datetime import datetime, timedelta

def calculate_analysis_cost(form_data):
    """
    محاسبه هزینه تحلیل بر اساس درخواست‌های کاربر
    """
    # قیمت پایه
    base_price = Decimal('500000')  # 500,000 تومان
    
    # هزینه‌های اضافی بر اساس نوع گزارش
    report_costs = {
        'comprehensive_pdf': Decimal('200000'),
        'executive_summary': Decimal('100000'),
        'detailed_analysis': Decimal('150000'),
        'action_plan': Decimal('100000'),
        'implementation_guide': Decimal('120000'),
        'checklist': Decimal('50000'),
        'visual_dashboard': Decimal('300000'),
        'interactive_report': Decimal('250000'),
        'presentation_slides': Decimal('150000'),
        'excel_data': Decimal('80000'),
        'csv_export': Decimal('50000'),
        'heatmap_analysis': Decimal('200000'),
        'traffic_flow_diagram': Decimal('180000'),
        'space_optimization_plan': Decimal('220000'),
    }
    
    # هزینه‌های اضافی بر اساس اهداف
    goal_costs = {
        'increase_sales': Decimal('100000'),
        'improve_customer_experience': Decimal('80000'),
        'reduce_operational_costs': Decimal('120000'),
        'optimize_space_utilization': Decimal('150000'),
        'reduce_congestion': Decimal('100000'),
        'improve_security': Decimal('90000'),
        'increase_operational_efficiency': Decimal('110000'),
    }
    
    # هزینه‌های اضافی بر اساس نوع فروشگاه
    store_type_costs = {
        'supermarket': Decimal('50000'),
        'hypermarket': Decimal('100000'),
        'convenience': Decimal('30000'),
        'pharmacy': Decimal('40000'),
        'electronics': Decimal('60000'),
        'clothing': Decimal('70000'),
        'home_appliances': Decimal('80000'),
        'bookstore': Decimal('30000'),
        'cosmetics': Decimal('40000'),
        'sports': Decimal('50000'),
        'jewelry': Decimal('60000'),
        'furniture': Decimal('80000'),
        'automotive': Decimal('70000'),
        'pet_shop': Decimal('40000'),
        'garden_center': Decimal('50000'),
        'department': Decimal('120000'),
        'wholesale': Decimal('100000'),
    }
    
    # هزینه‌های اضافی بر اساس اندازه فروشگاه
    store_size = int(form_data.get('store_size', 0))
    size_cost = Decimal('0')
    if store_size > 1000:
        size_cost = Decimal('100000')
    elif store_size > 500:
        size_cost = Decimal('50000')
    elif store_size > 200:
        size_cost = Decimal('25000')
    
    # محاسبه هزینه‌های گزارش
    report_format = form_data.get('report_format', [])
    if isinstance(report_format, str):
        report_format = [report_format]
    
    report_total = Decimal('0')
    for report_type in report_format:
        if report_type in report_costs:
            report_total += report_costs[report_type]
    
    # محاسبه هزینه‌های اهداف
    optimization_goals = form_data.get('optimization_goals', [])
    if isinstance(optimization_goals, str):
        optimization_goals = [optimization_goals]
    
    goals_total = Decimal('0')
    for goal in optimization_goals:
        if goal in goal_costs:
            goals_total += goal_costs[goal]
    
    # محاسبه هزینه نوع فروشگاه
    store_type = form_data.get('store_type', '')
    store_type_cost = store_type_costs.get(store_type, Decimal('0'))
    
    # محاسبه کل هزینه
    total_cost = base_price + report_total + goals_total + store_type_cost + size_cost
    
    # تخفیف‌های احتمالی
    discount = Decimal('0')
    discount_percentage = 0
    
    # تخفیف برای سفارشات بزرگ
    if total_cost > Decimal('1000000'):
        discount_percentage = 15
        discount = total_cost * Decimal('0.15')
    elif total_cost > Decimal('800000'):
        discount_percentage = 10
        discount = total_cost * Decimal('0.10')
    elif total_cost > Decimal('600000'):
        discount_percentage = 5
        discount = total_cost * Decimal('0.05')
    
    final_amount = total_cost - discount
    
    # جزئیات هزینه‌ها
    breakdown = [
        {
            'item': 'تحلیل پایه',
            'amount': base_price,
            'description': 'تحلیل اولیه فروشگاه'
        },
        {
            'item': 'نوع فروشگاه',
            'amount': store_type_cost,
            'description': f'تحلیل تخصصی {store_type}'
        },
        {
            'item': 'اندازه فروشگاه',
            'amount': size_cost,
            'description': f'تحلیل فروشگاه {store_size} متر مربع'
        },
        {
            'item': 'گزارش‌های درخواستی',
            'amount': report_total,
            'description': f'{len(report_format)} نوع گزارش'
        },
        {
            'item': 'اهداف بهینه‌سازی',
            'amount': goals_total,
            'description': f'{len(optimization_goals)} هدف'
        }
    ]
    
    # حذف آیتم‌های صفر
    breakdown = [item for item in breakdown if item['amount'] > 0]
    
    if discount > 0:
        breakdown.append({
            'item': f'تخفیف {discount_percentage}%',
            'amount': -discount,
            'description': 'تخفیف سفارش بزرگ'
        })
    
    return {
        'base_price': base_price,
        'report_cost': report_total,
        'goals_cost': goals_total,
        'store_type_cost': store_type_cost,
        'size_cost': size_cost,
        'total': total_cost,
        'discount': discount,
        'discount_percentage': discount_percentage,
        'final': final_amount,
        'breakdown': breakdown
    }

def generate_initial_ai_analysis(analysis_data):
    """
    تولید تحلیل اولیه هوش مصنوعی
    """
    store_name = analysis_data.get('store_name', 'فروشگاه شما')
    store_type = analysis_data.get('store_type', '')
    store_size = analysis_data.get('store_size', '')
    
    # تحلیل اولیه بر اساس نوع فروشگاه
    store_type_analysis = {
        'supermarket': {
            'title': 'تحلیل اولیه سوپرمارکت',
            'insights': [
                'چیدمان محصولات بر اساس الگوی خرید مشتریان',
                'بهینه‌سازی مسیر حرکت در راهروها',
                'قرارگیری محصولات پرفروش در نقاط استراتژیک',
                'مدیریت صف‌های پرداخت'
            ]
        },
        'hypermarket': {
            'title': 'تحلیل اولیه هایپرمارکت',
            'insights': [
                'طراحی مسیر خرید برای افزایش زمان حضور مشتری',
                'چیدمان بخش‌های مختلف برای حداکثر فروش',
                'مدیریت ترافیک در ساعات پیک',
                'بهینه‌سازی فضای پارکینگ و ورودی'
            ]
        },
        'pharmacy': {
            'title': 'تحلیل اولیه داروخانه',
            'insights': [
                'چیدمان داروها بر اساس اولویت و دسترسی',
                'طراحی فضای مشاوره و انتظار',
                'مدیریت موجودی و تاریخ انقضا',
                'بهینه‌سازی فضای نمایش محصولات بهداشتی'
            ]
        },
        'electronics': {
            'title': 'تحلیل اولیه فروشگاه الکترونیک',
            'insights': [
                'نمایش محصولات برای حداکثر جذابیت',
                'طراحی فضای تست و تجربه محصولات',
                'مدیریت امنیت و نظارت',
                'چیدمان بر اساس دسته‌بندی و قیمت'
            ]
        }
    }
    
    # دریافت تحلیل نوع فروشگاه
    analysis = store_type_analysis.get(store_type, {
        'title': 'تحلیل اولیه فروشگاه',
        'insights': [
            'بهینه‌سازی چیدمان محصولات',
            'بهبود تجربه مشتری',
            'افزایش کارایی عملیاتی',
            'مدیریت بهتر فضا'
        ]
    })
    
    # تولید متن تحلیل
    analysis_text = f"""
# تحلیل اولیه {store_name}

## خلاصه اجرایی
بر اساس اطلاعات ارائه شده، فروشگاه شما از نوع {store_type} با مساحت {store_size} متر مربع می‌باشد. 
تحلیل اولیه نشان می‌دهد که پتانسیل قابل توجهی برای بهبود عملکرد و افزایش فروش وجود دارد.

## نکات کلیدی شناسایی شده:

"""
    
    for i, insight in enumerate(analysis['insights'], 1):
        analysis_text += f"{i}. {insight}\n"
    
    analysis_text += f"""

## توصیه‌های اولیه:

### 1. بهینه‌سازی چیدمان
- بررسی و بهبود چیدمان محصولات بر اساس الگوی خرید مشتریان
- استفاده بهتر از فضای موجود
- کاهش مناطق بلااستفاده

### 2. بهبود تجربه مشتری
- بهینه‌سازی مسیر حرکت مشتریان
- کاهش زمان انتظار در صف‌ها
- بهبود نورپردازی و دکوراسیون

### 3. افزایش کارایی عملیاتی
- بهینه‌سازی فرآیندهای کاری
- بهبود مدیریت موجودی
- کاهش هزینه‌های عملیاتی

## مراحل بعدی:
تحلیل کامل و تفصیلی شامل موارد زیر خواهد بود:
- تحلیل دقیق ترافیک مشتریان
- پیشنهادات تخصصی چیدمان
- برنامه عملیاتی بهبود
- محاسبه ROI پیشنهادات

---
*این تحلیل اولیه بر اساس اطلاعات ارائه شده تولید شده است. تحلیل کامل و تفصیلی پس از پردازش کامل داده‌ها ارائه خواهد شد.*
"""
    
    return analysis_text

def format_currency(amount):
    """
    فرمت کردن مبلغ به صورت تومان
    """
    return f"{amount:,.0f} تومان"

def get_analysis_priority(store_size, store_type, goals_count):
    """
    تعیین اولویت تحلیل
    """
    priority_score = 0
    
    # امتیاز بر اساس اندازه فروشگاه
    if store_size > 1000:
        priority_score += 3
    elif store_size > 500:
        priority_score += 2
    elif store_size > 200:
        priority_score += 1
    
    # امتیاز بر اساس نوع فروشگاه
    high_priority_types = ['hypermarket', 'department', 'wholesale']
    medium_priority_types = ['supermarket', 'electronics', 'clothing', 'furniture']
    
    if store_type in high_priority_types:
        priority_score += 3
    elif store_type in medium_priority_types:
        priority_score += 2
    else:
        priority_score += 1
    
    # امتیاز بر اساس تعداد اهداف
    if goals_count > 5:
        priority_score += 2
    elif goals_count > 3:
        priority_score += 1
    
    # تعیین اولویت نهایی
    if priority_score >= 7:
        return 'urgent'
    elif priority_score >= 5:
        return 'high'
    elif priority_score >= 3:
        return 'medium'
    else:
        return 'low'

def estimate_analysis_duration(store_size, report_types, goals_count):
    """
    تخمین مدت زمان تحلیل
    """
    base_duration = 30  # 30 دقیقه پایه
    
    # اضافه کردن زمان بر اساس اندازه فروشگاه
    if store_size > 1000:
        base_duration += 60
    elif store_size > 500:
        base_duration += 30
    elif store_size > 200:
        base_duration += 15
    
    # اضافه کردن زمان بر اساس نوع گزارش
    complex_reports = ['visual_dashboard', 'interactive_report', 'heatmap_analysis', 'space_optimization_plan']
    for report_type in report_types:
        if report_type in complex_reports:
            base_duration += 30
        else:
            base_duration += 10
    
    # اضافه کردن زمان بر اساس تعداد اهداف
    base_duration += goals_count * 5
    
    return min(base_duration, 300)  # حداکثر 5 ساعت
