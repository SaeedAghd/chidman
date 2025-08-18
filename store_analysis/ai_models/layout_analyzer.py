"""
Module for analyzing store layout and providing recommendations.
"""

import cv2
import numpy as np
from pathlib import Path
import os
from django.conf import settings
import json
from datetime import datetime
import logging
from PIL import Image

logger = logging.getLogger(__name__)

class LayoutAnalyzer:
    """
    A class for analyzing store layout and providing recommendations.
    """
    
    def __init__(self):
        """
        Initialize the LayoutAnalyzer.
        """
        self.model = None
    
    def analyze_layout(self, image_path):
        """
        Analyze the store layout from an image path and return analysis results.
        
        Args:
            image_path (str): The path to the store layout image.
            
        Returns:
            dict: Analysis results including layout score, identified objects, empty spaces, and suggestions.
        """
        try:
            # Load the image
            img = Image.open(image_path).convert("RGB")
            img_np = np.array(img)
            
            # Step 1: Extract objects (e.g., shelves, counters, entrances)
            objects = self.extract_objects(img_np)
            
            # Step 2: Analyze empty spaces
            empty_spaces = self.analyze_empty_spaces(img_np, objects)
            
            # Step 3: Generate suggestions based on analysis
            analysis_data = {
                'objects': objects,
                'empty_spaces': empty_spaces,
                'image_shape': img_np.shape
            }
            suggestions = self.generate_suggestions(analysis_data)
            
            # For MVP, a simple layout score
            layout_score = 70 # Placeholder for actual scoring logic
            
            return {
                'layout_score': layout_score,
                'identified_objects': objects,
                'empty_spaces': empty_spaces,
                'suggestions': suggestions
            }
        except Exception as e:
            logger.error(f"Error analyzing layout: {e}")
            return {
                'layout_score': 0,
                'identified_objects': [],
                'empty_spaces': [],
                'suggestions': [f"Error during analysis: {e}"]
            }
    
    def get_recommendations(self, analysis_results):
        """
        Generate recommendations based on analysis results.
        
        Args:
            analysis_results: The results from analyze_layout
            
        Returns:
            list: List of recommendations
        """
        recommendations = []
        
        # Add traffic flow recommendations
        if analysis_results['traffic_flow']['score'] < 80:
            recommendations.extend(analysis_results['traffic_flow']['suggestions'])
        
        # Add product placement recommendations
        if analysis_results['product_placement']['score'] < 80:
            recommendations.extend(analysis_results['product_placement']['suggestions'])
        
        # Add space utilization recommendations
        if analysis_results['space_utilization']['score'] < 80:
            recommendations.extend(analysis_results['space_utilization']['suggestions'])
        
        return recommendations

    def analyze(self, image_path):
        """تحلیل چیدمان فروشگاه"""
        try:
            # تحلیل پایه چیدمان
            layout_score = self._calculate_layout_score(image_path)
            recommendations = self._generate_basic_recommendations(layout_score)
            
            return {
                'layout_score': layout_score,
                'recommendations': recommendations,
                'analysis_type': 'basic_layout'
            }
        except Exception as e:
            logger.error(f"Error in layout analysis: {str(e)}")
        return {
                'layout_score': 50,
                'recommendations': ['خطا در تحلیل چیدمان'],
                'error': str(e)
            }
    
    def _calculate_layout_score(self, image_path):
        """محاسبه امتیاز چیدمان"""
        try:
            # تحلیل ساده بر اساس اندازه و نسبت‌ها
            import cv2
            import numpy as np
            
            image = cv2.imread(image_path)
            if image is None:
                return 70  # امتیاز پیش‌فرض
            
            height, width = image.shape[:2]
            
            # محاسبه نسبت ابعاد
            aspect_ratio = width / height
            
            # امتیازدهی بر اساس نسبت ابعاد
            if 0.8 <= aspect_ratio <= 1.2:
                score = 85  # نسبت مناسب
            elif 0.6 <= aspect_ratio <= 1.5:
                score = 75  # نسبت قابل قبول
            else:
                score = 60  # نسبت نامناسب
            
            return score
            
        except Exception as e:
            logger.error(f"Error calculating layout score: {str(e)}")
            return 70
    
    def _generate_basic_recommendations(self, score):
        """تولید پیشنهادات پایه"""
        recommendations = []
        
        if score < 70:
            recommendations.extend([
                'بهبود نورپردازی در بخش ورودی',
                'جابجایی قفسه‌های محصولات پرفروش',
                'بهینه‌سازی مسیر حرکت مشتری'
            ])
        elif score < 80:
            recommendations.extend([
                'بهبود جزئی در چیدمان',
                'بهینه‌سازی نقاط توقف'
            ])
        else:
            recommendations.append('چیدمان فعلی مناسب است')
        
        return recommendations
    
    def analyze_psychology(self, store_analysis):
        """تحلیل روانشناسی فروش"""
        return {
            'customer_behavior': {
                'attention_points': self._analyze_attention_points(store_analysis),
                'emotional_triggers': self._analyze_emotional_triggers(store_analysis),
                'decision_making': self._analyze_decision_making(store_analysis)
            },
            'environmental_factors': {
                'lighting_impact': self._analyze_lighting_impact(store_analysis),
                'color_impact': self._analyze_color_impact(store_analysis),
                'space_perception': self._analyze_space_perception(store_analysis)
            },
            'recommendations': self._generate_psychological_recommendations(store_analysis)
        }
    
    def optimize_layout(self, store_analysis):
        """بهینه‌سازی چیدمان"""
        return {
            'current_layout': self._analyze_current_layout(store_analysis),
            'optimization_suggestions': self._generate_layout_suggestions(store_analysis),
            'implementation_steps': self._create_implementation_plan(store_analysis)
        }
    
    def analyze_customer_flow(self, store_analysis):
        """تحلیل جریان مشتری"""
        return {
            'flow_patterns': self._analyze_flow_patterns(store_analysis),
            'bottlenecks': self._identify_bottlenecks(store_analysis),
            'optimization_opportunities': self._find_flow_optimizations(store_analysis)
        }
    
    def analyze_product_placement(self, store_analysis):
        """تحلیل چیدمان محصولات"""
        return {
            'current_placement': self._analyze_current_placement(store_analysis),
            'category_analysis': self._analyze_categories(store_analysis),
            'placement_recommendations': self._generate_placement_suggestions(store_analysis)
        }
    
    def analyze_lighting(self, store_analysis):
        """تحلیل نورپردازی"""
        return {
            'current_lighting': self._analyze_current_lighting(store_analysis),
            'lighting_impact': self._analyze_lighting_effects(store_analysis),
            'optimization_suggestions': self._generate_lighting_recommendations(store_analysis)
        }
    
    def analyze_colors(self, store_analysis):
        """تحلیل روانشناسی رنگ‌ها"""
        return {
            'color_scheme': self._analyze_color_scheme(store_analysis),
            'psychological_impact': self._analyze_color_psychology(store_analysis),
            'color_recommendations': self._generate_color_suggestions(store_analysis)
        }
    
    def optimize_sales(self, store_analysis):
        """بهینه‌سازی فروش"""
        return {
            'current_performance': self._analyze_current_performance(store_analysis),
            'improvement_areas': self._identify_improvement_areas(store_analysis),
            'action_plan': self._create_sales_optimization_plan(store_analysis)
        }
    

    
    def extract_objects(self, image_np):
        """
        Extracts objects (e.g., walls, shelves, entrances, checkout counters) from the image.
        For MVP, this is a placeholder. In a real scenario, this would use a trained ML model.
        Args:
            image_np (np.array): The image as a NumPy array.
        Returns:
            list: A list of dictionaries, each representing an identified object with its type and approximate coordinates.
        """
        # Placeholder for object detection. Simulate some common store elements.
        # In a real application, this would involve a pre-trained model (e.g., YOLO) or custom model.
        height, width, _ = image_np.shape
        objects = []

        # Simulate a main entrance (bottom center)
        objects.append({'type': 'entrance', 'coords': [width // 2 - 50, height - 100, width // 2 + 50, height]})
        # Simulate a checkout counter (top right)
        objects.append({'type': 'checkout', 'coords': [width - 150, 0, width, 50]})
        # Simulate some shelves
        objects.append({'type': 'shelf', 'coords': [50, 50, 150, height - 50]})
        objects.append({'type': 'shelf', 'coords': [width - 150, 100, width - 50, height - 100]})
        objects.append({'type': 'shelf', 'coords': [width // 2 - 100, height // 2 - 50, width // 2 + 100, height // 2 + 50]})

        logger.info(f"Extracted {len(objects)} objects.")
        return objects
    
    def analyze_empty_spaces(self, image_np, objects):
        """
        Analyzes empty spaces in the store layout.
        For MVP, this is a simplified placeholder.
        Args:
            image_np (np.array): The image as a NumPy array.
            objects (list): List of identified objects with their coordinates.
        Returns:
            list: A list of dictionaries, each representing an empty space with its approximate coordinates.
        """
        height, width, _ = image_np.shape
        empty_spaces = []

        # Simple logic: consider areas not covered by objects as empty.
        # This is a very basic approximation for MVP.
        # In a real scenario, this would involve more sophisticated image processing
        # to identify contiguous empty regions.

        # Example: Check a few predefined areas
        # Top-left corner
        is_empty_top_left = True
        for obj in objects:
            x1, y1, x2, y2 = obj['coords']
            if not (x2 < width * 0.2 or y2 < height * 0.2): # If object is outside top-left 20% area
                is_empty_top_left = False
                break
        if is_empty_top_left:
            empty_spaces.append({'type': 'open_area', 'coords': [0, 0, int(width * 0.2), int(height * 0.2)]})

        # Center area (if not heavily occupied)
        is_empty_center = True
        for obj in objects:
            x1, y1, x2, y2 = obj['coords']
            # Check if object significantly overlaps with center 40% area
            if not (x2 < width * 0.3 or y2 < height * 0.3 or x1 > width * 0.7 or y1 > height * 0.7):
                is_empty_center = False
                break
        if is_empty_center:
            empty_spaces.append({'type': 'central_open_space', 'coords': [int(width * 0.3), int(height * 0.3), int(width * 0.7), int(height * 0.7)]})

        logger.info(f"Identified {len(empty_spaces)} empty spaces.")
        return empty_spaces
    
    def analyze_customer_flow(self, image, objects):
        """
        تحلیل جریان مشتری
        """
        # این متد در آینده پیاده‌سازی خواهد شد
        pass
    
    def generate_suggestions(self, analysis_data):
        """
        تولید پیشنهادات بهینه‌سازی
        """
        # این متد در آینده پیاده‌سازی خواهد شد
        pass
    
    # متدهای کمکی برای تحلیل‌های تخصصی
    def _analyze_attention_points(self, store_analysis):
        """تحلیل نقاط توجه"""
        try:
            # تحلیل نقاط توجه بر اساس داده‌های فروشگاه
            high_traffic_areas = store_analysis.high_traffic_areas or ''
            shelf_count = store_analysis.shelf_count or 0
            
            attention_points = []
            
            if high_traffic_areas:
                attention_points.extend(high_traffic_areas.split(','))
            
            if shelf_count > 10:
                attention_points.append('قفسه‌های متعدد')
            
            return {
                'points': attention_points,
                'score': len(attention_points) * 10,
                'insights': f'تعداد نقاط توجه: {len(attention_points)}'
            }
        except Exception as e:
            logger.error(f"Error in attention points analysis: {str(e)}")
            return {'points': [], 'score': 0, 'error': str(e)}
    
    def _analyze_emotional_triggers(self, store_analysis):
        """تحلیل محرک‌های احساسی"""
        try:
            design_style = store_analysis.design_style or 'modern'
            brand_colors = store_analysis.brand_colors or ''
            
            triggers = []
            
            if design_style in ['modern', 'minimalist']:
                triggers.append('طراحی مدرن و تمیز')
            elif design_style == 'traditional':
                triggers.append('طراحی سنتی و گرم')
            
            if brand_colors:
                triggers.append('رنگ‌بندی برند')
            
            return {
                'triggers': triggers,
                'score': len(triggers) * 15,
                'insights': f'تعداد محرک‌های احساسی: {len(triggers)}'
            }
        except Exception as e:
            logger.error(f"Error in emotional triggers analysis: {str(e)}")
            return {'triggers': [], 'score': 0, 'error': str(e)}
    
    def _analyze_decision_making(self, store_analysis):
        """تحلیل فرآیند تصمیم‌گیری"""
        try:
            store_type = store_analysis.store_type or 'other'
            shelf_contents = store_analysis.shelf_contents or ''
            
            decision_factors = []
            
            if store_type in ['supermarket', 'hypermarket']:
                decision_factors.append('دسترسی آسان به محصولات')
            elif store_type == 'clothing':
                decision_factors.append('نمایش مناسب محصولات')
            
            if shelf_contents:
                decision_factors.append('دسته‌بندی منطقی محصولات')
            
            return {
                'factors': decision_factors,
                'score': len(decision_factors) * 12,
                'insights': f'تعداد عوامل تصمیم‌گیری: {len(decision_factors)}'
            }
        except Exception as e:
            logger.error(f"Error in decision making analysis: {str(e)}")
            return {'factors': [], 'score': 0, 'error': str(e)}
    
    def _analyze_lighting_impact(self, store_analysis):
        """تحلیل تأثیر نورپردازی"""
        try:
            # تحلیل ساده نورپردازی
            return {
                'impact': 'متوسط',
                'score': 70,
                'recommendations': ['بهبود نورپردازی در نقاط کلیدی']
            }
        except Exception as e:
            logger.error(f"Error in lighting impact analysis: {str(e)}")
            return {'impact': 'نامشخص', 'score': 0, 'error': str(e)}
    
    def _analyze_color_impact(self, store_analysis):
        """تحلیل تأثیر رنگ‌ها"""
        try:
            brand_colors = store_analysis.brand_colors or ''
            
            if brand_colors:
                return {
                    'impact': 'مثبت',
                    'score': 80,
                    'colors': brand_colors.split(','),
                    'insights': 'رنگ‌بندی برند مشخص است'
                }
            else:
                return {
                    'impact': 'خنثی',
                    'score': 50,
                    'recommendations': ['تعریف رنگ‌بندی برند']
                }
        except Exception as e:
            logger.error(f"Error in color impact analysis: {str(e)}")
            return {'impact': 'نامشخص', 'score': 0, 'error': str(e)}
    
    def _analyze_space_perception(self, store_analysis):
        """تحلیل درک فضا"""
        try:
            store_size = store_analysis.store_size or 0
            shelf_count = store_analysis.shelf_count or 0
            
            if store_size > 0 and shelf_count > 0:
                density = shelf_count / store_size
                
                if density < 0.05:
                    perception = 'باز و وسیع'
                    score = 85
                elif density < 0.1:
                    perception = 'متعادل'
                    score = 75
                else:
                    perception = 'شلوغ و متراکم'
                    score = 60
            else:
                perception = 'نامشخص'
                score = 50
            
            return {
                'perception': perception,
                'score': score,
                'density': density if store_size > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error in space perception analysis: {str(e)}")
            return {'perception': 'نامشخص', 'score': 0, 'error': str(e)}
    
    def _generate_psychological_recommendations(self, store_analysis):
        """تولید توصیه‌های روانشناسی"""
        try:
            recommendations = []
            
            # توصیه‌های بر اساس تحلیل‌های انجام شده
            attention_analysis = self._analyze_attention_points(store_analysis)
            if attention_analysis.get('score', 0) < 50:
                recommendations.append('ایجاد نقاط توجه بیشتر')
            
            emotional_analysis = self._analyze_emotional_triggers(store_analysis)
            if emotional_analysis.get('score', 0) < 30:
                recommendations.append('بهبود محرک‌های احساسی')
            
            return recommendations if recommendations else ['تحلیل روانشناسی مناسب است']
        except Exception as e:
            logger.error(f"Error in psychological recommendations: {str(e)}")
            return ['خطا در تولید توصیه‌های روانشناسی']
    
    def _analyze_current_layout(self, store_analysis):
        """تحلیل چیدمان فعلی"""
        try:
            return {
                'layout_type': store_analysis.store_type or 'unknown',
                'size': store_analysis.store_size or 0,
                'shelves': store_analysis.shelf_count or 0,
                'score': 75  # امتیاز پیش‌فرض
            }
        except Exception as e:
            logger.error(f"Error in current layout analysis: {str(e)}")
            return {'error': str(e), 'score': 0}
    
    def _generate_layout_suggestions(self, store_analysis):
        """تولید پیشنهادات چیدمان"""
        try:
            suggestions = []
            
            store_type = store_analysis.store_type or 'other'
            if store_type in ['supermarket', 'hypermarket']:
                suggestions.append('استفاده از چیدمان شبکه‌ای')
            elif store_type == 'clothing':
                suggestions.append('استفاده از چیدمان آزاد')
            
            return suggestions if suggestions else ['چیدمان فعلی مناسب است']
        except Exception as e:
            logger.error(f"Error in layout suggestions: {str(e)}")
            return ['خطا در تولید پیشنهادات چیدمان']
    
    def _create_implementation_plan(self, store_analysis):
        """ایجاد برنامه اجرایی"""
        try:
            return [
                'مرحله 1: تحلیل وضعیت فعلی',
                'مرحله 2: طراحی چیدمان جدید',
                'مرحله 3: اجرای تغییرات',
                'مرحله 4: ارزیابی نتایج'
            ]
        except Exception as e:
            logger.error(f"Error in implementation plan: {str(e)}")
            return ['خطا در ایجاد برنامه اجرایی']
    
    def _analyze_flow_patterns(self, store_analysis):
        """تحلیل الگوهای جریان"""
        try:
            movement_paths = store_analysis.customer_movement_paths or 'mixed'
            
            patterns = {
                'clockwise': 'جریان ساعتگرد',
                'counterclockwise': 'جریان پادساعتگرد',
                'mixed': 'جریان مختلط',
                'random': 'جریان تصادفی'
            }
            
            return {
                'pattern': patterns.get(movement_paths, 'نامشخص'),
                'score': 70 if movement_paths == 'clockwise' else 60
            }
        except Exception as e:
            logger.error(f"Error in flow patterns analysis: {str(e)}")
            return {'pattern': 'نامشخص', 'score': 0, 'error': str(e)}
    
    def _identify_bottlenecks(self, store_analysis):
        """شناسایی گلوگاه‌ها"""
        try:
            bottlenecks = []
            
            checkout_location = store_analysis.checkout_location or ''
            if not checkout_location:
                bottlenecks.append('موقعیت نامناسب صندوق‌ها')
            
            unused_areas = store_analysis.unused_area_type or ''
            if unused_areas == 'congested':
                bottlenecks.append('مناطق شلوغ و متراکم')
            
            return bottlenecks if bottlenecks else ['گلوگاه خاصی شناسایی نشد']
        except Exception as e:
            logger.error(f"Error in bottleneck identification: {str(e)}")
            return ['خطا در شناسایی گلوگاه‌ها']
    
    def _find_flow_optimizations(self, store_analysis):
        """یافتن بهینه‌سازی‌های جریان"""
        try:
            optimizations = []
            
            entrances = store_analysis.entrances or 1
            if entrances == 1:
                optimizations.append('افزایش تعداد ورودی‌ها')
            
            high_traffic_areas = store_analysis.high_traffic_areas or ''
            if not high_traffic_areas:
                optimizations.append('شناسایی مناطق پرتردد')
            
            return optimizations if optimizations else ['جریان فعلی بهینه است']
        except Exception as e:
            logger.error(f"Error in flow optimizations: {str(e)}")
            return ['خطا در یافتن بهینه‌سازی‌ها']
    
    def _analyze_current_placement(self, store_analysis):
        """تحلیل چیدمان فعلی محصولات"""
        try:
            shelf_contents = store_analysis.shelf_contents or ''
            
            return {
                'has_content': bool(shelf_contents),
                'content_type': 'مشخص' if shelf_contents else 'نامشخص',
                'score': 80 if shelf_contents else 50
            }
        except Exception as e:
            logger.error(f"Error in current placement analysis: {str(e)}")
            return {'error': str(e), 'score': 0}
    
    def _analyze_categories(self, store_analysis):
        """تحلیل دسته‌بندی‌ها"""
        try:
            shelf_contents = store_analysis.shelf_contents or ''
            
            if shelf_contents:
                categories = shelf_contents.split(',')
                return {
                    'count': len(categories),
                    'categories': categories,
                    'score': min(len(categories) * 10, 100)
                }
            else:
                return {
                    'count': 0,
                    'categories': [],
                    'score': 30
                }
        except Exception as e:
            logger.error(f"Error in categories analysis: {str(e)}")
            return {'count': 0, 'categories': [], 'score': 0, 'error': str(e)}
    
    def _generate_placement_suggestions(self, store_analysis):
        """تولید پیشنهادات چیدمان محصولات"""
        try:
            suggestions = []
            
            store_type = store_analysis.store_type or 'other'
            if store_type in ['supermarket', 'hypermarket']:
                suggestions.append('چیدمان محصولات بر اساس دسته‌بندی')
            elif store_type == 'clothing':
                suggestions.append('چیدمان محصولات بر اساس سبک')
            
            return suggestions if suggestions else ['چیدمان محصولات مناسب است']
        except Exception as e:
            logger.error(f"Error in placement suggestions: {str(e)}")
            return ['خطا در تولید پیشنهادات چیدمان محصولات']
    
    def _analyze_current_lighting(self, store_analysis):
        """تحلیل نورپردازی فعلی"""
        try:
            # تحلیل ساده نورپردازی
            return {
                'type': 'مصنوعی',
                'score': 70,
                'insights': 'نورپردازی پایه وجود دارد'
            }
        except Exception as e:
            logger.error(f"Error in current lighting analysis: {str(e)}")
            return {'type': 'نامشخص', 'score': 0, 'error': str(e)}
    
    def _analyze_lighting_effects(self, store_analysis):
        """تحلیل تأثیرات نورپردازی"""
        try:
            return {
                'mood': 'خنثی',
                'visibility': 'خوب',
                'score': 75
            }
        except Exception as e:
            logger.error(f"Error in lighting effects analysis: {str(e)}")
            return {'mood': 'نامشخص', 'visibility': 'نامشخص', 'score': 0, 'error': str(e)}
    
    def _generate_lighting_recommendations(self, store_analysis):
        """تولید توصیه‌های نورپردازی"""
        try:
            return [
                'بهبود نورپردازی در نقاط کلیدی',
                'استفاده از نور طبیعی در صورت امکان',
                'بهینه‌سازی نورپردازی قفسه‌ها'
            ]
        except Exception as e:
            logger.error(f"Error in lighting recommendations: {str(e)}")
            return ['خطا در تولید توصیه‌های نورپردازی']
    
    def _analyze_color_scheme(self, store_analysis):
        """تحلیل طرح رنگی"""
        try:
            brand_colors = store_analysis.brand_colors or ''
            
            if brand_colors:
                colors = brand_colors.split(',')
                return {
                    'colors': colors,
                    'count': len(colors),
                    'score': min(len(colors) * 20, 100)
                }
            else:
                return {
                    'colors': [],
                    'count': 0,
                    'score': 30
                }
        except Exception as e:
            logger.error(f"Error in color scheme analysis: {str(e)}")
            return {'colors': [], 'count': 0, 'score': 0, 'error': str(e)}
    
    def _analyze_color_psychology(self, store_analysis):
        """تحلیل روانشناسی رنگ‌ها"""
        try:
            brand_colors = store_analysis.brand_colors or ''
            
            psychology = {}
            if 'قرمز' in brand_colors:
                psychology['قرمز'] = 'انرژی و هیجان'
            if 'آبی' in brand_colors:
                psychology['آبی'] = 'اعتماد و آرامش'
            if 'سبز' in brand_colors:
                psychology['سبز'] = 'طبیعت و رشد'
            
            return {
                'psychology': psychology,
                'score': len(psychology) * 25
            }
        except Exception as e:
            logger.error(f"Error in color psychology analysis: {str(e)}")
            return {'psychology': {}, 'score': 0, 'error': str(e)}
    
    def _generate_color_suggestions(self, store_analysis):
        """تولید پیشنهادات رنگی"""
        try:
            brand_colors = store_analysis.brand_colors or ''
            
            if not brand_colors:
                return [
                    'تعریف رنگ‌های اصلی برند',
                    'استفاده از رنگ‌های هماهنگ',
                    'بهبود کنتراست رنگی'
                ]
            else:
                return ['طرح رنگی فعلی مناسب است']
        except Exception as e:
            logger.error(f"Error in color suggestions: {str(e)}")
            return ['خطا در تولید پیشنهادات رنگی']
    
    def _analyze_current_performance(self, store_analysis):
        """تحلیل عملکرد فعلی"""
        try:
            return {
                'score': 75,
                'status': 'متوسط',
                'insights': 'عملکرد قابل قبول'
            }
        except Exception as e:
            logger.error(f"Error in current performance analysis: {str(e)}")
            return {'score': 0, 'status': 'نامشخص', 'error': str(e)}
    
    def _identify_improvement_areas(self, store_analysis):
        """شناسایی حوزه‌های بهبود"""
        try:
            areas = []
            
            unused_areas = store_analysis.unused_area_type or ''
            if unused_areas == 'empty':
                areas.append('استفاده از فضاهای خالی')
            
            if not store_analysis.high_traffic_areas:
                areas.append('بهبود مناطق پرتردد')
            
            return areas if areas else ['حوزه بهبود خاصی شناسایی نشد']
        except Exception as e:
            logger.error(f"Error in improvement areas identification: {str(e)}")
            return ['خطا در شناسایی حوزه‌های بهبود']
    
    def _create_sales_optimization_plan(self, store_analysis):
        """ایجاد برنامه بهینه‌سازی فروش"""
        try:
            return [
                'مرحله 1: تحلیل فروش فعلی',
                'مرحله 2: شناسایی نقاط ضعف',
                'مرحله 3: طراحی راهکارهای بهبود',
                'مرحله 4: اجرا و نظارت'
            ]
        except Exception as e:
            logger.error(f"Error in sales optimization plan: {str(e)}")
            return ['خطا در ایجاد برنامه بهینه‌سازی فروش'] 