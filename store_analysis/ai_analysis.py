#!/usr/bin/env python
"""
سیستم تحلیل هوشمند فروشگاه
تولید تحلیل تفصیلی و راهنمایی‌های عملی با استفاده از AI
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import openai
from django.conf import settings
from django.core.cache import cache

# Import ML libraries
try:
    import numpy as np
    ML_AVAILABLE = True
    PANDAS_AVAILABLE = False
    SKLEARN_AVAILABLE = False
    TENSORFLOW_AVAILABLE = False
    
    # Skip problematic libraries for now
    try:
        # Skip pandas due to compatibility issues
        # import pandas as pd
        # PANDAS_AVAILABLE = True
        pass
    except Exception:
        pass
        
    try:
        # Skip sklearn for now
        # from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
        # SKLEARN_AVAILABLE = True
        pass
    except Exception:
        pass
        
    try:
        # Skip tensorflow for now
        # import tensorflow as tf
        # TENSORFLOW_AVAILABLE = True
        pass
    except Exception:
        pass
        
except ImportError:
    # Create a dummy numpy for when it's not available
    class DummyNumpy:
        def array(self, data):
            return data
        def ndarray(self, *args, **kwargs):
            return []
    
    np = DummyNumpy()
    ML_AVAILABLE = False
    PANDAS_AVAILABLE = False
    SKLEARN_AVAILABLE = False
    TENSORFLOW_AVAILABLE = False
    logging.warning("ML libraries not available. Advanced analysis will be disabled.")

logger = logging.getLogger(__name__)

class StoreAnalysisAI:
    """کلاس تحلیل هوشمند فروشگاه"""
    
    def __init__(self):
        self.openai_client = None
        if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            self.openai_client = openai
        
        # Initialize ML models
        self.ml_models = {}
        if ML_AVAILABLE and SKLEARN_AVAILABLE:
            self._initialize_ml_models()
    
    def _initialize_ml_models(self):
        """راه‌اندازی مدل‌های ML"""
        try:
            if SKLEARN_AVAILABLE:
                from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
                
                # Sales prediction model
                self.ml_models['sales_predictor'] = RandomForestRegressor(
                    n_estimators=100,
                    random_state=42
                )
                
                # Conversion rate predictor
                self.ml_models['conversion_predictor'] = RandomForestRegressor(
                    n_estimators=100,
                    random_state=42
                )
                
                # Customer behavior classifier
                self.ml_models['behavior_classifier'] = RandomForestClassifier(
                    n_estimators=100,
                    random_state=42
                )
            
            # Neural network for complex patterns
            self.ml_models['neural_network'] = self._create_neural_network()
            
            logger.info("ML models initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing ML models: {e}")
            global ML_AVAILABLE
            ML_AVAILABLE = False
    
    def _create_neural_network(self):
        """ایجاد شبکه عصبی برای تحلیل پیچیده"""
        if not TENSORFLOW_AVAILABLE:
            return None
            
        try:
            from tensorflow import keras
            
            model = keras.Sequential([
                keras.layers.Dense(64, activation='relu', input_shape=(20,)),
                keras.layers.Dropout(0.2),
                keras.layers.Dense(32, activation='relu'),
                keras.layers.Dropout(0.2),
                keras.layers.Dense(16, activation='relu'),
                keras.layers.Dense(1, activation='linear')
            ])
            
            model.compile(
                optimizer='adam',
                loss='mse',
                metrics=['mae']
            )
            
            return model
            
        except Exception as e:
            logger.error(f"Error creating neural network: {e}")
            return None
    
    def generate_detailed_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """تولید تحلیل تفصیلی با استفاده از AI"""
        try:
            # اگر OpenAI در دسترس نباشد، از تحلیل محلی استفاده می‌کنیم
            if not self.openai_client:
                return self._generate_local_analysis(analysis_data)
            
            # تولید تحلیل با OpenAI
            return self._generate_openai_analysis(analysis_data)
            
        except Exception as e:
            logger.error(f"خطا در تولید تحلیل AI: {e}")
            return self._generate_local_analysis(analysis_data)
    
    def generate_advanced_ml_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """تولید تحلیل پیشرفته با استفاده از ML"""
        if not ML_AVAILABLE:
            return {"error": "ML libraries not available"}
        
        try:
            # تبدیل داده‌ها به فرمت مناسب برای ML
            features = self._extract_ml_features(analysis_data)
            
            # پیش‌بینی‌های مختلف
            predictions = {
                "sales_prediction": self._predict_sales(features),
                "conversion_optimization": self._predict_conversion_improvement(features),
                "customer_behavior": self._analyze_customer_behavior(features),
                "optimization_priority": self._get_optimization_priority(features),
                "roi_prediction": self._predict_roi(features)
            }
            
            # تحلیل الگوها
            pattern_analysis = self._analyze_patterns(features)
            
            # پیشنهادات مبتنی بر ML
            ml_recommendations = self._generate_ml_recommendations(features, predictions)
            
            return {
                "ml_predictions": predictions,
                "pattern_analysis": pattern_analysis,
                "ml_recommendations": ml_recommendations,
                "confidence_scores": self._calculate_confidence_scores(features),
                "generated_at": datetime.now().isoformat(),
                "analysis_type": "advanced_ml"
            }
            
        except Exception as e:
            logger.error(f"Error in ML analysis: {e}")
            return {"error": f"ML analysis failed: {str(e)}"}
    
    def _extract_ml_features(self, analysis_data: Dict[str, Any]):
        """استخراج ویژگی‌های ML از داده‌ها"""
        features = []
        
        # تبدیل داده‌ها به اعداد
        def safe_float(value, default=0.0):
            try:
                if isinstance(value, str):
                    return float(value)
                return float(value) if value is not None else default
            except (ValueError, TypeError):
                return default
        
        # ویژگی‌های عددی
        features.extend([
            safe_float(analysis_data.get('store_size', 500)),
            safe_float(analysis_data.get('entrance_count', 2)),
            safe_float(analysis_data.get('checkout_count', 3)),
            safe_float(analysis_data.get('shelf_count', 25)),
            safe_float(analysis_data.get('conversion_rate', 35.5)),
            safe_float(analysis_data.get('customer_traffic', 150)),
            safe_float(analysis_data.get('customer_dwell_time', 45)),
            safe_float(analysis_data.get('unused_area_size', 0)),
            safe_float(analysis_data.get('daily_sales_volume', 0)),
            safe_float(analysis_data.get('supplier_count', 0)),
            safe_float(analysis_data.get('camera_count', 0)),
            safe_float(analysis_data.get('morning_sales_percent', 30)),
            safe_float(analysis_data.get('noon_sales_percent', 40)),
            safe_float(analysis_data.get('evening_sales_percent', 30)),
            safe_float(analysis_data.get('sales_improvement_target', 20)),
            safe_float(analysis_data.get('optimization_timeline', 6)),
            safe_float(analysis_data.get('historical_data_months', 12)),
        ])
        
        # اضافه کردن ویژگی‌های لیستی با بررسی نوع داده
        product_categories = analysis_data.get('product_categories', [])
        if isinstance(product_categories, list):
            features.append(len(product_categories))
        elif isinstance(product_categories, str):
            features.append(1)  # اگر رشته باشد، یک دسته‌بندی در نظر می‌گیریم
        else:
            features.append(0)
        
        peak_days = analysis_data.get('peak_days', [])
        if isinstance(peak_days, list):
            features.append(len(peak_days))
        elif isinstance(peak_days, str):
            features.append(1)  # اگر رشته باشد، یک روز اوج در نظر می‌گیریم
        else:
            features.append(0)
        
        return np.array(features).reshape(1, -1)
    
    def _predict_sales(self, features) -> Dict[str, Any]:
        """پیش‌بینی فروش با ML"""
        try:
            # اینجا باید مدل آموزش دیده باشد
            # برای نمونه، از یک الگوریتم ساده استفاده می‌کنیم
            store_size = float(features[0, 0])
            conversion_rate = float(features[0, 4])
            customer_traffic = float(features[0, 5])
            
            # محاسبه فروش پیش‌بینی شده
            predicted_sales = customer_traffic * (conversion_rate / 100) * 1000  # متوسط خرید 1000 تومان
            
            # محاسبه پتانسیل بهبود
            improvement_potential = min(50, (50 - conversion_rate) * 2)
            
            return {
                "current_daily_sales": predicted_sales,
                "potential_daily_sales": predicted_sales * (1 + improvement_potential / 100),
                "improvement_potential": improvement_potential,
                "confidence": 0.85
            }
            
        except Exception as e:
            logger.error(f"Error in sales prediction: {e}")
            return {"error": str(e)}
    
    def _predict_conversion_improvement(self, features) -> Dict[str, Any]:
        """پیش‌بینی بهبود نرخ تبدیل"""
        try:
            current_conversion = float(features[0, 4])
            store_size = float(features[0, 0])
            unused_area = float(features[0, 7])
            
            # عوامل بهبود
            layout_improvement = min(15, (store_size - unused_area) / store_size * 20)
            checkout_improvement = min(10, float(features[0, 2]) * 2)  # بر اساس تعداد صندوق‌ها
            lighting_improvement = 5  # بهبود نورپردازی
            
            total_improvement = layout_improvement + checkout_improvement + lighting_improvement
            
            return {
                "current_conversion_rate": current_conversion,
                "predicted_improvement": total_improvement,
                "new_conversion_rate": min(100, current_conversion + total_improvement),
                "factors": {
                    "layout": layout_improvement,
                    "checkout": checkout_improvement,
                    "lighting": lighting_improvement
                },
                "confidence": 0.80
            }
            
        except Exception as e:
            logger.error(f"Error in conversion prediction: {e}")
            return {"error": str(e)}
    
    def _analyze_customer_behavior(self, features) -> Dict[str, Any]:
        """تحلیل رفتار مشتری"""
        try:
            dwell_time = float(features[0, 6])
            traffic = float(features[0, 5])
            conversion = float(features[0, 4])
            
            # طبقه‌بندی رفتار
            if dwell_time > 60 and conversion > 40:
                behavior_type = "high_engagement"
                description = "مشتریان با تعامل بالا و نرخ تبدیل خوب"
            elif dwell_time > 30 and conversion > 30:
                behavior_type = "moderate_engagement"
                description = "مشتریان با تعامل متوسط"
            else:
                behavior_type = "low_engagement"
                description = "نیاز به بهبود تعامل مشتری"
            
            return {
                "behavior_type": behavior_type,
                "description": description,
                "engagement_score": min(100, (dwell_time / 60) * 50 + (conversion / 50) * 50),
                "recommendations": self._get_behavior_recommendations(behavior_type),
                "practical_guide": self._generate_practical_recommendations(features)
            }
            
        except Exception as e:
            logger.error(f"Error in behavior analysis: {e}")
            return {"error": str(e)}
    
    def _get_behavior_recommendations(self, behavior_type: str) -> List[str]:
        """پیشنهادات بر اساس نوع رفتار"""
        recommendations = {
            "high_engagement": [
                "حفظ کیفیت خدمات",
                "افزایش تنوع محصولات",
                "برنامه‌های وفاداری"
            ],
            "moderate_engagement": [
                "بهبود چیدمان",
                "افزایش تعامل",
                "بهینه‌سازی مسیرها"
            ],
            "low_engagement": [
                "بازطراحی کامل",
                "آموزش کارکنان",
                "بهبود تجربه مشتری"
            ]
        }
        return recommendations.get(behavior_type, [])
    
    def _generate_practical_recommendations(self, features) -> Dict[str, Any]:
        """تولید راهنمایی‌های عملی چیدمان"""
        try:
            store_size = float(features[0, 0])
            entrance_count = float(features[0, 1])
            checkout_count = float(features[0, 2])
            shelf_count = float(features[0, 3])
            conversion_rate = float(features[0, 4])
            customer_traffic = float(features[0, 5])
            unused_area = float(features[0, 7])
            
            practical_guide = {
                "window_display": self._get_window_display_guide(store_size, conversion_rate),
                "shelf_layout": self._get_shelf_layout_guide(shelf_count, store_size),
                "path_design": self._get_path_design_guide(store_size, customer_traffic),
                "lighting": self._get_lighting_guide(store_size, conversion_rate),
                "color_scheme": self._get_color_scheme_guide(conversion_rate),
                "product_placement": self._get_product_placement_guide(shelf_count, conversion_rate)
            }
            
            return practical_guide
            
        except Exception as e:
            logger.error(f"Error generating practical recommendations: {e}")
            return {"error": str(e)}
    
    def _get_window_display_guide(self, store_size: float, conversion_rate: float) -> Dict[str, Any]:
        """راهنمای طراحی ویترین"""
        height = "1.2-1.8 متر" if store_size > 200 else "1.0-1.6 متر"
        lighting = "LED 3000K" if conversion_rate < 40 else "LED 4000K"
        
        return {
            "height": height,
            "lighting": lighting,
            "color_rule": "قانون 60-30-10",
            "product_count": "3-5 محصول اصلی",
            "rotation_frequency": "هفتگی",
            "tips": [
                "محصولات پرفروش در مرکز ویترین",
                "استفاده از پس‌زمینه ساده",
                "نورپردازی یکنواخت",
                "تغییر منظم محتوا"
            ]
        }
    
    def _get_shelf_layout_guide(self, shelf_count: float, store_size: float) -> Dict[str, Any]:
        """راهنمای چیدمان قفسه‌ها"""
        shelf_height = "0.3-2.1 متر"
        aisle_width = "1.2-1.8 متر" if store_size > 300 else "1.0-1.5 متر"
        
        return {
            "shelf_heights": {
                "bottom": "0.3-0.6 متر",
                "middle": "0.6-1.5 متر",
                "top": "1.5-2.1 متر"
            },
            "aisle_width": aisle_width,
            "product_arrangement": "محصولات پرفروش در سطح چشم (1.5 متر)",
            "spacing": "فاصله 15-20 سانتی‌متر بین محصولات",
            "tips": [
                "اجتناب از بن‌بست",
                "دسترسی آسان به همه محصولات",
                "استفاده از تابلوهای راهنما",
                "نظم و ترتیب منظم"
            ]
        }
    
    def _get_path_design_guide(self, store_size: float, customer_traffic: float) -> Dict[str, Any]:
        """راهنمای طراحی مسیر"""
        main_path_width = "2.4-3.0 متر" if customer_traffic > 100 else "2.0-2.4 متر"
        secondary_path_width = "1.8-2.4 متر"
        
        return {
            "main_path": {
                "width": main_path_width,
                "direction": "از ورودی تا صندوق",
                "products": "محصولات پرفروش در کنار مسیر"
            },
            "secondary_paths": {
                "width": secondary_path_width,
                "purpose": "دسترسی به بخش‌های مختلف"
            },
            "stopping_points": {
                "size": "1.5×1.5 متر",
                "purpose": "بررسی محصولات"
            },
            "tips": [
                "مسیر طبیعی و بدون مانع",
                "نقاط توقف استراتژیک",
                "دسترسی آسان به صندوق",
                "فضای کافی برای سبد خرید"
            ]
        }
    
    def _get_lighting_guide(self, store_size: float, conversion_rate: float) -> Dict[str, Any]:
        """راهنمای نورپردازی"""
        intensity = "500-800 لوکس" if conversion_rate < 40 else "300-500 لوکس"
        color_temp = "3000K (گرم)" if store_size < 200 else "4000K (خنثی)"
        
        return {
            "general_lighting": {
                "intensity": intensity,
                "color_temperature": color_temp,
                "type": "LED"
            },
            "accent_lighting": {
                "purpose": "تأکید بر محصولات خاص",
                "intensity": "800-1200 لوکس",
                "color_temperature": "2700K"
            },
            "tips": [
                "نورپردازی یکنواخت",
                "اجتناب از سایه‌های تیز",
                "استفاده از نور طبیعی",
                "کنترل نورپردازی بر اساس ساعت"
            ]
        }
    
    def _get_color_scheme_guide(self, conversion_rate: float) -> Dict[str, Any]:
        """راهنمای ترکیب رنگی"""
        if conversion_rate < 30:
            scheme = "گرم و انرژی‌بخش"
            colors = ["قرمز", "نارنجی", "زرد"]
        elif conversion_rate < 45:
            scheme = "متعادل و متوازن"
            colors = ["آبی", "سبز", "خاکستری"]
        else:
            scheme = "لوکس و آرام"
            colors = ["بنفش", "سفید", "سیاه"]
        
        return {
            "scheme": scheme,
            "primary_colors": colors,
            "rule": "قانون 60-30-10",
            "usage": {
                "60%": "رنگ اصلی (پس‌زمینه)",
                "30%": "رنگ ثانویه (قاب‌بندی)",
                "10%": "رنگ تأکیدی (جزئیات)"
            }
        }
    
    def _get_product_placement_guide(self, shelf_count: float, conversion_rate: float) -> Dict[str, Any]:
        """راهنمای قرارگیری محصولات"""
        return {
            "high_traffic_areas": [
                "کنار ورودی",
                "نزدیک صندوق",
                "انتهای مسیرهای اصلی"
            ],
            "product_arrangement": {
                "eye_level": "محصولات پرفروش",
                "top_shelf": "محصولات جدید",
                "bottom_shelf": "محصولات حجیم"
            },
            "cross_selling": {
                "strategy": "محصولات مرتبط در کنار هم",
                "examples": [
                    "کفش و جوراب",
                    "لباس و اکسسوری",
                    "مواد غذایی و نوشیدنی"
                ]
            },
            "seasonal_placement": {
                "front": "محصولات فصلی",
                "back": "محصولات همیشگی"
            }
        }
    
    def _get_optimization_priority(self, features) -> Dict[str, Any]:
        """اولویت‌بندی بهینه‌سازی"""
        try:
            priorities = []
            
            # محاسبه امتیاز برای هر بخش
            layout_score = 100 - (float(features[0, 7]) / float(features[0, 0]) * 100)  # فضای بلااستفاده
            checkout_score = float(features[0, 2]) * 10  # تعداد صندوق‌ها
            conversion_score = float(features[0, 4])  # نرخ تبدیل
            traffic_score = float(features[0, 5]) / 10  # ترافیک
            
            # اولویت‌بندی
            if layout_score < 70:
                priorities.append({"area": "layout", "priority": "high", "score": layout_score})
            if checkout_score < 30:
                priorities.append({"area": "checkout", "priority": "high", "score": checkout_score})
            if conversion_score < 35:
                priorities.append({"area": "conversion", "priority": "medium", "score": conversion_score})
            if traffic_score < 10:
                priorities.append({"area": "traffic", "priority": "low", "score": traffic_score})
            
            return {
                "priorities": sorted(priorities, key=lambda x: x["score"]),
                "overall_score": (layout_score + checkout_score + conversion_score + traffic_score) / 4
            }
            
        except Exception as e:
            logger.error(f"Error in optimization priority: {e}")
            return {"error": str(e)}
    
    def _predict_roi(self, features) -> Dict[str, Any]:
        """پیش‌بینی بازگشت سرمایه"""
        try:
            current_sales = float(features[0, 9])  # فروش روزانه
            improvement_target = float(features[0, 15])  # هدف بهبود
            timeline = float(features[0, 16])  # بازه زمانی
            
            # محاسبه ROI
            additional_sales = current_sales * (improvement_target / 100) * 365  # فروش سالانه اضافی
            estimated_cost = current_sales * 0.1 * timeline  # هزینه تخمینی (10% فروش فعلی)
            roi = (additional_sales - estimated_cost) / estimated_cost * 100
            
            return {
                "current_annual_sales": current_sales * 365,
                "additional_annual_sales": additional_sales,
                "estimated_cost": estimated_cost,
                "roi_percentage": roi,
                "payback_period": timeline,
                "confidence": 0.75
            }
            
        except Exception as e:
            logger.error(f"Error in ROI prediction: {e}")
            return {"error": str(e)}
    
    def _analyze_patterns(self, features) -> Dict[str, Any]:
        """تحلیل الگوها"""
        try:
            patterns = {
                "traffic_patterns": self._analyze_traffic_patterns(features),
                "sales_patterns": self._analyze_sales_patterns(features),
                "seasonal_patterns": self._analyze_seasonal_patterns(features)
            }
            return patterns
            
        except Exception as e:
            logger.error(f"Error in pattern analysis: {e}")
            return {"error": str(e)}
    
    def _analyze_traffic_patterns(self, features) -> Dict[str, Any]:
        """تحلیل الگوهای ترافیک"""
        morning = float(features[0, 11])
        noon = float(features[0, 12])
        evening = float(features[0, 13])
        
        peak_period = "morning" if morning > max(noon, evening) else "noon" if noon > evening else "evening"
        
        return {
            "peak_period": peak_period,
            "distribution": {
                "morning": morning,
                "noon": noon,
                "evening": evening
            },
            "recommendations": self._get_traffic_recommendations(peak_period)
        }
    
    def _get_traffic_recommendations(self, peak_period: str) -> List[str]:
        """پیشنهادات بر اساس دوره پیک"""
        recommendations = {
            "morning": [
                "افزایش کارکنان در ساعات صبح",
                "بهینه‌سازی موجودی برای ساعات صبح",
                "برنامه‌های تشویقی صبحگاهی"
            ],
            "noon": [
                "بهینه‌سازی صندوق‌ها برای ساعات شلوغی",
                "برنامه‌های ناهار",
                "مدیریت صف هوشمند"
            ],
            "evening": [
                "افزایش نورپردازی",
                "برنامه‌های عصرگاهی",
                "بهینه‌سازی مسیرهای خروج"
            ]
        }
        return recommendations.get(peak_period, [])
    
    def _analyze_sales_patterns(self, features) -> Dict[str, Any]:
        """تحلیل الگوهای فروش"""
        conversion_rate = float(features[0, 4])
        customer_traffic = float(features[0, 5])
        
        efficiency_score = (conversion_rate / 50) * (customer_traffic / 200) * 100
        
        return {
            "efficiency_score": efficiency_score,
            "performance_level": "high" if efficiency_score > 70 else "medium" if efficiency_score > 40 else "low",
            "optimization_potential": 100 - efficiency_score
        }
    
    def _analyze_seasonal_patterns(self, features) -> Dict[str, Any]:
        """تحلیل الگوهای فصلی"""
        # این بخش نیاز به داده‌های تاریخی دارد
        return {
            "note": "تحلیل فصلی نیاز به داده‌های تاریخی دارد",
            "recommendation": "جمع‌آوری داده‌های فروش ماهانه برای تحلیل فصلی"
        }
    
    def _generate_ml_recommendations(self, features, predictions: Dict) -> Dict[str, Any]:
        """تولید پیشنهادات مبتنی بر ML"""
        try:
            recommendations = {
                "immediate": [],
                "short_term": [],
                "long_term": []
            }
            
            # پیشنهادات فوری بر اساس تحلیل
            if predictions.get("conversion_optimization", {}).get("predicted_improvement", 0) > 10:
                recommendations["immediate"].append("بهینه‌سازی فوری چیدمان برای بهبود نرخ تبدیل")
            
            if float(features[0, 7]) > float(features[0, 0]) * 0.2:  # فضای بلااستفاده > 20%
                recommendations["immediate"].append("بازطراحی فوری فضای بلااستفاده")
            
            # پیشنهادات کوتاه مدت
            if predictions.get("roi_prediction", {}).get("roi_percentage", 0) > 50:
                recommendations["short_term"].append("پیاده‌سازی برنامه‌های بهبود با ROI بالا")
            
            # پیشنهادات بلند مدت
            if predictions.get("sales_prediction", {}).get("improvement_potential", 0) > 30:
                recommendations["long_term"].append("بازسازی کامل فروشگاه برای حداکثر پتانسیل")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating ML recommendations: {e}")
            return {"error": str(e)}
    
    def _calculate_confidence_scores(self, features) -> Dict[str, float]:
        """محاسبه امتیازات اطمینان"""
        try:
            # محاسبه اطمینان بر اساس کیفیت داده‌ها
            data_completeness = min(100, np.count_nonzero(features) / len(features) * 100)
            data_consistency = 85  # فرض بر این که داده‌ها سازگار هستند
            
            return {
                "data_completeness": data_completeness,
                "data_consistency": data_consistency,
                "overall_confidence": (data_completeness + data_consistency) / 2
            }
            
        except Exception as e:
            logger.error(f"Error calculating confidence scores: {e}")
            return {"error": str(e)}
    
    def _generate_openai_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """تولید تحلیل با OpenAI"""
        try:
            # آماده‌سازی داده‌ها برای AI
            store_info = self._prepare_store_info(analysis_data)
            
            # پرامپت برای تحلیل
            prompt = f"""
            شما یک متخصص تحلیل فروشگاه و بهینه‌سازی تجارت هستید. 
            لطفاً تحلیل تفصیلی و راهنمایی‌های عملی برای فروشگاه زیر ارائه دهید:

            اطلاعات فروشگاه:
            {store_info}

            لطفاً تحلیل خود را در قالب JSON با ساختار زیر ارائه دهید:
            {{
                "executive_summary": "خلاصه اجرایی",
                "detailed_analysis": {{
                    "strengths": ["نقاط قوت"],
                    "weaknesses": ["نقاط ضعف"],
                    "opportunities": ["فرصت‌ها"],
                    "threats": ["تهدیدها"]
                }},
                "recommendations": {{
                    "immediate": ["اقدامات فوری"],
                    "short_term": ["اقدامات کوتاه مدت"],
                    "long_term": ["اقدامات بلند مدت"]
                }},
                "optimization_plan": {{
                    "layout_optimization": "بهینه‌سازی چیدمان",
                    "pricing_strategy": "استراتژی قیمت‌گذاری",
                    "inventory_management": "مدیریت موجودی",
                    "customer_experience": "تجربه مشتری"
                }},
                "financial_projections": {{
                    "sales_increase": "درصد افزایش فروش",
                    "cost_reduction": "درصد کاهش هزینه",
                    "roi_timeline": "زمان بازگشت سرمایه"
                }},
                "implementation_timeline": {{
                    "phase_1": "فاز اول (1-2 ماه)",
                    "phase_2": "فاز دوم (3-6 ماه)",
                    "phase_3": "فاز سوم (6-12 ماه)"
                }}
            }}
            """
            
            # ارسال درخواست به OpenAI
            response = self.openai_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "شما یک متخصص تحلیل فروشگاه و بهینه‌سازی تجارت هستید."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            # پردازش پاسخ
            ai_response = response.choices[0].message.content
            analysis_result = json.loads(ai_response)
            
            # اضافه کردن متادیتا
            analysis_result['generated_at'] = datetime.now().isoformat()
            analysis_result['ai_model'] = 'gpt-3.5-turbo'
            analysis_result['confidence_score'] = 0.95
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"خطا در تحلیل OpenAI: {e}")
            return self._generate_local_analysis(analysis_data)
    
    def _generate_local_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """تولید تحلیل محلی (بدون نیاز به API)"""
        
        # استخراج داده‌های کلیدی
        store_size = analysis_data.get('store_size', 500)
        entrance_count = analysis_data.get('entrance_count', 2)
        checkout_count = analysis_data.get('checkout_count', 3)
        conversion_rate = analysis_data.get('conversion_rate', 35.5)
        customer_traffic = analysis_data.get('customer_traffic', 150)
        customer_dwell_time = analysis_data.get('customer_dwell_time', 45)
        unused_area_size = analysis_data.get('unused_area_size', 0)
        daily_sales_volume = analysis_data.get('daily_sales_volume', 0)
        product_categories = analysis_data.get('product_categories', [])
        has_surveillance = analysis_data.get('has_surveillance', False)
        
        # بررسی فایل‌های آپلود شده
        uploaded_files_count = sum([
            1 if analysis_data.get('store_photos') else 0,
            1 if analysis_data.get('store_plan') else 0,
            1 if analysis_data.get('shelf_photos') else 0,
            1 if analysis_data.get('entrance_photos') else 0,
            1 if analysis_data.get('checkout_photos') else 0,
            1 if analysis_data.get('customer_video') else 0,
            1 if analysis_data.get('surveillance_footage') else 0,
            1 if analysis_data.get('sales_file') else 0,
            1 if analysis_data.get('product_catalog') else 0,
        ])
        
        # تحلیل نقاط قوت
        strengths = []
        if entrance_count >= 2:
            strengths.append("برخورداری از تعداد کافی ورودی برای تسهیل جریان مشتریان")
        if checkout_count >= 3:
            strengths.append("ظرفیت مناسب صندوق‌های پرداخت")
        if conversion_rate > 30:
            strengths.append("داشتن نرخ تبدیل قابل قبول")
        if customer_traffic > 100:
            strengths.append("برخورداری از ترافیک مشتریان روزانه مطلوب")
        if customer_dwell_time > 30:
            strengths.append("زمان حضور مناسب مشتریان در فروشگاه")
        if has_surveillance:
            strengths.append("وجود سیستم نظارت و امنیت")
        if len(product_categories) > 3:
            strengths.append("تنوع مناسب در دسته‌بندی محصولات")
        if uploaded_files_count > 5:
            strengths.append("ارائه اطلاعات و مستندات جامع")
        if analysis_data.get('customer_video'):
            strengths.append("دسترسی به ویدیوی رفتار مشتریان برای تحلیل دقیق‌تر")
        if analysis_data.get('sales_file'):
            strengths.append("داشتن داده‌های فروش تاریخی برای تحلیل روندها")
        
        # تحلیل نقاط ضعف
        weaknesses = []
        if conversion_rate < 40:
            weaknesses.append("نیاز به بهبود نرخ تبدیل مشتریان")
        if entrance_count < 3:
            weaknesses.append("محدودیت در تعداد ورودی‌های فروشگاه")
        if checkout_count < 4:
            weaknesses.append("ظرفیت ناکافی صندوق‌های پرداخت در ساعات شلوغی")
        if customer_dwell_time < 30:
            weaknesses.append("کوتاه بودن زمان حضور مشتریان در فروشگاه")
        if unused_area_size > store_size * 0.2:
            weaknesses.append(f"بلااستفاده ماندن حدود {int(unused_area_size/store_size*100)}% از فضای فروشگاه")
        if not has_surveillance:
            weaknesses.append("عدم وجود سیستم نظارت برای تحلیل رفتار مشتریان")
        if uploaded_files_count < 3:
            weaknesses.append("عدم ارائه مستندات و تصاویر کافی برای تحلیل دقیق")
        if not analysis_data.get('customer_video') and not analysis_data.get('surveillance_footage'):
            weaknesses.append("عدم دسترسی به ویدیو برای تحلیل رفتار مشتریان")
        if not analysis_data.get('sales_file'):
            weaknesses.append("عدم ارائه داده‌های فروش برای تحلیل روندها")
        
        # فرصت‌ها
        opportunities = [
            "امکان بهبود نرخ تبدیل از طریق بهینه‌سازی چیدمان فروشگاه",
            "افزایش زمان حضور مشتریان با طراحی بهتر فضای فروشگاه",
            "بهینه‌سازی جریان حرکت مشتریان در فروشگاه",
            "پیاده‌سازی سیستم مدیریت صف هوشمند"
        ]
        
        if unused_area_size > 0:
            opportunities.append(f"امکان بهره‌برداری از {unused_area_size} متر مربع فضای بلااستفاده")
        
        if not has_surveillance:
            opportunities.append("پیاده‌سازی سیستم نظارت برای تحلیل دقیق‌تر رفتار مشتریان")
        
        if daily_sales_volume > 0:
            opportunities.append("بهینه‌سازی استراتژی قیمت‌گذاری بر اساس داده‌های فروش")
        
        if analysis_data.get('customer_video'):
            opportunities.append("امکان تحلیل ویدیویی رفتار مشتریان با استفاده از هوش مصنوعی")
        if analysis_data.get('store_photos'):
            opportunities.append("امکان تحلیل تصویری چیدمان با استفاده از تکنولوژی‌های پیشرفته")
        if analysis_data.get('sales_file'):
            opportunities.append("امکان پیش‌بینی فروش با استفاده از یادگیری ماشین")
        
        # تهدیدها
        threats = [
            "رقابت فزاینده با فروشگاه‌های مجاور",
            "تغییرات احتمالی در رفتار خرید مشتریان",
            "افزایش مستمر هزینه‌های عملیاتی"
        ]
        
        if unused_area_size > store_size * 0.3:
            threats.append("هدررفت سرمایه در فضای بلااستفاده")
        
        # پیشنهادات
        recommendations = {
            "immediate": [
                "بهینه‌سازی چیدمان قفسه‌ها و محصولات",
                "نصب تابلوهای راهنما و اطلاعات",
                "بهبود سیستم نورپردازی فروشگاه"
            ],
            "short_term": [
                "افزایش تعداد صندوق‌های پرداخت",
                "پیاده‌سازی سیستم مدیریت صف",
                "بهبود استراتژی قیمت‌گذاری محصولات"
            ],
            "long_term": [
                "بازسازی کامل فضای فروشگاه",
                "پیاده‌سازی سیستم‌های هوشمند مدیریت",
                "گسترش فضای فروشگاه و تنوع محصولات"
            ]
        }
        
        # اضافه کردن پیشنهادات خاص بر اساس داده‌ها
        if unused_area_size > 0:
            recommendations["immediate"].append(f"بازطراحی و بهره‌برداری از {unused_area_size} متر مربع فضای بلااستفاده")
        
        if not has_surveillance:
            recommendations["short_term"].append("نصب سیستم دوربین نظارتی و امنیتی")
        
        if customer_dwell_time < 30:
            recommendations["immediate"].append("بهبود طراحی مسیرهای حرکت مشتریان")
        
        # محاسبه پتانسیل بهبود (قبل از استفاده)
        conversion_improvement = min(25, (50 - conversion_rate) * 1.5)  # بهبود نرخ تبدیل
        traffic_improvement = min(20, (500 - customer_traffic) / 500 * 30)  # بهبود ترافیک
        space_improvement = min(15, (unused_area_size / store_size) * 30) if unused_area_size > 0 else 0
        
        # برنامه بهینه‌سازی واقعی‌تر
        optimization_plan = {
            "layout_optimization": f"بازطراحی چیدمان فروشگاه برای افزایش {conversion_improvement:.1f}% نرخ تبدیل (از {conversion_rate}% به {conversion_rate + conversion_improvement:.1f}%)",
            "traffic_optimization": f"بهبود جریان حرکت مشتریان برای افزایش {traffic_improvement:.1f}% ترافیک",
            "space_utilization": f"بهره‌برداری از {unused_area_size} متر مربع فضای بلااستفاده برای {space_improvement:.1f}% بهبود فروش",
            "pricing_strategy": "پیاده‌سازی استراتژی قیمت‌گذاری پویا بر اساس تحلیل رفتار مشتریان",
            "inventory_management": "بهینه‌سازی مدیریت موجودی بر اساس الگوی فروش و پیش‌بینی تقاضا",
            "customer_experience": "بهبود تجربه مشتریان با طراحی بهتر مسیرها و کاهش زمان انتظار",
            "technology_integration": "پیاده‌سازی سیستم‌های هوشمند برای مدیریت بهتر عملیات فروشگاه"
        }
        
        # پیش‌بینی مالی واقعی‌تر
        # محاسبه فروش فعلی
        current_daily_sales = customer_traffic * (conversion_rate / 100) * 15000  # متوسط خرید 15,000 تومان
        current_monthly_sales = current_daily_sales * 30
        current_yearly_sales = current_monthly_sales * 12
        
        total_sales_improvement = conversion_improvement + traffic_improvement + space_improvement
        
        # محاسبه فروش جدید
        new_daily_sales = current_daily_sales * (1 + total_sales_improvement / 100)
        additional_monthly_sales = (new_daily_sales - current_daily_sales) * 30
        additional_yearly_sales = additional_monthly_sales * 12
        
        # محاسبه هزینه‌ها و ROI
        implementation_cost = current_yearly_sales * 0.15  # 15% فروش سالانه
        operational_cost_reduction = current_yearly_sales * 0.08  # 8% کاهش هزینه‌های عملیاتی
        theft_reduction = current_yearly_sales * 0.02 if not has_surveillance else 0  # 2% کاهش سرقت
        
        total_cost_reduction = operational_cost_reduction + theft_reduction
        net_benefit = additional_yearly_sales + total_cost_reduction - implementation_cost
        roi_percentage = (net_benefit / implementation_cost) * 100 if implementation_cost > 0 else 0
        payback_period = implementation_cost / (additional_monthly_sales + total_cost_reduction / 12) if (additional_monthly_sales + total_cost_reduction / 12) > 0 else 0
        
        financial_projections = {
            "current_daily_sales": f"{current_daily_sales:,.0f} تومان",
            "current_monthly_sales": f"{current_monthly_sales:,.0f} تومان",
            "current_yearly_sales": f"{current_yearly_sales:,.0f} تومان",
            "new_daily_sales": f"{new_daily_sales:,.0f} تومان",
            "additional_monthly_sales": f"{additional_monthly_sales:,.0f} تومان",
            "additional_yearly_sales": f"{additional_yearly_sales:,.0f} تومان",
            "sales_increase_percentage": f"{total_sales_improvement:.1f}%",
            "implementation_cost": f"{implementation_cost:,.0f} تومان",
            "cost_reduction_percentage": f"{((total_cost_reduction / current_yearly_sales) * 100):.1f}%",
            "roi_percentage": f"{roi_percentage:.1f}%",
            "payback_period_months": f"{payback_period:.1f} ماه",
            "net_benefit_yearly": f"{net_benefit:,.0f} تومان"
        }
        
        # جدول زمانی پیاده‌سازی
        implementation_timeline = {
            "phase_1": "بهینه‌سازی چیدمان فروشگاه و سیستم نورپردازی",
            "phase_2": "افزایش صندوق‌های پرداخت و پیاده‌سازی سیستم مدیریت صف",
            "phase_3": "بازسازی کامل فضای فروشگاه و پیاده‌سازی سیستم‌های هوشمند"
        }
        
        if unused_area_size > 0:
            implementation_timeline["phase_1"] += f" و بازطراحی {unused_area_size} متر مربع فضای بلااستفاده"
        
        # تولید راهنمایی‌های عملی
        features = self._extract_ml_features(analysis_data)
        practical_guide = self._generate_practical_recommendations(features)
        
        return {
            "executive_summary": f"فروشگاه {analysis_data.get('store_name', '')} با نرخ تبدیل {conversion_rate}% و {customer_traffic} مشتری روزانه، در حال حاضر فروش روزانه‌ای معادل {current_daily_sales:,.0f} تومان دارد. با اجرای برنامه‌های بهینه‌سازی چیدمان و افزایش نرخ تبدیل به {conversion_rate + conversion_improvement:.1f}%، همچنین بهره‌برداری از {unused_area_size} متر مربع فضای بلااستفاده، فروش روزانه به {new_daily_sales:,.0f} تومان افزایش خواهد یافت. این بهبودها منجر به {total_sales_improvement:.1f}% رشد فروش، بازده سرمایه‌گذاری {roi_percentage:.1f}% و بازگشت سرمایه در مدت {payback_period:.1f} ماه خواهد شد.",
            "detailed_analysis": {
                "strengths": strengths,
                "weaknesses": weaknesses,
                "opportunities": opportunities,
                "threats": threats
            },
            "recommendations": recommendations,
            "optimization_plan": optimization_plan,
            "financial_projections": financial_projections,
            "implementation_timeline": implementation_timeline,
            "practical_guide": practical_guide,
            "generated_at": datetime.now().isoformat(),
            "ai_model": "local_analysis",
            "confidence_score": 0.85
        }
    
    def _prepare_store_info(self, analysis_data: Dict[str, Any]) -> str:
        """آماده‌سازی اطلاعات فروشگاه برای AI"""
        info_parts = []
        
        # اطلاعات پایه
        info_parts.append(f"نام فروشگاه: {analysis_data.get('store_name', 'نامشخص')}")
        info_parts.append(f"نوع فروشگاه: {analysis_data.get('store_type', 'نامشخص')}")
        info_parts.append(f"اندازه فروشگاه: {analysis_data.get('store_size', 'نامشخص')} متر مربع")
        
        # اطلاعات تکمیلی
        if analysis_data.get('store_location'):
            info_parts.append(f"آدرس: {analysis_data.get('store_location')}")
        if analysis_data.get('city'):
            info_parts.append(f"شهر: {analysis_data.get('city')}")
        if analysis_data.get('area'):
            info_parts.append(f"منطقه: {analysis_data.get('area')}")
        if analysis_data.get('establishment_year'):
            info_parts.append(f"سال تاسیس: {analysis_data.get('establishment_year')}")
        
        # اطلاعات فیزیکی
        info_parts.append(f"تعداد ورودی‌ها: {analysis_data.get('entrance_count', 0)}")
        info_parts.append(f"تعداد صندوق‌ها: {analysis_data.get('checkout_count', 0)}")
        info_parts.append(f"تعداد قفسه‌ها: {analysis_data.get('shelf_count', 0)}")
        
        # اطلاعات دقیق‌تر چیدمان
        if analysis_data.get('shelf_dimensions'):
            info_parts.append(f"ابعاد قفسه‌ها: {analysis_data.get('shelf_dimensions')}")
        if analysis_data.get('shelf_contents'):
            info_parts.append(f"محتوای قفسه‌ها: {analysis_data.get('shelf_contents')}")
        if analysis_data.get('unused_area_size'):
            info_parts.append(f"مناطق بلااستفاده: {analysis_data.get('unused_area_size')} متر مربع")
        if analysis_data.get('unused_area_type'):
            info_parts.append(f"نوع مناطق بلااستفاده: {analysis_data.get('unused_area_type')}")
        
        # طراحی و دکوراسیون
        if analysis_data.get('design_style'):
            info_parts.append(f"سبک طراحی: {analysis_data.get('design_style')}")
        if analysis_data.get('brand_colors'):
            info_parts.append(f"رنگ‌های برند: {analysis_data.get('brand_colors')}")
        info_parts.append(f"نورپردازی اصلی: {analysis_data.get('main_lighting', 'نامشخص')}")
        if analysis_data.get('lighting_intensity'):
            info_parts.append(f"شدت نورپردازی: {analysis_data.get('lighting_intensity')}")
        
        # اطلاعات عملکرد
        info_parts.append(f"نرخ تبدیل: {analysis_data.get('conversion_rate', 0)}%")
        info_parts.append(f"متوسط مشتریان روزانه: {analysis_data.get('customer_traffic', 0)}")
        info_parts.append(f"متوسط زمان حضور مشتری: {analysis_data.get('customer_dwell_time', 0)} دقیقه")
        
        # اطلاعات ترافیک دقیق‌تر
        if analysis_data.get('peak_hours'):
            info_parts.append(f"ساعات پیک: {analysis_data.get('peak_hours')}")
        if analysis_data.get('high_traffic_areas'):
            info_parts.append(f"مناطق پرتردد: {analysis_data.get('high_traffic_areas')}")
        
        # اطلاعات فروش
        info_parts.append(f"درصد فروش صبح: {analysis_data.get('morning_sales_percent', 0)}%")
        info_parts.append(f"درصد فروش ظهر: {analysis_data.get('noon_sales_percent', 0)}%")
        info_parts.append(f"درصد فروش شب: {analysis_data.get('evening_sales_percent', 0)}%")
        
        # محصولات و فروش
        if analysis_data.get('product_categories'):
            info_parts.append(f"دسته‌بندی محصولات: {', '.join(analysis_data.get('product_categories', []))}")
        if analysis_data.get('top_products'):
            info_parts.append(f"محصولات پرفروش: {analysis_data.get('top_products')}")
        if analysis_data.get('daily_sales_volume'):
            info_parts.append(f"فروش روزانه: {analysis_data.get('daily_sales_volume')} تومان")
        if analysis_data.get('supplier_count'):
            info_parts.append(f"تعداد تامین‌کنندگان: {analysis_data.get('supplier_count')}")
        
        # نظارت و امنیت
        if analysis_data.get('has_surveillance'):
            info_parts.append(f"دوربین نظارتی: بله")
            if analysis_data.get('camera_count'):
                info_parts.append(f"تعداد دوربین‌ها: {analysis_data.get('camera_count')}")
            if analysis_data.get('camera_locations'):
                info_parts.append(f"موقعیت دوربین‌ها: {analysis_data.get('camera_locations')}")
        else:
            info_parts.append(f"دوربین نظارتی: خیر")
        
        # فایل‌ها و اطلاعات اضافی
        if analysis_data.get('pos_system'):
            info_parts.append(f"نرم‌افزار صندوق: {analysis_data.get('pos_system')}")
        if analysis_data.get('inventory_system'):
            info_parts.append(f"نرم‌افزار موجودی: {analysis_data.get('inventory_system')}")
        if analysis_data.get('video_date'):
            info_parts.append(f"تاریخ ضبط ویدیو: {analysis_data.get('video_date')}")
        if analysis_data.get('video_duration'):
            info_parts.append(f"مدت ویدیو: {analysis_data.get('video_duration')} ثانیه")
        
        # نوع فایل‌های آپلود شده
        uploaded_files = []
        if analysis_data.get('store_photos'):
            uploaded_files.append("تصاویر فروشگاه")
        if analysis_data.get('store_plan'):
            uploaded_files.append("نقشه فروشگاه")
        if analysis_data.get('shelf_photos'):
            uploaded_files.append("تصاویر قفسه‌ها")
        if analysis_data.get('entrance_photos'):
            uploaded_files.append("تصاویر ورودی")
        if analysis_data.get('checkout_photos'):
            uploaded_files.append("تصاویر صندوق")
        if analysis_data.get('customer_video'):
            uploaded_files.append("ویدیوی مشتریان")
        if analysis_data.get('surveillance_footage'):
            uploaded_files.append("فیلم دوربین نظارتی")
        if analysis_data.get('sales_file'):
            uploaded_files.append("فایل فروش")
        if analysis_data.get('product_catalog'):
            uploaded_files.append("کاتالوگ محصولات")
        
        if uploaded_files:
            info_parts.append(f"فایل‌های آپلود شده: {', '.join(uploaded_files)}")
        
        return "\n".join(info_parts)
    
    def generate_implementation_guide(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """تولید راهنمای پیاده‌سازی عملی"""
        
        guide = {
            "title": "راهنمای پیاده‌سازی بهینه‌سازی فروشگاه",
            "overview": "این راهنما شامل مراحل عملی برای پیاده‌سازی پیشنهادات تحلیل است.",
            "phases": {},
            "checklist": {},
            "resources": {},
            "timeline": {}
        }
        
        # فاز اول (1-2 ماه)
        guide["phases"]["phase_1"] = {
            "title": "فاز اول: بهینه‌سازی سریع",
            "duration": "1-2 ماه",
            "budget": "کم",
            "priority": "بالا",
            "tasks": [
                "بازطراحی چیدمان قفسه‌ها",
                "بهبود نورپردازی",
                "نصب تابلوهای راهنما",
                "بهینه‌سازی مسیرهای مشتری"
            ],
            "expected_results": [
                "افزایش 5-10% نرخ تبدیل",
                "کاهش زمان انتظار",
                "بهبود تجربه مشتری"
            ]
        }
        
        # فاز دوم (3-6 ماه)
        guide["phases"]["phase_2"] = {
            "title": "فاز دوم: بهبود سیستم‌ها",
            "duration": "3-6 ماه",
            "budget": "متوسط",
            "priority": "متوسط",
            "tasks": [
                "افزایش تعداد صندوق‌ها",
                "پیاده‌سازی سیستم مدیریت صف",
                "بهبود استراتژی قیمت‌گذاری",
                "بهینه‌سازی موجودی"
            ],
            "expected_results": [
                "افزایش 15-20% فروش",
                "کاهش 20% هزینه‌های عملیاتی",
                "بهبود رضایت کارکنان"
            ]
        }
        
        # فاز سوم (6-12 ماه)
        guide["phases"]["phase_3"] = {
            "title": "فاز سوم: تحول دیجیتال",
            "duration": "6-12 ماه",
            "budget": "بالا",
            "priority": "کم",
            "tasks": [
                "پیاده‌سازی سیستم هوشمند",
                "بازسازی کامل فروشگاه",
                "گسترش فضای فروشگاه",
                "پیاده‌سازی تجارت الکترونیک"
            ],
            "expected_results": [
                "افزایش 25-30% فروش",
                "کاهش 30% هزینه‌ها",
                "رقابت‌پذیری بالا"
            ]
        }
        
        # چک‌لیست پیاده‌سازی
        guide["checklist"] = {
            "pre_implementation": [
                "تأیید بودجه",
                "تشکیل تیم پیاده‌سازی",
                "برنامه‌ریزی زمانی",
                "آموزش کارکنان"
            ],
            "during_implementation": [
                "نظارت بر پیشرفت",
                "مدیریت تغییرات",
                "حل مشکلات",
                "ارتباط با ذینفعان"
            ],
            "post_implementation": [
                "ارزیابی نتایج",
                "بهینه‌سازی فرآیندها",
                "آموزش مستمر",
                "برنامه‌ریزی آینده"
            ]
        }
        
        # منابع مورد نیاز
        guide["resources"] = {
            "human_resources": [
                "مدیر پروژه",
                "متخصص طراحی فروشگاه",
                "کارشناس IT",
                "کارکنان فروشگاه"
            ],
            "technical_resources": [
                "نرم‌افزار طراحی",
                "سیستم مدیریت صف",
                "تجهیزات نورپردازی",
                "تابلوهای راهنما"
            ],
            "financial_resources": [
                "بودجه پیاده‌سازی",
                "بودجه آموزش",
                "بودجه نگهداری",
                "بودجه اضطراری"
            ]
        }
        
        # جدول زمانی
        guide["timeline"] = {
            "week_1_2": "برنامه‌ریزی و آماده‌سازی",
            "week_3_4": "شروع فاز اول",
            "month_2": "تکمیل فاز اول",
            "month_3_4": "شروع فاز دوم",
            "month_5_6": "تکمیل فاز دوم",
            "month_7_12": "پیاده‌سازی فاز سوم"
        }
        
        return guide

# نمونه استفاده
if __name__ == "__main__":
    # تست سیستم
    ai_analyzer = StoreAnalysisAI()
    
    test_data = {
        'store_name': 'فروشگاه تست',
        'store_type': 'retail',
        'store_size': 'medium',
        'entrance_count': 2,
        'checkout_count': 3,
        'shelf_count': 25,
        'conversion_rate': 35.5,
        'avg_daily_customers': 150,
        'avg_customer_time': 45
    }
    
    result = ai_analyzer.generate_detailed_analysis(test_data)
    print(json.dumps(result, indent=2, ensure_ascii=False))
