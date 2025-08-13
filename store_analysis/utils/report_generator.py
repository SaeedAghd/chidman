from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from django.conf import settings
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def generate_pdf_report(analysis):
    """تولید گزارش PDF از نتایج تحلیل"""
    try:
        # ایجاد مسیر فایل
        report_dir = os.path.join(settings.MEDIA_ROOT, 'analysis_reports')
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"analysis_report_{analysis.id}_{timestamp}.pdf"
        filepath = os.path.join(report_dir, filename)
        
        # ایجاد سند PDF
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # استایل‌ها
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=20
        )
        normal_style = styles['Normal']
        
        # محتوای گزارش
        story = []
        
        # عنوان
        story.append(Paragraph(f"گزارش تحلیل فروشگاه {analysis.store_name}", title_style))
        story.append(Spacer(1, 12))
        
        # اطلاعات فروشگاه
        story.append(Paragraph("اطلاعات فروشگاه", heading_style))
        store_info = [
            ["نام فروشگاه:", analysis.store_name],
            ["نوع فروشگاه:", analysis.get_store_type_display()],
            ["مساحت:", f"{analysis.store_size} متر مربع"],
            ["شهر:", analysis.city or "-"],
            ["منطقه:", analysis.area or "-"],
            ["محل صندوق:", analysis.checkout_location or "-"],
            ["تعداد قفسه:", str(analysis.shelf_count or 0)],
            ["مناطق بلااستفاده:", analysis.unused_areas or "-"],
            ["دوربین نظارتی:", "دارد" if analysis.has_surveillance else "ندارد"],
            ["تعداد دوربین:", str(analysis.camera_count or 0)],
            ["مسیر حرکت مشتریان:", analysis.get_customer_movement_paths_display()],
            ["سبک طراحی:", analysis.design_style or "-"],
            ["رنگ‌های اصلی:", analysis.brand_colors or "-"]
        ]
        store_table = Table(store_info, colWidths=[2*inch, 4*inch])
        store_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(store_table)
        story.append(Spacer(1, 20))
        
        # تحلیل اولیه
        if analysis.initial_analysis:
            story.append(Paragraph("تحلیل اولیه", heading_style))
            initial = analysis.initial_analysis
            
            if 'summary' in initial:
                story.append(Paragraph("خلاصه:", normal_style))
                for key, value in initial['summary'].items():
                    story.append(Paragraph(f"• {key}: {value}", normal_style))
                story.append(Spacer(1, 12))
            
            if 'suggestions' in initial:
                story.append(Paragraph("پیشنهادات:", normal_style))
                for suggestion in initial['suggestions']:
                    story.append(Paragraph(f"• {suggestion}", normal_style))
                story.append(Spacer(1, 12))
        
        # تحلیل تکمیلی
        if analysis.detailed_analysis:
            story.append(Paragraph("تحلیل تکمیلی", heading_style))
            detailed = analysis.detailed_analysis
            
            if 'summary' in detailed:
                story.append(Paragraph("خلاصه:", normal_style))
                for key, value in detailed['summary'].items():
                    story.append(Paragraph(f"• {key}: {value}", normal_style))
                story.append(Spacer(1, 12))
            
            if 'suggestions' in detailed:
                story.append(Paragraph("پیشنهادات:", normal_style))
                for suggestion in detailed['suggestions']:
                    story.append(Paragraph(f"• {suggestion}", normal_style))
                story.append(Spacer(1, 12))
        
        # ساخت PDF
        doc.build(story)
        
        return os.path.join('analysis_reports', filename)
        
    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}")
        return None 