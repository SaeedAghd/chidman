import logging
import os
from typing import Optional
from django.conf import settings
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from ..models import StoreAnalysis

logger = logging.getLogger(__name__)

class ReportGenerator:
    """تولیدکننده گزارش PDF"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_fonts()
    
    def _setup_fonts(self):
        """تنظیم فونت‌های فارسی"""
        try:
            # تلاش برای بارگذاری فونت فارسی
            font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Vazir.ttf')
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('Vazir', font_path))
                self.farsi_style = ParagraphStyle(
                    'Farsi',
                    parent=self.styles['Normal'],
                    fontName='Vazir',
                    fontSize=12,
                    alignment=1,  # وسط
                )
            else:
                self.farsi_style = self.styles['Normal']
        except Exception as e:
            logger.warning(f"Could not load Persian font: {e}")
            self.farsi_style = self.styles['Normal']
    
    def generate_analysis_report(self, analysis: StoreAnalysis) -> Optional[str]:
        """تولید گزارش تحلیل فروشگاه"""
        try:
            # ایجاد نام فایل
            filename = f"analysis_report_{analysis.id}_{analysis.store_name.replace(' ', '_')}.pdf"
            filepath = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
            
            # ایجاد دایرکتوری اگر وجود ندارد
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # ایجاد سند PDF
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            
            # عنوان گزارش
            title = Paragraph(f"گزارش تحلیل فروشگاه {analysis.store_name}", self.styles['Title'])
            story.append(title)
            story.append(Spacer(1, 20))
            
            # اطلاعات کلی
            story.extend(self._generate_basic_info(analysis))
            story.append(Spacer(1, 20))
            
            # نتایج تحلیل
            if hasattr(analysis, 'analysis_result') and analysis.analysis_result:
                story.extend(self._generate_analysis_results(analysis.analysis_result))
                story.append(Spacer(1, 20))
            
            # توصیه‌ها
            story.extend(self._generate_recommendations(analysis))
            
            # ساخت PDF
            doc.build(story)
            
            logger.info(f"Report generated successfully: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return None
    
    def _generate_basic_info(self, analysis: StoreAnalysis) -> list:
        """تولید بخش اطلاعات کلی"""
        elements = []
        
        # عنوان بخش
        section_title = Paragraph("اطلاعات کلی فروشگاه", self.styles['Heading2'])
        elements.append(section_title)
        elements.append(Spacer(1, 10))
        
        # جدول اطلاعات
        data = [
            ['نام فروشگاه', analysis.store_name],
            ['نوع فروشگاه', analysis.get_store_type_display()],
            ['شهر', analysis.city or 'نامشخص'],
            ['منطقه', analysis.area or 'نامشخص'],
            ['متراژ', f"{analysis.store_size} متر مربع" if analysis.store_size else 'نامشخص'],
            ['تاریخ تحلیل', analysis.created_at.strftime('%Y/%m/%d')],
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements
    
    def _generate_analysis_results(self, result) -> list:
        """تولید بخش نتایج تحلیل"""
        elements = []
        
        # عنوان بخش
        section_title = Paragraph("نتایج تحلیل", self.styles['Heading2'])
        elements.append(section_title)
        elements.append(Spacer(1, 10))
        
        # جدول امتیازات
        data = [
            ['بخش تحلیل', 'امتیاز'],
            ['امتیاز کلی', f"{result.overall_score}/100"],
            ['امتیاز چیدمان', f"{result.layout_score}/100"],
            ['امتیاز ترافیک', f"{result.traffic_score}/100"],
            ['امتیاز طراحی', f"{result.design_score}/100"],
            ['امتیاز فروش', f"{result.sales_score}/100"],
        ]
        
        table = Table(data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 15))
        
        # تحلیل کلی
        if result.overall_analysis:
            overall_title = Paragraph("تحلیل کلی", self.styles['Heading3'])
            elements.append(overall_title)
            elements.append(Spacer(1, 5))
            
            overall_text = Paragraph(result.overall_analysis, self.farsi_style)
            elements.append(overall_text)
            elements.append(Spacer(1, 10))
        
        return elements
    
    def _generate_recommendations(self, analysis: StoreAnalysis) -> list:
        """تولید بخش توصیه‌ها"""
        elements = []
        
        # عنوان بخش
        section_title = Paragraph("توصیه‌های بهبود", self.styles['Heading2'])
        elements.append(section_title)
        elements.append(Spacer(1, 10))
        
        # توصیه‌های کلی
        recommendations = [
            "بهبود چیدمان قفسه‌ها برای افزایش دسترسی مشتریان",
            "بهینه‌سازی مسیر حرکت مشتریان",
            "بهبود نورپردازی و طراحی بصری",
            "تحلیل و بهبود استراتژی فروش",
            "استفاده از تکنولوژی‌های نوین برای ردیابی رفتار مشتریان"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            rec_text = Paragraph(f"{i}. {rec}", self.farsi_style)
            elements.append(rec_text)
            elements.append(Spacer(1, 5))
        
        return elements

def generate_pdf_report(analysis: StoreAnalysis) -> Optional[str]:
    """تابع قدیمی برای سازگاری"""
    generator = ReportGenerator()
    return generator.generate_analysis_report(analysis) 