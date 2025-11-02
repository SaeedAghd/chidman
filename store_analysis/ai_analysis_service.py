#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
from django.utils import timezone
from .ai_models.advanced_analyzer import AdvancedStoreAnalyzer
from .ai_models.layout_analyzer import LayoutAnalyzer
from .ai_models.traffic_analyzer import TrafficAnalyzer
from .ai_models.customer_behavior_analyzer import CustomerBehaviorAnalyzer

logger = logging.getLogger(__name__)

class AIAnalysisService:
    """سرویس تحلیل هوش مصنوعی برای فروشگاه‌ها"""
    
    def __init__(self):
        self.advanced_analyzer = AdvancedStoreAnalyzer()
        self.layout_analyzer = LayoutAnalyzer()
        self.traffic_analyzer = TrafficAnalyzer()
        self.customer_behavior_analyzer = CustomerBehaviorAnalyzer()
    
    def analyze_store(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل فروشگاه با استفاده از OpenAI"""
        try:
            logger.info(f"شروع تحلیل AI برای فروشگاه: {store_data.get('store_name', 'نامشخص')}")
            
            # استفاده از تحلیل پیشرفته که شامل OpenAI است
            advanced_analysis = self.advanced_analyzer.analyze_store(store_data)
            
            # تحلیل‌های محلی
            layout_analysis = self.layout_analyzer.analyze_layout(store_data)
            traffic_analysis = self.traffic_analyzer.analyze_traffic_patterns(store_data)
            customer_analysis = self.customer_behavior_analyzer.analyze_customer_behavior(store_data)
            
            # ترکیب نتایج
            combined_results = {
                'advanced_analysis': advanced_analysis,
                'layout_analysis': layout_analysis,
                'traffic_analysis': traffic_analysis,
                'customer_behavior': customer_analysis,
                'overall_score': self._calculate_overall_score(advanced_analysis, layout_analysis, traffic_analysis, customer_analysis),
                'recommendations': self._generate_recommendations(advanced_analysis, layout_analysis, traffic_analysis, customer_analysis),
                'key_insights': self._generate_key_insights(store_data, advanced_analysis),
                'timestamp': timezone.now().isoformat()
            }
            
            logger.info(f"تحلیل AI تکمیل شد برای فروشگاه: {store_data.get('store_name', 'نامشخص')}")
            return combined_results
            
        except Exception as e:
            logger.error(f"خطا در تحلیل AI: {str(e)}")
            # Fallback to simple analysis
            return self._fallback_analysis(store_data)
    
    def _fallback_analysis(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل ساده در صورت خطا در OpenAI"""
        try:
            from .ai_analysis_service_simple import SimpleAIAnalysisService
            simple_service = SimpleAIAnalysisService()
            return simple_service.analyze_store(store_data)
        except:
            return {
                'status': 'error',
                'error_message': 'تحلیل AI در دسترس نیست',
                'overall_score': 5,
                'recommendations': ['لطفاً دوباره تلاش کنید'],
                'key_insights': ['سیستم تحلیل موقتاً در دسترس نیست'],
                'timestamp': timezone.now().isoformat()
            }
    
    def perform_complete_analysis(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """انجام تحلیل کامل هوش مصنوعی"""
        try:
            logger.info(f"شروع تحلیل AI برای فروشگاه: {store_data.get('store_name', 'نامشخص')}")
            
            # 1. تحلیل پیشرفته کلی
            advanced_analysis = self.advanced_analyzer.analyze_store(store_data)
            
            # 2. تحلیل چیدمان
            layout_analysis = self.layout_analyzer.analyze_layout(store_data)
            
            # 3. تحلیل ترافیک
            traffic_analysis = self.traffic_analyzer.analyze_traffic_patterns(store_data)
            
            # 4. تحلیل رفتار مشتریان
            customer_analysis = self.customer_behavior_analyzer.analyze_customer_behavior(store_data)
            
            # 5. ترکیب نتایج و تولید گزارش نهایی
            final_report = self._generate_final_report(
                store_data, 
                advanced_analysis, 
                layout_analysis, 
                traffic_analysis, 
                customer_analysis
            )
            
            # 6. فرمت کردن گزارش نهایی به متن روان و حرفه‌ای (گام ۱ راهکار پیشنهادی)
            formatted_text = self._format_final_report(final_report, store_data)
            
            logger.info(f"تحلیل AI تکمیل شد برای فروشگاه: {store_data.get('store_name', 'نامشخص')}")
            
            return {
                'status': 'completed',
                'timestamp': timezone.now().isoformat(),
                'store_name': store_data.get('store_name', 'نامشخص'),
                'formatted_text': formatted_text,  # متن فرمت شده برای نمایش
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
    
    def _calculate_overall_score(self, advanced: Dict, layout: Dict, traffic: Dict, customer: Dict) -> int:
        """محاسبه امتیاز کلی"""
        scores = []
        if advanced and 'score' in advanced:
            scores.append(advanced['score'])
        if layout and 'score' in layout:
            scores.append(layout['score'])
        if traffic and 'score' in traffic:
            scores.append(traffic['score'])
        if customer and 'score' in customer:
            scores.append(customer['score'])
        
        return sum(scores) // len(scores) if scores else 5
    
    def _generate_recommendations(self, advanced: Dict, layout: Dict, traffic: Dict, customer: Dict) -> List[str]:
        """تولید توصیه‌ها"""
        recommendations = []
        
        if advanced and 'recommendations' in advanced:
            recommendations.extend(advanced['recommendations'])
        if layout and 'recommendations' in layout:
            recommendations.extend(layout['recommendations'])
        if traffic and 'recommendations' in traffic:
            recommendations.extend(traffic['recommendations'])
        if customer and 'recommendations' in customer:
            recommendations.extend(customer['recommendations'])
        
        return recommendations[:10]  # حداکثر 10 توصیه
    
    def _generate_key_insights(self, store_data: Dict, advanced: Dict) -> List[str]:
        """تولید بینش‌های کلیدی"""
        insights = []
        
        store_name = store_data.get('store_name', 'فروشگاه')
        store_type = store_data.get('store_type', 'عمومی')
        
        insights.append(f"فروشگاه {store_name} از نوع {store_type} است")
        
        if advanced and 'insights' in advanced:
            insights.extend(advanced['insights'])
        
        return insights[:5]  # حداکثر 5 بینش
    
    def _generate_final_report(self, store_data: Dict, advanced: Dict, layout: Dict, 
                             traffic: Dict, customer: Dict) -> Dict[str, Any]:
        """تولید گزارش نهایی ترکیبی"""
        
        store_name = store_data.get('store_name', 'فروشگاه شما')
        store_type = store_data.get('store_type', 'عمومی')
        store_size = store_data.get('store_size', 0)
        
        # محاسبه امتیاز کلی
        overall_score = self._calculate_overall_score(advanced, layout, traffic, customer)
        
        # تولید خلاصه اجرایی
        executive_summary = self._generate_executive_summary(store_data, overall_score)
        
        # تولید توصیه‌های عملی
        recommendations = self._generate_recommendations(advanced, layout, traffic, customer)
        
        # برنامه اجرایی
        implementation_plan = self._generate_implementation_plan(recommendations)
        
        # پیش‌بینی بهبودها
        improvements = self._predict_improvements(overall_score, store_data)
        
        # متریک‌های کلیدی
        metrics = self._calculate_key_metrics(advanced, layout, traffic, customer)
        
        return {
            'summary': executive_summary,
            'detailed': {
                'advanced_analysis': advanced,
                'layout_analysis': layout,
                'traffic_analysis': traffic,
                'customer_analysis': customer
            },
            'recommendations': recommendations,
            'implementation': implementation_plan,
            'improvements': improvements,
            'metrics': metrics,
            'visualizations': self._generate_visualization_data(store_data, metrics)
        }
    
    def _calculate_overall_score(self, advanced: Dict, layout: Dict, 
                               traffic: Dict, customer: Dict) -> float:
        """محاسبه امتیاز کلی فروشگاه"""
        scores = []
        
        if 'score' in advanced:
            scores.append(advanced['score'])
        if 'layout_score' in layout:
            scores.append(layout['layout_score'])
        if 'traffic_score' in traffic:
            scores.append(traffic['traffic_score'])
        if 'customer_score' in customer:
            scores.append(customer['customer_score'])
        
        return sum(scores) / len(scores) if scores else 70.0
    
    def _generate_executive_summary(self, store_data: Dict, overall_score: float) -> str:
        """تولید خلاصه اجرایی"""
        store_name = store_data.get('store_name', 'فروشگاه شما')
        
        if overall_score >= 85:
            performance_level = "عالی"
            status_color = "🟢"
        elif overall_score >= 70:
            performance_level = "خوب"
            status_color = "🟡"
        else:
            performance_level = "نیاز به بهبود"
            status_color = "🔴"
        
        return f"""
# خلاصه اجرایی تحلیل {store_name}

## 📊 وضعیت کلی
{status_color} **امتیاز کلی:** {overall_score:.1f}/100 ({performance_level})

## 🎯 نقاط کلیدی
- **نوع فروشگاه:** {store_data.get('store_type', 'عمومی')}
- **متراژ:** {store_data.get('store_size', 0)} متر مربع
- **مشتریان روزانه:** {store_data.get('daily_customers', 0)} نفر

## 📈 پتانسیل بهبود
بر اساس تحلیل هوش مصنوعی، فروشگاه شما پتانسیل بهبود {100 - overall_score:.1f}% را دارد.

## ⚡ اقدامات اولویت‌دار
1. بهینه‌سازی چیدمان قفسه‌ها
2. بهبود مسیرهای حرکتی مشتریان
3. افزایش کارایی صندوق‌های پرداخت
        """
    
    def _generate_recommendations(self, advanced: Dict, layout: Dict, 
                                traffic: Dict, customer: Dict) -> List[Dict]:
        """تولید توصیه‌های عملی"""
        recommendations = []
        
        # توصیه‌های چیدمان
        if 'layout_recommendations' in layout:
            for rec in layout['layout_recommendations']:
                recommendations.append({
                    'category': 'چیدمان',
                    'priority': rec.get('priority', 'متوسط'),
                    'title': rec.get('title', 'بهینه‌سازی چیدمان'),
                    'description': rec.get('description', ''),
                    'impact': rec.get('impact', 'متوسط'),
                    'implementation_time': rec.get('time', '1-2 هفته')
                })
        
        # توصیه‌های ترافیک
        if 'traffic_recommendations' in traffic:
            for rec in traffic['traffic_recommendations']:
                recommendations.append({
                    'category': 'ترافیک',
                    'priority': rec.get('priority', 'متوسط'),
                    'title': rec.get('title', 'بهینه‌سازی مسیرها'),
                    'description': rec.get('description', ''),
                    'impact': rec.get('impact', 'متوسط'),
                    'implementation_time': rec.get('time', '1-3 هفته')
                })
        
        # توصیه‌های رفتار مشتری
        if 'customer_recommendations' in customer:
            for rec in customer['customer_recommendations']:
                recommendations.append({
                    'category': 'رفتار مشتری',
                    'priority': rec.get('priority', 'متوسط'),
                    'title': rec.get('title', 'بهبود تجربه مشتری'),
                    'description': rec.get('description', ''),
                    'impact': rec.get('impact', 'متوسط'),
                    'implementation_time': rec.get('time', '2-4 هفته')
                })
        
        return recommendations
    
    def _generate_implementation_plan(self, recommendations: List[Dict]) -> Dict[str, Any]:
        """تولید برنامه اجرایی"""
        phases = {
            'phase_1': {
                'title': 'فاز اول - اقدامات سریع (1-2 هفته)',
                'tasks': [],
                'budget': 0,
                'timeline': '1-2 هفته'
            },
            'phase_2': {
                'title': 'فاز دوم - بهبودهای متوسط (2-4 هفته)',
                'tasks': [],
                'budget': 0,
                'timeline': '2-4 هفته'
            },
            'phase_3': {
                'title': 'فاز سوم - بهینه‌سازی کامل (1-2 ماه)',
                'tasks': [],
                'budget': 0,
                'timeline': '1-2 ماه'
            }
        }
        
        for rec in recommendations:
            if rec['implementation_time'] in ['1-2 هفته', '1 هفته']:
                phases['phase_1']['tasks'].append(rec)
            elif rec['implementation_time'] in ['2-4 هفته', '3 هفته']:
                phases['phase_2']['tasks'].append(rec)
            else:
                phases['phase_3']['tasks'].append(rec)
        
        return phases
    
    def _predict_improvements(self, current_score: float, store_data: Dict) -> Dict[str, Any]:
        """پیش‌بینی بهبودها"""
        potential_improvement = 100 - current_score
        
        return {
            'sales_increase': f"{potential_improvement * 0.3:.1f}%",
            'customer_satisfaction': f"{potential_improvement * 0.4:.1f}%",
            'efficiency_improvement': f"{potential_improvement * 0.5:.1f}%",
            'wait_time_reduction': f"{potential_improvement * 0.6:.1f}%",
            'operational_cost_reduction': f"{potential_improvement * 0.2:.1f}%"
        }
    
    def _calculate_key_metrics(self, advanced: Dict, layout: Dict, 
                             traffic: Dict, customer: Dict) -> Dict[str, float]:
        """محاسبه متریک‌های کلیدی"""
        metrics = {
            'layout_efficiency': layout.get('layout_score', 70.0),
            'traffic_flow': traffic.get('traffic_score', 70.0),
            'customer_experience': customer.get('customer_score', 70.0),
            'overall_performance': advanced.get('score', 70.0),
            'space_utilization': layout.get('space_utilization', 75.0),
            'checkout_efficiency': traffic.get('checkout_efficiency', 80.0),
            'product_visibility': layout.get('product_visibility', 70.0),
            'customer_engagement': customer.get('engagement_score', 75.0)
        }
        
        return metrics
    
    def _generate_visualization_data(self, store_data: Dict, metrics: Dict) -> Dict[str, Any]:
        """تولید داده‌های بصری"""
        return {
            'radar_chart': {
                'labels': ['کارایی چیدمان', 'جریان ترافیک', 'تجربه مشتری', 'عملکرد کلی'],
                'data': [
                    metrics['layout_efficiency'],
                    metrics['traffic_flow'],
                    metrics['customer_experience'],
                    metrics['overall_performance']
                ]
            },
            'bar_chart': {
                'labels': ['استفاده از فضا', 'کارایی صندوق', 'قابلیت دید محصولات', 'تعامل مشتری'],
                'data': [
                    metrics['space_utilization'],
                    metrics['checkout_efficiency'],
                    metrics['product_visibility'],
                    metrics['customer_engagement']
                ]
            },
            'progress_chart': {
                'current_score': metrics['overall_performance'],
                'target_score': 95.0,
                'improvement_potential': 95.0 - metrics['overall_performance']
            }
        }
    
    def _format_final_report(self, report: Dict[str, Any], store_data: Dict[str, Any]) -> str:
        """
        بازنویسی خروجی به زبان فارسی روان و ساختارمند
        
        این متد تمام داده‌های تحلیلی را به یک گزارش حرفه‌ای و خوانا تبدیل می‌کند.
        Uncle Bob: "این یک Adapter Pattern است که presentation را از business logic جدا می‌کند"
        """
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
                if isinstance(rec, dict):
                    title = rec.get('title', rec.get('recommendation', f'توصیه {i}'))
                    desc = rec.get('description', rec.get('details', ''))
                    priority = rec.get('priority', '')
                    priority_icon = {'بالا': '🔴', 'متوسط': '🟡', 'پایین': '🟢'}.get(priority, '📌')
                    formatted_recs += f"\n{priority_icon} {i}. {title}"
                    if desc:
                        formatted_recs += f"\n   {desc}"
                else:
                    formatted_recs += f"\n📌 {i}. {rec}"
            
            # پردازش متن فارسی برای توصیه‌ها
            formatted_recs = process_persian_text_for_pdf(formatted_recs)
            
            # فرمت کردن پیش‌بینی بهبودها
            improvements_text = ""
            if isinstance(improvements, dict):
                for key, value in improvements.items():
                    if isinstance(value, (int, float)):
                        improvements_text += f"\n• {key}: +{value}%"
                    elif isinstance(value, dict):
                        improvement_val = value.get('improvement', value.get('value', ''))
                        if improvement_val:
                            improvements_text += f"\n• {key}: {improvement_val}"
            
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

# تابع کمکی برای استفاده در views
def perform_ai_analysis_for_order(order_id: str, store_data: Dict[str, Any]) -> Dict[str, Any]:
    """انجام تحلیل AI برای یک سفارش"""
    service = AIAnalysisService()
    return service.perform_complete_analysis(store_data)
