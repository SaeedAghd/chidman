"""
سیستم تحلیل تصاویر هوشمند پیشرفته
Advanced Intelligent Image Analysis System
"""

import cv2
import numpy as np
import base64
import io
from PIL import Image, ImageEnhance, ImageFilter
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

@dataclass
class ImageAnalysisResult:
    """نتیجه تحلیل تصویر"""
    store_type_confidence: float
    size_estimation: Dict[str, Any]
    layout_analysis: Dict[str, Any]
    color_analysis: Dict[str, Any]
    object_detection: List[Dict[str, Any]]
    consistency_score: float
    recommendations: List[str]
    quality_score: float
    professional_grade: bool

class AdvancedImageAnalyzer:
    """تحلیلگر تصاویر پیشرفته با قابلیت‌های AI"""
    
    def __init__(self):
        self.liara_ai_service = None
        self._init_liara_ai()
        
    def _init_liara_ai(self):
        """راه‌اندازی سرویس Chidmano1 AI"""
        try:
            from .liara_ai_service import LiaraAIService
            self.liara_ai_service = LiaraAIService()
        except Exception as e:
            logger.warning(f"Chidmano1 AI service not available: {e}")
    
    def analyze_store_images(self, images: List[str], store_info: Dict[str, Any]) -> ImageAnalysisResult:
        """
        تحلیل کامل تصاویر فروشگاه با AI پیشرفته
        
        Args:
            images: لیست تصاویر base64
            store_info: اطلاعات فروشگاه از کاربر
            
        Returns:
            ImageAnalysisResult: نتیجه تحلیل کامل
        """
        try:
            # 1. تحلیل اولیه تصاویر
            basic_analysis = self._basic_image_analysis(images)
            
            # 2. تحلیل با AI پیشرفته
            ai_analysis = self._advanced_ai_analysis(images, store_info)
            
            # 3. مقایسه و تطبیق
            consistency_analysis = self._consistency_check(basic_analysis, ai_analysis, store_info)
            
            # 4. تولید توصیه‌های حرفه‌ای
            recommendations = self._generate_professional_recommendations(
                basic_analysis, ai_analysis, consistency_analysis, store_info
            )
            
            # 5. محاسبه امتیاز کلی
            overall_score = self._calculate_overall_score(
                basic_analysis, ai_analysis, consistency_analysis
            )
            
            return ImageAnalysisResult(
                store_type_confidence=ai_analysis.get('store_type_confidence', 0.0),
                size_estimation=basic_analysis.get('size_estimation', {}),
                layout_analysis=basic_analysis.get('layout_analysis', {}),
                color_analysis=basic_analysis.get('color_analysis', {}),
                object_detection=basic_analysis.get('object_detection', []),
                consistency_score=consistency_analysis.get('score', 0.0),
                recommendations=recommendations,
                quality_score=basic_analysis.get('quality_score', 0.0),
                professional_grade=overall_score > 0.8
            )
            
        except Exception as e:
            logger.error(f"Error in advanced image analysis: {e}")
            return self._create_fallback_result()
    
    def _basic_image_analysis(self, images: List[str]) -> Dict[str, Any]:
        """تحلیل اولیه تصاویر با OpenCV"""
        results = {
            'size_estimation': {},
            'layout_analysis': {},
            'color_analysis': {},
            'object_detection': [],
            'quality_score': 0.0
        }
        
        try:
            for i, img_base64 in enumerate(images):
                # تبدیل base64 به تصویر
                img = self._base64_to_image(img_base64)
                if img is None:
                    continue
                
                # تحلیل اندازه
                size_analysis = self._analyze_image_size(img, i)
                results['size_estimation'][f'image_{i}'] = size_analysis
                
                # تحلیل چیدمان
                layout_analysis = self._analyze_layout(img, i)
                results['layout_analysis'][f'image_{i}'] = layout_analysis
                
                # تحلیل رنگ
                color_analysis = self._analyze_colors(img, i)
                results['color_analysis'][f'image_{i}'] = color_analysis
                
                # تشخیص اشیاء
                objects = self._detect_objects(img, i)
                results['object_detection'].extend(objects)
                
                # امتیاز کیفیت
                quality = self._calculate_image_quality(img)
                results['quality_score'] = max(results['quality_score'], quality)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in basic image analysis: {e}")
            return results
    
    def _advanced_ai_analysis(self, images: List[str], store_info: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل پیشرفته با AI"""
        if not self.liara_ai_service:
            return self._fallback_ai_analysis(store_info)
        
        try:
            # آماده‌سازی prompt برای AI
            prompt = self._create_advanced_analysis_prompt(images, store_info)
            
            # درخواست به Chidmano1 AI
            response = self.liara_ai_service.analyze_store_images(
                images=images,
                store_info=store_info,
                analysis_type='comprehensive'
            )
            
            if response and response.get('status') == 'success':
                return response.get('analysis', {})
            else:
                return self._fallback_ai_analysis(store_info)
                
        except Exception as e:
            logger.error(f"Error in advanced AI analysis: {e}")
            return self._fallback_ai_analysis(store_info)
    
    def _consistency_check(self, basic_analysis: Dict, ai_analysis: Dict, store_info: Dict) -> Dict[str, Any]:
        """بررسی سازگاری بین تحلیل‌ها و اطلاعات کاربر"""
        consistency_score = 0.0
        inconsistencies = []
        
        try:
            # بررسی نوع فروشگاه
            user_store_type = store_info.get('store_type', '').lower()
            ai_store_type = ai_analysis.get('detected_store_type', '').lower()
            
            if user_store_type and ai_store_type:
                if user_store_type in ai_store_type or ai_store_type in user_store_type:
                    consistency_score += 0.3
                else:
                    inconsistencies.append(f"نوع فروشگاه: کاربر '{user_store_type}' اما AI تشخیص '{ai_store_type}'")
            
            # بررسی اندازه فروشگاه
            user_size = store_info.get('store_size', 0)
            estimated_size = basic_analysis.get('size_estimation', {}).get('total_estimated_size', 0)
            
            if user_size and estimated_size:
                size_diff = abs(user_size - estimated_size) / max(user_size, estimated_size)
                if size_diff < 0.3:  # اختلاف کمتر از 30%
                    consistency_score += 0.3
                else:
                    inconsistencies.append(f"اندازه فروشگاه: کاربر {user_size}m² اما تخمین {estimated_size}m²")
            
            # بررسی کیفیت تصاویر
            quality_score = basic_analysis.get('quality_score', 0)
            if quality_score > 0.7:
                consistency_score += 0.2
            elif quality_score < 0.4:
                inconsistencies.append("کیفیت تصاویر پایین است")
            
            # بررسی تنوع تصاویر
            num_images = len(basic_analysis.get('size_estimation', {}))
            if num_images >= 3:
                consistency_score += 0.2
            else:
                inconsistencies.append("تعداد تصاویر کافی نیست (حداقل 3 تصویر)")
            
            return {
                'score': min(consistency_score, 1.0),
                'inconsistencies': inconsistencies,
                'recommendations': self._generate_consistency_recommendations(inconsistencies)
            }
            
        except Exception as e:
            logger.error(f"Error in consistency check: {e}")
            return {'score': 0.0, 'inconsistencies': [], 'recommendations': []}
    
    def _generate_professional_recommendations(self, basic_analysis: Dict, ai_analysis: Dict, 
                                             consistency_analysis: Dict, store_info: Dict) -> List[str]:
        """تولید توصیه‌های حرفه‌ای"""
        recommendations = []
        
        try:
            # توصیه‌های بر اساس سازگاری
            if consistency_analysis.get('score', 0) < 0.7:
                recommendations.extend([
                    "📸 تصاویر بیشتری از زوایای مختلف فروشگاه تهیه کنید",
                    "🎯 اطمینان حاصل کنید که تصاویر نمایانگر واقعی فروشگاه هستند",
                    "📏 اندازه دقیق فروشگاه را اندازه‌گیری و ثبت کنید"
                ])
            
            # توصیه‌های بر اساس کیفیت تصاویر
            quality_score = basic_analysis.get('quality_score', 0)
            if quality_score < 0.6:
                recommendations.extend([
                    "📷 از نور مناسب برای عکاسی استفاده کنید",
                    "🔍 تصاویر را با وضوح بالا تهیه کنید",
                    "📐 تصاویر را از زوایای مختلف و کامل بگیرید"
                ])
            
            # توصیه‌های بر اساس نوع فروشگاه
            store_type = store_info.get('store_type', '').lower()
            if 'فروشگاه' in store_type or 'shop' in store_type:
                recommendations.extend([
                    "🏪 چیدمان محصولات را به صورت حرفه‌ای تنظیم کنید",
                    "💡 از نورپردازی مناسب برای نمایش محصولات استفاده کنید",
                    "🎨 رنگ‌بندی هماهنگ و جذاب انتخاب کنید"
                ])
            elif 'رستوران' in store_type or 'restaurant' in store_type:
                recommendations.extend([
                    "🍽️ میزها و صندلی‌ها را به صورت منظم چیدمان کنید",
                    "🌿 از گیاهان و تزئینات مناسب استفاده کنید",
                    "💡 نورپردازی گرم و دوستانه ایجاد کنید"
                ])
            
            # توصیه‌های کلی
            recommendations.extend([
                "📊 تحلیل‌های منظم از عملکرد فروشگاه انجام دهید",
                "🎯 اهداف مشخص و قابل اندازه‌گیری تعریف کنید",
                "📈 از داده‌های مشتریان برای بهبود استفاده کنید"
            ])
            
            return recommendations[:10]  # حداکثر 10 توصیه
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return ["خطا در تولید توصیه‌ها"]
    
    def _base64_to_image(self, base64_string: str) -> Optional[np.ndarray]:
        """تبدیل base64 به تصویر OpenCV"""
        try:
            # حذف prefix اگر وجود دارد
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            # تبدیل base64 به bytes
            img_bytes = base64.b64decode(base64_string)
            
            # تبدیل به PIL Image
            pil_image = Image.open(io.BytesIO(img_bytes))
            
            # تبدیل به OpenCV format
            opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            return opencv_image
            
        except Exception as e:
            logger.error(f"Error converting base64 to image: {e}")
            return None
    
    def _analyze_image_size(self, img: np.ndarray, image_index: int) -> Dict[str, Any]:
        """تحلیل اندازه تصویر و تخمین اندازه فروشگاه"""
        try:
            height, width = img.shape[:2]
            
            # تخمین اندازه بر اساس ویژگی‌های تصویر
            # این یک تخمین ساده است - در واقعیت باید از AI استفاده کرد
            estimated_size = (width * height) / 10000  # فرمول ساده
            
            return {
                'dimensions': {'width': width, 'height': height},
                'estimated_area': estimated_size,
                'aspect_ratio': width / height,
                'resolution_quality': 'high' if width > 1000 and height > 1000 else 'medium'
            }
            
        except Exception as e:
            logger.error(f"Error analyzing image size: {e}")
            return {}
    
    def _analyze_layout(self, img: np.ndarray, image_index: int) -> Dict[str, Any]:
        """تحلیل چیدمان و ساختار تصویر"""
        try:
            # تبدیل به خاکستری
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # تشخیص لبه‌ها
            edges = cv2.Canny(gray, 50, 150)
            
            # تشخیص خطوط
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
            
            # تحلیل چیدمان
            layout_analysis = {
                'has_horizontal_lines': False,
                'has_vertical_lines': False,
                'symmetry_score': 0.0,
                'organization_level': 'low'
            }
            
            if lines is not None:
                horizontal_lines = 0
                vertical_lines = 0
                
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                    
                    if abs(angle) < 15 or abs(angle - 180) < 15:
                        horizontal_lines += 1
                    elif abs(angle - 90) < 15 or abs(angle + 90) < 15:
                        vertical_lines += 1
                
                layout_analysis['has_horizontal_lines'] = horizontal_lines > 0
                layout_analysis['has_vertical_lines'] = vertical_lines > 0
                layout_analysis['symmetry_score'] = min(1.0, (horizontal_lines + vertical_lines) / 10)
                
                if layout_analysis['symmetry_score'] > 0.7:
                    layout_analysis['organization_level'] = 'high'
                elif layout_analysis['symmetry_score'] > 0.4:
                    layout_analysis['organization_level'] = 'medium'
            
            return layout_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing layout: {e}")
            return {}
    
    def _analyze_colors(self, img: np.ndarray, image_index: int) -> Dict[str, Any]:
        """تحلیل رنگ‌های تصویر"""
        try:
            # تبدیل به HSV برای تحلیل بهتر رنگ‌ها
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # محاسبه هیستوگرام رنگ‌ها
            hist_h = cv2.calcHist([hsv], [0], None, [180], [0, 180])
            hist_s = cv2.calcHist([hsv], [1], None, [256], [0, 256])
            hist_v = cv2.calcHist([hsv], [2], None, [256], [0, 256])
            
            # رنگ غالب
            dominant_hue = np.argmax(hist_h)
            dominant_saturation = np.argmax(hist_s)
            dominant_value = np.argmax(hist_v)
            
            # تنوع رنگ
            color_diversity = len(np.where(hist_h > hist_h.max() * 0.1)[0])
            
            return {
                'dominant_hue': int(dominant_hue),
                'dominant_saturation': int(dominant_saturation),
                'dominant_value': int(dominant_value),
                'color_diversity': int(color_diversity),
                'brightness_level': 'bright' if dominant_value > 128 else 'dark',
                'saturation_level': 'vibrant' if dominant_saturation > 128 else 'muted'
            }
            
        except Exception as e:
            logger.error(f"Error analyzing colors: {e}")
            return {}
    
    def _detect_objects(self, img: np.ndarray, image_index: int) -> List[Dict[str, Any]]:
        """تشخیص اشیاء در تصویر"""
        try:
            # اینجا می‌توان از مدل‌های پیش‌آموخته استفاده کرد
            # برای حال حاضر، تشخیص ساده انجام می‌دهیم
            
            objects = []
            
            # تشخیص مستطیل‌ها (میز، قفسه، و غیره)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # فقط اشیاء بزرگ
                    x, y, w, h = cv2.boundingRect(contour)
                    objects.append({
                        'type': 'rectangle',
                        'position': {'x': int(x), 'y': int(y)},
                        'size': {'width': int(w), 'height': int(h)},
                        'area': int(area),
                        'confidence': min(1.0, area / 10000)
                    })
            
            return objects
            
        except Exception as e:
            logger.error(f"Error detecting objects: {e}")
            return []
    
    def _calculate_image_quality(self, img: np.ndarray) -> float:
        """محاسبه کیفیت تصویر"""
        try:
            # محاسبه وضوح
            height, width = img.shape[:2]
            resolution_score = min(1.0, (width * height) / (1920 * 1080))
            
            # محاسبه کنتراست
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            contrast = gray.std()
            contrast_score = min(1.0, contrast / 100)
            
            # محاسبه روشنایی
            brightness = gray.mean()
            brightness_score = 1.0 - abs(brightness - 128) / 128
            
            # امتیاز کلی
            quality_score = (resolution_score * 0.4 + contrast_score * 0.3 + brightness_score * 0.3)
            
            return quality_score
            
        except Exception as e:
            logger.error(f"Error calculating image quality: {e}")
            return 0.0
    
    def _create_advanced_analysis_prompt(self, images: List[str], store_info: Dict[str, Any]) -> str:
        """ایجاد prompt پیشرفته برای AI"""
        return f"""
        تحلیل حرفه‌ای فروشگاه با هوش مصنوعی پیشرفته
        
        اطلاعات فروشگاه:
        - نام: {store_info.get('store_name', 'نامشخص')}
        - نوع: {store_info.get('store_type', 'نامشخص')}
        - اندازه: {store_info.get('store_size', 'نامشخص')} متر مربع
        - شهر: {store_info.get('city', 'نامشخص')}
        
        لطفاً تصاویر ارائه شده را با دقت تحلیل کنید و موارد زیر را بررسی کنید:
        
        1. نوع فروشگاه تشخیص داده شده
        2. کیفیت چیدمان و طراحی
        3. تناسب رنگ‌ها و نورپردازی
        4. نقاط قوت و ضعف
        5. توصیه‌های بهبود
        6. امتیاز کلی (0-100)
        
        تحلیل باید حرفه‌ای، دقیق و قابل اجرا باشد.
        """
    
    def _fallback_ai_analysis(self, store_info: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل جایگزین در صورت عدم دسترسی به AI"""
        return {
            'detected_store_type': store_info.get('store_type', 'عمومی'),
            'store_type_confidence': 0.7,
            'analysis_quality': 'basic',
            'recommendations': [
                'برای تحلیل دقیق‌تر، تصاویر بیشتری تهیه کنید',
                'اطمینان حاصل کنید که تصاویر نمایانگر واقعی فروشگاه هستند'
            ]
        }
    
    def _generate_consistency_recommendations(self, inconsistencies: List[str]) -> List[str]:
        """تولید توصیه‌های بر اساس ناسازگاری‌ها"""
        recommendations = []
        
        for inconsistency in inconsistencies:
            if 'نوع فروشگاه' in inconsistency:
                recommendations.append('نوع فروشگاه را با دقت انتخاب کنید')
            elif 'اندازه فروشگاه' in inconsistency:
                recommendations.append('اندازه دقیق فروشگاه را اندازه‌گیری کنید')
            elif 'کیفیت تصاویر' in inconsistency:
                recommendations.append('تصاویر با کیفیت بالاتر تهیه کنید')
            elif 'تعداد تصاویر' in inconsistency:
                recommendations.append('تصاویر بیشتری از زوایای مختلف تهیه کنید')
        
        return recommendations
    
    def _calculate_overall_score(self, basic_analysis: Dict, ai_analysis: Dict, consistency_analysis: Dict) -> float:
        """محاسبه امتیاز کلی"""
        try:
            # امتیاز کیفیت تصاویر (40%)
            quality_score = basic_analysis.get('quality_score', 0) * 0.4
            
            # امتیاز AI (30%)
            ai_confidence = ai_analysis.get('store_type_confidence', 0) * 0.3
            
            # امتیاز سازگاری (30%)
            consistency_score = consistency_analysis.get('score', 0) * 0.3
            
            return quality_score + ai_confidence + consistency_score
            
        except Exception as e:
            logger.error(f"Error calculating overall score: {e}")
            return 0.0
    
    def _create_fallback_result(self) -> ImageAnalysisResult:
        """ایجاد نتیجه جایگزین در صورت خطا"""
        return ImageAnalysisResult(
            store_type_confidence=0.5,
            size_estimation={},
            layout_analysis={},
            color_analysis={},
            object_detection=[],
            consistency_score=0.5,
            recommendations=['خطا در تحلیل تصاویر - لطفاً دوباره تلاش کنید'],
            quality_score=0.5,
            professional_grade=False
        )
