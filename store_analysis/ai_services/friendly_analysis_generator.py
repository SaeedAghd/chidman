"""
تولیدکننده تحلیل دوستانه و زیبا
خروجی ساده و قابل فهم برای مغازه‌داران
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class FriendlyAnalysisGenerator:
    """تولیدکننده تحلیل دوستانه و زیبا"""
    
    def __init__(self):
        self.friendly_templates = self._load_friendly_templates()
        self.emojis = {
            'success': '✅',
            'warning': '⚠️',
            'info': 'ℹ️',
            'money': '💰',
            'customers': '👥',
            'products': '📦',
            'light': '💡',
            'star': '⭐',
            'chart': '📊',
            'heart': '❤️',
            'fire': '🔥',
            'rocket': '🚀',
            'trophy': '🏆',
            'target': '🎯',
            'clock': '⏰',
            'location': '📍',
            'phone': '📞',
            'shopping': '🛒',
            'smile': '😊',
            'thumbs_up': '👍',
            'thinking': '🤔',
            'celebration': '🎉'
        }
    
    def _load_friendly_templates(self) -> Dict[str, List[str]]:
        """بارگذاری قالب‌های دوستانه"""
        return {
            'greetings': [
                "سلام! من تحلیلگر هوشمند فروشگاه شما هستم 😊",
                "درود! بیایید فروشگاه شما را بهتر کنیم 🚀",
                "سلام عزیز! آماده‌ام تا فروشگاه شما را تحلیل کنم 💡",
                "درود بر شما! من اینجا هستم تا کمک‌تان کنم ⭐"
            ],
            'compliments': [
                "فروشگاه شما پتانسیل زیادی دارد! 🔥",
                "کار خوبی انجام داده‌اید! 👍",
                "فروشگاه شما زیبا و منظم است! 😊",
                "مشتریان شما خوش‌شانس هستند! ❤️"
            ],
            'encouragement': [
                "نگران نباشید، همه چیز قابل بهبود است! 💪",
                "با کمی تلاش، فروشگاه شما عالی می‌شود! 🌟",
                "هر قدم کوچک، شما را به موفقیت نزدیک‌تر می‌کند! 🎯",
                "من اینجا هستم تا راهنماییتان کنم! 🤝"
            ],
            'action_starters': [
                "بیایید شروع کنیم:",
                "اولین قدم این است:",
                "برای شروع، این کار را انجام دهید:",
                "حالا وقت آن است که:"
            ],
            'success_predictions': [
                "با این تغییرات، فروش شما افزایش خواهد یافت! 📈",
                "مشتریان شما راضی‌تر خواهند شد! 😊",
                "پول بیشتری درمی‌آورید! 💰",
                "فروشگاه شما محبوب‌تر می‌شود! 🏆"
            ]
        }
    
    def generate_friendly_analysis(self, store_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """تولید تحلیل دوستانه و زیبا"""
        
        store_name = store_data.get('store_name', 'فروشگاه شما')
        store_type = store_data.get('store_type', 'عمومی')
        
        # انتخاب تصادفی از قالب‌ها
        greeting = random.choice(self.friendly_templates['greetings'])
        compliment = random.choice(self.friendly_templates['compliments'])
        
        # تولید تحلیل دوستانه
        friendly_analysis = {
            'header': {
                'title': f"گزارش تحلیل فروشگاه {store_name}",
                'subtitle': "تحلیل هوشمند و راهنمای عملی",
                'date': datetime.now().strftime('%Y/%m/%d'),
                'greeting': greeting
            },
            'overview': self._generate_overview(store_data, analysis_results),
            'scores': self._generate_friendly_scores(analysis_results),
            'strengths': self._generate_friendly_strengths(store_data, analysis_results),
            'improvements': self._generate_friendly_improvements(store_data, analysis_results),
            'action_plan': self._generate_friendly_action_plan(store_data, analysis_results),
            'predictions': self._generate_friendly_predictions(store_data, analysis_results),
            'tips': self._generate_friendly_tips(store_data, analysis_results),
            'conclusion': self._generate_friendly_conclusion(store_data, analysis_results)
        }
        
        return friendly_analysis
    
    def _generate_overview(self, store_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """تولید خلاصه دوستانه"""
        store_name = store_data.get('store_name', 'فروشگاه شما')
        store_type = store_data.get('store_type', 'عمومی')
        store_size = store_data.get('store_size', 'نامشخص')
        
        return {
            'title': f"نگاه کلی به {store_name}",
            'content': f"""
            {self.emojis['location']} **نام فروشگاه:** {store_name}
            {self.emojis['shopping']} **نوع فروشگاه:** {store_type}
            {self.emojis['chart']} **اندازه فروشگاه:** {store_size} متر مربع
            
            {self.emojis['heart']} **پیام من به شما:**
            سلام! من تمام اطلاعات فروشگاه شما را بررسی کردم و تحلیل کاملی انجام دادم. 
            نگران نباشید، من اینجا هستم تا کمکتان کنم فروشگاهتان را بهتر کنید!
            """,
            'highlight': "هر فروشگاهی پتانسیل رشد دارد و شما هم می‌توانید! 💪"
        }
    
    def _generate_friendly_scores(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """تولید امتیازات دوستانه"""
        overall_score = analysis_results.get('overall_score', 0.6)
        score_percentage = int(overall_score * 100)
        
        # تعیین وضعیت بر اساس امتیاز
        if score_percentage >= 80:
            status = "عالی"
            emoji = "🏆"
            message = "فروشگاه شما در وضعیت بسیار خوبی است!"
        elif score_percentage >= 60:
            status = "خوب"
            emoji = "⭐"
            message = "فروشگاه شما خوب است، اما می‌تواند بهتر شود!"
        else:
            status = "نیاز به بهبود"
            emoji = "💡"
            message = "فروشگاه شما نیاز به بهبود دارد، اما نگران نباشید!"
        
        return {
            'title': f"امتیاز کلی فروشگاه شما {emoji}",
            'score': score_percentage,
            'status': status,
            'message': message,
            'details': [
                f"{self.emojis['chart']} امتیاز شما: {score_percentage} از 100",
                f"{self.emojis['thinking']} وضعیت: {status}",
                f"{self.emojis['heart']} {message}"
            ]
        }
    
    def _generate_friendly_strengths(self, store_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """تولید نقاط قوت دوستانه"""
        store_name = store_data.get('store_name', 'فروشگاه شما')
        
        strengths = [
            f"{self.emojis['thumbs_up']} فروشگاه {store_name} در موقعیت خوبی قرار دارد",
            f"{self.emojis['customers']} مشتریان شما راضی هستند",
            f"{self.emojis['products']} محصولات شما متنوع و جذاب است",
            f"{self.emojis['location']} موقعیت فروشگاه شما مناسب است",
            f"{self.emojis['smile']} شما صاحب فروشگاه خوبی هستید"
        ]
        
        return {
            'title': f"نقاط قوت {store_name} {self.emojis['star']}",
            'subtitle': "چیزهایی که در فروشگاه شما خوب است:",
            'items': strengths,
            'message': "این نقاط قوت را حفظ کنید و تقویت کنید! 💪"
        }
    
    def _generate_friendly_improvements(self, store_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """تولید پیشنهادات بهبود دوستانه"""
        store_name = store_data.get('store_name', 'فروشگاه شما')
        
        improvements = [
            f"{self.emojis['light']} نور فروشگاه را بهتر کنید",
            f"{self.emojis['products']} کالاها را بهتر بچینید",
            f"{self.emojis['customers']} با مشتریان بهتر صحبت کنید",
            f"{self.emojis['money']} قیمت‌ها را واضح بنویسید",
            f"{self.emojis['shopping']} فروشگاه را تمیز نگه دارید",
            f"{self.emojis['phone']} در اینترنت بیشتر دیده شوید"
        ]
        
        return {
            'title': f"راه‌های بهتر کردن {store_name} {self.emojis['rocket']}",
            'subtitle': "این کارها را انجام دهید تا فروشگاهتان بهتر شود:",
            'items': improvements,
            'message': "هر کدام از این کارها، فروش شما را بیشتر می‌کند! 📈"
        }
    
    def _generate_friendly_action_plan(self, store_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """تولید برنامه عملی دوستانه"""
        store_name = store_data.get('store_name', 'فروشگاه شما')
        
        return {
            'title': f"برنامه عملی برای {store_name} {self.emojis['target']}",
            'phases': [
                {
                    'title': f"مرحله اول: کارهای فوری {self.emojis['clock']}",
                    'duration': "این هفته",
                    'items': [
                        f"{self.emojis['light']} نور فروشگاه را بهتر کنید",
                        f"{self.emojis['products']} کالاها را مرتب بچینید",
                        f"{self.emojis['money']} قیمت‌ها را واضح بنویسید"
                    ],
                    'message': "این کارها را همین هفته انجام دهید! ⚡"
                },
                {
                    'title': f"مرحله دوم: کارهای مهم {self.emojis['star']}",
                    'duration': "این ماه",
                    'items': [
                        f"{self.emojis['customers']} با مشتریان بهتر صحبت کنید",
                        f"{self.emojis['shopping']} فروشگاه را تمیز نگه دارید",
                        f"{self.emojis['phone']} در اینترنت بیشتر دیده شوید"
                    ],
                    'message': "این کارها را این ماه انجام دهید! 📅"
                },
                {
                    'title': f"مرحله سوم: کارهای بلندمدت {self.emojis['rocket']}",
                    'duration': "سه ماه آینده",
                    'items': [
                        f"{self.emojis['products']} کالاهای جدید اضافه کنید",
                        f"{self.emojis['customers']} مشتریان را تشویق کنید",
                        f"{self.emojis['chart']} فروش را بهتر کنید"
                    ],
                    'message': "این کارها را در سه ماه آینده انجام دهید! 🎯"
                }
            ]
        }
    
    def _generate_friendly_predictions(self, store_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """تولید پیش‌بینی‌های دوستانه"""
        store_name = store_data.get('store_name', 'فروشگاه شما')
        
        return {
            'title': f"پیش‌بینی آینده {store_name} {self.emojis['crystal_ball']}",
            'predictions': [
                f"{self.emojis['money']} فروش شما ۲۰ درصد بیشتر می‌شود",
                f"{self.emojis['customers']} مشتریان شما راضی‌تر می‌شوند",
                f"{self.emojis['chart']} پول بیشتری درمی‌آورید",
                f"{self.emojis['trophy']} فروشگاه شما محبوب‌تر می‌شود"
            ],
            'timeline': {
                '1_month': f"{self.emojis['clock']} یک ماه: تغییرات کوچک",
                '3_months': f"{self.emojis['star']} سه ماه: بهبود قابل توجه",
                '6_months': f"{self.emojis['rocket']} شش ماه: موفقیت بزرگ"
            },
            'message': "اگر این کارها را انجام دهید، نتایج عالی خواهید گرفت! 🎉"
        }
    
    def _generate_friendly_tips(self, store_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """تولید نکات دوستانه"""
        store_name = store_data.get('store_name', 'فروشگاه شما')
        
        tips = [
            f"{self.emojis['heart']} همیشه با مشتریان با لبخند صحبت کنید",
            f"{self.emojis['light']} نور فروشگاه را روشن و دلنشین نگه دارید",
            f"{self.emojis['products']} کالاها را مرتب و زیبا بچینید",
            f"{self.emojis['money']} قیمت‌ها را واضح و خوانا بنویسید",
            f"{self.emojis['shopping']} فروشگاه را همیشه تمیز نگه دارید",
            f"{self.emojis['customers']} از مشتریان نظر بخواهید",
            f"{self.emojis['phone']} در شبکه‌های اجتماعی فعال باشید",
            f"{self.emojis['chart']} فروش روزانه را یادداشت کنید"
        ]
        
        return {
            'title': f"نکات طلایی برای {store_name} {self.emojis['gold']}",
            'subtitle': "این نکات را همیشه به یاد داشته باشید:",
            'items': tips,
            'message': "این نکات ساده، فروش شما را دو برابر می‌کند! 💎"
        }
    
    def _generate_friendly_conclusion(self, store_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """تولید نتیجه‌گیری دوستانه"""
        store_name = store_data.get('store_name', 'فروشگاه شما')
        
        return {
            'title': f"پیام نهایی من به شما {self.emojis['heart']}",
            'content': f"""
            {self.emojis['smile']} **عزیز من،**
            
            من تمام اطلاعات فروشگاه {store_name} شما را بررسی کردم و راه‌های بهتر کردن آن را پیدا کردم.
            
            {self.emojis['thumbs_up']} **نگران نباشید!** هر فروشگاهی می‌تواند بهتر شود و شما هم می‌توانید!
            
            {self.emojis['rocket']} **اگر این کارها را انجام دهید:**
            - فروش شما بیشتر می‌شود
            - مشتریان شما راضی‌تر می‌شوند  
            - پول بیشتری درمی‌آورید
            - فروشگاه شما محبوب‌تر می‌شود
            
            {self.emojis['heart']} **من اینجا هستم تا کمکتان کنم!** اگر سوالی دارید، بپرسید.
            
            {self.emojis['celebration']} **موفق باشید!** امیدوارم فروشگاه شما روز به روز بهتر شود.
            
            با احترام،
            تحلیلگر هوشمند فروشگاه شما 🤖
            """,
            'signature': "تحلیلگر هوشمند فروشگاه شما 🤖"
        }
