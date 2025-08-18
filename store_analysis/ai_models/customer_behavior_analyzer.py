import logging
import numpy as np
from typing import Dict, List, Tuple
from django.conf import settings

logger = logging.getLogger(__name__)

class CustomerBehaviorAnalyzer:
    """تحلیل‌گر رفتار مشتری با استفاده از هوش مصنوعی"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def analyze_customer_behavior(self, store_data: Dict) -> Dict:
        """
        تحلیل رفتار مشتری بر اساس داده‌های فروشگاه
        
        Args:
            store_data: داده‌های فروشگاه شامل مسیرها، نقاط توقف و غیره
            
        Returns:
            Dict: نتایج تحلیل رفتار مشتری
        """
        try:
            # تحلیل مسیرهای حرکت مشتری
            path_analysis = self._analyze_customer_paths(store_data)
            
            # تحلیل نقاط توقف و زمان‌بندی
            stopping_analysis = self._analyze_stopping_patterns(store_data)
            
            # تحلیل الگوهای خرید
            purchase_analysis = self._analyze_purchase_patterns(store_data)
            
            # تحلیل تأثیر عوامل محیطی
            environmental_analysis = self._analyze_environmental_factors(store_data)
            
            # ترکیب نتایج
            results = {
                'path_analysis': path_analysis,
                'stopping_analysis': stopping_analysis,
                'purchase_analysis': purchase_analysis,
                'environmental_analysis': environmental_analysis,
                'overall_score': self._calculate_overall_score(path_analysis, stopping_analysis, purchase_analysis, environmental_analysis),
                'recommendations': self._generate_recommendations(path_analysis, stopping_analysis, purchase_analysis, environmental_analysis)
            }
            
            self.logger.info("Customer behavior analysis completed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in customer behavior analysis: {str(e)}")
            return {
                'error': f'خطا در تحلیل رفتار مشتری: {str(e)}',
                'overall_score': 0.0,
                'recommendations': ['خطا در تحلیل رفتار مشتری']
            }
    
    def _analyze_customer_paths(self, store_data: Dict) -> Dict:
        """تحلیل مسیرهای حرکت مشتری"""
        try:
            # استخراج داده‌های مسیر
            paths = store_data.get('customer_movement_paths', 'mixed')
            high_traffic_areas = store_data.get('high_traffic_areas', '')
            
            # تحلیل الگوهای مسیر
            path_score = 0.0
            path_insights = []
            
            if paths == 'clockwise':
                path_score = 0.8
                path_insights.append('مسیر ساعتگرد طبیعی و روان است')
            elif paths == 'counterclockwise':
                path_score = 0.7
                path_insights.append('مسیر پادساعتگرد نیاز به بهینه‌سازی دارد')
            elif paths == 'mixed':
                path_score = 0.6
                path_insights.append('مسیرهای مختلط نیاز به استانداردسازی دارند')
            else:
                path_score = 0.5
                path_insights.append('مسیرهای تصادفی نیاز به طراحی مجدد دارند')
            
            return {
                'score': path_score,
                'pattern': paths,
                'insights': path_insights,
                'high_traffic_areas': high_traffic_areas.split(',') if high_traffic_areas else []
            }
            
        except Exception as e:
            self.logger.error(f"Error in path analysis: {str(e)}")
            return {'score': 0.0, 'error': str(e)}
    
    def _analyze_stopping_patterns(self, store_data: Dict) -> Dict:
        """تحلیل الگوهای توقف مشتری"""
        try:
            # تحلیل نقاط توقف
            shelf_count = store_data.get('shelf_count', 0)
            store_size = store_data.get('store_size', 0)
            
            # محاسبه تراکم قفسه‌ها
            shelf_density = shelf_count / store_size if store_size > 0 else 0
            
            stopping_score = 0.0
            stopping_insights = []
            
            if shelf_density > 0.1:  # قفسه‌های متراکم
                stopping_score = 0.9
                stopping_insights.append('تراکم قفسه‌ها مناسب است')
            elif shelf_density > 0.05:
                stopping_score = 0.7
                stopping_insights.append('تراکم قفسه‌ها متوسط است')
            else:
                stopping_score = 0.4
                stopping_insights.append('تراکم قفسه‌ها کم است')
            
            return {
                'score': stopping_score,
                'shelf_density': shelf_density,
                'insights': stopping_insights
            }
            
        except Exception as e:
            self.logger.error(f"Error in stopping pattern analysis: {str(e)}")
            return {'score': 0.0, 'error': str(e)}
    
    def _analyze_purchase_patterns(self, store_data: Dict) -> Dict:
        """تحلیل الگوهای خرید مشتری"""
        try:
            # تحلیل الگوهای خرید بر اساس نوع فروشگاه
            store_type = store_data.get('store_type', 'other')
            
            purchase_score = 0.0
            purchase_insights = []
            
            if store_type in ['supermarket', 'hypermarket']:
                purchase_score = 0.8
                purchase_insights.append('نوع فروشگاه مناسب برای خریدهای روزانه است')
            elif store_type == 'clothing':
                purchase_score = 0.7
                purchase_insights.append('نوع فروشگاه مناسب برای خریدهای انتخابی است')
            else:
                purchase_score = 0.6
                purchase_insights.append('نوع فروشگاه نیاز به تحلیل بیشتر دارد')
            
            return {
                'score': purchase_score,
                'store_type': store_type,
                'insights': purchase_insights
            }
            
        except Exception as e:
            self.logger.error(f"Error in purchase pattern analysis: {str(e)}")
            return {'score': 0.0, 'error': str(e)}
    
    def _analyze_environmental_factors(self, store_data: Dict) -> Dict:
        """تحلیل عوامل محیطی مؤثر بر رفتار مشتری"""
        try:
            # تحلیل عوامل محیطی
            design_style = store_data.get('design_style', 'modern')
            brand_colors = store_data.get('brand_colors', '')
            peak_hours = store_data.get('peak_hours', '')
            
            environmental_score = 0.0
            environmental_insights = []
            
            # تحلیل سبک طراحی
            if design_style in ['modern', 'minimalist']:
                environmental_score += 0.3
                environmental_insights.append('سبک طراحی مدرن و جذاب است')
            elif design_style == 'traditional':
                environmental_score += 0.2
                environmental_insights.append('سبک طراحی سنتی نیاز به به‌روزرسانی دارد')
            
            # تحلیل رنگ‌ها
            if brand_colors:
                environmental_score += 0.2
                environmental_insights.append('رنگ‌بندی برند مشخص است')
            
            # تحلیل ساعات پیک
            if peak_hours:
                environmental_score += 0.2
                environmental_insights.append('ساعات پیک فروش مشخص است')
            
        return {
                'score': min(environmental_score, 1.0),
                'design_style': design_style,
                'brand_colors': brand_colors,
                'peak_hours': peak_hours,
                'insights': environmental_insights
            }
            
        except Exception as e:
            self.logger.error(f"Error in environmental analysis: {str(e)}")
            return {'score': 0.0, 'error': str(e)}
    
    def _calculate_overall_score(self, path_analysis: Dict, stopping_analysis: Dict, 
                                purchase_analysis: Dict, environmental_analysis: Dict) -> float:
        """محاسبه امتیاز کلی"""
        try:
            scores = [
                path_analysis.get('score', 0.0),
                stopping_analysis.get('score', 0.0),
                purchase_analysis.get('score', 0.0),
                environmental_analysis.get('score', 0.0)
            ]
            
            # حذف امتیازهای صفر از محاسبه
            valid_scores = [score for score in scores if score > 0]
            
            if not valid_scores:
                return 0.0
            
            return sum(valid_scores) / len(valid_scores)
            
        except Exception as e:
            self.logger.error(f"Error in overall score calculation: {str(e)}")
            return 0.0
    
    def generate_recommendations(self, analysis_results: Dict) -> List[str]:
        """
        تولید پیشنهادات بر اساس نتایج تحلیل
        
        Args:
            analysis_results: نتایج تحلیل رفتار مشتری
            
        Returns:
            List[str]: لیست پیشنهادات
        """
        try:
            recommendations = []
            
            # پیشنهادات بر اساس تحلیل مسیر
            path_score = analysis_results.get('path_analysis', {}).get('score', 0.0)
            if path_score < 0.7:
                recommendations.append('بهینه‌سازی مسیرهای حرکت مشتری')
                recommendations.append('استانداردسازی جهت حرکت در فروشگاه')
            
            # پیشنهادات بر اساس تحلیل توقف
            stopping_score = analysis_results.get('stopping_analysis', {}).get('score', 0.0)
            if stopping_score < 0.7:
                recommendations.append('بهبود تراکم و چیدمان قفسه‌ها')
                recommendations.append('ایجاد نقاط توقف جذاب')
            
            # پیشنهادات بر اساس تحلیل خرید
            purchase_score = analysis_results.get('purchase_analysis', {}).get('score', 0.0)
            if purchase_score < 0.7:
                recommendations.append('بهینه‌سازی چیدمان محصولات')
                recommendations.append('ایجاد مسیرهای خرید منطقی')
            
            # پیشنهادات بر اساس تحلیل محیطی
            environmental_score = analysis_results.get('environmental_analysis', {}).get('score', 0.0)
            if environmental_score < 0.7:
                recommendations.append('بهبود طراحی و دکوراسیون')
                recommendations.append('بهینه‌سازی نورپردازی و رنگ‌بندی')
            
            # پیشنهادات عمومی
            overall_score = analysis_results.get('overall_score', 0.0)
            if overall_score < 0.6:
                recommendations.append('بازطراحی کلی چیدمان فروشگاه')
                recommendations.append('استفاده از مشاوره تخصصی')
            
            return recommendations if recommendations else ['چیدمان فعلی مناسب است']
            
        except Exception as e:
            self.logger.error(f"Error in recommendation generation: {str(e)}")
            return ['خطا در تولید پیشنهادات']
    
    def _generate_recommendations(self, path_analysis: Dict, stopping_analysis: Dict, 
                                 purchase_analysis: Dict, environmental_analysis: Dict) -> List[str]:
        """تولید پیشنهادات داخلی"""
        analysis_results = {
            'path_analysis': path_analysis,
            'stopping_analysis': stopping_analysis,
            'purchase_analysis': purchase_analysis,
            'environmental_analysis': environmental_analysis
        }
        return self.generate_recommendations(analysis_results) 