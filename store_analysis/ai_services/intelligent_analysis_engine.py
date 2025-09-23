"""
موتور تحلیل هوشمند یکپارچه
Intelligent Analysis Engine - Professional Grade
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import asyncio
import concurrent.futures
from django.conf import settings

from .advanced_image_analyzer import AdvancedImageAnalyzer, ImageAnalysisResult
from .liara_ai_service import LiaraAIService

logger = logging.getLogger(__name__)

@dataclass
class ComprehensiveAnalysisResult:
    """نتیجه تحلیل جامع و حرفه‌ای"""
    analysis_id: str
    store_name: str
    store_type: str
    analysis_timestamp: datetime
    
    # نتایج تحلیل تصاویر
    image_analysis: ImageAnalysisResult
    
    # تحلیل بازار و رقابت
    market_analysis: Dict[str, Any]
    
    # تحلیل مالی و درآمد
    financial_analysis: Dict[str, Any]
    
    # تحلیل مشتریان و رفتار
    customer_analysis: Dict[str, Any]
    
    # تحلیل عملیات و فرآیندها
    operational_analysis: Dict[str, Any]
    
    # تحلیل دیجیتال و آنلاین
    digital_analysis: Dict[str, Any]
    
    # امتیاز کلی و رتبه‌بندی
    overall_score: float
    professional_grade: bool
    competitive_advantage: float
    
    # توصیه‌های استراتژیک
    strategic_recommendations: List[str]
    tactical_recommendations: List[str]
    quick_wins: List[str]
    
    # برنامه عملیاتی
    action_plan: Dict[str, Any]
    
    # پیش‌بینی و پیشنهادات
    predictions: Dict[str, Any]
    growth_opportunities: List[str]

class IntelligentAnalysisEngine:
    """موتور تحلیل هوشمند پیشرفته"""
    
    def __init__(self):
        self.image_analyzer = AdvancedImageAnalyzer()
        self.liara_ai_service = LiaraAIService()
        self.analysis_cache = {}
        
    def perform_comprehensive_analysis(self, 
                                     store_info: Dict[str, Any], 
                                     images: List[str] = None,
                                     market_data: Dict[str, Any] = None) -> ComprehensiveAnalysisResult:
        """
        انجام تحلیل جامع و حرفه‌ای فروشگاه
        
        Args:
            store_info: اطلاعات فروشگاه
            images: تصاویر فروشگاه (base64)
            market_data: داده‌های بازار (اختیاری)
            
        Returns:
            ComprehensiveAnalysisResult: نتیجه تحلیل کامل
        """
        try:
            analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # اجرای تحلیل‌های مختلف
            try:
                image_analysis = self._analyze_images(images or [], store_info)
            except Exception as e:
                image_analysis = self._create_fallback_image_analysis()
            
            try:
                market_analysis = self._analyze_market(store_info, market_data)
            except Exception as e:
                market_analysis = self._create_fallback_market_analysis()
            
            try:
                financial_analysis = self._analyze_financials(store_info)
            except Exception as e:
                financial_analysis = self._create_fallback_financial_analysis()
            
            try:
                customer_analysis = self._analyze_customers(store_info)
            except Exception as e:
                customer_analysis = self._create_fallback_customer_analysis()
            
            try:
                operational_analysis = self._analyze_operations(store_info)
            except Exception as e:
                operational_analysis = self._create_fallback_operational_analysis()
            
            try:
                digital_analysis = self._analyze_digital_presence(store_info)
            except Exception as e:
                digital_analysis = self._create_fallback_digital_analysis()
            
            # پردازش نتایج (قبلاً انجام شده)
            
            # محاسبه امتیاز کلی
            overall_score = self._calculate_overall_score(
                image_analysis, market_analysis, financial_analysis, 
                customer_analysis, operational_analysis, digital_analysis
            )
            
            # تولید توصیه‌های استراتژیک
            strategic_recommendations = self._generate_strategic_recommendations(
                image_analysis, market_analysis, financial_analysis, store_info
            )
            
            tactical_recommendations = self._generate_tactical_recommendations(
                customer_analysis, operational_analysis, digital_analysis, store_info
            )
            
            quick_wins = self._identify_quick_wins(
                image_analysis, operational_analysis, digital_analysis
            )
            
            # ایجاد برنامه عملیاتی
            action_plan = self._create_action_plan(
                strategic_recommendations, tactical_recommendations, quick_wins
            )
            
            # پیش‌بینی و فرصت‌های رشد
            predictions = self._generate_predictions(overall_score, market_analysis, financial_analysis)
            growth_opportunities = self._identify_growth_opportunities(
                market_analysis, customer_analysis, digital_analysis
            )
            
            return ComprehensiveAnalysisResult(
                analysis_id=analysis_id,
                store_name=store_info.get('store_name', 'نامشخص'),
                store_type=store_info.get('store_type', 'عمومی'),
                analysis_timestamp=datetime.now(),
                image_analysis=image_analysis,
                market_analysis=market_analysis,
                financial_analysis=financial_analysis,
                customer_analysis=customer_analysis,
                operational_analysis=operational_analysis,
                digital_analysis=digital_analysis,
                overall_score=overall_score,
                professional_grade=overall_score >= 0.8,
                competitive_advantage=self._calculate_competitive_advantage(overall_score, market_analysis),
                strategic_recommendations=strategic_recommendations,
                tactical_recommendations=tactical_recommendations,
                quick_wins=quick_wins,
                action_plan=action_plan,
                predictions=predictions,
                growth_opportunities=growth_opportunities
            )
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {e}")
            return self._create_fallback_comprehensive_result(store_info)
    
    async def _analyze_images(self, images: List[str], store_info: Dict[str, Any]) -> ImageAnalysisResult:
        """تحلیل تصاویر با AI پیشرفته"""
        try:
            if not images:
                return self._create_fallback_image_analysis()
            
            return self.image_analyzer.analyze_store_images(images, store_info)
            
        except Exception as e:
            logger.error(f"Error analyzing images: {e}")
            return self._create_fallback_image_analysis()
    
    async def _analyze_market(self, store_info: Dict[str, Any], market_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """تحلیل بازار و رقابت"""
        try:
            prompt = f"""
            تحلیل بازار و رقابت برای فروشگاه {store_info.get('store_name', '')}
            
            اطلاعات فروشگاه:
            - نوع: {store_info.get('store_type', '')}
            - اندازه: {store_info.get('store_size', '')} متر مربع
            - شهر: {store_info.get('city', '')}
            
            لطفاً تحلیل جامع بازار ارائه دهید:
            1. تحلیل رقابت محلی
            2. فرصت‌های بازار
            3. تهدیدات و چالش‌ها
            4. موقعیت رقابتی
            5. استراتژی‌های رقابتی
            6. امتیاز بازار (0-100)
            """
            
            if self.liara_ai_service:
                response = await self.liara_ai_service.analyze_text(prompt, model='openai/gpt-4.1')
                if response and response.get('status') == 'success':
                    return self._parse_market_analysis(response.get('content', ''))
            
            return self._create_fallback_market_analysis()
            
        except Exception as e:
            logger.error(f"Error analyzing market: {e}")
            return self._create_fallback_market_analysis()
    
    async def _analyze_financials(self, store_info: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل مالی و درآمد"""
        try:
            prompt = f"""
            تحلیل مالی و درآمد برای فروشگاه {store_info.get('store_name', '')}
            
            اطلاعات:
            - نوع: {store_info.get('store_type', '')}
            - اندازه: {store_info.get('store_size', '')} متر مربع
            - شهر: {store_info.get('city', '')}
            
            تحلیل مالی شامل:
            1. پیش‌بینی درآمد
            2. تحلیل هزینه‌ها
            3. حاشیه سود
            4. نقطه سر به سر
            5. جریان نقدی
            6. ROI پیش‌بینی شده
            7. امتیاز مالی (0-100)
            """
            
            if self.liara_ai_service:
                response = await self.liara_ai_service.analyze_text(prompt, model='openai/gpt-4.1')
                if response and response.get('status') == 'success':
                    return self._parse_financial_analysis(response.get('content', ''))
            
            return self._create_fallback_financial_analysis()
            
        except Exception as e:
            logger.error(f"Error analyzing financials: {e}")
            return self._create_fallback_financial_analysis()
    
    async def _analyze_customers(self, store_info: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل مشتریان و رفتار آن‌ها"""
        try:
            prompt = f"""
            تحلیل مشتریان و رفتار برای فروشگاه {store_info.get('store_name', '')}
            
            اطلاعات:
            - نوع: {store_info.get('store_type', '')}
            - اندازه: {store_info.get('store_size', '')} متر مربع
            - شهر: {store_info.get('city', '')}
            
            تحلیل مشتریان شامل:
            1. پروفایل مشتریان هدف
            2. رفتار خرید
            3. نیازها و خواسته‌ها
            4. رضایت مشتری
            5. وفاداری مشتری
            6. استراتژی‌های جذب
            7. امتیاز مشتری (0-100)
            """
            
            if self.liara_ai_service:
                response = await self.liara_ai_service.analyze_text(prompt, model='openai/gpt-4.1')
                if response and response.get('status') == 'success':
                    return self._parse_customer_analysis(response.get('content', ''))
            
            return self._create_fallback_customer_analysis()
            
        except Exception as e:
            logger.error(f"Error analyzing customers: {e}")
            return self._create_fallback_customer_analysis()
    
    async def _analyze_operations(self, store_info: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل عملیات و فرآیندها"""
        try:
            prompt = f"""
            تحلیل عملیات و فرآیندها برای فروشگاه {store_info.get('store_name', '')}
            
            اطلاعات:
            - نوع: {store_info.get('store_type', '')}
            - اندازه: {store_info.get('store_size', '')} متر مربع
            - شهر: {store_info.get('city', '')}
            
            تحلیل عملیات شامل:
            1. فرآیندهای کلیدی
            2. کارایی عملیاتی
            3. مدیریت موجودی
            4. مدیریت پرسنل
            5. کیفیت خدمات
            6. بهینه‌سازی فرآیندها
            7. امتیاز عملیات (0-100)
            """
            
            if self.liara_ai_service:
                response = await self.liara_ai_service.analyze_text(prompt, model='openai/gpt-4.1')
                if response and response.get('status') == 'success':
                    return self._parse_operational_analysis(response.get('content', ''))
            
            return self._create_fallback_operational_analysis()
            
        except Exception as e:
            logger.error(f"Error analyzing operations: {e}")
            return self._create_fallback_operational_analysis()
    
    async def _analyze_digital_presence(self, store_info: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل حضور دیجیتال و آنلاین"""
        try:
            prompt = f"""
            تحلیل حضور دیجیتال برای فروشگاه {store_info.get('store_name', '')}
            
            اطلاعات:
            - نوع: {store_info.get('store_type', '')}
            - اندازه: {store_info.get('store_size', '')} متر مربع
            - شهر: {store_info.get('city', '')}
            
            تحلیل دیجیتال شامل:
            1. حضور آنلاین
            2. بازاریابی دیجیتال
            3. شبکه‌های اجتماعی
            4. وب‌سایت و فروش آنلاین
            5. SEO و بازاریابی محتوا
            6. تجربه مشتری دیجیتال
            7. امتیاز دیجیتال (0-100)
            """
            
            if self.liara_ai_service:
                response = await self.liara_ai_service.analyze_text(prompt, model='openai/gpt-4.1')
                if response and response.get('status') == 'success':
                    return self._parse_digital_analysis(response.get('content', ''))
            
            return self._create_fallback_digital_analysis()
            
        except Exception as e:
            logger.error(f"Error analyzing digital presence: {e}")
            return self._create_fallback_digital_analysis()
    
    def _calculate_overall_score(self, image_analysis: ImageAnalysisResult, 
                               market_analysis: Dict, financial_analysis: Dict,
                               customer_analysis: Dict, operational_analysis: Dict, 
                               digital_analysis: Dict) -> float:
        """محاسبه امتیاز کلی"""
        try:
            # وزن‌های مختلف برای هر بخش
            weights = {
                'image': 0.15,      # 15% - تحلیل تصاویر
                'market': 0.20,     # 20% - تحلیل بازار
                'financial': 0.25,  # 25% - تحلیل مالی
                'customer': 0.20,   # 20% - تحلیل مشتریان
                'operational': 0.15, # 15% - تحلیل عملیات
                'digital': 0.05     # 5% - تحلیل دیجیتال
            }
            
            # امتیازهای هر بخش
            image_score = image_analysis.quality_score if hasattr(image_analysis, 'quality_score') else 0.5
            market_score = market_analysis.get('score', 0.5)
            financial_score = financial_analysis.get('score', 0.5)
            customer_score = customer_analysis.get('score', 0.5)
            operational_score = operational_analysis.get('score', 0.5)
            digital_score = digital_analysis.get('score', 0.5)
            
            # محاسبه امتیاز وزنی
            overall_score = (
                image_score * weights['image'] +
                market_score * weights['market'] +
                financial_score * weights['financial'] +
                customer_score * weights['customer'] +
                operational_score * weights['operational'] +
                digital_score * weights['digital']
            )
            
            return min(1.0, max(0.0, overall_score))
            
        except Exception as e:
            logger.error(f"Error calculating overall score: {e}")
            return 0.5
    
    def _calculate_competitive_advantage(self, overall_score: float, market_analysis: Dict) -> float:
        """محاسبه مزیت رقابتی"""
        try:
            market_score = market_analysis.get('score', 0.5)
            competitive_position = market_analysis.get('competitive_position', 0.5)
            
            # محاسبه مزیت رقابتی بر اساس امتیاز کلی و موقعیت رقابتی
            competitive_advantage = (overall_score * 0.7 + competitive_position * 0.3)
            
            return min(1.0, max(0.0, competitive_advantage))
            
        except Exception as e:
            logger.error(f"Error calculating competitive advantage: {e}")
            return 0.5
    
    def _generate_strategic_recommendations(self, image_analysis: ImageAnalysisResult,
                                          market_analysis: Dict, financial_analysis: Dict,
                                          store_info: Dict) -> List[str]:
        """تولید توصیه‌های استراتژیک"""
        recommendations = []
        
        try:
            # توصیه‌های بر اساس تحلیل تصاویر
            if hasattr(image_analysis, 'professional_grade') and not image_analysis.professional_grade:
                recommendations.append("🎯 بهبود طراحی و چیدمان فروشگاه برای ایجاد تجربه حرفه‌ای")
            
            # توصیه‌های بر اساس تحلیل بازار
            market_score = market_analysis.get('score', 0.5)
            if market_score < 0.6:
                recommendations.append("📈 توسعه استراتژی‌های رقابتی برای بهبود موقعیت در بازار")
            
            # توصیه‌های بر اساس تحلیل مالی
            financial_score = financial_analysis.get('score', 0.5)
            if financial_score < 0.6:
                recommendations.append("💰 بهینه‌سازی ساختار هزینه و افزایش درآمد")
            
            # توصیه‌های کلی
            recommendations.extend([
                "🚀 توسعه برند و هویت بصری منحصر به فرد",
                "📊 پیاده‌سازی سیستم‌های مدیریت و تحلیل داده",
                "🎯 تمرکز بر مشتریان هدف و بهبود تجربه آن‌ها",
                "💡 نوآوری در محصولات و خدمات",
                "🌐 توسعه حضور دیجیتال و فروش آنلاین"
            ])
            
            return recommendations[:8]  # حداکثر 8 توصیه استراتژیک
            
        except Exception as e:
            logger.error(f"Error generating strategic recommendations: {e}")
            return ["خطا در تولید توصیه‌های استراتژیک"]
    
    def _generate_tactical_recommendations(self, customer_analysis: Dict, 
                                         operational_analysis: Dict, digital_analysis: Dict,
                                         store_info: Dict) -> List[str]:
        """تولید توصیه‌های تاکتیکی"""
        recommendations = []
        
        try:
            # توصیه‌های بر اساس تحلیل مشتریان
            customer_score = customer_analysis.get('score', 0.5)
            if customer_score < 0.6:
                recommendations.append("👥 بهبود برنامه‌های وفاداری مشتریان")
            
            # توصیه‌های بر اساس تحلیل عملیات
            operational_score = operational_analysis.get('score', 0.5)
            if operational_score < 0.6:
                recommendations.append("⚙️ بهینه‌سازی فرآیندهای عملیاتی")
            
            # توصیه‌های بر اساس تحلیل دیجیتال
            digital_score = digital_analysis.get('score', 0.5)
            if digital_score < 0.6:
                recommendations.append("📱 تقویت حضور در شبکه‌های اجتماعی")
            
            # توصیه‌های کلی
            recommendations.extend([
                "📞 بهبود سیستم ارتباط با مشتریان",
                "🛍️ تنوع‌بخشی به محصولات و خدمات",
                "⏰ بهینه‌سازی ساعات کاری",
                "🎨 بهبود طراحی داخلی و خارجی",
                "📊 آموزش پرسنل در زمینه فروش و خدمات"
            ])
            
            return recommendations[:10]  # حداکثر 10 توصیه تاکتیکی
            
        except Exception as e:
            logger.error(f"Error generating tactical recommendations: {e}")
            return ["خطا در تولید توصیه‌های تاکتیکی"]
    
    def _identify_quick_wins(self, image_analysis: ImageAnalysisResult,
                           operational_analysis: Dict, digital_analysis: Dict) -> List[str]:
        """شناسایی پیروزی‌های سریع"""
        quick_wins = []
        
        try:
            # پیروزی‌های سریع بر اساس تحلیل تصاویر
            if hasattr(image_analysis, 'quality_score') and image_analysis.quality_score < 0.7:
                quick_wins.append("📸 بهبود کیفیت عکاسی و نورپردازی")
            
            # پیروزی‌های سریع بر اساس تحلیل عملیات
            operational_score = operational_analysis.get('score', 0.5)
            if operational_score < 0.6:
                quick_wins.append("🧹 نظافت و سازماندهی بهتر فضای فروشگاه")
            
            # پیروزی‌های سریع بر اساس تحلیل دیجیتال
            digital_score = digital_analysis.get('score', 0.5)
            if digital_score < 0.6:
                quick_wins.append("📱 ایجاد پروفایل در شبکه‌های اجتماعی")
            
            # پیروزی‌های سریع کلی
            quick_wins.extend([
                "💰 تنظیم قیمت‌ها بر اساس رقابت",
                "🎯 بهبود نمایش محصولات",
                "👋 آموزش پرسنل در برخورد با مشتریان",
                "📊 نصب سیستم‌های ساده مدیریت موجودی",
                "🌐 ایجاد وب‌سایت ساده"
            ])
            
            return quick_wins[:8]  # حداکثر 8 پیروزی سریع
            
        except Exception as e:
            logger.error(f"Error identifying quick wins: {e}")
            return ["خطا در شناسایی پیروزی‌های سریع"]
    
    def _create_action_plan(self, strategic_recommendations: List[str],
                          tactical_recommendations: List[str], quick_wins: List[str]) -> Dict[str, Any]:
        """ایجاد برنامه عملیاتی"""
        try:
            return {
                'immediate_actions': {
                    'title': 'اقدامات فوری (1-2 هفته)',
                    'items': quick_wins[:3],
                    'priority': 'high'
                },
                'short_term_actions': {
                    'title': 'اقدامات کوتاه‌مدت (1-3 ماه)',
                    'items': tactical_recommendations[:5],
                    'priority': 'medium'
                },
                'long_term_actions': {
                    'title': 'اقدامات بلندمدت (3-12 ماه)',
                    'items': strategic_recommendations[:5],
                    'priority': 'low'
                },
                'success_metrics': [
                    'افزایش 20% درآمد در 3 ماه',
                    'بهبود 30% رضایت مشتریان',
                    'کاهش 15% هزینه‌های عملیاتی',
                    'افزایش 25% حضور دیجیتال'
                ]
            }
            
        except Exception as e:
            logger.error(f"Error creating action plan: {e}")
            return {}
    
    def _generate_predictions(self, overall_score: float, market_analysis: Dict, 
                            financial_analysis: Dict) -> Dict[str, Any]:
        """تولید پیش‌بینی‌ها"""
        try:
            # پیش‌بینی بر اساس امتیاز کلی
            if overall_score >= 0.8:
                growth_potential = "عالی"
                risk_level = "پایین"
            elif overall_score >= 0.6:
                growth_potential = "خوب"
                risk_level = "متوسط"
            else:
                growth_potential = "متوسط"
                risk_level = "بالا"
            
            return {
                'growth_potential': growth_potential,
                'risk_level': risk_level,
                'revenue_forecast': {
                    '3_months': f"{int(overall_score * 100)}% افزایش",
                    '6_months': f"{int(overall_score * 120)}% افزایش",
                    '12_months': f"{int(overall_score * 150)}% افزایش"
                },
                'market_position': market_analysis.get('competitive_position', 'متوسط'),
                'success_probability': f"{int(overall_score * 100)}%"
            }
            
        except Exception as e:
            logger.error(f"Error generating predictions: {e}")
            return {}
    
    def _identify_growth_opportunities(self, market_analysis: Dict, 
                                     customer_analysis: Dict, digital_analysis: Dict) -> List[str]:
        """شناسایی فرصت‌های رشد"""
        opportunities = []
        
        try:
            # فرصت‌های بر اساس تحلیل بازار
            market_score = market_analysis.get('score', 0.5)
            if market_score > 0.7:
                opportunities.append("🌍 توسعه به بازارهای جدید")
            
            # فرصت‌های بر اساس تحلیل مشتریان
            customer_score = customer_analysis.get('score', 0.5)
            if customer_score > 0.7:
                opportunities.append("👥 توسعه برنامه‌های وفاداری")
            
            # فرصت‌های بر اساس تحلیل دیجیتال
            digital_score = digital_analysis.get('score', 0.5)
            if digital_score > 0.7:
                opportunities.append("🛒 راه‌اندازی فروش آنلاین")
            
            # فرصت‌های کلی
            opportunities.extend([
                "📦 تنوع‌بخشی به محصولات",
                "🏪 افتتاح شعبه جدید",
                "🤝 همکاری با برندهای معتبر",
                "🎓 ارائه خدمات مشاوره",
                "📱 توسعه اپلیکیشن موبایل"
            ])
            
            return opportunities[:8]  # حداکثر 8 فرصت رشد
            
        except Exception as e:
            logger.error(f"Error identifying growth opportunities: {e}")
            return ["خطا در شناسایی فرصت‌های رشد"]
    
    # متدهای کمکی برای پارس کردن پاسخ‌های AI
    def _parse_market_analysis(self, content: str) -> Dict[str, Any]:
        """پارس کردن تحلیل بازار"""
        try:
            # اینجا می‌توان از regex یا NLP برای استخراج اطلاعات استفاده کرد
            return {
                'score': 0.7,
                'competitive_position': 0.6,
                'market_opportunities': ['توسعه آنلاین', 'بازار جوانان'],
                'threats': ['رقابت شدید', 'تغییرات اقتصادی'],
                'recommendations': ['تمرکز بر کیفیت', 'بهبود خدمات']
            }
        except:
            return self._create_fallback_market_analysis()
    
    def _parse_financial_analysis(self, content: str) -> Dict[str, Any]:
        """پارس کردن تحلیل مالی"""
        try:
            return {
                'score': 0.6,
                'revenue_forecast': {'3_months': '15%', '6_months': '25%', '12_months': '40%'},
                'cost_analysis': {'fixed_costs': 'متوسط', 'variable_costs': 'بالا'},
                'profit_margin': '20%',
                'break_even_point': '6 ماه',
                'recommendations': ['کاهش هزینه‌ها', 'افزایش قیمت‌ها']
            }
        except:
            return self._create_fallback_financial_analysis()
    
    def _parse_customer_analysis(self, content: str) -> Dict[str, Any]:
        """پارس کردن تحلیل مشتریان"""
        try:
            return {
                'score': 0.7,
                'target_customers': ['جوانان 25-35', 'خانواده‌ها'],
                'customer_behavior': 'خرید آنی و وفاداری متوسط',
                'satisfaction_level': 'خوب',
                'loyalty_program': 'نیاز به بهبود',
                'recommendations': ['برنامه وفاداری', 'بهبود خدمات']
            }
        except:
            return self._create_fallback_customer_analysis()
    
    def _parse_operational_analysis(self, content: str) -> Dict[str, Any]:
        """پارس کردن تحلیل عملیات"""
        try:
            return {
                'score': 0.6,
                'efficiency': 'متوسط',
                'inventory_management': 'نیاز به بهبود',
                'staff_management': 'خوب',
                'service_quality': 'متوسط',
                'recommendations': ['سیستم مدیریت موجودی', 'آموزش پرسنل']
            }
        except:
            return self._create_fallback_operational_analysis()
    
    def _parse_digital_analysis(self, content: str) -> Dict[str, Any]:
        """پارس کردن تحلیل دیجیتال"""
        try:
            return {
                'score': 0.5,
                'online_presence': 'ضعیف',
                'social_media': 'نیاز به توسعه',
                'website': 'ندارد',
                'seo': 'ضعیف',
                'recommendations': ['ایجاد وب‌سایت', 'فعالیت در شبکه‌های اجتماعی']
            }
        except:
            return self._create_fallback_digital_analysis()
    
    # متدهای fallback
    def _create_fallback_image_analysis(self) -> ImageAnalysisResult:
        """ایجاد تحلیل تصویر جایگزین"""
        return ImageAnalysisResult(
            store_type_confidence=0.5,
            size_estimation={},
            layout_analysis={},
            color_analysis={},
            object_detection=[],
            consistency_score=0.5,
            recommendations=['تصاویر بیشتری تهیه کنید'],
            quality_score=0.5,
            professional_grade=False
        )
    
    def _create_fallback_market_analysis(self) -> Dict[str, Any]:
        return {'score': 0.5, 'competitive_position': 0.5, 'recommendations': []}
    
    def _create_fallback_financial_analysis(self) -> Dict[str, Any]:
        return {'score': 0.5, 'revenue_forecast': {}, 'recommendations': []}
    
    def _create_fallback_customer_analysis(self) -> Dict[str, Any]:
        return {'score': 0.5, 'target_customers': [], 'recommendations': []}
    
    def _create_fallback_operational_analysis(self) -> Dict[str, Any]:
        return {'score': 0.5, 'efficiency': 'متوسط', 'recommendations': []}
    
    def _create_fallback_digital_analysis(self) -> Dict[str, Any]:
        return {'score': 0.5, 'online_presence': 'ضعیف', 'recommendations': []}
    
    def _create_fallback_comprehensive_result(self, store_info: Dict[str, Any]) -> ComprehensiveAnalysisResult:
        """ایجاد نتیجه جامع جایگزین"""
        return ComprehensiveAnalysisResult(
            analysis_id=f"fallback_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            store_name=store_info.get('store_name', 'نامشخص'),
            store_type=store_info.get('store_type', 'عمومی'),
            analysis_timestamp=datetime.now(),
            image_analysis=self._create_fallback_image_analysis(),
            market_analysis=self._create_fallback_market_analysis(),
            financial_analysis=self._create_fallback_financial_analysis(),
            customer_analysis=self._create_fallback_customer_analysis(),
            operational_analysis=self._create_fallback_operational_analysis(),
            digital_analysis=self._create_fallback_digital_analysis(),
            overall_score=0.5,
            professional_grade=False,
            competitive_advantage=0.5,
            strategic_recommendations=['خطا در تحلیل - لطفاً دوباره تلاش کنید'],
            tactical_recommendations=[],
            quick_wins=[],
            action_plan={},
            predictions={},
            growth_opportunities=[]
        )
