# from celery import shared_task
from django.utils import timezone
from .models import StoreAnalysis, DetailedAnalysis
from .ai_models import TrafficAnalyzer, CustomerBehaviorAnalyzer, LayoutAnalyzer
from .utils.report_generator import generate_pdf_report
from .utils.notification import send_email_notification, send_whatsapp_notification
import logging
from django.core.mail import send_mail
from django.conf import settings
import requests
import json
import os
import time

logger = logging.getLogger(__name__)

# @shared_task
def analyze_store_task(analysis_id):
    """تسک تحلیل فروشگاه با Celery"""
    try:
        analysis = StoreAnalysis.objects.get(id=analysis_id)
        analysis.status = 'processing'
        analysis.save()
        
        # تحلیل با استفاده از سرویس‌ها
        from .services.store_analysis_service import StoreAnalysisService
        service = StoreAnalysisService()
        result = service.analyze_store(analysis)
        
        logger.info(f"Analysis completed for {analysis_id}")
        return True
        
    except StoreAnalysis.DoesNotExist:
        logger.error(f"Analysis {analysis_id} not found")
        return False
    except Exception as e:
        logger.error(f"Analysis failed for {analysis_id}: {e}")
        try:
            analysis = StoreAnalysis.objects.get(id=analysis_id)
            analysis.status = 'failed'
            analysis.error_message = str(e)
            analysis.save()
        except Exception as save_error:
            logger.error(f"Failed to save error status: {save_error}")
        return False

# @shared_task
def generate_report_task(analysis_id):
    """تسک تولید گزارش با Celery"""
    try:
        analysis = StoreAnalysis.objects.get(id=analysis_id)
        
        # تولید گزارش PDF
        report_path = generate_pdf_report(analysis)
        
        if report_path:
            logger.info(f"Report generated for {analysis_id}")
            return report_path
        else:
            logger.error(f"Failed to generate report for {analysis_id}")
            return None
            
    except Exception as e:
        logger.error(f"Report generation failed for {analysis_id}: {e}")
        return None

# @shared_task
def cleanup_temp_files_task():
    """تسک پاکسازی فایل‌های موقت"""
    try:
        from .services.file_optimizer import FileOptimizer
        optimizer = FileOptimizer()
        optimizer.cleanup_temp_files()
        logger.info("Temp files cleanup completed")
        return True
    except Exception as e:
        logger.error(f"Temp files cleanup failed: {e}")
        return False

class TaskProcessor:
    @staticmethod
    def process_task(task):
        """
        پردازش تسک‌های مختلف
        """
        if task.task_type == 'generate_report':
            return TaskProcessor.generate_report(task)
        return False
    
    @staticmethod
    def generate_report(task):
        """
        تولید گزارش PDF و ارسال آن
        """
        try:
            # دریافت داده‌های فروشگاه
            store_data = task.data.get('store_data', {})
            initial_analysis = task.data.get('initial_analysis', {})
            
            # ایجاد تحلیل فروشگاه
            analysis = StoreAnalysis.objects.create(
                store_type=store_data.get('store_type', 'retail'),
                customer_traffic=store_data.get('customer_traffic', 0),
                store_description=store_data.get('store_description', ''),
                main_entrance=store_data.get('main_entrance', 'front'),
                checkout_location=store_data.get('checkout_location', 'front'),
                special_areas=store_data.get('special_areas', ''),
                initial_analysis=initial_analysis,
                status='completed'
            )
            
            # تولید گزارش PDF
            report_path = generate_pdf_report(analysis)
            analysis.report_file = report_path
            analysis.save()
            
            # ارسال ایمیل
            if store_data.get('email'):
                send_mail(
                    'گزارش تحلیل فروشگاه',
                    'گزارش تحلیل فروشگاه شما آماده است. لطفاً به پنل کاربری مراجعه کنید.',
                    settings.DEFAULT_FROM_EMAIL,
                    [store_data['email']],
                    fail_silently=False,
                )
            
            # ارسال پیام واتساپ
            if store_data.get('phone'):
                TaskProcessor.send_whatsapp_message(
                    store_data['phone'],
                    'گزارش تحلیل فروشگاه شما آماده است. لطفاً به پنل کاربری مراجعه کنید.'
                )
            
            return True
            
        except Exception as e:
            print(f"Error in generate_report: {str(e)}")
            return False
    
    @staticmethod
    def send_whatsapp_message(phone, message):
        """
        ارسال پیام واتساپ
        """
        try:
            headers = {
                'Authorization': f'Bearer {settings.WHATSAPP_API_TOKEN}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'to': phone,
                'message': message
            }
            
            response = requests.post(
                settings.WHATSAPP_API_URL,
                headers=headers,
                json=data
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return False

# @shared_task
def process_detailed_analysis(analysis_id):
    try:
        analysis = StoreAnalysis.objects.get(id=analysis_id)
        analyzer = LayoutAnalyzer()
        
        # تحلیل اولیه
        initial_analysis = analyzer.analyze_layout(
            store_type=analysis.store_type,
            store_size=analysis.store_size,
            main_entrance=analysis.main_entrance,
            checkout_location=analysis.checkout_location,
            special_areas=analysis.special_areas,
            customer_traffic=analysis.customer_traffic,
            avg_customer_time=analysis.avg_customer_time,
            customer_type=analysis.customer_type,
            main_lighting=analysis.main_lighting,
            lighting_intensity=analysis.lighting_intensity,
            color_temperature=analysis.color_temperature,
            product_categories=analysis.product_categories,
            product_placement=analysis.product_placement
        )
        
        # ذخیره تحلیل اولیه
        analysis.initial_analysis = initial_analysis
        analysis.status = 'processing'
        analysis.save()
        
        # ارسال ایمیل تحلیل اولیه
        send_mail(
            'تحلیل اولیه فروشگاه',
            f'تحلیل اولیه فروشگاه {analysis.store_name} با موفقیت انجام شد.',
            settings.DEFAULT_FROM_EMAIL,
            [analysis.email],
            fail_silently=True,
        )
        
        # تحلیل تکمیلی
        detailed_analysis = analyzer.generate_detailed_analysis(initial_analysis)
        
        # ذخیره تحلیل تکمیلی
        analysis.detailed_analysis = detailed_analysis
        analysis.status = 'completed'
        analysis.save()
        
        # ارسال ایمیل تحلیل تکمیلی
        send_mail(
            'تحلیل تکمیلی فروشگاه',
            f'تحلیل تکمیلی فروشگاه {analysis.store_name} با موفقیت انجام شد.',
            settings.DEFAULT_FROM_EMAIL,
            [analysis.email],
            fail_silently=True,
        )
        
        return True
    except Exception as e:
        if analysis:
            analysis.status = 'failed'
            analysis.save()
            
            # ارسال ایمیل خطا
            send_mail(
                'خطا در تحلیل فروشگاه',
                f'متأسفانه در تحلیل فروشگاه {analysis.store_name} خطایی رخ داد.',
                settings.DEFAULT_FROM_EMAIL,
                [analysis.email],
                fail_silently=True,
            )
        
        raise e

# @shared_task
def analyze_store_layout(analysis_id):
    try:
        analysis = StoreAnalysis.objects.get(id=analysis_id)
        analysis.status = 'processing'
        analysis.save()

        analyzer = LayoutAnalyzer()
        result = analyzer.analyze(analysis.layout_image.path)

        analysis.analysis_result = result
        analysis.status = 'completed'
        analysis.save()

        return True
    except Exception as e:
        if analysis:
            analysis.status = 'failed'
            analysis.save()
        raise e 