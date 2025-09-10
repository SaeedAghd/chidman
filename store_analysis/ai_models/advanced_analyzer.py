import openai
import cv2
import numpy as np
from PIL import Image
import io
import base64
from typing import Dict, List, Tuple, Optional, Any
import json
import logging
from dataclasses import dataclass
from enum import Enum
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

class AnalysisType(Enum):
    LAYOUT = "layout"
    TRAFFIC = "traffic"
    DESIGN = "design"
    SALES = "sales"
    CUSTOMER_BEHAVIOR = "customer_behavior"
    OPTIMIZATION = "optimization"

@dataclass
class AnalysisResult:
    score: float
    analysis: str
    recommendations: List[str]
    visual_data: Optional[Dict] = None
    metrics: Optional[Dict] = None

class AdvancedStoreAnalyzer:
    """
    سیستم پیشرفته تحلیل چیدمان فروشگاه با هوش مصنوعی
    """
    
    def __init__(self):
        self.openai_client = None
        self.setup_openai()
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def analyze_store(self, store_data: Dict) -> Dict[str, Any]:
        """تحلیل فروشگاه به صورت همزمان"""
        try:
            # محاسبه امتیاز کلی
            overall_score = self._calculate_basic_score(store_data)
            
            # تولید تحلیل پایه
            analysis = self._generate_basic_analysis(store_data)
            
            # تولید توصیه‌ها
            recommendations = self._generate_basic_recommendations(store_data)
            
            return {
                'score': overall_score,
                'analysis': analysis,
                'recommendations': recommendations,
                'metrics': self._extract_basic_metrics(store_data)
            }
        except Exception as e:
            logger.error(f"Error in basic store analysis: {e}")
            return {
                'score': 70.0,
                'analysis': 'تحلیل پایه انجام شد',
                'recommendations': ['لطفاً برای تحلیل پیشرفته از OpenAI استفاده کنید'],
                'metrics': {}
            }
    
    def _calculate_basic_score(self, store_data: Dict) -> float:
        """محاسبه امتیاز پایه"""
        score = 70.0
        
        # بهبود بر اساس اندازه فروشگاه
        store_size = store_data.get('store_size', 0)
        if store_size > 100:
            score += 10
        if store_size > 200:
            score += 10
            
        # بهبود بر اساس تعداد مشتریان
        daily_customers = store_data.get('daily_customers', 0)
        if daily_customers > 100:
            score += 10
            
        return min(score, 100.0)
    
    def _generate_basic_analysis(self, store_data: Dict) -> str:
        """تولید تحلیل پایه"""
        store_name = store_data.get('store_name', 'فروشگاه')
        store_type = store_data.get('store_type', 'عمومی')
        store_size = store_data.get('store_size', 0)
        
        return f"""
        تحلیل پایه {store_name}
        
        نوع فروشگاه: {store_type}
        متراژ: {store_size} متر مربع
        
        این تحلیل پایه بر اساس داده‌های ورودی انجام شده است.
        برای تحلیل پیشرفته و دقیق‌تر، از OpenAI API استفاده کنید.
        """
    
    def _generate_basic_recommendations(self, store_data: Dict) -> List[str]:
        """تولید توصیه‌های پایه"""
        recommendations = []
        
        store_size = store_data.get('store_size', 0)
        if store_size < 100:
            recommendations.append('متراژ فروشگاه را افزایش دهید')
            
        daily_customers = store_data.get('daily_customers', 0)
        if daily_customers < 50:
            recommendations.append('استراتژی‌های جذب مشتری را بهبود دهید')
            
        return recommendations
    
    def _extract_basic_metrics(self, store_data: Dict) -> Dict:
        """استخراج متریک‌های پایه"""
        return {
            'store_size': store_data.get('store_size', 0),
            'daily_customers': store_data.get('daily_customers', 0),
            'store_type': store_data.get('store_type', 'عمومی')
        }
        
    def setup_openai(self):
        """تنظیم OpenAI Client"""
        try:
            from openai import OpenAI
            # فقط API key را ارسال کن، بدون تنظیمات proxy
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        except ImportError:
            logger.warning("OpenAI library not found, using fallback")
            self.openai_client = None
        except Exception as e:
            logger.error(f"Error setting up OpenAI client: {e}")
            self.openai_client = None
    
    async def analyze_store_comprehensive(self, store_data: Dict) -> Dict[str, AnalysisResult]:
        """
        تحلیل جامع فروشگاه با تمام جنبه‌ها
        """
        tasks = [
            self.analyze_layout_advanced(store_data),
            self.analyze_traffic_patterns(store_data),
            self.analyze_design_elements(store_data),
            self.analyze_sales_optimization(store_data),
            self.analyze_customer_behavior(store_data),
            self.generate_optimization_plan(store_data)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            AnalysisType.LAYOUT.value: results[0],
            AnalysisType.TRAFFIC.value: results[1],
            AnalysisType.DESIGN.value: results[2],
            AnalysisType.SALES.value: results[3],
            AnalysisType.CUSTOMER_BEHAVIOR.value: results[4],
            AnalysisType.OPTIMIZATION.value: results[5]
        }
    
    async def analyze_layout_advanced(self, store_data: Dict) -> AnalysisResult:
        """
        تحلیل پیشرفته چیدمان با AI
        """
        prompt = self._create_layout_prompt(store_data)
        
        try:
            response = await self._get_ai_response(prompt, "layout_expert")
            
            # تحلیل تصویر اگر موجود باشد
            image_analysis = None
            if store_data.get('store_plan'):
                image_analysis = await self._analyze_store_image(store_data['store_plan'])
            
            # محاسبه امتیاز بر اساس معیارهای مختلف
            score = self._calculate_layout_score(store_data, response, image_analysis)
            
            # تولید توصیه‌های عملی
            recommendations = self._generate_layout_recommendations(store_data, response)
            
            return AnalysisResult(
                score=score,
                analysis=response,
                recommendations=recommendations,
                visual_data=image_analysis,
                metrics=self._extract_layout_metrics(store_data)
            )
            
        except Exception as e:
            logger.error(f"Error in layout analysis: {e}")
            return AnalysisResult(
                score=0.0,
                analysis="خطا در تحلیل چیدمان",
                recommendations=["لطفاً دوباره تلاش کنید"]
            )
    
    async def analyze_traffic_patterns(self, store_data: Dict) -> AnalysisResult:
        """
        تحلیل الگوهای ترافیک مشتری
        """
        prompt = self._create_traffic_prompt(store_data)
        
        try:
            response = await self._get_ai_response(prompt, "traffic_analyst")
            
            # تحلیل ویدیو اگر موجود باشد
            video_analysis = None
            if store_data.get('customer_video_file'):
                video_analysis = await self._analyze_customer_video(store_data['customer_video_file'])
            
            score = self._calculate_traffic_score(store_data, response, video_analysis)
            recommendations = self._generate_traffic_recommendations(store_data, response)
            
            return AnalysisResult(
                score=score,
                analysis=response,
                recommendations=recommendations,
                visual_data=video_analysis,
                metrics=self._extract_traffic_metrics(store_data)
            )
            
        except Exception as e:
            logger.error(f"Error in traffic analysis: {e}")
            return AnalysisResult(
                score=0.0,
                analysis="خطا در تحلیل ترافیک",
                recommendations=["لطفاً دوباره تلاش کنید"]
            )
    
    async def analyze_design_elements(self, store_data: Dict) -> AnalysisResult:
        """
        تحلیل عناصر طراحی و دکوراسیون
        """
        prompt = self._create_design_prompt(store_data)
        
        try:
            response = await self._get_ai_response(prompt, "design_expert")
            
            # تحلیل عکس‌های فروشگاه
            photo_analysis = None
            if store_data.get('store_photos'):
                photo_analysis = await self._analyze_store_photos(store_data['store_photos'])
            
            score = self._calculate_design_score(store_data, response, photo_analysis)
            recommendations = self._generate_design_recommendations(store_data, response)
            
            return AnalysisResult(
                score=score,
                analysis=response,
                recommendations=recommendations,
                visual_data=photo_analysis,
                metrics=self._extract_design_metrics(store_data)
            )
            
        except Exception as e:
            logger.error(f"Error in design analysis: {e}")
            return AnalysisResult(
                score=0.0,
                analysis="خطا در تحلیل طراحی",
                recommendations=["لطفاً دوباره تلاش کنید"]
            )
    
    async def analyze_sales_optimization(self, store_data: Dict) -> AnalysisResult:
        """
        تحلیل بهینه‌سازی فروش
        """
        prompt = self._create_sales_prompt(store_data)
        
        try:
            response = await self._get_ai_response(prompt, "sales_optimizer")
            
            score = self._calculate_sales_score(store_data, response)
            recommendations = self._generate_sales_recommendations(store_data, response)
            
            return AnalysisResult(
                score=score,
                analysis=response,
                recommendations=recommendations,
                metrics=self._extract_sales_metrics(store_data)
            )
            
        except Exception as e:
            logger.error(f"Error in sales analysis: {e}")
            return AnalysisResult(
                score=0.0,
                analysis="خطا در تحلیل فروش",
                recommendations=["لطفاً دوباره تلاش کنید"]
            )
    
    async def analyze_customer_behavior(self, store_data: Dict) -> AnalysisResult:
        """
        تحلیل رفتار مشتری
        """
        prompt = self._create_customer_behavior_prompt(store_data)
        
        try:
            response = await self._get_ai_response(prompt, "customer_psychologist")
            
            score = self._calculate_customer_behavior_score(store_data, response)
            recommendations = self._generate_customer_behavior_recommendations(store_data, response)
            
            return AnalysisResult(
                score=score,
                analysis=response,
                recommendations=recommendations,
                metrics=self._extract_customer_behavior_metrics(store_data)
            )
            
        except Exception as e:
            logger.error(f"Error in customer behavior analysis: {e}")
            return AnalysisResult(
                score=0.0,
                analysis="خطا در تحلیل رفتار مشتری",
                recommendations=["لطفاً دوباره تلاش کنید"]
            )
    
    async def generate_optimization_plan(self, store_data: Dict) -> AnalysisResult:
        """
        تولید برنامه بهینه‌سازی جامع
        """
        prompt = self._create_optimization_prompt(store_data)
        
        try:
            response = await self._get_ai_response(prompt, "optimization_planner")
            
            # تولید نقشه بهینه‌سازی
            optimization_map = await self._generate_optimization_map(store_data)
            
            return AnalysisResult(
                score=0.0,  # امتیاز در این بخش معنی ندارد
                analysis=response,
                recommendations=self._extract_optimization_steps(response),
                visual_data=optimization_map
            )
            
        except Exception as e:
            logger.error(f"Error in optimization planning: {e}")
            return AnalysisResult(
                score=0.0,
                analysis="خطا در تولید برنامه بهینه‌سازی",
                recommendations=["لطفاً دوباره تلاش کنید"]
            )
    
    async def _get_ai_response(self, prompt: str, system_role: str) -> str:
        """دریافت پاسخ از AI"""
        if not self.openai_client:
            return "سیستم AI در دسترس نیست"
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_prompt(system_role)},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return "خطا در ارتباط با سیستم AI"
    
    def _get_system_prompt(self, role: str) -> str:
        """دریافت prompt سیستم بر اساس نقش"""
        prompts = {
            "layout_expert": """شما یک متخصص چیدمان فروشگاه با 20 سال تجربه هستید. 
            تحلیل شما باید دقیق، علمی و قابل اجرا باشد.""",
            
            "traffic_analyst": """شما یک تحلیلگر ترافیک فروشگاه با تخصص در روانشناسی مشتری هستید.
            تحلیل شما باید بر اساس داده‌های واقعی و الگوهای رفتاری باشد.""",
            
            "design_expert": """شما یک طراح داخلی و متخصص دکوراسیون فروشگاه هستید.
            تحلیل شما باید زیبایی‌شناختی و کاربردی باشد.""",
            
            "sales_optimizer": """شما یک متخصص بهینه‌سازی فروش با تجربه در افزایش درآمد فروشگاه‌ها هستید.
            تحلیل شما باید عملی و قابل اندازه‌گیری باشد.""",
            
            "customer_psychologist": """شما یک روانشناس مشتری با تخصص در رفتار خرید هستید.
            تحلیل شما باید بر اساس اصول روانشناسی و رفتارشناسی باشد.""",
            
            "optimization_planner": """شما یک برنامه‌ریز استراتژیک با تخصص در بهینه‌سازی فروشگاه‌ها هستید.
            برنامه شما باید جامع، مرحله‌ای و قابل اجرا باشد."""
        }
        return prompts.get(role, "شما یک متخصص تحلیل فروشگاه هستید.")
    
    def _create_layout_prompt(self, store_data: Dict) -> str:
        """ایجاد prompt برای تحلیل چیدمان"""
        return f"""
        تحلیل چیدمان فروشگاه {store_data.get('store_name', '')}:
        
        مشخصات فروشگاه:
        - نوع: {store_data.get('store_type', '')}
        - متراژ: {store_data.get('store_size', '')} متر مربع
        - ابعاد: {store_data.get('store_dimensions', '')}
        - تعداد قفسه: {store_data.get('shelf_count', '')}
        - ورودی‌ها: {store_data.get('entrances', '')}
        
        چیدمان:
        - ابعاد قفسه‌ها: {store_data.get('shelf_dimensions', '')}
        - محتوای قفسه‌ها: {store_data.get('shelf_contents', '')}
        - محل صندوق: {store_data.get('checkout_location', '')}
        
        مناطق بلااستفاده:
        - نوع: {store_data.get('unused_area_type', '')}
        - متراژ: {store_data.get('unused_area_size', '')}
        - دلیل: {store_data.get('unused_area_reason', '')}
        
        لطفاً تحلیل دقیقی از چیدمان ارائه دهید و امتیازی بین 0 تا 100 بدهید.
        """
    
    def _create_traffic_prompt(self, store_data: Dict) -> str:
        """ایجاد prompt برای تحلیل ترافیک"""
        return f"""
        تحلیل ترافیک فروشگاه {store_data.get('store_name', '')}:
        
        ترافیک:
        - سطح ترافیک: {store_data.get('customer_traffic', '')}
        - ساعات پیک: {store_data.get('peak_hours', '')}
        - مسیر حرکت: {store_data.get('customer_movement_paths', '')}
        
        دوربین‌ها:
        - تعداد: {store_data.get('camera_count', '')}
        - موقعیت: {store_data.get('camera_locations', '')}
        - پوشش: {store_data.get('camera_coverage', '')}
        
        لطفاً تحلیل دقیقی از الگوهای ترافیک ارائه دهید.
        """
    
    def _create_design_prompt(self, store_data: Dict) -> str:
        """ایجاد prompt برای تحلیل طراحی"""
        return f"""
        تحلیل طراحی فروشگاه {store_data.get('store_name', '')}:
        
        طراحی:
        - سبک: {store_data.get('design_style', '')}
        - رنگ‌ها: {store_data.get('brand_colors', '')}
        - عناصر دکوراتیو: {store_data.get('decorative_elements', '')}
        - نورپردازی: {store_data.get('main_lighting', '')}
        
        لطفاً تحلیل دقیقی از طراحی و دکوراسیون ارائه دهید.
        """
    
    def _create_sales_prompt(self, store_data: Dict) -> str:
        """ایجاد prompt برای تحلیل فروش"""
        return f"""
        تحلیل فروش فروشگاه {store_data.get('store_name', '')}:
        
        فروش:
        - حجم روزانه: {store_data.get('sales_volume', '')}
        - ساعات پیک: {store_data.get('peak_hours', '')}
        - محصولات پرفروش: {store_data.get('top_products', '')}
        
        لطفاً تحلیل دقیقی از بهینه‌سازی فروش ارائه دهید.
        """
    
    def _create_customer_behavior_prompt(self, store_data: Dict) -> str:
        """ایجاد prompt برای تحلیل رفتار مشتری"""
        return f"""
        تحلیل رفتار مشتری فروشگاه {store_data.get('store_name', '')}:
        
        رفتار:
        - مسیر حرکت: {store_data.get('customer_movement_paths', '')}
        - مناطق پرتردد: {store_data.get('high_traffic_areas', '')}
        - توضیحات: {store_data.get('customer_path_notes', '')}
        
        لطفاً تحلیل دقیقی از رفتار مشتری ارائه دهید.
        """
    
    def _create_optimization_prompt(self, store_data: Dict) -> str:
        """ایجاد prompt برای برنامه بهینه‌سازی"""
        return f"""
        برنامه بهینه‌سازی فروشگاه {store_data.get('store_name', '')}:
        
        بر اساس تمام تحلیل‌های انجام شده، یک برنامه جامع و مرحله‌ای برای بهینه‌سازی ارائه دهید.
        برنامه باید شامل:
        1. اولویت‌بندی مشکلات
        2. راه‌حل‌های عملی
        3. زمان‌بندی اجرا
        4. معیارهای موفقیت
        """
    
    async def _analyze_store_image(self, image_file) -> Dict:
        """تحلیل تصویر نقشه فروشگاه"""
        try:
            # تبدیل فایل به تصویر
            image = Image.open(image_file)
            
            # تحلیل اولیه تصویر
            analysis = {
                'size': image.size,
                'format': image.format,
                'mode': image.mode,
                'features': []
            }
            
            # تشخیص عناصر تصویر (در نسخه کامل پیاده‌سازی می‌شود)
            # analysis['features'] = await self._detect_image_features(image)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing store image: {e}")
            return {'error': str(e)}
    
    async def _analyze_customer_video(self, video_file) -> Dict:
        """تحلیل ویدیوی مسیر مشتری"""
        try:
            # تحلیل ویدیو (در نسخه کامل پیاده‌سازی می‌شود)
            analysis = {
                'duration': 0,
                'movement_patterns': [],
                'traffic_density': 0
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing customer video: {e}")
            return {'error': str(e)}
    
    async def _analyze_store_photos(self, photos) -> Dict:
        """تحلیل عکس‌های فروشگاه"""
        try:
            analysis = {
                'total_photos': len(photos),
                'design_elements': [],
                'color_scheme': {},
                'lighting_analysis': {}
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing store photos: {e}")
            return {'error': str(e)}
    
    async def _generate_optimization_map(self, store_data: Dict) -> Dict:
        """تولید نقشه بهینه‌سازی"""
        try:
            # تولید نقشه بهینه‌سازی (در نسخه کامل پیاده‌سازی می‌شود)
            optimization_map = {
                'zones': [],
                'recommendations': [],
                'priority_levels': []
            }
            
            return optimization_map
            
        except Exception as e:
            logger.error(f"Error generating optimization map: {e}")
            return {'error': str(e)}
    
    def _calculate_layout_score(self, store_data: Dict, analysis: str, image_analysis: Dict = None) -> float:
        """محاسبه امتیاز چیدمان"""
        score = 50.0  # امتیاز پایه
        
        # عوامل مثبت
        if store_data.get('shelf_count', 0) > 10:
            score += 10
        if store_data.get('store_size', 0) > 100:
            score += 5
        if store_data.get('unused_area_size', 0) < 20:
            score += 10
        
        # عوامل منفی
        if store_data.get('unused_area_size', 0) > 50:
            score -= 15
        if not store_data.get('checkout_location'):
            score -= 10
        
        return max(0, min(100, score))
    
    def _calculate_traffic_score(self, store_data: Dict, analysis: str, video_analysis: Dict = None) -> float:
        """محاسبه امتیاز ترافیک"""
        score = 50.0
        
        traffic_levels = {'low': 30, 'medium': 60, 'high': 80, 'very_high': 90}
        score += traffic_levels.get(store_data.get('customer_traffic', 'medium'), 50)
        
        if store_data.get('has_surveillance'):
            score += 10
        if store_data.get('has_customer_video'):
            score += 15
        
        return max(0, min(100, score))
    
    def _calculate_design_score(self, store_data: Dict, analysis: str, photo_analysis: Dict = None) -> float:
        """محاسبه امتیاز طراحی"""
        score = 50.0
        
        design_styles = {
            'modern': 80, 'traditional': 60, 'minimal': 70,
            'busy': 40, 'simple': 65, 'bright': 75, 'dim': 45
        }
        score += design_styles.get(store_data.get('design_style', 'simple'), 50)
        
        if store_data.get('brand_colors'):
            score += 10
        if store_data.get('decorative_elements'):
            score += 5
        
        return max(0, min(100, score))
    
    def _calculate_sales_score(self, store_data: Dict, analysis: str) -> float:
        """محاسبه امتیاز فروش"""
        score = 50.0
        
        sales_volume = float(store_data.get('sales_volume', 0))
        if sales_volume > 10000000:  # 10 میلیون تومان
            score += 20
        elif sales_volume > 5000000:  # 5 میلیون تومان
            score += 10
        
        if store_data.get('peak_hours'):
            score += 10
        if store_data.get('top_products'):
            score += 10
        
        return max(0, min(100, score))
    
    def _calculate_customer_behavior_score(self, store_data: Dict, analysis: str) -> float:
        """محاسبه امتیاز رفتار مشتری"""
        score = 50.0
        
        movement_paths = {
            'clockwise': 70, 'counterclockwise': 70, 'mixed': 60, 'random': 40
        }
        score += movement_paths.get(store_data.get('customer_movement_paths', 'mixed'), 50)
        
        if store_data.get('high_traffic_areas'):
            score += 10
        if store_data.get('customer_path_notes'):
            score += 10
        
        return max(0, min(100, score))
    
    def _generate_layout_recommendations(self, store_data: Dict, analysis: str) -> List[str]:
        """تولید توصیه‌های چیدمان"""
        recommendations = []
        
        if store_data.get('unused_area_size', 0) > 30:
            recommendations.append("مناطق بلااستفاده را به فضاهای فروش تبدیل کنید")
        
        if not store_data.get('checkout_location'):
            recommendations.append("محل صندوق‌های پرداخت را بهینه‌سازی کنید")
        
        if store_data.get('shelf_count', 0) < 10:
            recommendations.append("تعداد قفسه‌ها را افزایش دهید")
        
        return recommendations
    
    def _generate_traffic_recommendations(self, store_data: Dict, analysis: str) -> List[str]:
        """تولید توصیه‌های ترافیک"""
        recommendations = []
        
        if store_data.get('customer_traffic') == 'low':
            recommendations.append("استراتژی‌های جذب مشتری را بهبود دهید")
        
        if not store_data.get('has_surveillance'):
            recommendations.append("سیستم دوربین نظارتی نصب کنید")
        
        return recommendations
    
    def _generate_design_recommendations(self, store_data: Dict, analysis: str) -> List[str]:
        """تولید توصیه‌های طراحی"""
        recommendations = []
        
        if store_data.get('design_style') == 'dim':
            recommendations.append("نورپردازی فروشگاه را بهبود دهید")
        
        if not store_data.get('brand_colors'):
            recommendations.append("رنگ‌بندی برند را مشخص کنید")
        
        return recommendations
    
    def _generate_sales_recommendations(self, store_data: Dict, analysis: str) -> List[str]:
        """تولید توصیه‌های فروش"""
        recommendations = []
        
        sales_volume = float(store_data.get('sales_volume', 0))
        if sales_volume < 5000000:
            recommendations.append("استراتژی‌های افزایش فروش را پیاده‌سازی کنید")
        
        return recommendations
    
    def _generate_customer_behavior_recommendations(self, store_data: Dict, analysis: str) -> List[str]:
        """تولید توصیه‌های رفتار مشتری"""
        recommendations = []
        
        if store_data.get('customer_movement_paths') == 'random':
            recommendations.append("مسیر حرکت مشتریان را هدایت کنید")
        
        return recommendations
    
    def _extract_optimization_steps(self, analysis: str) -> List[str]:
        """استخراج مراحل بهینه‌سازی از تحلیل"""
        # در نسخه کامل، این تابع متن تحلیل را پردازش می‌کند
        return [
            "مرحله 1: تحلیل وضعیت فعلی",
            "مرحله 2: شناسایی مشکلات",
            "مرحله 3: طراحی راه‌حل‌ها",
            "مرحله 4: اجرای تغییرات",
            "مرحله 5: ارزیابی نتایج"
        ]
    
    def _extract_layout_metrics(self, store_data: Dict) -> Dict:
        """استخراج متریک‌های چیدمان"""
        return {
            'shelf_efficiency': store_data.get('shelf_count', 0) / max(store_data.get('store_size', 1), 1),
            'unused_area_percentage': (store_data.get('unused_area_size', 0) / max(store_data.get('store_size', 1), 1)) * 100,
            'checkout_accessibility': 1 if store_data.get('checkout_location') else 0
        }
    
    def _extract_traffic_metrics(self, store_data: Dict) -> Dict:
        """استخراج متریک‌های ترافیک"""
        return {
            'traffic_level': store_data.get('customer_traffic', 'medium'),
            'surveillance_coverage': 1 if store_data.get('has_surveillance') else 0,
            'video_analysis_available': 1 if store_data.get('has_customer_video') else 0
        }
    
    def _extract_design_metrics(self, store_data: Dict) -> Dict:
        """استخراج متریک‌های طراحی"""
        return {
            'design_style': store_data.get('design_style', 'simple'),
            'color_scheme': store_data.get('brand_colors', ''),
            'lighting_type': store_data.get('main_lighting', 'artificial')
        }
    
    def _extract_sales_metrics(self, store_data: Dict) -> Dict:
        """استخراج متریک‌های فروش"""
        return {
            'daily_sales': float(store_data.get('sales_volume', 0)),
            'peak_hours': store_data.get('peak_hours', ''),
            'top_products_count': len(store_data.get('top_products', '').split(',')) if store_data.get('top_products') else 0
        }
    
    def _extract_customer_behavior_metrics(self, store_data: Dict) -> Dict:
        """استخراج متریک‌های رفتار مشتری"""
        return {
            'movement_pattern': store_data.get('customer_movement_paths', 'mixed'),
            'high_traffic_areas_count': len(store_data.get('high_traffic_areas', '').split(',')) if store_data.get('high_traffic_areas') else 0,
            'behavior_notes_length': len(store_data.get('customer_path_notes', ''))
        }
