#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from django.conf import settings
from django.utils import timezone
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

logger = logging.getLogger(__name__)

class ProfessionalReportGenerator:
    """تولیدکننده گزارش حرفه‌ای فروشگاه با ساختار استاندارد جهانی"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_persian_fonts()
        self._setup_custom_styles()
    
    def _setup_persian_fonts(self):
        """تنظیم فونت‌های فارسی"""
        try:
            # ثبت فونت فارسی
            font_path = os.path.join(settings.STATIC_ROOT, 'fonts', 'Vazir.ttf')
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('Vazir', font_path))
                logger.info("✅ فونت فارسی ثبت شد")
            else:
                logger.warning("⚠️ فونت فارسی یافت نشد")
        except Exception as e:
            logger.error(f"❌ خطا در ثبت فونت: {e}")
    
    def _setup_custom_styles(self):
        """تنظیم استایل‌های سفارشی"""
        # استایل عنوان اصلی
        self.styles.add(ParagraphStyle(
            name='PersianTitle',
            parent=self.styles['Title'],
            fontName='Vazir',
            fontSize=24,
            spaceAfter=30,
            alignment=2,  # راست‌چین
            textColor=colors.darkblue
        ))
        
        # استایل زیرعنوان
        self.styles.add(ParagraphStyle(
            name='PersianHeading',
            parent=self.styles['Heading1'],
            fontName='Vazir',
            fontSize=16,
            spaceAfter=12,
            alignment=2,
            textColor=colors.darkgreen
        ))
        
        # استایل متن فارسی
        self.styles.add(ParagraphStyle(
            name='PersianNormal',
            parent=self.styles['Normal'],
            fontName='Vazir',
            fontSize=12,
            spaceAfter=6,
            alignment=2,
            wordWrap='CJK'
        ))
    
    def validate_input_completeness(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """اعتبارسنجی کامل بودن داده‌های ورودی"""
        missing = []
        confidence_scores = {}
        
        # بررسی فایل فروش
        if not data.get("sales_file") and not data.get("sales_data"):
            missing.append("فایل فروش (csv/xlsx)")
            confidence_scores['sales'] = 0.3
        else:
            confidence_scores['sales'] = 0.9
        
        # بررسی پلان فروشگاه
        if not data.get("store_plan") and not data.get("layout_image"):
            missing.append("نقشه یا پلان فروشگاه")
            confidence_scores['layout'] = 0.4
        else:
            confidence_scores['layout'] = 0.8
        
        # بررسی ویدیو مشتری
        if not data.get("customer_video") and not data.get("traffic_data"):
            missing.append("ویدیوی مسیر مشتری")
            confidence_scores['traffic'] = 0.2
        else:
            confidence_scores['traffic'] = 0.9
        
        # بررسی تصاویر فروشگاه
        if not data.get("store_photos") or len(data.get("store_photos", [])) < 3:
            missing.append("تصاویر عمومی فروشگاه (حداقل 3 تصویر)")
            confidence_scores['visuals'] = 0.5
        else:
            confidence_scores['visuals'] = 0.8
        
        # محاسبه اعتماد کلی
        overall_confidence = sum(confidence_scores.values()) / len(confidence_scores)
        
        validation_result = {
            'missing_data': missing,
            'confidence_scores': confidence_scores,
            'overall_confidence': overall_confidence,
            'validation_message': self._generate_validation_message(missing, overall_confidence)
        }
        
        return validation_result
    
    def _generate_validation_message(self, missing: List[str], confidence: float) -> str:
        """تولید پیام اعتبارسنجی"""
        if not missing:
            return "✅ تمام داده‌های ضروری برای تحلیل موجود است."
        
        confidence_percent = int(confidence * 100)
        missing_text = "\n- ".join(missing)
        
        return f"""⚠️ تحلیل بر اساس داده‌های ناقص انجام می‌شود (اعتماد: {confidence_percent}%).
موارد زیر ارسال نشده‌اند:
- {missing_text}

توصیه: برای دریافت گزارش دقیق‌تر، لطفاً داده‌های ناقص را تکمیل کنید."""
    
    def generate_executive_summary(self, analysis_data: Dict[str, Any], store_data: Dict[str, Any]) -> str:
        """تولید خلاصه اجرایی"""
        store_name = store_data.get('store_name', 'فروشگاه')
        store_type = store_data.get('store_type', 'عمومی')
        
        # شاخص‌های کلیدی فعلی
        current_kpis = analysis_data.get('current_kpis', {})
        
        # اهداف پیشنهادی
        improvement_goals = analysis_data.get('improvement_goals', {})
        
        # پیش‌بینی اثرات
        predicted_effects = analysis_data.get('predicted_effects', {})
        
        summary = f"""
<h2>خلاصه اجرایی - گزارش تحلیل چیدمان {store_name}</h2>

<h3>📊 شاخص‌های کلیدی فعلی:</h3>
• ترافیک روزانه: {current_kpis.get('daily_traffic', 'نامشخص')} نفر
• نرخ تبدیل: {current_kpis.get('conversion_rate', 'نامشخص')}%
• فروش در متر مربع: {current_kpis.get('sales_per_sqm', 'نامشخص')} تومان
• زمان ماندگاری مشتری: {current_kpis.get('dwell_time', 'نامشخص')} دقیقه
• تعداد اقلام سبد خرید: {current_kpis.get('basket_items', 'نامشخص')} قلم

<h3>🎯 اهداف پیشنهادی:</h3>
• افزایش فروش: {improvement_goals.get('sales_increase', 'نامشخص')}%
• بهبود نرخ تبدیل: {improvement_goals.get('conversion_improvement', 'نامشخص')}%
• کاهش فضای بلااستفاده: {improvement_goals.get('space_optimization', 'نامشخص')}%
• بهبود تجربه بصری: {improvement_goals.get('visual_improvement', 'نامشخص')}%

<h3>📈 پیش‌بینی اثر اجرای اصلاحات:</h3>
• رشد فروش: +{predicted_effects.get('sales_growth', 'نامشخص')}%
• بهبود نرخ تبدیل: +{predicted_effects.get('conversion_growth', 'نامشخص')}%
• ROI: {predicted_effects.get('roi', 'نامشخص')}%
• زمان بازگشت سرمایه: {predicted_effects.get('payback_period', 'نامشخص')} ماه
"""
        
        return summary
    
    def generate_current_condition_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """تولید تحلیل وضعیت فعلی"""
        current_condition = analysis_data.get('current_condition', {})
        
        analysis = f"""
<h2>وضعیت فعلی فروشگاه</h2>

<h3>📋 خلاصه بصری پلان فعلی:</h3>
{current_condition.get('layout_summary', 'تحلیل پلان در حال انجام...')}

<h3>🔥 Heatmap حرکتی:</h3>
{current_condition.get('traffic_heatmap', 'تحلیل ترافیک در حال انجام...')}

<h3>📊 جداول عددی:</h3>
<table>
<tr><th>شاخص</th><th>مقدار فعلی</th><th>وضعیت</th></tr>
<tr><td>فروش روزانه</td><td>{current_condition.get('daily_sales', 'نامشخص')}</td><td>{self._get_status_emoji(current_condition.get('sales_status', 'medium'))}</td></tr>
<tr><td>نرخ تبدیل</td><td>{current_condition.get('conversion_rate', 'نامشخص')}%</td><td>{self._get_status_emoji(current_condition.get('conversion_status', 'medium'))}</td></tr>
<tr><td>فضای بلااستفاده</td><td>{current_condition.get('unused_space', 'نامشخص')}</td><td>{self._get_status_emoji(current_condition.get('space_status', 'medium'))}</td></tr>
<tr><td>ترافیک مسیر اصلی</td><td>{current_condition.get('main_traffic', 'نامشخص')}%</td><td>{self._get_status_emoji(current_condition.get('traffic_status', 'medium'))}</td></tr>
<tr><td>نور طبیعی</td><td>{current_condition.get('natural_light', 'نامشخص')}</td><td>{self._get_status_emoji(current_condition.get('light_status', 'medium'))}</td></tr>
</table>
"""
        
        return analysis
    
    def _get_status_emoji(self, status: str) -> str:
        """دریافت ایموجی وضعیت"""
        status_map = {
            'excellent': '🟢 عالی',
            'good': '🟢 خوب',
            'medium': '🟡 متوسط',
            'poor': '🔴 ضعیف',
            'critical': '🔴 بحرانی'
        }
        return status_map.get(status, '🟡 نامشخص')
    
    def generate_sales_analysis(self, analysis_data: Dict[str, Any], validation: Dict[str, Any]) -> str:
        """تولید تحلیل فروش"""
        sales_data = analysis_data.get('sales_analysis', {})
        
        analysis = f"""
<h2>تحلیل داده‌های فروش</h2>

{validation.get('validation_message', '')}

<h3>📈 نمودار ترند فروش:</h3>
{sales_data.get('sales_trend', 'تحلیل ترند فروش در حال انجام...')}

<h3>📊 دسته‌بندی محصولات:</h3>
{sales_data.get('product_categories', 'تحلیل دسته‌بندی محصولات در حال انجام...')}

<h3>🤖 تحلیل هوش مصنوعی:</h3>
• الگوی فصلی: {sales_data.get('seasonal_pattern', 'در حال تحلیل...')}
• پرفروش‌ترین دسته‌ها: {sales_data.get('top_categories', 'در حال تحلیل...')}
• نقاط ضعف فروش: {sales_data.get('weak_points', 'در حال تحلیل...')}
"""
        
        return analysis
    
    def generate_customer_flow_analysis(self, analysis_data: Dict[str, Any], validation: Dict[str, Any]) -> str:
        """تولید تحلیل مسیر مشتری"""
        flow_data = analysis_data.get('customer_flow', {})
        
        analysis = f"""
<h2>مسیر و رفتار مشتریان</h2>

{validation.get('validation_message', '')}

<h3>🗺️ Heatmap رفت‌وآمد:</h3>
{flow_data.get('traffic_heatmap', 'تحلیل ترافیک در حال انجام...')}

<h3>⏸️ نقاط توقف:</h3>
{flow_data.get('stop_points', 'تحلیل نقاط توقف در حال انجام...')}

<h3>📋 جداول مسیر مشتری:</h3>
<table>
<tr><th>مسیر معمول مشتری</th><th>درصد تردد</th><th>زمان توقف میانگین</th></tr>
<tr><td>ورودی تا تخفیف‌ها</td><td>{flow_data.get('entrance_to_discount', 'نامشخص')}%</td><td>{flow_data.get('discount_dwell_time', 'نامشخص')} ثانیه</td></tr>
<tr><td>قفسه جدیدها</td><td>{flow_data.get('new_items_traffic', 'نامشخص')}%</td><td>{flow_data.get('new_items_dwell_time', 'نامشخص')} ثانیه</td></tr>
<tr><td>صندوق پرداخت</td><td>{flow_data.get('checkout_traffic', 'نامشخص')}%</td><td>{flow_data.get('checkout_time', 'نامشخص')} ثانیه</td></tr>
</table>
"""
        
        return analysis
    
    def generate_design_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """تولید تحلیل طراحی و دکوراسیون"""
        design_data = analysis_data.get('design_analysis', {})
        
        analysis = f"""
<h2>طراحی و دکوراسیون</h2>

<h3>🎨 ترکیب رنگ برند:</h3>
{design_data.get('color_scheme', 'تحلیل رنگ‌بندی در حال انجام...')}

<h3>💡 نوع نورپردازی:</h3>
{design_data.get('lighting_analysis', 'تحلیل نورپردازی در حال انجام...')}

<h3>💡 پیشنهادات نورپردازی:</h3>
• افزایش کنتراست در بخش تخفیف‌ها
• نور متمرکز بر نقاط VIP
• بهبود رنگ‌بندی مطابق با مسیر روانی مشتری

<h3>🎯 تأثیر روانی رنگ‌ها:</h3>
{design_data.get('color_psychology', 'تحلیل روانشناسی رنگ در حال انجام...')}
"""
        
        return analysis
    
    def generate_layout_proposal(self, analysis_data: Dict[str, Any]) -> str:
        """تولید پیشنهادات چیدمان"""
        layout_data = analysis_data.get('layout_proposal', {})
        
        analysis = f"""
<h2>پلان جدید و پیشنهادات چیدمان</h2>

<h3>🔄 تصویر پیشنهادی قبل/بعد:</h3>
{layout_data.get('before_after', 'تصاویر پیشنهادی در حال تولید...')}

<h3>📋 جدول تغییرات:</h3>
<table>
<tr><th>ناحیه</th><th>تغییر پیشنهادی</th><th>هدف</th><th>اثر بر فروش</th></tr>
<tr><td>ورودی</td><td>{layout_data.get('entrance_change', 'نامشخص')}</td><td>کاهش ترافیک سرد</td><td>+{layout_data.get('entrance_effect', 'نامشخص')}%</td></tr>
<tr><td>قفسه نوشیدنی</td><td>{layout_data.get('beverage_change', 'نامشخص')}</td><td>افزایش دید</td><td>+{layout_data.get('beverage_effect', 'نامشخص')}%</td></tr>
<tr><td>بخش تخفیف‌ها</td><td>{layout_data.get('discount_change', 'نامشخص')}</td><td>بهبود جذب</td><td>+{layout_data.get('discount_effect', 'نامشخص')}%</td></tr>
</table>
"""
        
        return analysis
    
    def generate_financial_analysis(self, analysis_data: Dict[str, Any], validation: Dict[str, Any]) -> str:
        """تولید تحلیل مالی و ROI"""
        financial_data = analysis_data.get('financial_analysis', {})
        
        analysis = f"""
<h2>تحلیل مالی و ROI</h2>

{validation.get('validation_message', '')}

<h3>💰 هزینه اجرای اصلاحات:</h3>
• هزینه فوری: {financial_data.get('immediate_cost', 'نامشخص')} تومان
• هزینه میان‌مدت: {financial_data.get('medium_cost', 'نامشخص')} تومان
• هزینه بلندمدت: {financial_data.get('long_cost', 'نامشخص')} تومان
• کل هزینه: {financial_data.get('total_cost', 'نامشخص')} تومان

<h3>📈 رشد فروش پیش‌بینی‌شده:</h3>
• ماه اول: +{financial_data.get('month1_growth', 'نامشخص')}%
• ماه سوم: +{financial_data.get('month3_growth', 'نامشخص')}%
• ماه ششم: +{financial_data.get('month6_growth', 'نامشخص')}%

<h3>🔄 بازگشت سرمایه:</h3>
• ROI: {financial_data.get('roi', 'نامشخص')}%
• زمان بازگشت سرمایه: {financial_data.get('payback_period', 'نامشخص')} ماه
• NPV: {financial_data.get('npv', 'نامشخص')} تومان

<h3>📊 نمودار پیش‌بینی رشد درآمد:</h3>
{financial_data.get('revenue_chart', 'نمودار در حال تولید...')}
"""
        
        return analysis
    
    def generate_execution_plan(self, analysis_data: Dict[str, Any]) -> str:
        """تولید برنامه اجرایی"""
        execution_data = analysis_data.get('execution_plan', {})
        
        plan = f"""
<h2>برنامه اجرایی و هشدارهای سیستم</h2>

<h3>⚡ فوری (۰–۳ ماه):</h3>
• بهبود نورپردازی ویترین
• نصب تابلو راهنما
• اصلاح مسیرهای اضطراری

<h3>🔄 میان‌مدت (۳–۹ ماه):</h3>
• اصلاح چیدمان قفسه‌های کناری
• بهبود سیستم صف‌بندی
• نصب سیستم‌های نمایشی

<h3>🏗️ بلندمدت (۹–۱۸ ماه):</h3>
• بازسازی کامل ورودی
• نصب سیستم‌های هوشمند
• بهینه‌سازی کامل فضای فروش

<h3>⚠️ هشدارهای سیستم:</h3>
• در صورت ارسال تصاویر دقیق‌تر از قفسه‌ها، می‌توان نسخهٔ اصلاح‌شدهٔ این گزارش را با جزئیات کامل‌تری تولید کرد.
• تمام پیشنهادات بر اساس استانداردهای جهانی طراحی فروشگاه ارائه شده‌اند.
• اجرای تغییرات باید با نظارت متخصص انجام شود.
"""
        
        return plan
    
    def generate_complete_report(self, store_data: Dict[str, Any], analysis_data: Dict[str, Any], output_file: str) -> str:
        """تولید گزارش کامل"""
        try:
            # اعتبارسنجی داده‌ها
            validation = self.validate_input_completeness(store_data)
            
            # ایجاد سند PDF
            doc = SimpleDocTemplate(output_file, pagesize=(8.5*inch, 11*inch))
            story = []
            
            # صفحه 1: جلد و مشخصات
            story.append(Paragraph("گزارش تحلیل چیدمان فروشگاه", self.styles['PersianTitle']))
            story.append(Spacer(1, 20))
            
            # مشخصات مشتری
            customer_info = f"""
<h3>مشخصات مشتری:</h3>
• نام فروشگاه: {store_data.get('store_name', 'نامشخص')}
• شهر: {store_data.get('city', 'نامشخص')}
• متراژ: {store_data.get('area', 'نامشخص')} متر مربع
• نوع فروشگاه: {store_data.get('store_type', 'نامشخص')}
• تاریخ ارسال داده‌ها: {datetime.now().strftime('%Y/%m/%d')}
• نام تحلیلگر: AI Retail Analyst v2 – GPT-4.1 Engine
• درجه اطمینان مدل: {int(validation['overall_confidence'] * 100)}%
"""
            story.append(Paragraph(customer_info, self.styles['PersianNormal']))
            story.append(PageBreak())
            
            # صفحه 2: خلاصه اجرایی
            executive_summary = self.generate_executive_summary(analysis_data, store_data)
            story.append(Paragraph(executive_summary, self.styles['PersianNormal']))
            story.append(PageBreak())
            
            # صفحه 3: وضعیت فعلی
            current_condition = self.generate_current_condition_analysis(analysis_data)
            story.append(Paragraph(current_condition, self.styles['PersianNormal']))
            story.append(PageBreak())
            
            # صفحه 4: تحلیل فروش
            sales_analysis = self.generate_sales_analysis(analysis_data, validation)
            story.append(Paragraph(sales_analysis, self.styles['PersianNormal']))
            story.append(PageBreak())
            
            # صفحه 5: مسیر مشتری
            customer_flow = self.generate_customer_flow_analysis(analysis_data, validation)
            story.append(Paragraph(customer_flow, self.styles['PersianNormal']))
            story.append(PageBreak())
            
            # صفحه 6: طراحی
            design_analysis = self.generate_design_analysis(analysis_data)
            story.append(Paragraph(design_analysis, self.styles['PersianNormal']))
            story.append(PageBreak())
            
            # صفحه 7: پیشنهادات چیدمان
            layout_proposal = self.generate_layout_proposal(analysis_data)
            story.append(Paragraph(layout_proposal, self.styles['PersianNormal']))
            story.append(PageBreak())
            
            # صفحه 8: تحلیل مالی
            financial_analysis = self.generate_financial_analysis(analysis_data, validation)
            story.append(Paragraph(financial_analysis, self.styles['PersianNormal']))
            story.append(PageBreak())
            
            # صفحه 9: برنامه اجرایی
            execution_plan = self.generate_execution_plan(analysis_data)
            story.append(Paragraph(execution_plan, self.styles['PersianNormal']))
            
            # ساخت PDF
            doc.build(story)
            
            logger.info(f"✅ گزارش حرفه‌ای تولید شد: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"❌ خطا در تولید گزارش: {e}")
            raise e
