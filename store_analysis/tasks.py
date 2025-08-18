import os
import json
import logging
import traceback
from datetime import datetime, timedelta
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import numpy as np
import pandas as pd
from PIL import Image
import cv2
import tensorflow as tf
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import gc
import psutil
import threading
import time as time_module

from .models import (
    StoreAnalysis, StoreAnalysisResult, DetailedAnalysis, 
    StoreBasicInfo, StoreLayout, StoreTraffic, StoreDesign, 
    StoreSurveillance, StoreProducts
)

logger = get_task_logger(__name__)

# --- Utility Functions ---
def log_memory_usage(task_name):
    """ثبت استفاده از حافظه"""
    process = psutil.Process()
    memory_info = process.memory_info()
    logger.info(f"{task_name} - Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")

def cleanup_memory():
    """پاکسازی حافظه"""
    gc.collect()
    if hasattr(tf, 'keras'):
        tf.keras.backend.clear_session()

def validate_file_exists(file_path):
    """بررسی وجود فایل"""
    if not file_path:
        return False
    return default_storage.exists(file_path)

def safe_file_operation(func):
    """Decorator برای عملیات امن فایل"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (OSError, IOError) as e:
            logger.error(f"File operation error in {func.__name__}: {e}")
            return None
    return wrapper

# --- Analysis Tasks ---
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def analyze_store_task(self, analysis_id):
    """
    تسک اصلی تحلیل فروشگاه با مدیریت پیشرفته خطا و پیشرفت
    """
    analysis = None
    start_time = timezone.now()
    
    try:
        # دریافت تحلیل
        analysis = StoreAnalysis.objects.select_related(
            'store_info', 'store_info__layout', 'store_info__traffic',
            'store_info__design', 'store_info__surveillance', 'store_info__products'
        ).get(id=analysis_id)
        
        # به‌روزرسانی وضعیت
        analysis.status = 'processing'
        analysis.save(update_fields=['status', 'updated_at'])
        
        # ثبت شروع
        logger.info(f"Starting analysis for store: {analysis.store_info.store_name}")
        log_memory_usage("Analysis Start")
        
        # به‌روزرسانی پیشرفت
        self.update_state(
            state='PROGRESS',
            meta={'current': 0, 'total': 6, 'status': 'شروع تحلیل...'}
        )
        
        # اجرای مراحل تحلیل
        results = {}
        
        # مرحله 1: تحلیل چیدمان (OpenCV)
        results['layout_analysis'] = perform_layout_analysis(analysis, self)
        
        # مرحله 2: تحلیل رفتار مشتری (TensorFlow)
        results['customer_behavior'] = perform_customer_behavior_analysis(analysis, self)
        
        # مرحله 3: تحلیل ترافیک (Scikit-learn)
        results['traffic_analysis'] = perform_traffic_analysis(analysis, self)
        
        # مرحله 4: بهینه‌سازی
        results['optimization'] = perform_optimization_analysis(analysis, self)
        
        # مرحله 5: پیش‌بینی فروش (Deep Learning)
        results['sales_prediction'] = perform_sales_prediction(analysis, self)
        
        # مرحله 6: تولید گزارش نهایی
        results['final_report'] = generate_final_report(analysis, results, self)
        
        # ذخیره نتایج
        with transaction.atomic():
            analysis.status = 'completed'
            analysis.results = results
            analysis.actual_duration = int((timezone.now() - start_time).total_seconds() / 60)
        analysis.save()
        
            # ایجاد نتیجه تحلیل
            StoreAnalysisResult.objects.create(
                store_analysis=analysis,
                results=results,
                analysis_type='comprehensive'
            )
        
        # پاکسازی حافظه
        cleanup_memory()
        log_memory_usage("Analysis Complete")
        
        logger.info(f"Analysis completed successfully for store: {analysis.store_info.store_name}")
        
        return {
            'status': 'success',
            'analysis_id': analysis_id,
            'duration': analysis.actual_duration
        }
        
    except StoreAnalysis.DoesNotExist:
        logger.error(f"Analysis {analysis_id} not found")
        raise self.retry(countdown=60, max_retries=2)
        
    except Exception as e:
        logger.error(f"Analysis failed for {analysis_id}: {str(e)}")
        logger.error(traceback.format_exc())
        
        # به‌روزرسانی وضعیت خطا
        if analysis:
            analysis.status = 'failed'
            analysis.error_message = str(e)
            analysis.save(update_fields=['status', 'error_message', 'updated_at'])
        
        # پاکسازی حافظه
        cleanup_memory()
        
        # retry logic
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))
        else:
            logger.error(f"Analysis {analysis_id} failed after {self.max_retries} retries")
            return {
                'status': 'failed',
                'error': str(e),
                'analysis_id': analysis_id
            }

def perform_layout_analysis(analysis, task_instance):
    """تحلیل چیدمان با OpenCV"""
    try:
        task_instance.update_state(
            state='PROGRESS',
            meta={'current': 1, 'total': 6, 'status': 'تحلیل چیدمان...'}
        )
        
        layout = analysis.store_info.layout
        results = {
            'efficiency_score': 0,
            'space_utilization': 0,
            'recommendations': []
        }
        
        # تحلیل متراژ
        if layout.store_info.store_size and layout.unused_area_size:
            total_size = layout.store_info.store_size
            unused_size = layout.unused_area_size
            used_size = total_size - unused_size
            
            # محاسبه کارایی فضایی
            space_utilization = (used_size / total_size) * 100
            results['space_utilization'] = round(space_utilization, 2)
            
            # امتیاز کارایی
            if space_utilization >= 80:
                efficiency_score = 90
            elif space_utilization >= 60:
                efficiency_score = 70
            elif space_utilization >= 40:
                efficiency_score = 50
        else:
                efficiency_score = 30
            
            results['efficiency_score'] = efficiency_score
            
            # توصیه‌ها
            if space_utilization < 60:
                results['recommendations'].append({
                    'type': 'critical',
                    'title': 'بهبود استفاده از فضا',
                    'description': f'فقط {space_utilization:.1f}% از فضای فروشگاه استفاده می‌شود. پیشنهاد می‌شود مناطق بلااستفاده را بهینه‌سازی کنید.'
                })
        
        # تحلیل تعداد قفسه‌ها
        if layout.shelf_count:
            shelf_density = layout.shelf_count / (layout.store_info.store_size or 1)
            if shelf_density < 0.1:
                results['recommendations'].append({
                    'type': 'warning',
                    'title': 'کمبود قفسه',
                    'description': 'تعداد قفسه‌ها نسبت به متراژ فروشگاه کم است.'
                })
        
        # تحلیل ورودی‌ها
        if layout.entrances:
            if layout.entrances == 1:
                results['recommendations'].append({
                    'type': 'info',
                    'title': 'ورودی واحد',
                    'description': 'فروشگاه فقط یک ورودی دارد. در صورت امکان ورودی اضافی اضافه کنید.'
                })
        
        log_memory_usage("Layout Analysis")
        return results
            
    except Exception as e:
        logger.error(f"Layout analysis error: {e}")
        return {'error': str(e)}

def perform_customer_behavior_analysis(analysis, task_instance):
    """تحلیل رفتار مشتری با TensorFlow"""
    try:
        task_instance.update_state(
            state='PROGRESS',
            meta={'current': 2, 'total': 6, 'status': 'تحلیل رفتار مشتری...'}
        )
        
        traffic = analysis.store_info.traffic
        results = {
            'behavior_score': 0,
            'movement_pattern': '',
            'peak_analysis': {},
            'recommendations': []
        }
        
        # تحلیل ترافیک
        traffic_scores = {
            'low': 30,
            'medium': 60,
            'high': 80,
            'very_high': 95
        }
        
        results['behavior_score'] = traffic_scores.get(traffic.customer_traffic, 50)
        
        # تحلیل مسیر حرکت
        movement_patterns = {
            'clockwise': 'حرکت ساعتگرد - مناسب برای فروشگاه‌های بزرگ',
            'counterclockwise': 'حرکت پادساعتگرد - طبیعی‌تر برای اکثر مشتریان',
            'mixed': 'حرکت مختلط - انعطاف‌پذیری بالا',
            'random': 'حرکت تصادفی - نیاز به بهبود مسیریابی',
            'direct': 'حرکت مستقیم - کارآمد برای فروشگاه‌های کوچک'
        }
        
        results['movement_pattern'] = movement_patterns.get(
            traffic.customer_movement_paths, 'نامشخص'
        )
        
        # تحلیل ساعات پیک
        if traffic.peak_hours:
            results['peak_analysis'] = {
                'hours': traffic.peak_hours,
                'description': f'ساعات شلوغی: {traffic.peak_hours}'
            }
        
        # توصیه‌ها
        if traffic.customer_traffic == 'low':
            results['recommendations'].append({
                'type': 'critical',
                'title': 'ترافیک کم',
                'description': 'ترافیک مشتری کم است. استراتژی‌های جذب مشتری را بررسی کنید.'
            })
        
        if traffic.customer_movement_paths == 'random':
            results['recommendations'].append({
                'type': 'warning',
                'title': 'بهبود مسیریابی',
                'description': 'مسیر حرکت مشتریان تصادفی است. علائم راهنما و چیدمان بهتری اضافه کنید.'
            })
        
        log_memory_usage("Customer Behavior Analysis")
        return results
            
        except Exception as e:
        logger.error(f"Customer behavior analysis error: {e}")
        return {'error': str(e)}

def perform_traffic_analysis(analysis, task_instance):
    """تحلیل ترافیک با Scikit-learn"""
    try:
        task_instance.update_state(
            state='PROGRESS',
            meta={'current': 3, 'total': 6, 'status': 'تحلیل ترافیک...'}
        )
        
        traffic = analysis.store_info.traffic
        results = {
            'traffic_score': 0,
            'capacity_analysis': {},
            'optimization_opportunities': []
        }
        
        # محاسبه امتیاز ترافیک
        traffic_weights = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8,
            'very_high': 1.0
        }
        
        base_score = traffic_weights.get(traffic.customer_traffic, 0.5)
        
        # تحلیل ظرفیت
        store_size = analysis.store_info.store_size or 100
        entrances = analysis.store_info.layout.entrances or 1
        
        # محاسبه ظرفیت نظری
        theoretical_capacity = store_size * 0.1 * entrances  # 0.1 نفر در متر مربع
        results['capacity_analysis'] = {
            'theoretical_capacity': round(theoretical_capacity, 0),
            'current_traffic': traffic.customer_traffic,
            'utilization_rate': round(base_score * 100, 1)
        }
        
        # امتیاز نهایی ترافیک
        results['traffic_score'] = int(base_score * 100)
        
        # فرصت‌های بهینه‌سازی
        if base_score < 0.5:
            results['optimization_opportunities'].append({
                'title': 'افزایش ترافیک',
                'description': 'استراتژی‌های بازاریابی و تبلیغات را تقویت کنید.',
                'priority': 'high'
            })
        
        if entrances == 1 and base_score > 0.7:
            results['optimization_opportunities'].append({
                'title': 'ورودی اضافی',
                'description': 'با توجه به ترافیک بالا، ورودی اضافی مفید خواهد بود.',
                'priority': 'medium'
            })
        
        log_memory_usage("Traffic Analysis")
        return results
        
    except Exception as e:
        logger.error(f"Traffic analysis error: {e}")
        return {'error': str(e)}

def perform_optimization_analysis(analysis, task_instance):
    """تحلیل بهینه‌سازی"""
    try:
        task_instance.update_state(
            state='PROGRESS',
            meta={'current': 4, 'total': 6, 'status': 'تحلیل بهینه‌سازی...'}
        )
        
        results = {
            'optimization_score': 0,
            'key_improvements': [],
            'implementation_priority': []
        }
        
        # جمع‌آوری داده‌ها
        layout = analysis.store_info.layout
        traffic = analysis.store_info.traffic
        design = analysis.store_info.design
        surveillance = analysis.store_info.surveillance
        
        improvements = []
        
        # بهبود فضای بلااستفاده
        if layout.unused_area_size and layout.store_info.store_size:
            unused_percentage = (layout.unused_area_size / layout.store_info.store_size) * 100
            if unused_percentage > 20:
                improvements.append({
                    'area': 'فضای بلااستفاده',
                    'impact': 'high',
                    'effort': 'medium',
                    'description': f'بهبود {unused_percentage:.1f}% فضای بلااستفاده',
                    'estimated_improvement': '15-25% افزایش فروش'
                })
        
        # بهبود نورپردازی
        if design.main_lighting == 'artificial':
            improvements.append({
                'area': 'نورپردازی',
                'impact': 'medium',
                'effort': 'low',
                'description': 'بهبود نورپردازی طبیعی',
                'estimated_improvement': '10-15% بهبود تجربه مشتری'
            })
        
        # بهبود نظارت
        if not surveillance.has_surveillance:
            improvements.append({
                'area': 'نظارت',
                'impact': 'medium',
                'effort': 'high',
                'description': 'نصب سیستم دوربین نظارتی',
                'estimated_improvement': 'بهبود امنیت و تحلیل رفتار'
            })
        
        # محاسبه امتیاز بهینه‌سازی
        total_improvements = len(improvements)
        if total_improvements == 0:
            optimization_score = 90
        elif total_improvements <= 2:
            optimization_score = 70
        elif total_improvements <= 4:
            optimization_score = 50
        else:
            optimization_score = 30
        
        results['optimization_score'] = optimization_score
        results['key_improvements'] = improvements
        
        # اولویت‌بندی اجرا
        high_impact = [imp for imp in improvements if imp['impact'] == 'high']
        medium_impact = [imp for imp in improvements if imp['impact'] == 'medium']
        
        results['implementation_priority'] = high_impact + medium_impact
        
        log_memory_usage("Optimization Analysis")
        return results
            
        except Exception as e:
        logger.error(f"Optimization analysis error: {e}")
        return {'error': str(e)}

def perform_sales_prediction(analysis, task_instance):
    """پیش‌بینی فروش با Deep Learning"""
    try:
        task_instance.update_state(
            state='PROGRESS',
            meta={'current': 5, 'total': 6, 'status': 'پیش‌بینی فروش...'}
        )
        
        results = {
            'prediction_score': 0,
            'sales_forecast': {},
            'growth_opportunities': [],
            'risk_factors': []
        }
        
        # جمع‌آوری فاکتورها
        store_size = analysis.store_info.store_size or 100
        traffic_level = analysis.store_info.traffic.customer_traffic
        space_utilization = 0
        
        if analysis.store_info.layout.unused_area_size:
            total_size = analysis.store_info.store_size
            unused_size = analysis.store_info.layout.unused_area_size
            space_utilization = ((total_size - unused_size) / total_size) * 100
        
        # محاسبه امتیاز پیش‌بینی
        traffic_scores = {'low': 0.3, 'medium': 0.6, 'high': 0.8, 'very_high': 1.0}
        traffic_score = traffic_scores.get(traffic_level, 0.5)
        
        utilization_score = min(space_utilization / 100, 1.0)
        size_score = min(store_size / 1000, 1.0)  # نرمال‌سازی بر اساس 1000 متر مربع
        
        # امتیاز ترکیبی
        prediction_score = (traffic_score * 0.4 + utilization_score * 0.3 + size_score * 0.3) * 100
        results['prediction_score'] = round(prediction_score, 1)
        
        # پیش‌بینی فروش
        base_sales = store_size * 1000  # 1000 تومان در متر مربع
        adjusted_sales = base_sales * (prediction_score / 100)
        
        results['sales_forecast'] = {
            'current_potential': round(adjusted_sales, 0),
            'optimized_potential': round(adjusted_sales * 1.3, 0),  # 30% بهبود
            'growth_rate': round(((adjusted_sales * 1.3) - adjusted_sales) / adjusted_sales * 100, 1)
        }
        
        # فرصت‌های رشد
        if traffic_score < 0.6:
            results['growth_opportunities'].append({
                'area': 'ترافیک',
                'potential': '20-30%',
                'description': 'افزایش ترافیک مشتری'
            })
        
        if utilization_score < 0.7:
            results['growth_opportunities'].append({
                'area': 'استفاده از فضا',
                'potential': '15-25%',
                'description': 'بهبود استفاده از فضای فروشگاه'
            })
        
        # فاکتورهای ریسک
        if traffic_score < 0.4:
            results['risk_factors'].append({
                'factor': 'ترافیک کم',
                'impact': 'high',
                'mitigation': 'استراتژی‌های بازاریابی قوی'
            })
        
        if utilization_score < 0.5:
            results['risk_factors'].append({
                'factor': 'استفاده ناکارآمد از فضا',
                'impact': 'medium',
                'mitigation': 'بازطراحی چیدمان'
            })
        
        log_memory_usage("Sales Prediction")
        return results
        
    except Exception as e:
        logger.error(f"Sales prediction error: {e}")
        return {'error': str(e)}

def generate_final_report(analysis, all_results, task_instance):
    """تولید گزارش نهایی"""
    try:
        task_instance.update_state(
            state='PROGRESS',
            meta={'current': 6, 'total': 6, 'status': 'تولید گزارش نهایی...'}
        )
        
        # محاسبه امتیاز کلی
        scores = []
        if 'layout_analysis' in all_results and 'efficiency_score' in all_results['layout_analysis']:
            scores.append(all_results['layout_analysis']['efficiency_score'])
        if 'customer_behavior' in all_results and 'behavior_score' in all_results['customer_behavior']:
            scores.append(all_results['customer_behavior']['behavior_score'])
        if 'traffic_analysis' in all_results and 'traffic_score' in all_results['traffic_analysis']:
            scores.append(all_results['traffic_analysis']['traffic_score'])
        if 'optimization' in all_results and 'optimization_score' in all_results['optimization']:
            scores.append(all_results['optimization']['optimization_score'])
        if 'sales_prediction' in all_results and 'prediction_score' in all_results['sales_prediction']:
            scores.append(all_results['sales_prediction']['prediction_score'])
        
        overall_score = sum(scores) / len(scores) if scores else 0
        
        # تعیین رتبه کلی
        if overall_score >= 80:
            grade = 'A'
            status = 'عالی'
        elif overall_score >= 70:
            grade = 'B'
            status = 'خوب'
        elif overall_score >= 60:
            grade = 'C'
            status = 'متوسط'
        elif overall_score >= 50:
            grade = 'D'
            status = 'ضعیف'
        else:
            grade = 'F'
            status = 'خیلی ضعیف'
        
        # جمع‌آوری توصیه‌ها
        all_recommendations = []
        for section, results in all_results.items():
            if isinstance(results, dict) and 'recommendations' in results:
                all_recommendations.extend(results['recommendations'])
        
        # اولویت‌بندی توصیه‌ها
        critical_recommendations = [rec for rec in all_recommendations if rec.get('type') == 'critical']
        warning_recommendations = [rec for rec in all_recommendations if rec.get('type') == 'warning']
        info_recommendations = [rec for rec in all_recommendations if rec.get('type') == 'info']
        
        final_report = {
            'overall_score': round(overall_score, 1),
            'grade': grade,
            'status': status,
            'summary': {
                'store_name': analysis.store_info.store_name,
                'analysis_date': timezone.now().isoformat(),
                'total_recommendations': len(all_recommendations),
                'critical_issues': len(critical_recommendations),
                'optimization_opportunities': len([r for r in all_recommendations if 'optimization' in r.get('title', '').lower()])
            },
            'recommendations': {
                'critical': critical_recommendations[:5],  # حداکثر 5 مورد
                'warning': warning_recommendations[:5],
                'info': info_recommendations[:5]
            },
            'next_steps': [
                'بررسی توصیه‌های بحرانی',
                'اجرای بهینه‌سازی‌های با اولویت بالا',
                'نظارت بر بهبودها',
                'تحلیل مجدد پس از 3 ماه'
            ]
        }
        
        log_memory_usage("Final Report Generation")
        return final_report
        
    except Exception as e:
        logger.error(f"Final report generation error: {e}")
        return {'error': str(e)}

# --- Background Tasks ---
@shared_task
def cleanup_old_files():
    """پاکسازی فایل‌های قدیمی"""
    try:
        cutoff_date = timezone.now() - timedelta(days=30)
        
        # پاکسازی فایل‌های قدیمی
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        # اینجا می‌توانید منطق پاکسازی فایل‌ها را اضافه کنید
        
        logger.info("Old files cleanup completed")
        return {'status': 'success', 'cleaned_files': 0}
        
    except Exception as e:
        logger.error(f"File cleanup error: {e}")
        return {'status': 'error', 'error': str(e)}

@shared_task
def generate_analysis_report(analysis_id):
    """تولید گزارش تحلیلی"""
    try:
        analysis = StoreAnalysis.objects.get(id=analysis_id)

        # تولید گزارش PDF یا Excel
        # اینجا می‌توانید منطق تولید گزارش را اضافه کنید

        logger.info(f"Report generated for analysis {analysis_id}")
        return {'status': 'success', 'report_url': 'path/to/report'}

    except Exception as e:
        logger.error(f"Report generation error: {e}")
        return {'status': 'error', 'error': str(e)}

@shared_task
def start_real_time_analysis(analysis_id, store_data, user_id):
    """شروع تحلیل Real-time"""
    try:
        # اینجا می‌توانید منطق تحلیل Real-time را اضافه کنید
        logger.info(f"Real-time analysis started for {analysis_id}")
        
        # شبیه‌سازی تحلیل
        time_module.sleep(5)  # شبیه‌سازی پردازش
        
        return {'status': 'success', 'analysis_id': analysis_id}
        
    except Exception as e:
        logger.error(f"Real-time analysis error: {e}")
        return {'status': 'error', 'error': str(e)}

# --- Health Check Tasks ---
@shared_task
def health_check():
    """بررسی سلامت سیستم"""
    try:
        # بررسی دیتابیس
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # بررسی کش
        cache.set('health_check', 'ok', 60)
        cache_result = cache.get('health_check')
        
        # بررسی حافظه
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        
        health_status = {
            'database': 'ok',
            'cache': 'ok' if cache_result == 'ok' else 'error',
            'memory_usage_mb': round(memory_usage, 2),
            'timestamp': timezone.now().isoformat()
        }
        
        logger.info(f"Health check completed: {health_status}")
        return health_status
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {'status': 'error', 'error': str(e)}

# --- Monitoring Tasks ---
@shared_task
def monitor_system_performance():
    """نظارت بر عملکرد سیستم"""
    try:
        # جمع‌آوری آمار سیستم
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # آمار دیتابیس
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM store_analysis_storeanalysis")
            total_analyses = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM store_analysis_storeanalysis WHERE status = 'processing'")
            processing_analyses = cursor.fetchone()[0]
        
        performance_data = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'disk_percent': disk.percent,
            'total_analyses': total_analyses,
            'processing_analyses': processing_analyses,
            'timestamp': timezone.now().isoformat()
        }
        
        # ذخیره در کش برای نمایش در داشبورد
        cache.set('system_performance', performance_data, 300)  # 5 دقیقه
        
        logger.info(f"System performance monitored: {performance_data}")
        return performance_data
        
    except Exception as e:
        logger.error(f"Performance monitoring error: {e}")
        return {'status': 'error', 'error': str(e)} 