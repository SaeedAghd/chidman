import logging
import numpy as np
from typing import Dict, List, Tuple
from django.conf import settings

logger = logging.getLogger(__name__)

class TrafficAnalyzer:
    """تحلیل‌گر ترافیک فروشگاه با استفاده از هوش مصنوعی"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def analyze_traffic_patterns(self, store_data: Dict) -> Dict:
        """
        تحلیل الگوهای ترافیک فروشگاه
        
        Args:
            store_data: داده‌های فروشگاه شامل ترافیک، ساعات پیک و غیره
            
        Returns:
            Dict: نتایج تحلیل ترافیک
        """
        try:
            # تحلیل الگوهای ترافیک
            traffic_analysis = self._analyze_traffic_flow(store_data)
            
            # تحلیل ساعات پیک
            peak_hours_analysis = self._analyze_peak_hours(store_data)
            
            # تحلیل توزیع ترافیک
            distribution_analysis = self._analyze_traffic_distribution(store_data)
            
            # تحلیل تأثیر عوامل خارجی
            external_factors_analysis = self._analyze_external_factors(store_data)
            
            # ترکیب نتایج
            results = {
                'traffic_analysis': traffic_analysis,
                'peak_hours_analysis': peak_hours_analysis,
                'distribution_analysis': distribution_analysis,
                'external_factors_analysis': external_factors_analysis,
                'overall_score': self._calculate_traffic_score(traffic_analysis, peak_hours_analysis, distribution_analysis, external_factors_analysis),
                'recommendations': self._generate_traffic_recommendations(traffic_analysis, peak_hours_analysis, distribution_analysis, external_factors_analysis)
            }
            
            self.logger.info("Traffic analysis completed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in traffic analysis: {str(e)}")
            return {
                'error': f'خطا در تحلیل ترافیک: {str(e)}',
                'overall_score': 0.0,
                'recommendations': ['خطا در تحلیل ترافیک']
            }
    
    def _analyze_traffic_flow(self, store_data: Dict) -> Dict:
        """تحلیل جریان ترافیک"""
        try:
            # استخراج داده‌های ترافیک
            high_traffic_areas = store_data.get('high_traffic_areas', '')
            customer_movement_paths = store_data.get('customer_movement_paths', 'mixed')
            entrances = store_data.get('entrances', 1)
            
            # تحلیل جریان ترافیک
            flow_score = 0.0
            flow_insights = []
            
            # تحلیل مناطق پرتردد
            if high_traffic_areas:
                flow_score += 0.3
                flow_insights.append('مناطق پرتردد شناسایی شده‌اند')
            else:
                flow_insights.append('نیاز به شناسایی مناطق پرتردد')
            
            # تحلیل مسیرهای حرکت
            if customer_movement_paths == 'clockwise':
                flow_score += 0.4
                flow_insights.append('مسیر حرکت طبیعی و روان است')
            elif customer_movement_paths == 'counterclockwise':
                flow_score += 0.3
                flow_insights.append('مسیر حرکت نیاز به بهینه‌سازی دارد')
            else:
                flow_score += 0.2
                flow_insights.append('مسیرهای حرکت نامنظم هستند')
            
            # تحلیل تعداد ورودی‌ها
            if entrances > 1:
                flow_score += 0.2
                flow_insights.append('چندین ورودی برای توزیع ترافیک وجود دارد')
            else:
                flow_insights.append('افزایش تعداد ورودی‌ها می‌تواند مفید باشد')
            
            return {
                'score': min(flow_score, 1.0),
                'high_traffic_areas': high_traffic_areas.split(',') if high_traffic_areas else [],
                'movement_pattern': customer_movement_paths,
                'entrances': entrances,
                'insights': flow_insights
            }
            
        except Exception as e:
            self.logger.error(f"Error in traffic flow analysis: {str(e)}")
            return {'score': 0.0, 'error': str(e)}
    
    def _analyze_peak_hours(self, store_data: Dict) -> Dict:
        """تحلیل ساعات پیک ترافیک"""
        try:
            # استخراج داده‌های ساعات پیک
            peak_hours = store_data.get('peak_hours', '')
            
            peak_score = 0.0
            peak_insights = []
            
            if peak_hours:
                peak_score = 0.8
                peak_insights.append('ساعات پیک فروش مشخص است')
                peak_insights.append(f'ساعات پیک: {peak_hours}')
            else:
                peak_score = 0.3
                peak_insights.append('ساعات پیک فروش نامشخص است')
                peak_insights.append('نیاز به تحلیل ساعات پیک')
            
            return {
                'score': peak_score,
                'peak_hours': peak_hours,
                'insights': peak_insights
            }
            
        except Exception as e:
            self.logger.error(f"Error in peak hours analysis: {str(e)}")
            return {'score': 0.0, 'error': str(e)}
    
    def _analyze_traffic_distribution(self, store_data: Dict) -> Dict:
        """تحلیل توزیع ترافیک در فروشگاه"""
        try:
            # تحلیل توزیع ترافیک بر اساس نوع فروشگاه
            store_type = store_data.get('store_type', 'other')
            store_size = store_data.get('store_size', 0)
            
            distribution_score = 0.0
            distribution_insights = []
            
            # تحلیل بر اساس نوع فروشگاه
            if store_type in ['supermarket', 'hypermarket']:
                distribution_score += 0.4
                distribution_insights.append('نوع فروشگاه مناسب برای ترافیک بالا')
            elif store_type == 'clothing':
                distribution_score += 0.3
                distribution_insights.append('نوع فروشگاه مناسب برای ترافیک متوسط')
            else:
                distribution_score += 0.2
                distribution_insights.append('نوع فروشگاه نیاز به تحلیل بیشتر')
            
            # تحلیل بر اساس اندازه فروشگاه
            if store_size > 500:
                distribution_score += 0.3
                distribution_insights.append('فروشگاه بزرگ با ظرفیت ترافیک بالا')
            elif store_size > 200:
                distribution_score += 0.2
                distribution_insights.append('فروشگاه متوسط با ظرفیت ترافیک مناسب')
            else:
                distribution_score += 0.1
                distribution_insights.append('فروشگاه کوچک با ظرفیت ترافیک محدود')
            
            return {
                'score': min(distribution_score, 1.0),
                'store_type': store_type,
                'store_size': store_size,
                'insights': distribution_insights
            }
            
        except Exception as e:
            self.logger.error(f"Error in traffic distribution analysis: {str(e)}")
            return {'score': 0.0, 'error': str(e)}
    
    def _analyze_external_factors(self, store_data: Dict) -> Dict:
        """تحلیل عوامل خارجی مؤثر بر ترافیک"""
        try:
            # تحلیل عوامل خارجی
            store_location = store_data.get('store_location', '')
            city = store_data.get('city', '')
            area = store_data.get('area', '')
            
            external_score = 0.0
            external_insights = []
            
            # تحلیل موقعیت فروشگاه
            if store_location:
                external_score += 0.3
                external_insights.append('موقعیت فروشگاه مشخص است')
            else:
                external_insights.append('موقعیت فروشگاه نامشخص است')
            
            # تحلیل شهر
            if city:
                external_score += 0.2
                external_insights.append(f'فروشگاه در شهر {city} قرار دارد')
            else:
                external_insights.append('شهر فروشگاه مشخص نیست')
            
            # تحلیل منطقه
            if area:
                external_score += 0.2
                external_insights.append(f'فروشگاه در منطقه {area} قرار دارد')
            else:
                external_insights.append('منطقه فروشگاه مشخص نیست')
            
            return {
                'score': min(external_score, 1.0),
                'location': store_location,
                'city': city,
                'area': area,
                'insights': external_insights
            }
            
        except Exception as e:
            self.logger.error(f"Error in external factors analysis: {str(e)}")
            return {'score': 0.0, 'error': str(e)}
    
    def _calculate_traffic_score(self, traffic_analysis: Dict, peak_hours_analysis: Dict, 
                                distribution_analysis: Dict, external_factors_analysis: Dict) -> float:
        """محاسبه امتیاز کلی ترافیک"""
        try:
            scores = [
                traffic_analysis.get('score', 0.0),
                peak_hours_analysis.get('score', 0.0),
                distribution_analysis.get('score', 0.0),
                external_factors_analysis.get('score', 0.0)
            ]
            
            # حذف امتیازهای صفر از محاسبه
            valid_scores = [score for score in scores if score > 0]
            
            if not valid_scores:
                return 0.0
            
            return sum(valid_scores) / len(valid_scores)
            
        except Exception as e:
            self.logger.error(f"Error in traffic score calculation: {str(e)}")
            return 0.0
    
    def generate_traffic_recommendations(self, analysis_results: Dict) -> List[str]:
        """
        تولید پیشنهادات ترافیک بر اساس نتایج تحلیل
        
        Args:
            analysis_results: نتایج تحلیل ترافیک
            
        Returns:
            List[str]: لیست پیشنهادات
        """
        try:
            recommendations = []
            
            # پیشنهادات بر اساس تحلیل جریان ترافیک
            traffic_score = analysis_results.get('traffic_analysis', {}).get('score', 0.0)
            if traffic_score < 0.7:
                recommendations.append('بهینه‌سازی جریان ترافیک در فروشگاه')
                recommendations.append('ایجاد مسیرهای واضح برای حرکت مشتریان')
            
            # پیشنهادات بر اساس تحلیل ساعات پیک
            peak_score = analysis_results.get('peak_hours_analysis', {}).get('score', 0.0)
            if peak_score < 0.7:
                recommendations.append('تحلیل و شناسایی ساعات پیک فروش')
                recommendations.append('بهینه‌سازی نیروی انسانی در ساعات پیک')
            
            # پیشنهادات بر اساس تحلیل توزیع ترافیک
            distribution_score = analysis_results.get('distribution_analysis', {}).get('score', 0.0)
            if distribution_score < 0.7:
                recommendations.append('بهبود توزیع ترافیک در فروشگاه')
                recommendations.append('ایجاد نقاط جذاب در مناطق کم‌تردد')
            
            # پیشنهادات بر اساس تحلیل عوامل خارجی
            external_score = analysis_results.get('external_factors_analysis', {}).get('score', 0.0)
            if external_score < 0.7:
                recommendations.append('تحلیل عوامل خارجی مؤثر بر ترافیک')
                recommendations.append('بهبود دسترسی به فروشگاه')
            
            # پیشنهادات عمومی
            overall_score = analysis_results.get('overall_score', 0.0)
            if overall_score < 0.6:
                recommendations.append('بازطراحی کلی سیستم ترافیک فروشگاه')
                recommendations.append('استفاده از تکنولوژی‌های نوین برای مدیریت ترافیک')
            
            return recommendations if recommendations else ['سیستم ترافیک فعلی مناسب است']
            
        except Exception as e:
            self.logger.error(f"Error in traffic recommendation generation: {str(e)}")
            return ['خطا در تولید پیشنهادات ترافیک']
    
    def _generate_traffic_recommendations(self, traffic_analysis: Dict, peak_hours_analysis: Dict, 
                                         distribution_analysis: Dict, external_factors_analysis: Dict) -> List[str]:
        """تولید پیشنهادات ترافیک داخلی"""
        analysis_results = {
            'traffic_analysis': traffic_analysis,
            'peak_hours_analysis': peak_hours_analysis,
            'distribution_analysis': distribution_analysis,
            'external_factors_analysis': external_factors_analysis
        }
        return self.generate_traffic_recommendations(analysis_results) 