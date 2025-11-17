"""
سرویس هوش مصنوعی پیشرفته لیارا برای چیدمانو
استفاده از بهترین مدل‌های AI برای تحلیل حرفه‌ای فروشگاه‌ها
"""

import requests
import json
import logging
from typing import Dict, List, Any, Optional
from django.conf import settings
from django.core.cache import cache
import time

logger = logging.getLogger(__name__)

class LiaraAIService:
    """سرویس هوش مصنوعی پیشرفته لیارا"""
    
    def __init__(self):
        # URL صحیح API لیارا AI - بر اساس پاسخ پشتیبانی لیارا
        # سرویس AI از طریق دامنه ai.liara.ir ارائه می‌شود
        # Endpoint صحیح: https://ai.liara.ir/api/{workspaceID}/v1/chat/completions
        base_url_raw = getattr(settings, 'LIARA_AI_BASE_URL', 'https://ai.liara.ir/api')
        
        # 🔧 اصلاح خودکار URL اشتباه (اگر از api.liara.ir استفاده شده باشد)
        if 'api.liara.ir' in base_url_raw:
            logger.warning(f"⚠️ URL قدیمی شناسایی شد: {base_url_raw} - در حال اصلاح به URL صحیح")
            # تبدیل api.liara.ir/v1 به ai.liara.ir/api
            base_url_raw = base_url_raw.replace('api.liara.ir/v1', 'ai.liara.ir/api')
            base_url_raw = base_url_raw.replace('api.liara.ir', 'ai.liara.ir/api')
            # حذف /v1 از انتها اگر وجود دارد
            if base_url_raw.endswith('/v1'):
                base_url_raw = base_url_raw[:-3]
            logger.info(f"✅ URL اصلاح شد به: {base_url_raw}")
        
        self.base_url = base_url_raw.rstrip('/')
        self.api_key = getattr(settings, 'LIARA_AI_API_KEY', '').strip() if getattr(settings, 'LIARA_AI_API_KEY', '') else ''
        # Workspace ID برای API لیارا AI (همان project_id)
        # 🔧 strip کردن فاصله‌های اضافی برای جلوگیری از خطای 403
        self.workspace_id = getattr(settings, 'LIARA_AI_PROJECT_ID', '').strip() if getattr(settings, 'LIARA_AI_PROJECT_ID', '') else ''
        # نگه‌داری project_id برای سازگاری با کد قدیمی
        self.project_id = self.workspace_id
        
        # لاگ برای ردیابی تنظیمات
        logger.info(f"🔧 LiaraAIService initialized: base_url={self.base_url}, api_key_exists={'✅' if self.api_key else '❌'}, workspace_id={'✅' if self.workspace_id else '❌'}")
        
        if not self.api_key:
            logger.warning("⚠️ LIARA_AI_API_KEY تنظیم نشده است - تحلیل AI غیرفعال خواهد بود")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Chidmano-AI-Client/1.0'
        }
        
        # مدل‌های موجود در لیارا بر اساس مستندات
        # تمام مدل‌های لیارا سازگار با OpenAI SDK هستند
        # خواندن مدل از تنظیمات برای امکان تغییر از طریق environment variable
        default_model = getattr(settings, 'LIARA_AI_MODEL', 'openai/gpt-4o-mini')
        self.models = {
            'analysis': default_model,           # تحلیل اصلی
            'design': default_model,             # تحلیل طراحی
            'marketing': default_model,          # تحلیل بازاریابی
            'psychology': default_model,         # روانشناسی مشتری
            'optimization': default_model,       # بهینه‌سازی
            'summary': default_model             # خلاصه‌سازی
        }
        logger.info(f"🤖 استفاده از مدل AI: {default_model}")
    
    def _make_request(self, model: str, prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> Dict:
        """ارسال درخواست به API لیارا"""
        # بررسی وجود API key
        if not self.api_key:
            logger.error("❌ LIARA_AI_API_KEY تنظیم نشده است - نمی‌توان درخواست ارسال کرد")
            return {
                'error': 'LIARA_AI_API_KEY تنظیم نشده است',
                'error_message': 'کلید API لیارا تنظیم نشده است. لطفاً با پشتیبانی تماس بگیرید.'
            }
        
        try:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "شما بهترین متخصص تحلیل فروشگاه و مشاور کسب‌وکار دنیا هستید. تخصص شما در بهینه‌سازی چیدمان فروشگاه‌ها و افزایش فروش است. فقط از زبان فارسی استفاده کنید و هرگز از کلمات انگلیسی مثل regards، Small، Kids_Clothing، Neutral، attractiveness، Design، functionality، example استفاده نکنید."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1
            }
            
            # ساخت URL API - بر اساس پاسخ پشتیبانی لیارا
            # Endpoint صحیح: https://ai.liara.ir/api/{workspaceID}/v1/chat/completions
            if not self.workspace_id:
                logger.error("❌ LIARA_AI_PROJECT_ID (workspaceID) تنظیم نشده است")
                return {
                    'error': 'workspace_id_missing',
                    'error_message': 'Workspace ID تنظیم نشده است. لطفاً LIARA_AI_PROJECT_ID را در settings تنظیم کنید.'
                }
            
            # 🔧 اطمینان از حذف فاصله‌های اضافی در URL
            workspace_id_clean = self.workspace_id.strip() if self.workspace_id else ''
            api_url = f"{self.base_url.rstrip('/')}/{workspace_id_clean}/v1/chat/completions"
            
            logger.info(f"🚀 ارسال درخواست به Liara AI: URL={api_url}, Model={model}, API Key موجود={'✅' if self.api_key else '❌'}, Workspace ID={'✅' if self.workspace_id else '❌'}")
            logger.info(f"📤 Payload size: {len(str(payload))} chars, max_tokens={max_tokens}")
            
            try:
                response = requests.post(
                    api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=120  # افزایش timeout به 120 ثانیه برای مدل‌های بزرگتر
                )
                logger.info(f"📡 پاسخ Liara AI دریافت شد: Status={response.status_code}, URL={api_url}")
            except requests.exceptions.Timeout as timeout_err:
                logger.error(f"⏱️ Timeout در ارسال درخواست: {timeout_err}")
                raise
            except requests.exceptions.RequestException as req_err:
                logger.error(f"❌ خطا در ارسال درخواست: {req_err}")
                raise
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ درخواست به Liara AI موفق: model={model}")
                # بررسی وجود choices در پاسخ
                if 'choices' not in result or not result.get('choices'):
                    logger.warning(f"⚠️ پاسخ API فاقد choices است: {result.keys()}")
                return result
            elif response.status_code == 401:
                logger.error(f"❌ خطا در احراز هویت Liara AI: API key نامعتبر")
                return {
                    'error': 'authentication_failed',
                    'error_message': 'خطا در احراز هویت API. لطفاً API key را بررسی کنید.'
                }
            elif response.status_code == 403:
                error_detail = response.text[:500] if response.text else 'بدون جزئیات'
                logger.error(f"❌ خطا در دسترسی به Liara AI (403): {error_detail}")
                logger.error(f"   URL: {api_url}")
                logger.error(f"   Workspace ID: {self.workspace_id}")
                logger.error(f"   API Key موجود: {'✅' if self.api_key else '❌'}")
                return {
                    'error': 'access_denied',
                    'error_message': 'دسترسی رد شد (403). لطفاً بررسی کنید:\n'
                                   '1. API Key معتبر است و منقضی نشده\n'
                                   '2. Workspace ID صحیح است\n'
                                   '3. API Key برای این Workspace مجاز است\n'
                                   '4. در پنل لیارا دسترسی‌های لازم فعال است',
                    'error_detail': error_detail,
                    'workspace_id': self.workspace_id
                }
            elif response.status_code == 429:
                logger.warning(f"⚠️ Rate limit در Liara AI")
                return {
                    'error': 'rate_limit',
                    'error_message': 'درخواست بیش از حد. لطفاً کمی صبر کنید.'
                }
            else:
                error_detail = response.text[:500] if response.text else 'بدون جزئیات'
                logger.error(f"❌ خطا در API لیارا: {response.status_code} - {error_detail}")
                return {
                    'error': f'api_error_{response.status_code}',
                    'error_message': f'خطا در ارتباط با API: {response.status_code}',
                    'error_detail': error_detail
                }
                
        except requests.exceptions.Timeout:
            logger.warning(f"⚠️ Timeout در ارتباط با لیارا AI - درخواست بیش از 45 ثانیه طول کشید")
            return {
                'error': 'timeout',
                'error_message': 'زمان درخواست به پایان رسید. لطفاً دوباره تلاش کنید.'
            }
        except requests.exceptions.ConnectionError:
            logger.error(f"❌ خطا در اتصال به لیارا AI - بررسی اتصال اینترنت")
            return {
                'error': 'connection_error',
                'error_message': 'خطا در اتصال به سرور. لطفاً اتصال اینترنت را بررسی کنید.'
            }
        except Exception as e:
            logger.error(f"❌ خطا در ارتباط با لیارا AI: {e}", exc_info=True)
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            return {
                'error': 'unexpected_error',
                'error_message': f'خطای غیرمنتظره: {str(e)}'
            }
    
    def analyze_store_comprehensive(self, store_data: Dict[str, Any], images: List[str] = None, videos: List[Dict] = None, sales_data_file: str = None) -> Dict[str, Any]:
        """تحلیل جامع و حرفه‌ای فروشگاه با استفاده از چندین مدل AI و پردازش تصاویر، ویدیو و داده‌های فروش"""
        
        # بررسی وجود API key
        if not self.api_key:
            error_msg = "LIARA_AI_API_KEY تنظیم نشده است. تحلیل نمی‌تواند انجام شود."
            logger.error(f"❌ {error_msg}")
            return {
                'error': 'api_key_missing',
                'error_message': error_msg,
                'analysis_text': f'⚠️ خطا: {error_msg} لطفاً با پشتیبانی تماس بگیرید.'
            }
        
        store_name = store_data.get('store_name', 'فروشگاه')
        store_type = store_data.get('store_type', 'عمومی')
        
        logger.info(f"🚀 شروع تحلیل جامع فروشگاه {store_name} با {len(images) if images else 0} تصویر، {len(videos) if videos else 0} ویدیو، {'فایل فروش' if sales_data_file else 'بدون فایل فروش'}")
        
        # تحلیل‌های موازی با مدل‌های مختلف
        analyses = {}
        errors = []
        
        # 1. تحلیل اصلی با GPT-4 Turbo (شامل اطلاعات تصاویر، ویدیو و داده‌های فروش)
        logger.info(f"🔍 شروع تحلیل اصلی برای {store_name}")
        main_analysis = self._analyze_main_store(store_data, images, videos, sales_data_file)
        if main_analysis and not main_analysis.get('error'):
            analyses['main'] = main_analysis
            logger.info(f"✅ تحلیل اصلی موفق بود")
        elif main_analysis and main_analysis.get('error'):
            errors.append(f"تحلیل اصلی: {main_analysis.get('error_message', 'خطای نامشخص')}")
            logger.error(f"❌ خطا در تحلیل اصلی: {main_analysis.get('error_message', 'خطای نامشخص')}")
            logger.error(f"❌ جزئیات خطا: {main_analysis.get('error', 'unknown')}")
        else:
            logger.error(f"❌ تحلیل اصلی None برگشت")
        
        # 2. تحلیل طراحی با Claude-3 Opus (با تمرکز بر تصاویر و ویدیو)
        # ترکیب images و videos برای تحلیل طراحی
        all_media_for_design = images + (videos if videos else [])
        design_analysis = self._analyze_store_design(store_data, all_media_for_design)
        if design_analysis and not design_analysis.get('error'):
            analyses['design'] = design_analysis
        elif design_analysis and design_analysis.get('error'):
            errors.append(f"تحلیل طراحی: {design_analysis.get('error_message', 'خطای نامشخص')}")
            logger.error(f"❌ خطا در تحلیل طراحی: {design_analysis.get('error_message', 'خطای نامشخص')}")
        
        # 3. تحلیل روانشناسی مشتری با Claude-3 Sonnet (با استفاده از ویدیو جریان مشتری)
        psychology_analysis = self._analyze_customer_psychology(store_data, videos)
        if psychology_analysis and not psychology_analysis.get('error'):
            analyses['psychology'] = psychology_analysis
        elif psychology_analysis and psychology_analysis.get('error'):
            errors.append(f"تحلیل روانشناسی: {psychology_analysis.get('error_message', 'خطای نامشخص')}")
            logger.error(f"❌ خطا در تحلیل روانشناسی: {psychology_analysis.get('error_message', 'خطای نامشخص')}")
        
        # 4. تحلیل بازاریابی با GPT-4o (با استفاده از داده‌های فروش)
        marketing_analysis = self._analyze_marketing_potential(store_data, sales_data_file)
        if marketing_analysis and not marketing_analysis.get('error'):
            analyses['marketing'] = marketing_analysis
        elif marketing_analysis and marketing_analysis.get('error'):
            errors.append(f"تحلیل بازاریابی: {marketing_analysis.get('error_message', 'خطای نامشخص')}")
            logger.error(f"❌ خطا در تحلیل بازاریابی: {marketing_analysis.get('error_message', 'خطای نامشخص')}")
        
        # 5. بهینه‌سازی با GPT-4 Turbo (با استفاده از همه داده‌ها)
        optimization_analysis = self._analyze_optimization(store_data, images, videos, sales_data_file)
        if optimization_analysis and not optimization_analysis.get('error'):
            analyses['optimization'] = optimization_analysis
        elif optimization_analysis and optimization_analysis.get('error'):
            errors.append(f"تحلیل بهینه‌سازی: {optimization_analysis.get('error_message', 'خطای نامشخص')}")
            logger.error(f"❌ خطا در تحلیل بهینه‌سازی: {optimization_analysis.get('error_message', 'خطای نامشخص')}")
        
        # اگر هیچ تحلیلی موفق نبود، خطا برگردان
        if not analyses:
            error_msg = "همه تحلیل‌ها با خطا مواجه شدند. " + " | ".join(errors) if errors else "خطای نامشخص"
            logger.error(f"❌ {error_msg}")
            return {
                'error': 'all_analyses_failed',
                'error_message': error_msg,
                'analysis_text': f'⚠️ خطا: {error_msg} لطفاً دوباره تلاش کنید یا با پشتیبانی تماس بگیرید.'
            }
        
        # ترکیب و خلاصه‌سازی نتایج
        final_analysis = self._combine_analyses(analyses, store_data, images, videos, sales_data_file)
        
        # اگر خطاهایی وجود داشت، به نتایج اضافه کن
        if errors:
            final_analysis['warnings'] = errors
            logger.warning(f"⚠️ برخی تحلیل‌ها با خطا مواجه شدند: {len(errors)} خطا")
        
        return final_analysis
    
    def _analyze_main_store(self, store_data: Dict[str, Any], images: List[str] = None, videos: List[Dict] = None, sales_data_file: str = None) -> Dict[str, Any]:
        """تحلیل اصلی فروشگاه با GPT-4 Turbo - شامل همه فیلدهای فرم و پردازش ویدیو و داده‌های فروش"""
        
        # آماده‌سازی اطلاعات ویدیو
        video_info = ""
        if videos:
            video_info = "\n**🎥 ویدیوهای آپلود شده:**\n"
            for video in videos:
                video_type = video.get('type', 'نامشخص')
                video_type_persian = {
                    'customer_flow_video': 'ویدیو جریان مشتریان',
                    'surveillance_footage': 'فیلم نظارتی',
                    'store_video': 'ویدیو کلی فروشگاه'
                }.get(video_type, video_type)
                video_info += f"- {video_type_persian}: موجود است و باید تحلیل شود\n"
        else:
            video_info = "\n**🎥 ویدیو:** ویدیویی آپلود نشده است. تحلیل بر اساس داده‌های متنی انجام می‌شود.\n"
        
        # آماده‌سازی اطلاعات داده‌های فروش
        sales_info = ""
        if sales_data_file:
            sales_info = f"\n**📊 داده‌های فروش:** فایل داده‌های فروش موجود است. باید تحلیل دقیق فروش انجام شود.\n"
        else:
            sales_info = f"\n**📊 داده‌های فروش:** فایل داده‌های فروش موجود نیست. تحلیل بر اساس اطلاعات متنی انجام می‌شود.\n"
        
        prompt = f"""
        شما بهترین متخصص تحلیل فروشگاه دنیا هستید با تخصص در:
        - علم چیدمان و دکوراسیون (Retail Design & Merchandising)
        - روانشناسی بازاریابی و رفتار مصرف‌کننده (Consumer Psychology & Marketing)
        - تئوری رنگ و تأثیرات روانشناختی (Color Theory & Psychology)
        - پیکربندی فضا و معماری داخلی (Space Planning & Interior Architecture)
        - اصلاح و بهینه‌سازی جریان مشتری (Customer Flow Optimization)
        - تحلیل رفتار مشتری و دید مشتری (Customer Behavior & Visual Merchandising)
        - جذابیت بصری و هنر نمایش (Visual Appeal & Display Art)
        - علم مواد و تأثیرات حسی (Material Science & Sensory Impact)
        
        تحلیل کاملاً حرفه‌ای، تخصصی، فنی و شخصی‌سازی شده برای فروشگاه "{store_data.get('store_name', 'فروشگاه')}" ارائه دهید.

        **قوانین مهم:**
        1. تمام پاسخ شما باید کاملاً به زبان فارسی باشد
        2. از هیچ کلمه انگلیسی، آلمانی، چینی یا عبری استفاده نکنید
        3. فقط از کلمات و اصطلاحات فارسی استفاده کنید
        4. تحلیل باید حرفه‌ای، تخصصی و قابل فهم برای صاحب فروشگاه باشد
        5. از اعداد و ارقام فارسی استفاده کنید (مثال: ۶.۸ به جای 6.8)
        6. هرگز از کلمات انگلیسی استفاده نکنید
        7. از اصول علمی چیدمان، روانشناسی رنگ، و رفتار مشتری استفاده کنید
        8. تحلیل باید عمیق، دقیق و قابل اجرا باشد

        **📋 اطلاعات پایه فروشگاه:**
        - نام: {store_data.get('store_name', 'نامشخص')}
        - نوع: {store_data.get('store_type', 'عمومی')}
        - اندازه: {store_data.get('store_size', 'نامشخص')}
        - آدرس: {store_data.get('store_address', 'نامشخص')}
        - توضیحات: {store_data.get('description', 'نامشخص')}
        - شهر: {store_data.get('city', 'نامشخص')}
        - منطقه: {store_data.get('area', 'نامشخص')}
        - نوع موقعیت: {store_data.get('location_type', 'نامشخص')}
        - سال تأسیس: {store_data.get('establishment_year', 'نامشخص')}
        - تعداد پرسنل: {store_data.get('workforce_count', 'نامشخص')}
        
        **📐 ابعاد و ساختار فیزیکی:**
        - طول: {store_data.get('store_length', 'نامشخص')} متر
        - عرض: {store_data.get('store_width', 'نامشخص')} متر
        - ارتفاع: {store_data.get('store_height', 'نامشخص')} متر
        - تعداد طبقات: {store_data.get('floor_count', 'نامشخص')}
        - موقعیت انبار: {store_data.get('warehouse_location', 'نامشخص')}
        - تعداد ورودی: {store_data.get('entrance_count', 'نامشخص')}
        - تعداد صندوق: {store_data.get('checkout_count', 'نامشخص')}
        - تعداد قفسه: {store_data.get('shelf_count', 'نامشخص')}
        - ابعاد قفسه‌ها: {store_data.get('shelf_dimensions', 'نامشخص')}
        - چیدمان قفسه‌ها: {store_data.get('shelf_layout', 'نامشخص')}
        
        **🎨 طراحی و دکوراسیون:**
        - سبک طراحی: {store_data.get('design_style', 'نامشخص')}
        - رنگ اصلی برند: {store_data.get('primary_brand_color', 'نامشخص')}
        - رنگ ثانویه برند: {store_data.get('secondary_brand_color', 'نامشخص')}
        - رنگ تاکیدی برند: {store_data.get('accent_brand_color', 'نامشخص')}
        - نوع نورپردازی: {store_data.get('lighting_type', 'نامشخص')}
        - شدت نورپردازی: {store_data.get('lighting_intensity', 'نامشخص')}
        - نوع ویترین: {store_data.get('window_display_type', 'نامشخص')}
        - اندازه ویترین: {store_data.get('window_display_size', 'نامشخص')}
        - تم ویترین: {store_data.get('window_display_theme', 'نامشخص')}
        
        **🏗️ مواد و بافت فروشگاه (Material Science & Sensory Design):**
        - جنس کف‌پوش: {store_data.get('floor_material', 'نامشخص')}
        - رنگ کف: {store_data.get('floor_color', 'نامشخص')}
        - پوشش دیوارها: {store_data.get('wall_material', 'نامشخص')}
        - رنگ دیوار: {store_data.get('wall_color', 'نامشخص')}
        - نوع سقف: {store_data.get('ceiling_type', 'نامشخص')}
        - رنگ سقف: {store_data.get('ceiling_color', 'نامشخص')}
        - احساس کلی فضا: {store_data.get('overall_ambiance', 'نامشخص')}
        
        **🎪 نواحی تجربه مشتری (Experience Zones):**
        - منطقه آزمایش محصول: {store_data.get('has_test_zone', 'ندارد')}
        - منطقه استراحت: {store_data.get('has_rest_area', 'ندارد')}
        - منطقه کودکان: {store_data.get('has_kids_zone', 'ندارد')}
        - Wi-Fi رایگان: {store_data.get('has_wifi', 'ندارد')}
        - شارژر موبایل: {store_data.get('has_charging', 'ندارد')}
        - سرویس بهداشتی: {store_data.get('has_restroom', 'ندارد')}
        
        **👥 رفتار و جریان مشتری (Customer Behavior & Flow):**
        - تعداد مشتری روزانه: {store_data.get('daily_customers', 'نامشخص')}
        - زمان حضور مشتریان: {store_data.get('customer_time', 'نامشخص')}
        - جریان مشتریان: {store_data.get('customer_flow', 'نامشخص')}
        - نقاط توقف: {store_data.get('stopping_points', 'نامشخص')}
        - مناطق پرترافیک: {store_data.get('high_traffic_areas', 'نامشخص')}
        
        **💰 فروش و محصولات:**
        - فروش روزانه: {store_data.get('daily_sales', 'نامشخص')} تومان
        - فروش ماهانه: {store_data.get('monthly_sales', 'نامشخص')} تومان
        - تعداد محصولات: {store_data.get('product_count', 'نامشخص')}
        - محصولات پرفروش: {store_data.get('top_products', 'نامشخص')}
        - محصولات گران‌قیمت: {store_data.get('expensive_products', 'نامشخص')}
        - محصولات ارزان‌قیمت: {store_data.get('cheap_products', 'نامشخص')}
        
        **🛡️ امنیت و نظارت:**
        - دوربین نظارتی: {store_data.get('has_cameras', 'ندارد')}
        - تعداد دوربین: {store_data.get('camera_count', 'نامشخص')}
        - مکان‌های نصب دوربین: {store_data.get('camera_locations', 'نامشخص')}
        
        **🏆 تحلیل رقابتی (Competitive Analysis):**
        - تعداد رقبای مستقیم: {store_data.get('direct_competitors_count', 'نامشخص')}
        - نام رقبای اصلی: {store_data.get('main_competitors', 'نامشخص')}
        - نقطه قوت رقبا: {store_data.get('competitors_strength', 'نامشخص')}
        - نقطه قوت شما: {store_data.get('your_strength', 'نامشخص')}
        
        **📅 تحلیل فصلی و رویدادمحور (Seasonal Planning):**
        - فصل پرفروش: {store_data.get('peak_season', 'نامشخص')}
        - رویدادهای مهم: {store_data.get('important_events', 'نامشخص')}
        - تغییر چیدمان فصلی: {store_data.get('seasonal_changes', 'نامشخص')}
        - محصولات فصلی: {store_data.get('seasonal_products', 'نامشخص')}
        
        **🎯 اهداف بهینه‌سازی:**
        - اهداف انتخاب شده: {store_data.get('optimization_goals', 'نامشخص')}
        
        {video_info}
        {sales_info}

        **لطفاً تحلیل جامع ارائه دهید:**

        ## 🎯 تحلیل حرفه‌ای فروشگاه {store_data.get('store_name', 'فروشگاه')}

        ### 📊 امتیاز کلی (1-100)
        [بر اساس تمام عوامل، امتیاز دقیق دهید]

        ### 💪 نقاط قوت استراتژیک
        [حداقل 7 مورد با تحلیل عمیق]

        ### ⚠️ چالش‌های کلیدی
        [حداقل 7 مورد با راه‌حل]

        ### 🎨 تحلیل طراحی و چیدمان
        **نورپردازی:**
        [تحلیل دقیق نورپردازی فعلی و پیشنهادات]

        **رنگ‌بندی:**
        [تحلیل روانشناسی رنگ‌ها و تأثیر بر مشتری]

        **چیدمان محصولات:**
        [تحلیل چیدمان فعلی و بهینه‌سازی]

        ### 🧠 تحلیل روانشناسی مشتری
        **رفتار مشتری:**
        [تحلیل رفتار مشتریان در فروشگاه]

        **تجربه خرید:**
        [تحلیل journey مشتری]

        ### 📈 پتانسیل افزایش فروش
        **تخمین افزایش:**
        [درصد دقیق افزایش فروش با تحلیل]

        **استراتژی‌های کلیدی:**
        [5 استراتژی اصلی برای افزایش فروش]

        ### 🏗️ تحلیل مواد و بافت (Material Science)
        **تحلیل حسی:**
        [تأثیر مواد استفاده شده (کف، دیوار، سقف) روی احساس مشتری]
        
        **پیشنهادات بهبود:**
        [چه موادی را تغییر دهیم و چرا - با تأکید بر تأثیر روانشناختی]
        
        **هماهنگی رنگ و بافت:**
        [تحلیل هماهنگی رنگ کف، دیوار، و سقف]
        
        ### 🎪 تحلیل تجربه مشتری (Experience Zones)
        **وضعیت فعلی:**
        [ارزیابی نواحی تجربه موجود: منطقه آزمایش، استراحت، کودکان، Wi-Fi، سرویس]
        
        **پیشنهادات ارتقاء:**
        [چه نواحی جدیدی اضافه کنیم؟ چگونه نواحی موجود را بهتر کنیم؟]
        
        **تأثیر بر زمان ماندگاری:**
        [چگونه این نواحی باعث افزایش زمان حضور و فروش می‌شوند؟]
        
        ### 🏆 تحلیل رقابتی (Competitive Analysis)
        **موقعیت شما در بازار:**
        [تحلیل SWOT - نقاط قوت، ضعف، فرصت‌ها، تهدیدها]
        
        **برتری رقابتی:**
        [چگونه نقطه قوت خود را برجسته‌تر کنیم؟]
        
        **پر کردن شکاف:**
        [چگونه نقطه قوت رقبا را خنثی کنیم؟]
        
        **استراتژی تمایز:**
        [چگونه متفاوت از رقبا باشیم؟]
        
        ### 📅 تحلیل فصلی و رویدادمحور (Seasonal Planning)
        **فصل پرفروش:**
        [چگونه برای فصل پرفروش آماده شویم؟ چه تغییراتی لازم است؟]
        
        **رویدادهای کلیدی:**
        [چیدمان و تزئینات ویژه برای هر رویداد (نوروز، یلدا، مدرسه، ...)]
        
        **تقویم فصلی:**
        [برنامه دقیق ماه‌به‌ماه برای تغییر چیدمان و معرفی محصولات فصلی]
        
        **پیش‌بینی فروش:**
        [پیش‌بینی افزایش فروش در هر فصل با تحلیل تاریخی]

        ### 🚀 توصیه‌های عملی
        **فوری (1-2 هفته):**
        [اقدامات فوری]

        **کوتاه‌مدت (1-3 ماه):**
        [اقدامات کوتاه‌مدت]

        **بلندمدت (3-12 ماه):**
        [اقدامات بلندمدت]

        **نکته مهم: تمام تحلیل‌ها باید کاملاً شخصی‌سازی شده و مختص این فروشگاه باشد!**
        
        **تأکید نهایی:**
        - فقط از زبان فارسی استفاده کنید
        - هیچ کلمه غیرفارسی در پاسخ نباشد
        - تحلیل باید برای صاحب فروشگاه ایرانی قابل فهم باشد
        - از اصطلاحات تجاری فارسی استفاده کنید
        - تحلیل باید شامل **مواد**، **تجربه**، **رقبا**، و **فصول** باشد
        """
        
        result = self._make_request(self.models['analysis'], prompt, max_tokens=4000)
        if result and 'error' in result:
            return result  # برگرداندن خطا
        if result and 'choices' in result:
            return {
                'type': 'main_analysis',
                'content': result['choices'][0]['message']['content'],
                'model': 'gpt-4-turbo'
            }
        return {
            'error': 'api_request_failed',
            'error_message': 'خطا در دریافت پاسخ از API. لطفاً دوباره تلاش کنید.'
        }
    
    def _analyze_store_design(self, store_data: Dict[str, Any], images: List[str] = None) -> Dict[str, Any]:
        """تحلیل طراحی با Claude-3 Opus"""
        
        prompt = f"""
        شما متخصص طراحی فروشگاه و معماری داخلی هستید. تحلیل حرفه‌ای طراحی برای فروشگاه "{store_data.get('store_name', 'فروشگاه')}" ارائه دهید.

        **اطلاعات طراحی:**
        - نوع فروشگاه: {store_data.get('store_type', 'عمومی')}
        - اندازه: {store_data.get('store_size', 'نامشخص')}
        - چیدمان: {store_data.get('layout_type', 'نامشخص')}
        - نورپردازی: {store_data.get('lighting_type', 'نامشخص')}
        - رنگ‌بندی: {store_data.get('color_scheme', 'نامشخص')}
        - محصولات: {store_data.get('products', 'نامشخص')}

        **تحلیل طراحی حرفه‌ای:**

        ## 🎨 تحلیل طراحی فروشگاه {store_data.get('store_name', 'فروشگاه')}

        ### 🏗️ تحلیل معماری داخلی
        **فضا و جریان:**
        [تحلیل جریان مشتری و بهینه‌سازی فضا]

        **نقاط کانونی:**
        [شناسایی و بهینه‌سازی نقاط کانونی]

        ### 💡 تحلیل نورپردازی
        **نورپردازی فعلی:**
        [تحلیل نورپردازی موجود]

        **بهینه‌سازی نور:**
        [پیشنهادات نورپردازی حرفه‌ای]

        ### 🎨 تحلیل رنگ‌بندی
        **روانشناسی رنگ:**
        [تحلیل تأثیر رنگ‌ها بر مشتری]

        **پالت رنگ بهینه:**
        [پیشنهاد پالت رنگ حرفه‌ای]

        ### 📐 تحلیل چیدمان
        **چیدمان محصولات:**
        [تحلیل و بهینه‌سازی چیدمان]

        **فاصله‌گذاری:**
        [تحلیل فاصله‌گذاری و تراکم]

        ### 🎯 توصیه‌های طراحی
        **بهبودهای فوری:**
        [توصیه‌های فوری طراحی]

        **تحولات بلندمدت:**
        [پیشنهادات تحولی طراحی]

        **نکته: تحلیل باید کاملاً تخصصی و عملی باشد!**
        """
        
        result = self._make_request(self.models['design'], prompt, max_tokens=3000)
        if result and 'error' in result:
            return result  # برگرداندن خطا
        if result and 'choices' in result:
            return {
                'type': 'design_analysis',
                'content': result['choices'][0]['message']['content'],
                'model': 'claude-3-opus'
            }
        return {
            'error': 'api_request_failed',
            'error_message': 'خطا در دریافت پاسخ از API طراحی. لطفاً دوباره تلاش کنید.'
        }
    
    def _analyze_customer_psychology(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل روانشناسی مشتری با Claude-3 Sonnet"""
        
        prompt = f"""
        شما متخصص روانشناسی مصرف‌کننده و رفتارشناسی مشتری هستید. تحلیل روانشناسی برای فروشگاه "{store_data.get('store_name', 'فروشگاه')}" ارائه دهید.

        **اطلاعات فروشگاه:**
        - نوع: {store_data.get('store_type', 'عمومی')}
        - مشتریان روزانه: {store_data.get('daily_customers', 'نامشخص')}
        - فروش روزانه: {store_data.get('daily_sales', 'نامشخص')}
        - محصولات: {store_data.get('products', 'نامشخص')}
        - منطقه: {store_data.get('area', 'نامشخص')}

        **تحلیل روانشناسی مشتری:**

        ## 🧠 تحلیل روانشناسی مشتری - {store_data.get('store_name', 'فروشگاه')}

        ### 👥 پروفایل مشتری
        **مشتریان هدف:**
        [تحلیل دقیق مشتریان هدف]

        **رفتار خرید:**
        [تحلیل الگوهای رفتاری]

        ### 🎯 انگیزه‌های خرید
        **انگیزه‌های اصلی:**
        [شناسایی انگیزه‌های خرید]

        **عوامل تأثیرگذار:**
        [تحلیل عوامل روانی تأثیرگذار]

        ### 🛒 تجربه خرید
        **Journey مشتری:**
        [تحلیل مسیر مشتری در فروشگاه]

        **نقاط تصمیم‌گیری:**
        [شناسایی نقاط کلیدی تصمیم]

        ### 💭 روانشناسی فضا
        **تأثیر محیط:**
        [تحلیل تأثیر محیط بر رفتار]

        **احساسات مشتری:**
        [تحلیل احساسات و واکنش‌ها]

        ### 🎨 روانشناسی بصری
        **تأثیر رنگ‌ها:**
        [تحلیل تأثیر روانی رنگ‌ها]

        **تأثیر نور:**
        [تحلیل تأثیر نور بر روان]

        ### 🚀 استراتژی‌های روانشناسی
        **تکنیک‌های فروش:**
        [تکنیک‌های روانشناسی فروش]

        **بهینه‌سازی تجربه:**
        [بهینه‌سازی تجربه مشتری]

        **نکته: تحلیل باید بر اساس اصول روانشناسی باشد!**
        """
        
        result = self._make_request(self.models['psychology'], prompt, max_tokens=3000)
        if result and 'error' in result:
            return result  # برگرداندن خطا
        if result and 'choices' in result:
            return {
                'type': 'psychology_analysis',
                'content': result['choices'][0]['message']['content'],
                'model': 'claude-3-sonnet'
            }
        return {
            'error': 'api_request_failed',
            'error_message': 'خطا در دریافت پاسخ از API روانشناسی. لطفاً دوباره تلاش کنید.'
        }
    
    def _analyze_marketing_potential(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل بازاریابی با GPT-4o"""
        
        prompt = f"""
        شما متخصص بازاریابی و استراتژی کسب‌وکار هستید. تحلیل بازاریابی برای فروشگاه "{store_data.get('store_name', 'فروشگاه')}" ارائه دهید.

        **اطلاعات کسب‌وکار:**
        - نام: {store_data.get('store_name', 'فروشگاه')}
        - نوع: {store_data.get('store_type', 'عمومی')}
        - منطقه: {store_data.get('area', 'نامشخص')}
        - مشتریان روزانه: {store_data.get('daily_customers', 'نامشخص')}
        - فروش روزانه: {store_data.get('daily_sales', 'نامشخص')}
        - محصولات: {store_data.get('products', 'نامشخص')}

        **تحلیل بازاریابی حرفه‌ای:**

        ## 📈 تحلیل بازاریابی - {store_data.get('store_name', 'فروشگاه')}

        ### 🎯 تحلیل بازار
        **موقعیت رقابتی:**
        [تحلیل موقعیت در بازار]

        **فرصت‌های بازار:**
        [شناسایی فرصت‌های رشد]

        ### 👥 تحلیل مشتری
        **بازار هدف:**
        [تحلیل دقیق بازار هدف]

        **نیازهای مشتری:**
        [شناسایی نیازهای پنهان]

        ### 💰 تحلیل درآمد
        **پتانسیل درآمد:**
        [تحلیل پتانسیل افزایش درآمد]

        **نقاط ضعف درآمد:**
        [شناسایی نقاط ضعف]

        ### 🚀 استراتژی‌های بازاریابی
        **بازاریابی دیجیتال:**
        [استراتژی‌های دیجیتال]

        **بازاریابی محلی:**
        [استراتژی‌های محلی]

        **بازاریابی تجربی:**
        [استراتژی‌های تجربی]

        ### 📊 تحلیل رقابتی
        **مزیت‌های رقابتی:**
        [شناسایی مزیت‌ها]

        **تهدیدات:**
        [تحلیل تهدیدات]

        ### 🎯 برنامه عملیاتی
        **اقدامات فوری:**
        [اقدامات 30 روزه]

        **اقدامات بلندمدت:**
        [اقدامات 6 ماهه]

        **نکته: تحلیل باید عملی و قابل اجرا باشد!**
        """
        
        result = self._make_request(self.models['marketing'], prompt, max_tokens=3000)
        if result and 'error' in result:
            return result  # برگرداندن خطا
        if result and 'choices' in result:
            return {
                'type': 'marketing_analysis',
                'content': result['choices'][0]['message']['content'],
                'model': 'gpt-4o'
            }
        return {
            'error': 'api_request_failed',
            'error_message': 'خطا در دریافت پاسخ از API بازاریابی. لطفاً دوباره تلاش کنید.'
        }
    
    def _analyze_optimization(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل بهینه‌سازی با GPT-4 Turbo"""
        
        prompt = f"""
        شما متخصص بهینه‌سازی فروشگاه و افزایش کارایی هستید. تحلیل بهینه‌سازی برای فروشگاه "{store_data.get('store_name', 'فروشگاه')}" ارائه دهید.

        **اطلاعات فروشگاه:**
        - نام: {store_data.get('store_name', 'فروشگاه')}
        - نوع: {store_data.get('store_type', 'عمومی')}
        - اندازه: {store_data.get('store_size', 'نامشخص')}
        - مشتریان روزانه: {store_data.get('daily_customers', 'نامشخص')}
        - فروش روزانه: {store_data.get('daily_sales', 'نامشخص')}
        - چیدمان: {store_data.get('layout_type', 'نامشخص')}

        **تحلیل بهینه‌سازی حرفه‌ای:**

        ## ⚡ تحلیل بهینه‌سازی - {store_data.get('store_name', 'فروشگاه')}

        ### 📊 تحلیل کارایی
        **نرخ تبدیل:**
        [تحلیل نرخ تبدیل مشتری]

        **کارایی فضا:**
        [تحلیل استفاده از فضا]

        ### 🎯 بهینه‌سازی چیدمان
        **چیدمان محصولات:**
        [بهینه‌سازی چیدمان]

        **جریان مشتری:**
        [بهینه‌سازی جریان]

        ### 💡 بهینه‌سازی نور
        **نورپردازی:**
        [بهینه‌سازی نور]

        **صرفه‌جویی انرژی:**
        [بهینه‌سازی مصرف]

        ### 🎨 بهینه‌سازی بصری
        **رنگ‌بندی:**
        [بهینه‌سازی رنگ‌ها]

        **نمایش محصولات:**
        [بهینه‌سازی نمایش]

        ### 📈 بهینه‌سازی فروش
        **نقاط فروش:**
        [بهینه‌سازی نقاط فروش]

        **تکنیک‌های فروش:**
        [بهینه‌سازی تکنیک‌ها]

        ### 🚀 برنامه بهینه‌سازی
        **مرحله 1 (فوری):**
        [بهینه‌سازی‌های فوری]

        **مرحله 2 (کوتاه‌مدت):**
        [بهینه‌سازی‌های کوتاه‌مدت]

        **مرحله 3 (بلندمدت):**
        [بهینه‌سازی‌های بلندمدت]

        ### 📊 شاخص‌های عملکرد
        **KPI های کلیدی:**
        [تعریف شاخص‌های عملکرد]

        **نحوه اندازه‌گیری:**
        [روش‌های اندازه‌گیری]

        **نکته: تحلیل باید قابل اندازه‌گیری و عملی باشد!**
        """
        
        result = self._make_request(self.models['optimization'], prompt, max_tokens=3000)
        if result and 'error' in result:
            return result  # برگرداندن خطا
        if result and 'choices' in result:
            return {
                'type': 'optimization_analysis',
                'content': result['choices'][0]['message']['content'],
                'model': 'gpt-4-turbo'
            }
        return {
            'error': 'api_request_failed',
            'error_message': 'خطا در دریافت پاسخ از API بهینه‌سازی. لطفاً دوباره تلاش کنید.'
        }
    
    def _combine_analyses(self, analyses: Dict[str, Any], store_data: Dict[str, Any], images: List[str] = None) -> Dict[str, Any]:
        """ترکیب و خلاصه‌سازی تحلیل‌ها"""
        
        if not analyses:
            return self._get_fallback_analysis(store_data)
        
        # استخراج فقط محتوای تحلیل‌ها (نه کل ساختار JSON)
        combined_text = ""
        for key, analysis in analyses.items():
            if analysis and 'content' in analysis:
                combined_text += f"\n\n### {key.upper()} Analysis:\n{analysis['content']}\n"
        
        # ایجاد خلاصه نهایی با محتوای خالص
        summary_prompt = f"""
        شما متخصص نگارش فارسی و تحلیل فروشگاه هستید. 
        
        **قوانین CRITICAL:**
        1. تمام پاسخ به زبان فارسی روان و سلیس باشد
        2. از جملات کامل و حرفه‌ای استفاده کنید
        3. هیچ کلمه انگلیسی در متن نباشد
        4. از اعداد فارسی استفاده کنید
        5. متن باید برای صاحب فروشگاه ایرانی قابل فهم باشد
        
        **تحلیل‌های انجام شده برای فروشگاه "{store_data.get('store_name', 'فروشگاه')}":**
        
        {combined_text}
        
        **حالا لطفاً گزارش نهایی را به زبان فارسی روان و حرفه‌ای بنویسید:**

        ## 🎯 گزارش نهایی تحلیل فروشگاه {store_data.get('store_name', 'فروشگاه')}

        ### 📊 خلاصه اجرایی
        [خلاصه 3-4 خطی از وضعیت کلی]

        ### 🎯 امتیاز کلی
        [امتیاز نهایی 1-100]

        ### 💪 نقاط قوت کلیدی
        [5 نقطه قوت اصلی]

        ### ⚠️ چالش‌های مهم
        [5 چالش اصلی]

        ### 🚀 توصیه‌های اولویت‌دار
        [5 توصیه اولویت‌دار]

        ### 📈 پتانسیل افزایش فروش
        [درصد و توضیح]

        ### 🎯 برنامه عملیاتی
        **فوری (1-2 هفته):**
        [اقدامات فوری]

        **کوتاه‌مدت (1-3 ماه):**
        [اقدامات کوتاه‌مدت]

        **بلندمدت (3-12 ماه):**
        [اقدامات بلندمدت]

        **نکته: گزارش باید جامع، عملی و قابل اجرا باشد!**
        """
        
        result = self._make_request(self.models['summary'], summary_prompt, max_tokens=2000)
        if result and 'error' in result:
            # اگر خطا در خلاصه‌سازی باشد، ولی تحلیل‌های جزئی موفق بوده‌اند، از آن‌ها استفاده کن
            logger.warning(f"⚠️ خطا در خلاصه‌سازی: {result.get('error_message')} - استفاده از تحلیل‌های جزئی")
            # ترکیب دستی تحلیل‌های جزئی
            combined_text = ""
            for key, analysis in analyses.items():
                if analysis and 'content' in analysis:
                    combined_text += f"\n\n### {key.upper()}:\n{analysis['content']}\n"
            
            if combined_text:
                return {
                    'final_report': combined_text[:5000],  # محدود کردن طول
                    'detailed_analyses': analyses,
                    'store_info': store_data,
                    'analysis_timestamp': time.time(),
                    'ai_models_used': list(set([analysis.get('model', 'unknown') for analysis in analyses.values() if analysis])),
                    'warning': 'خلاصه‌سازی با خطا مواجه شد، از تحلیل‌های جزئی استفاده شد'
                }
            else:
                # اگر هیچ تحلیلی وجود ندارد، خطا برگردان
                return {
                    'error': result.get('error', 'summarization_failed'),
                    'error_message': result.get('error_message', 'خطا در خلاصه‌سازی تحلیل'),
                    'detailed_analyses': analyses,
                    'store_info': store_data
                }
        if result and 'choices' in result:
            return {
                'final_report': result['choices'][0]['message']['content'],
                'detailed_analyses': analyses,
                'store_info': store_data,
                'analysis_timestamp': time.time(),
                'ai_models_used': list(set([analysis.get('model', 'unknown') for analysis in analyses.values() if analysis]))
            }
        
        # اگر result None باشد، بررسی کن که آیا تحلیل‌های جزئی وجود دارند
        if analyses:
            logger.warning("⚠️ خلاصه‌سازی با خطا مواجه شد، استفاده از تحلیل‌های جزئی")
            combined_text = ""
            for key, analysis in analyses.items():
                if analysis and 'content' in analysis:
                    combined_text += f"\n\n### {key.upper()}:\n{analysis['content']}\n"
            if combined_text:
                return {
                    'final_report': combined_text[:5000],
                    'detailed_analyses': analyses,
                    'store_info': store_data,
                    'analysis_timestamp': time.time(),
                    'ai_models_used': list(set([analysis.get('model', 'unknown') for analysis in analyses.values() if analysis])),
                    'warning': 'خلاصه‌سازی با خطا مواجه شد'
                }
        
        # فقط در صورت عدم وجود هیچ تحلیلی، به fallback برو
        logger.error("❌ هیچ تحلیلی موفق نبود - استفاده از fallback")
        return self._get_fallback_analysis(store_data)
    
    def _get_fallback_analysis(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """تحلیل fallback در صورت خطا"""
        return {
            'final_report': f"تحلیل فروشگاه {store_data.get('store_name', 'فروشگاه')} در حال پردازش است. لطفاً مجدداً تلاش کنید.",
            'detailed_analyses': {},
            'store_info': store_data,
            'analysis_timestamp': time.time(),
            'ai_models_used': ['fallback'],
            'error': 'خطا در ارتباط با سرویس AI'
        }
    
    def get_ai_insights(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """دریافت بینش‌های AI برای فروشگاه"""
        
        # بررسی cache
        cache_key = f"ai_analysis_{hash(str(store_data))}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # انجام تحلیل
        result = self.analyze_store_comprehensive(store_data)
        
        # ذخیره در cache (1 ساعت)
        cache.set(cache_key, result, 3600)
        
        return result
