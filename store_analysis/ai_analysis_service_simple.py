#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Optimized by Craser for Chidmano AI - Enhanced Analysis Service

import json
import logging
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import numpy as np
import os
import pandas as pd
from django.core.cache import cache
from django.utils import timezone
from pathlib import Path

from .services.liara_ai_client import LiaraAIClient, LiaraAIError

logger = logging.getLogger(__name__)

class SimpleAIAnalysisService:
    """سرویس تحلیل هوش مصنوعی پیشرفته برای فروشگاه‌ها - بهینه‌سازی شده"""
    
    def __init__(self):
        self.cache_timeout = 3600  # 1 hour cache
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.analysis_cache = {}
        self.ai_client = LiaraAIClient()
        
    async def analyze_store_async(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل ناهمزمان فروشگاه با استفاده از AI پیشرفته"""
        try:
            # بررسی cache
            cache_key = f"analysis_{hash(str(store_data))}"
            cached_result = cache.get(cache_key)
            if cached_result:
                logger.info("تحلیل از cache بازیابی شد")
                return cached_result
            
            logger.info(f"شروع تحلیل AI پیشرفته برای فروشگاه: {store_data.get('store_name', 'نامشخص')}")
            
            # تحلیل‌های موازی
            tasks = [
                self._analyze_layout_advanced(store_data),
                self._analyze_traffic_patterns_advanced(store_data),
                self._analyze_customer_behavior_advanced(store_data),
                self._analyze_sales_data(store_data),
                self._analyze_image_data(store_data)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # ترکیب نتایج
            analysis_result = self._combine_analysis_results(store_data, results)
            
            # ذخیره در cache
            cache.set(cache_key, analysis_result, self.cache_timeout)
            
            logger.info(f"تحلیل AI پیشرفته تکمیل شد - امتیاز: {analysis_result.get('overall_score', 0)}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"خطا در تحلیل ناهمزمان: {e}")
            return self._get_fallback_analysis(store_data)
    
    def analyze_store(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل فروشگاه با استفاده از تحلیل پیشرفته"""
        try:
            # اجرای تحلیل ناهمزمان
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.analyze_store_async(store_data))
            loop.close()
            return result
        except Exception as e:
            logger.error(f"خطا در تحلیل فروشگاه: {e}")
            return self._get_fallback_analysis(store_data)
    
    async def _analyze_layout_advanced(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل پیشرفته چیدمان فروشگاه"""
        try:
            store_type = store_data.get('store_type', 'عمومی')
            store_size = float(store_data.get('store_size', 0))
            
            # تحلیل بر اساس نوع فروشگاه
            layout_scores = {
                'supermarket': {'aisle_width': 0.9, 'product_density': 0.8, 'checkout_efficiency': 0.7},
                'clothing': {'display_area': 0.9, 'fitting_rooms': 0.8, 'circulation': 0.7},
                'electronics': {'demo_area': 0.9, 'security': 0.8, 'product_grouping': 0.7},
                'pharmacy': {'prescription_area': 0.9, 'otc_display': 0.8, 'privacy': 0.7},
                'عمومی': {'general_layout': 0.7, 'product_placement': 0.6, 'customer_flow': 0.6}
            }
            
            base_scores = layout_scores.get(store_type, layout_scores['عمومی'])
            
            # تنظیم بر اساس اندازه فروشگاه
            size_factor = min(store_size / 100, 1.0) if store_size > 0 else 0.5
            
            return {
                'layout_type': store_type,
                'size_factor': size_factor,
                'scores': {k: v * size_factor for k, v in base_scores.items()},
                'recommendations': self._get_layout_recommendations(store_type, store_size),
                'confidence': 0.85
            }
            
        except Exception as e:
            logger.error(f"خطا در تحلیل چیدمان: {e}")
            return {'error': str(e), 'confidence': 0.3}
    
    async def _analyze_traffic_patterns_advanced(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل پیشرفته الگوهای ترافیک"""
        try:
            # تحلیل بر اساس داده‌های موجود
            peak_hours = store_data.get('peak_hours', '10-12, 18-20')
            customer_count = int(store_data.get('daily_customers', 100))
            
            # محاسبه الگوهای ترافیک
            traffic_patterns = {
                'peak_hours': peak_hours,
                'average_customers_per_hour': customer_count / 12,
                'traffic_density': 'high' if customer_count > 200 else 'medium' if customer_count > 100 else 'low',
                'bottlenecks': self._identify_bottlenecks(store_data),
                'flow_efficiency': self._calculate_flow_efficiency(store_data)
            }
            
            return {
                'patterns': traffic_patterns,
                'recommendations': self._get_traffic_recommendations(traffic_patterns),
                'confidence': 0.8
            }
            
        except Exception as e:
            logger.error(f"خطا در تحلیل ترافیک: {e}")
            return {'error': str(e), 'confidence': 0.3}
    
    async def _analyze_customer_behavior_advanced(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل پیشرفته رفتار مشتریان"""
        try:
            # تحلیل بر اساس نوع محصولات و چیدمان
            product_categories = store_data.get('product_categories', [])
            store_type = store_data.get('store_type', 'عمومی')
            
            behavior_analysis = {
                'dwell_time': self._estimate_dwell_time(store_type, product_categories),
                'purchase_patterns': self._analyze_purchase_patterns(product_categories),
                'customer_segments': self._identify_customer_segments(store_type),
                'conversion_factors': self._identify_conversion_factors(store_data)
            }
            
            return {
                'behavior': behavior_analysis,
                'recommendations': self._get_behavior_recommendations(behavior_analysis),
                'confidence': 0.75
            }
            
        except Exception as e:
            logger.error(f"خطا در تحلیل رفتار مشتری: {e}")
            return {'error': str(e), 'confidence': 0.3}
    
    async def _analyze_sales_data(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل داده‌های فروش با pandas"""
        try:
            # بررسی وجود فایل فروش
            sales_file_path = None
            if 'uploaded_files' in store_data:
                uploaded_files = store_data['uploaded_files']
                if 'sales_file' in uploaded_files and 'path' in uploaded_files['sales_file']:
                    sales_file_path = uploaded_files['sales_file']['path']
            
            if sales_file_path and os.path.exists(sales_file_path):
                # تحلیل فایل فروش واقعی
                return await self._analyze_real_sales_data(sales_file_path)
            else:
                # تحلیل تخمینی بر اساس داده‌های موجود
                return await self._analyze_estimated_sales_data(store_data)
                
        except Exception as e:
            logger.error(f"خطا در تحلیل فروش: {e}")
            return {'error': str(e), 'confidence': 0.3}
    
    async def _analyze_image_data(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل داده‌های تصویری"""
        try:
            if 'image_analysis' in store_data:
                return store_data['image_analysis']
            else:
                return {'status': 'no_images', 'confidence': 0.5}
                
        except Exception as e:
            logger.error(f"خطا در تحلیل تصاویر: {e}")
            return {'error': str(e), 'confidence': 0.3}
    
    def _combine_analysis_results(self, store_data: Dict[str, Any], results: List[Any]) -> Dict[str, Any]:
        """ترکیب نتایج تحلیل‌ها"""
        try:
            # استخراج نتایج موفق
            successful_results = [r for r in results if not isinstance(r, Exception)]
            
            if not successful_results:
                return self._get_fallback_analysis(store_data)
            
            # محاسبه امتیاز کلی
            overall_score = self._calculate_advanced_score(successful_results)
            
            # تولید گزارش نهایی
            final_report = {
                "status": "ok",
                "confidence": min(0.95, sum(r.get('confidence', 0.5) for r in successful_results) / len(successful_results)),
                "summary": self._generate_advanced_summary(store_data, successful_results),
                "key_findings": self._extract_key_findings(successful_results),
                "recommendations": self._generate_advanced_recommendations(successful_results),
                "predictions": self._generate_predictions(store_data, successful_results),
                "overall_score": overall_score,
                "report_ready": True,
                "timestamp": timezone.now().isoformat()
            }
            
            if self.ai_client.enabled:
                try:
                    enriched = self._generate_managerial_summary_with_ai(store_data, final_report)
                    if enriched:
                        final_report.update(enriched)
                        final_report.setdefault('metadata', {})['summary_model'] = 'openai/gpt-4o-mini'
                except LiaraAIError as exc:
                    logger.warning("⚠️ خطا در تولید خلاصه مدیریتی با Liara: %s", exc)
                except Exception as exc:  # pragma: no cover
                    logger.error("❌ خطای غیرمنتظره در خلاصه مدیریتی: %s", exc, exc_info=True)

            return final_report
            
        except Exception as e:
            logger.error(f"خطا در ترکیب نتایج: {e}")
            return self._get_fallback_analysis(store_data)
    
    def _get_fallback_analysis(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل fallback در صورت خطا"""
        return {
            "status": "ok",
            "confidence": 0.6,
            "summary": f"تحلیل پایه برای فروشگاه {store_data.get('store_name', 'نامشخص')} انجام شد. برای تحلیل دقیق‌تر، لطفاً اطلاعات بیشتری ارائه دهید.",
            "key_findings": ["نیاز به اطلاعات بیشتر برای تحلیل دقیق"],
            "recommendations": {
                "layout": ["بهبود چیدمان کلی"],
                "lighting": ["بررسی سیستم روشنایی"],
                "customer_flow": ["بهینه‌سازی مسیر مشتریان"]
            },
            "predictions": {
                "expected_sales_increase": "+15%",
                "roi": "6 ماه"
            },
            "overall_score": 65,
            "report_ready": True,
            "timestamp": timezone.now().isoformat()
        }

    def _generate_managerial_summary_with_ai(self, store_data: Dict[str, Any], base_report: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """تهیه خلاصه مدیریتی دقیق با GPT-4o-mini"""

        system_prompt = (
            "تو یک مشاور ارشد خرده‌فروشی هستی. خروجی باید JSON با کلیدهای "
            "summary (متن مدیریتی حداکثر 180 کلمه)، key_findings (لیست بولت کوتاه)، "
            "recommendations (لیستی شامل سه پیشنهاد اجرایی با تمرکز مدیریتی) باشد."
        )

        data_snippet = {
            "store": store_data,
            "report": {
                "summary": base_report.get('summary'),
                "key_findings": base_report.get('key_findings'),
                "recommendations": base_report.get('recommendations'),
                "predictions": base_report.get('predictions'),
                "overall_score": base_report.get('overall_score'),
            }
        }

        # محدود کردن طول prompt
        data_snippet_str = json.dumps(data_snippet, ensure_ascii=False, default=str)
        if len(data_snippet_str) > 2500:
            data_snippet_str = data_snippet_str[:2500]
            logger.warning("⚠️ Managerial summary prompt truncated to 2500 chars")
        
        user_prompt = (
            "تحلیل اولیه انجام شده است. لطفاً بر اساس داده‌های زیر خلاصه مدیریتی ارائه کن:\n"
            f"{data_snippet_str}"
        )

        try:
            response = self.ai_client.chat(
                model='openai/gpt-4o-mini',
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.25,
                max_output_tokens=1500,
            )

            data = response.json()
            enriched: Dict[str, Any] = {}
            if data.get('summary'):
                enriched['summary'] = data['summary']
            if data.get('key_findings'):
                enriched['key_findings'] = data['key_findings']
            if data.get('recommendations'):
                enriched['executive_recommendations'] = data['recommendations']
            
            if enriched:
                logger.info("✅ Managerial summary با AI تولید شد")
            else:
                logger.warning("⚠️ Managerial summary خالی است")
            
            return enriched
        except LiaraAIError as exc:
            logger.warning("⚠️ خطا در تولید Managerial summary با Liara: %s", exc)
            return None
        except Exception as exc:
            logger.error("❌ خطای غیرمنتظره در Managerial summary: %s", exc, exc_info=True)
            return None
    
    # متدهای کمکی برای تحلیل پیشرفته
    def _get_layout_recommendations(self, store_type: str, store_size: float) -> List[str]:
        """تولید توصیه‌های چیدمان"""
        recommendations = {
            'supermarket': [
                "عرض راهروها را به حداقل 1.5 متر افزایش دهید",
                "محصولات پرفروش را در انتهای راهروها قرار دهید",
                "صندوق‌های پرداخت را در نقاط مختلف قرار دهید"
            ],
            'clothing': [
                "فضای کافی برای اتاق‌های پرو فراهم کنید",
                "محصولات جدید را در ورودی نمایش دهید",
                "مسیر گردش مشتریان را بهینه کنید"
            ],
            'electronics': [
                "فضای نمایش محصولات را افزایش دهید",
                "سیستم امنیتی را تقویت کنید",
                "محصولات مرتبط را کنار هم قرار دهید"
            ],
            'pharmacy': [
                "بخش نسخه را از سایر بخش‌ها جدا کنید",
                "محصولات OTC را در دسترس قرار دهید",
                "حریم خصوصی مشتریان را حفظ کنید"
            ]
        }
        return recommendations.get(store_type, ["بهبود چیدمان کلی فروشگاه"])
    
    def _identify_bottlenecks(self, store_data: Dict[str, Any]) -> List[str]:
        """شناسایی گلوگاه‌ها"""
        bottlenecks = []
        store_size = float(store_data.get('store_size', 0))
        daily_customers = int(store_data.get('daily_customers', 100))
        
        if store_size < 50 and daily_customers > 100:
            bottlenecks.append("فضای محدود برای تعداد مشتریان")
        
        if daily_customers > 200:
            bottlenecks.append("نیاز به صندوق‌های پرداخت بیشتر")
        
        return bottlenecks
    
    def _calculate_flow_efficiency(self, store_data: Dict[str, Any]) -> float:
        """محاسبه کارایی جریان مشتریان"""
        store_size = float(store_data.get('store_size', 0))
        daily_customers = int(store_data.get('daily_customers', 100))
        
        if store_size == 0:
            return 0.5
        
        # محاسبه بر اساس نسبت مشتری به متر مربع
        customer_density = daily_customers / store_size
        
        if customer_density < 2:
            return 0.9
        elif customer_density < 4:
            return 0.7
        else:
            return 0.5
    
    def _estimate_dwell_time(self, store_type: str, product_categories: List[str]) -> Dict[str, Any]:
        """تخمین زمان ماندگاری مشتریان"""
        base_times = {
            'supermarket': {'min': 15, 'max': 45, 'avg': 25},
            'clothing': {'min': 20, 'max': 60, 'avg': 35},
            'electronics': {'min': 30, 'max': 90, 'avg': 50},
            'pharmacy': {'min': 10, 'max': 30, 'avg': 18},
            'عمومی': {'min': 15, 'max': 40, 'avg': 25}
        }
        
        return base_times.get(store_type, base_times['عمومی'])
    
    def _analyze_purchase_patterns(self, product_categories: List[str]) -> Dict[str, Any]:
        """تحلیل الگوهای خرید"""
        return {
            'impulse_buy_potential': 'high' if len(product_categories) > 5 else 'medium',
            'cross_selling_opportunities': len(product_categories),
            'seasonal_patterns': 'moderate'
        }
    
    def _identify_customer_segments(self, store_type: str) -> List[str]:
        """شناسایی بخش‌های مشتریان"""
        segments = {
            'supermarket': ['خانواده‌ها', 'سالمندان', 'شاغلین'],
            'clothing': ['جوانان', 'میانسالان', 'خانواده‌ها'],
            'electronics': ['تکنولوژی‌دوستان', 'حرفه‌ای‌ها', 'دانشجویان'],
            'pharmacy': ['سالمندان', 'والدین', 'بیماران مزمن']
        }
        return segments.get(store_type, ['مشتریان عمومی'])
    
    def _identify_conversion_factors(self, store_data: Dict[str, Any]) -> List[str]:
        """شناسایی عوامل تبدیل"""
        factors = []
        
        if store_data.get('lighting_type') == 'mixed':
            factors.append("روشنایی مناسب")
        
        if float(store_data.get('store_size', 0)) > 100:
            factors.append("فضای کافی")
        
        if int(store_data.get('daily_customers', 0)) > 150:
            factors.append("ترافیک بالا")
        
        return factors if factors else ["نیاز به بهبود عوامل تبدیل"]
    
    def _get_traffic_recommendations(self, traffic_patterns: Dict[str, Any]) -> List[str]:
        """توصیه‌های ترافیک"""
        recommendations = []
        
        if traffic_patterns['traffic_density'] == 'high':
            recommendations.append("افزایش تعداد صندوق‌های پرداخت")
            recommendations.append("بهینه‌سازی مسیرهای ورود و خروج")
        
        if traffic_patterns['flow_efficiency'] < 0.6:
            recommendations.append("بازطراحی چیدمان برای بهبود جریان")
        
        return recommendations
    
    def _get_behavior_recommendations(self, behavior_analysis: Dict[str, Any]) -> List[str]:
        """توصیه‌های رفتار مشتری"""
        recommendations = []
        
        dwell_time = behavior_analysis.get('dwell_time', {}).get('avg', 25)
        if dwell_time < 20:
            recommendations.append("افزایش جذابیت محصولات برای افزایش زمان ماندگاری")
        
        if behavior_analysis.get('purchase_patterns', {}).get('impulse_buy_potential') == 'high':
            recommendations.append("بهینه‌سازی قرارگیری محصولات برای خریدهای آنی")
        
        return recommendations
    
    async def _analyze_real_sales_data(self, file_path: str) -> Dict[str, Any]:
        """تحلیل فایل فروش واقعی"""
        try:
            # خواندن فایل با pandas
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                return {'error': 'فرمت فایل پشتیبانی نمی‌شود', 'confidence': 0.3}
            
            # تحلیل آماری
            analysis = {
                'total_sales': df['sales'].sum() if 'sales' in df.columns else 0,
                'average_daily_sales': df['sales'].mean() if 'sales' in df.columns else 0,
                'growth_rate': self._calculate_growth_rate(df),
                'peak_hours': self._identify_peak_hours(df),
                'seasonal_patterns': self._analyze_seasonal_patterns(df),
                'confidence': 0.9
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"خطا در تحلیل فایل فروش: {e}")
            return {'error': str(e), 'confidence': 0.3}
    
    async def _analyze_estimated_sales_data(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل تخمینی فروش"""
        try:
            store_size = float(store_data.get('store_size', 0))
            daily_customers = int(store_data.get('daily_customers', 100))
            store_type = store_data.get('store_type', 'عمومی')
            
            # تخمین فروش بر اساس نوع فروشگاه
            avg_purchase_values = {
                'supermarket': 150000,
                'clothing': 300000,
                'electronics': 2000000,
                'pharmacy': 200000,
                'عمومی': 200000
            }
            
            avg_purchase = avg_purchase_values.get(store_type, 200000)
            estimated_daily_sales = daily_customers * avg_purchase * 0.3  # 30% conversion rate
            
            return {
                'estimated_daily_sales': estimated_daily_sales,
                'estimated_monthly_sales': estimated_daily_sales * 30,
                'conversion_rate': 0.3,
                'average_purchase_value': avg_purchase,
                'confidence': 0.6
            }
            
        except Exception as e:
            logger.error(f"خطا در تحلیل تخمینی فروش: {e}")
            return {'error': str(e), 'confidence': 0.3}
    
    def _calculate_growth_rate(self, df: pd.DataFrame) -> float:
        """محاسبه نرخ رشد"""
        try:
            if 'date' in df.columns and 'sales' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                first_month = df['sales'].iloc[:len(df)//2].mean()
                last_month = df['sales'].iloc[len(df)//2:].mean()
                return ((last_month - first_month) / first_month) * 100
            return 0
        except:
            return 0
    
    def _identify_peak_hours(self, df: pd.DataFrame) -> List[str]:
        """شناسایی ساعات پیک"""
        try:
            if 'hour' in df.columns:
                peak_hours = df.groupby('hour')['sales'].sum().nlargest(3).index.tolist()
                return [f"{h}:00" for h in peak_hours]
            return ["10-12", "18-20"]
        except:
            return ["10-12", "18-20"]
    
    def _analyze_seasonal_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """تحلیل الگوهای فصلی"""
        try:
            if 'date' in df.columns:
                df['month'] = pd.to_datetime(df['date']).dt.month
                monthly_sales = df.groupby('month')['sales'].sum()
                return {
                    'peak_month': monthly_sales.idxmax(),
                    'low_month': monthly_sales.idxmin(),
                    'seasonality_factor': monthly_sales.max() / monthly_sales.min()
                }
            return {'seasonality_factor': 1.2}
        except:
            return {'seasonality_factor': 1.2}
    
    def _calculate_advanced_score(self, results: List[Dict[str, Any]]) -> int:
        """محاسبه امتیاز پیشرفته"""
        try:
            total_score = 0
            weight_sum = 0
            
            for result in results:
                if 'confidence' in result:
                    weight = result['confidence']
                    score = self._extract_score_from_result(result)
                    total_score += score * weight
                    weight_sum += weight
            
            if weight_sum > 0:
                return int(total_score / weight_sum)
            return 70
        except:
            return 70
    
    def _extract_score_from_result(self, result: Dict[str, Any]) -> int:
        """استخراج امتیاز از نتیجه"""
        if 'scores' in result:
            scores = result['scores']
            if isinstance(scores, dict):
                return int(sum(scores.values()) / len(scores) * 100)
        return 70
    
    def _generate_advanced_summary(self, store_data: Dict[str, Any], results: List[Dict[str, Any]]) -> str:
        """تولید خلاصه پیشرفته"""
        store_name = store_data.get('store_name', 'فروشگاه شما')
        store_type = store_data.get('store_type', 'عمومی')
        
        summary = f"تحلیل جامع فروشگاه {store_name} از نوع {store_type} انجام شد. "
        
        # اضافه کردن نکات کلیدی
        key_points = []
        for result in results:
            if 'recommendations' in result:
                key_points.append("نیاز به بهبود چیدمان")
            if 'patterns' in result and 'traffic_density' in result['patterns']:
                density = result['patterns']['traffic_density']
                key_points.append(f"ترافیک {density}")
        
        if key_points:
            summary += f"نکات کلیدی: {', '.join(key_points[:3])}. "
        
        summary += "با اجرای توصیه‌های ارائه شده، می‌توانید فروش خود را به طور قابل توجهی افزایش دهید."
        
        return summary
    
    def _extract_key_findings(self, results: List[Dict[str, Any]]) -> List[str]:
        """استخراج یافته‌های کلیدی"""
        findings = []
        
        for result in results:
            if 'bottlenecks' in result:
                findings.extend(result['bottlenecks'])
            if 'patterns' in result and 'traffic_density' in result['patterns']:
                density = result['patterns']['traffic_density']
                findings.append(f"ترافیک {density} مشتریان")
        
        return findings[:5] if findings else ["نیاز به بهبود کلی چیدمان"]
    
    def _generate_advanced_recommendations(self, results: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """تولید توصیه‌های پیشرفته"""
        recommendations = {
            "layout": [],
            "lighting": [],
            "customer_flow": []
        }
        
        for result in results:
            if 'recommendations' in result:
                recs = result['recommendations']
                if isinstance(recs, list):
                    recommendations["layout"].extend(recs[:2])
                elif isinstance(recs, dict):
                    for category, items in recs.items():
                        if category in recommendations:
                            recommendations[category].extend(items[:2])
        
        # حذف موارد تکراری
        for category in recommendations:
            recommendations[category] = list(set(recommendations[category]))[:3]
        
        return recommendations
    
    def _generate_predictions(self, store_data: Dict[str, Any], results: List[Dict[str, Any]]) -> Dict[str, str]:
        """تولید پیش‌بینی‌ها"""
        # محاسبه افزایش فروش بر اساس امتیاز کلی
        overall_score = self._calculate_advanced_score(results)
        
        if overall_score > 80:
            sales_increase = "+25%"
            roi = "3 ماه"
        elif overall_score > 70:
            sales_increase = "+20%"
            roi = "4 ماه"
        elif overall_score > 60:
            sales_increase = "+15%"
            roi = "5 ماه"
        else:
            sales_increase = "+10%"
            roi = "6 ماه"
        
        return {
            "expected_sales_increase": sales_increase,
            "roi": roi
        }
    
    def _calculate_data_completeness(self, store_data: Dict) -> Dict:
        """محاسبه درصد اطلاعات موجود"""
        # فیلدهای مهم برای تحلیل
        important_fields = [
            'store_name', 'store_type', 'store_size', 'store_location',
            'daily_customers', 'monthly_revenue', 'employee_count',
            'checkout_count', 'fixed_shelves', 'high_traffic_areas',
            'ignored_sections', 'customer_videos', 'store_photos'
        ]
        
        # فیلدهای اختیاری (کمتر مهم)
        optional_fields = [
            'phone', 'email', 'store_dimensions', 'city', 'area',
            'establishment_year', 'working_hours'
        ]
        
        # محاسبه فیلدهای پر شده
        filled_important = 0
        filled_optional = 0
        
        for field in important_fields:
            value = store_data.get(field)
            if value and value != '' and value != [] and value != 0:
                filled_important += 1
        
        for field in optional_fields:
            value = store_data.get(field)
            if value and value != '' and value != [] and value != 0:
                filled_optional += 1
        
        # محاسبه درصد
        total_important = len(important_fields)
        total_optional = len(optional_fields)
        
        important_percentage = (filled_important / total_important) * 100
        optional_percentage = (filled_optional / total_optional) * 100
        
        # وزن‌دهی: فیلدهای مهم 80% و اختیاری 20%
        overall_percentage = (important_percentage * 0.8) + (optional_percentage * 0.2)
        
        return {
            'percentage': round(overall_percentage, 1),
            'important_fields_filled': filled_important,
            'important_fields_total': total_important,
            'optional_fields_filled': filled_optional,
            'optional_fields_total': total_optional,
            'missing_important_fields': [field for field in important_fields if not store_data.get(field) or store_data.get(field) == '' or store_data.get(field) == []],
            'filled_fields': [field for field in important_fields + optional_fields if store_data.get(field) and store_data.get(field) != '' and store_data.get(field) != []]
        }
    
    def _calculate_analysis_confidence(self, data_completeness: Dict) -> str:
        """محاسبه سطح اطمینان تحلیل"""
        percentage = data_completeness['percentage']
        
        if percentage >= 80:
            return "عالی"
        elif percentage >= 60:
            return "خوب"
        elif percentage >= 40:
            return "متوسط"
        elif percentage >= 20:
            return "ضعیف"
        else:
            return "خیلی ضعیف"
    
    def _generate_missing_data_warning(self, data_completeness: Dict) -> Dict:
        """تولید هشدار برای اطلاعات ناقص"""
        percentage = data_completeness['percentage']
        missing_fields = data_completeness['missing_important_fields']
        
        if percentage >= 70:
            return {
                'level': 'info',
                'message': f'تحلیل بر اساس {percentage}% اطلاعات موجود انجام شده است.',
                'suggestion': 'برای تحلیل دقیق‌تر، اطلاعات بیشتری اضافه کنید.'
            }
        elif percentage >= 40:
            return {
                'level': 'warning',
                'message': f'تحلیل بر اساس {percentage}% اطلاعات موجود انجام شده است. برخی اطلاعات مهم ناقص است.',
                'suggestion': f'فیلدهای ناقص: {", ".join(missing_fields[:5])}',
                'impact': 'دقت تحلیل کاهش یافته است.'
            }
        else:
            return {
                'level': 'error',
                'message': f'تحلیل بر اساس {percentage}% اطلاعات موجود انجام شده است. اطلاعات بسیار ناقص است.',
                'suggestion': f'لطفاً فیلدهای مهم زیر را تکمیل کنید: {", ".join(missing_fields[:5])}',
                'impact': 'تحلیل با دقت پایین انجام شده و ممکن است نتایج قابل اعتماد نباشد.'
            }
    
    def _calculate_overall_score(self, layout: Dict, traffic: Dict, customer: Dict) -> int:
        """محاسبه امتیاز کلی"""
        scores = []
        if layout and 'score' in layout:
            scores.append(layout['score'])
        if traffic and 'score' in traffic:
            scores.append(traffic['score'])
        if customer and 'score' in customer:
            scores.append(customer['score'])
        
        return sum(scores) // len(scores) if scores else 5
    
    def _generate_recommendations(self, layout: Dict, traffic: Dict, customer: Dict) -> List[str]:
        """تولید توصیه‌ها"""
        recommendations = []
        
        if layout and 'recommendations' in layout:
            recommendations.extend(layout['recommendations'])
        if traffic and 'recommendations' in traffic:
            recommendations.extend(traffic['recommendations'])
        if customer and 'recommendations' in customer:
            recommendations.extend(customer['recommendations'])
        
        return recommendations[:10]  # حداکثر 10 توصیه
    
    def _generate_key_insights(self, store_data: Dict, layout: Dict) -> List[str]:
        """تولید بینش‌های کلیدی"""
        insights = []
        
        store_name = store_data.get('store_name', 'فروشگاه')
        store_type = store_data.get('store_type', 'عمومی')
        
        insights.append(f"فروشگاه {store_name} از نوع {store_type} است")
        
        if layout and 'insights' in layout:
            insights.extend(layout['insights'])
        
        return insights[:5]  # حداکثر 5 بینش
    
    def perform_complete_analysis(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """انجام تحلیل کامل هوش مصنوعی"""
        try:
            logger.info(f"شروع تحلیل AI برای فروشگاه: {store_data.get('store_name', 'نامشخص')}")
            
            # تحلیل چیدمان
            layout_analysis = self._analyze_layout(store_data)
            
            # تحلیل ترافیک
            traffic_analysis = self._analyze_traffic_patterns(store_data)
            
            # تحلیل رفتار مشتریان
            customer_analysis = self._analyze_customer_behavior(store_data)
            
            # تحلیل کلی
            overall_analysis = self._analyze_overall_performance(store_data)
            
            # ترکیب نتایج و تولید گزارش نهایی
            final_report = self._generate_final_report(
                store_data, 
                layout_analysis, 
                traffic_analysis, 
                customer_analysis,
                overall_analysis
            )
            
            # پردازش متن فارسی برای PDF
            formatted_text = self._format_final_report_for_pdf(final_report, store_data)
            
            logger.info(f"تحلیل AI تکمیل شد برای فروشگاه: {store_data.get('store_name', 'نامشخص')}")
            
            return {
                'status': 'completed',
                'timestamp': timezone.now().isoformat(),
                'store_name': store_data.get('store_name', 'نامشخص'),
                'formatted_text': formatted_text,  # متن فرمت شده برای PDF
                'analysis_summary': final_report['summary'],
                'detailed_analysis': final_report['detailed'],
                'recommendations': final_report['recommendations'],
                'implementation_plan': final_report['implementation'],
                'expected_improvements': final_report['improvements'],
                'visualizations': final_report['visualizations'],
                'metrics': final_report['metrics']
            }
            
        except Exception as e:
            logger.error(f"خطا در تحلیل AI: {str(e)}")
            return {
                'status': 'error',
                'error_message': str(e),
                'timestamp': timezone.now().isoformat()
            }
    
    def _analyze_layout(self, store_data: Dict) -> Dict:
        """تحلیل چیدمان فروشگاه"""
        store_size = store_data.get('store_size', '0')
        checkout_count = store_data.get('checkout_count', '1')
        fixed_shelves = store_data.get('fixed_shelves', [])
        
        # تبدیل به عدد
        try:
            store_size_num = int(store_size) if isinstance(store_size, str) else store_size
            checkout_count_num = int(checkout_count) if isinstance(checkout_count, str) else checkout_count
        except (ValueError, TypeError):
            store_size_num = 0
            checkout_count_num = 1
        
        # محاسبه امتیاز چیدمان
        layout_score = 70.0  # امتیاز پایه
        
        # بهبود بر اساس اندازه فروشگاه
        if store_size_num > 100:
            layout_score += 10
        if store_size_num > 200:
            layout_score += 10
            
        # بهبود بر اساس تعداد صندوق‌ها
        if checkout_count_num >= 3:
            layout_score += 10
            
        # بهبود بر اساس قفسه‌های ثابت
        if isinstance(fixed_shelves, list) and len(fixed_shelves) > 2:
            layout_score += 5
            
        return {
            'score': min(layout_score, 100.0),
            'insights': [
                f'فروشگاه با متراژ {store_size} متر مربع',
                f'تعداد {checkout_count} صندوق پرداخت',
                f'تعداد {len(fixed_shelves)} قفسه ثابت'
            ],
            'recommendations': [
                'بهینه‌سازی چیدمان قفسه‌ها',
                'ایجاد مسیرهای واضح',
                'بهبود دسترسی به محصولات'
            ]
        }
    
    def _analyze_traffic_patterns(self, store_data: Dict) -> Dict:
        """تحلیل الگوهای ترافیک"""
        daily_customers = store_data.get('daily_customers', 0)
        high_traffic_areas = store_data.get('high_traffic_areas', [])
        ignored_sections = store_data.get('ignored_sections', [])
        
        # محاسبه امتیاز ترافیک
        traffic_score = 70.0
        
        # بهبود بر اساس تعداد مشتریان
        if daily_customers > 100:
            traffic_score += 15
        if daily_customers > 200:
            traffic_score += 10
            
        # بهبود بر اساس مناطق پرتردد
        if len(high_traffic_areas) >= 3:
            traffic_score += 10
            
        # کاهش بر اساس بخش‌های نادیده گرفته شده
        if len(ignored_sections) > 2:
            traffic_score -= 10
            
        return {
            'score': max(traffic_score, 0.0),
            'insights': [
                f'تعداد {daily_customers} مشتری روزانه',
                f'تعداد {len(high_traffic_areas)} منطقه پرتردد',
                f'تعداد {len(ignored_sections)} بخش نادیده گرفته شده'
            ],
            'recommendations': [
                'بهبود جریان ترافیک',
                'کاهش بخش‌های نادیده گرفته شده',
                'بهینه‌سازی مناطق پرتردد'
            ]
        }
    
    def _analyze_customer_behavior(self, store_data: Dict) -> Dict:
        """تحلیل رفتار مشتریان"""
        top_selling_products = store_data.get('top_selling_products', [])
        attraction_elements = store_data.get('attraction_elements', [])
        lighting_type = store_data.get('lighting_type', '')
        
        # محاسبه امتیاز رفتار مشتری
        behavior_score = 70.0
        
        # بهبود بر اساس محصولات پرفروش
        if len(top_selling_products) >= 3:
            behavior_score += 15
            
        # بهبود بر اساس عناصر جذاب
        if len(attraction_elements) >= 2:
            behavior_score += 10
            
        # بهبود بر اساس نوع نورپردازی
        if lighting_type in ['led', 'natural']:
            behavior_score += 5
            
        return {
            'score': min(behavior_score, 100.0),
            'insights': [
                f'تعداد {len(top_selling_products)} محصول پرفروش',
                f'تعداد {len(attraction_elements)} عنصر جذاب',
                f'نوع نورپردازی: {lighting_type}'
            ],
            'recommendations': [
                'بهبود چیدمان محصولات پرفروش',
                'افزایش عناصر جذاب',
                'بهینه‌سازی نورپردازی'
            ]
        }
    
    def _analyze_overall_performance(self, store_data: Dict) -> Dict:
        """تحلیل عملکرد کلی"""
        store_type = store_data.get('store_type', 'عمومی')
        report_detail_level = store_data.get('report_detail_level', 'basic')
        
        # محاسبه امتیاز کلی
        overall_score = 75.0
        
        # بهبود بر اساس نوع فروشگاه
        if store_type in ['سوپرمارکت', 'هایپرمارکت']:
            overall_score += 10
            
        # بهبود بر اساس سطح جزئیات گزارش
        if report_detail_level == 'detailed':
            overall_score += 5
            
        return {
            'score': min(overall_score, 100.0),
            'insights': [
                f'نوع فروشگاه: {store_type}',
                f'سطح جزئیات: {report_detail_level}'
            ],
            'recommendations': [
                'بهبود کلی چیدمان',
                'بهینه‌سازی فرآیندها',
                'افزایش رضایت مشتری'
            ]
        }
    
    def _generate_final_report(self, store_data: Dict, layout: Dict, traffic: Dict, 
                             customer: Dict, overall: Dict) -> Dict[str, Any]:
        """تولید گزارش نهایی ترکیبی"""
        
        store_name = store_data.get('store_name', 'فروشگاه شما')
        store_type = store_data.get('store_type', 'عمومی')
        store_size = store_data.get('store_size', 0)
        
        # محاسبه امتیاز کلی
        overall_score = (layout['score'] + traffic['score'] + customer['score'] + overall['score']) / 4
        
        # تولید خلاصه اجرایی
        executive_summary = f"""
        تحلیل هوش مصنوعی {store_name}
        
        نوع فروشگاه: {store_type}
        متراژ: {store_size} متر مربع
        امتیاز کلی: {overall_score:.1f}/100
        
        نتایج کلیدی:
        - کارایی چیدمان: {layout['score']:.1f}%
        - جریان ترافیک: {traffic['score']:.1f}%
        - رفتار مشتری: {customer['score']:.1f}%
        - عملکرد کلی: {overall['score']:.1f}%
        """
        
        # تولید توصیه‌های عملی
        all_recommendations = []
        all_recommendations.extend(layout['recommendations'])
        all_recommendations.extend(traffic['recommendations'])
        all_recommendations.extend(customer['recommendations'])
        all_recommendations.extend(overall['recommendations'])
        
        # حذف تکرارها
        unique_recommendations = list(set(all_recommendations))
        
        # برنامه اجرایی
        implementation_plan = {
            'مرحله 1': 'تحلیل وضعیت فعلی (1-2 هفته)',
            'مرحله 2': 'طراحی چیدمان جدید (2-3 هفته)',
            'مرحله 3': 'اجرای تغییرات (3-4 هفته)',
            'مرحله 4': 'نظارت و بهینه‌سازی (مستمر)'
        }
        
        # پیش‌بینی بهبودها
        improvements = {
            'sales_increase': '15-25%',
            'customer_satisfaction': '20-30%',
            'efficiency_improvement': '25-35%',
            'wait_time_reduction': '30-40%'
        }
        
        # متریک‌های کلیدی
        metrics = {
            'overall_performance': overall_score,
            'layout_efficiency': layout['score'],
            'traffic_flow': traffic['score'],
            'customer_experience': customer['score'],
            'space_utilization': overall['score']
        }
        
        return {
            'summary': executive_summary,
            'detailed': {
                'layout_analysis': layout,
                'traffic_analysis': traffic,
                'customer_analysis': customer,
                'overall_analysis': overall
            },
            'recommendations': unique_recommendations,
            'implementation': implementation_plan,
            'improvements': improvements,
            'visualizations': {
                'charts': ['performance_chart', 'traffic_flow_chart', 'customer_behavior_chart'],
                'heatmaps': ['traffic_heatmap', 'sales_heatmap']
            },
            'metrics': metrics
        }
    
    def _format_final_report_for_pdf(self, report: Dict[str, Any], store_data: Dict[str, Any]) -> str:
        """فرمت کردن گزارش نهایی برای PDF با پردازش فارسی"""
        try:
            # استخراج داده‌های کلیدی
            name = store_data.get("store_name", "فروشگاه شما")
            store_type = store_data.get("store_type", "عمومی")
            score = report.get("metrics", {}).get("overall_performance", 70)
            summary = report.get("summary", "تحلیل انجام شد")
            recs = report.get("recommendations", [])
            improvements = report.get("improvements", {})
            
            # پردازش متن فارسی برای PDF
            def process_persian_text_for_pdf(text):
                """پردازش متن فارسی برای PDF"""
                if not text:
                    return text
                
                try:
                    import arabic_reshaper
                    # اعمال Character Shaping برای اتصال کاراکترها
                    processed_text = arabic_reshaper.reshape(text)
                    return processed_text
                except Exception as e:
                    logger.warning(f"⚠️ خطا در پردازش متن فارسی: {e}")
                    return text
            
            # فرمت کردن توصیه‌ها
            formatted_recs = ""
            for i, rec in enumerate(recs[:10], 1):  # حداکثر 10 توصیه
                formatted_recs += f"\n📌 {i}. {rec}"
            
            # پردازش متن فارسی برای توصیه‌ها
            formatted_recs = process_persian_text_for_pdf(formatted_recs)
            
            # فرمت کردن پیش‌بینی بهبودها
            improvements_text = ""
            if isinstance(improvements, dict):
                for key, value in improvements.items():
                    improvements_text += f"\n• {key}: {value}"
            
            # پردازش متن فارسی برای بهبودها
            improvements_text = process_persian_text_for_pdf(improvements_text)
            
            # تولید گزارش نهایی
            final_text = f"""
{'='*60}
🛍️ گزارش تحلیلی هوشمند فروشگاه {name}
{'='*60}

📋 مشخصات فروشگاه:
   • نام: {name}
   • نوع: {store_type}
   • امتیاز کلی: {score:.1f}/100

{'='*60}
📊 خلاصه اجرایی:
{'='*60}

{summary.strip()}

{'='*60}
✅ توصیه‌های کلیدی برای بهبود:
{'='*60}
{formatted_recs.strip()}

{'='*60}
📈 پیش‌بینی بهبودها پس از اجرای توصیه‌ها:
{'='*60}
{improvements_text.strip() if improvements_text else '• افزایش کلی عملکرد فروشگاه'}

{'='*60}
📅 تاریخ تحلیل: {timezone.now().strftime('%Y/%m/%d - %H:%M')}
💡 این گزارش توسط سیستم هوش مصنوعی چیدمانو تولید شده است
{'='*60}
            """
            
            # پردازش نهایی متن فارسی برای PDF
            final_text = process_persian_text_for_pdf(final_text)
            
            return final_text.strip()
            
        except Exception as e:
            logger.error(f"خطا در فرمت کردن گزارش نهایی: {str(e)}")
            return f"گزارش تحلیلی فروشگاه {store_data.get('store_name', 'نامشخص')}"

def perform_ai_analysis_for_order(order_id: str, store_data: Dict) -> Dict[str, Any]:
    """تابع کمکی برای اجرای تحلیل AI"""
    service = SimpleAIAnalysisService()
    return service.perform_complete_analysis(store_data)
