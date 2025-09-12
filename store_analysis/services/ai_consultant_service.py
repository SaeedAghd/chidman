"""
سرویس مشاور هوش مصنوعی حرفه‌ای
"""
import logging
from typing import Dict, Any, Optional
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from ..models import AIConsultantSession, AIConsultantQuestion, StoreAnalysis

logger = logging.getLogger(__name__)

class AIConsultantService:
    """سرویس مشاور هوش مصنوعی حرفه‌ای"""
    
    def __init__(self):
        self.free_questions_limit = 3
        self.paid_session_duration = timedelta(days=1)
        self.paid_session_price = 200000  # تومان
    
    def create_consultant_session(self, user, store_analysis: StoreAnalysis) -> AIConsultantSession:
        """ایجاد جلسه مشاوره جدید"""
        try:
            # بررسی وجود جلسه فعال
            existing_session = AIConsultantSession.objects.filter(
                user=user,
                store_analysis=store_analysis,
                status='active'
            ).first()
            
            if existing_session:
                return existing_session
            
            # ایجاد جلسه جدید
            session = AIConsultantSession.objects.create(
                user=user,
                store_analysis=store_analysis,
                expires_at=timezone.now() + timedelta(hours=24)  # 24 ساعت برای سوالات رایگان
            )
            
            logger.info(f"جلسه مشاوره جدید ایجاد شد: {session.session_id}")
            return session
            
        except Exception as e:
            logger.error(f"خطا در ایجاد جلسه مشاوره: {str(e)}")
            raise
    
    def ask_question(self, session: AIConsultantSession, question: str) -> Dict[str, Any]:
        """پرسیدن سوال از مشاور هوش مصنوعی"""
        try:
            start_time = timezone.now()
            
            # بررسی مجوز سوال
            if not session.can_ask_free_question() and not session.can_ask_paid_question():
                return {
                    'success': False,
                    'error': 'محدودیت سوالات تمام شده. برای ادامه باید پرداخت کنید.',
                    'requires_payment': True,
                    'remaining_free': session.get_remaining_free_questions()
                }
            
            # تعیین نوع سوال
            is_free = session.can_ask_free_question()
            
            # ایجاد سوال
            question_obj = AIConsultantQuestion.objects.create(
                session=session,
                question=question,
                is_free=is_free
            )
            
            # تولید پاسخ هوش مصنوعی
            answer = self._generate_ai_response(session, question)
            
            # ذخیره پاسخ
            end_time = timezone.now()
            question_obj.answer = answer
            question_obj.is_answered = True
            question_obj.response_time = end_time - start_time
            question_obj.save()
            
            # به‌روزرسانی آمار جلسه
            if is_free:
                session.free_questions_used += 1
            else:
                session.paid_questions_used += 1
            session.save()
            
            return {
                'success': True,
                'answer': answer,
                'is_free': is_free,
                'remaining_free': session.get_remaining_free_questions(),
                'response_time': str(question_obj.response_time),
                'question_id': question_obj.id
            }
            
        except Exception as e:
            logger.error(f"خطا در پاسخ به سوال: {str(e)}")
            return {
                'success': False,
                'error': 'خطا در تولید پاسخ. لطفاً دوباره تلاش کنید.',
                'requires_payment': False
            }
    
    def _generate_ai_response(self, session: AIConsultantSession, question: str) -> str:
        """تولید پاسخ هوش مصنوعی بر اساس اطلاعات تحلیل"""
        try:
            # دریافت اطلاعات کامل تحلیل
            store_analysis = session.store_analysis
            analysis_data = store_analysis.get_analysis_data()
            results = store_analysis.results or {}
            
            # ساخت context برای پاسخ
            context = self._build_analysis_context(store_analysis, analysis_data, results)
            
            # تولید پاسخ بر اساس context
            response = self._generate_contextual_response(question, context)
            
            return response
            
        except Exception as e:
            logger.error(f"خطا در تولید پاسخ AI: {str(e)}")
            return "متأسفانه در حال حاضر قادر به پاسخ‌دهی نیستم. لطفاً سوال خود را مجدداً مطرح کنید."
    
    def _build_analysis_context(self, store_analysis, analysis_data: Dict, results: Dict) -> Dict[str, Any]:
        """ساخت context کامل از اطلاعات تحلیل"""
        context = {
            'store_info': {
                'name': store_analysis.store_name or 'نامشخص',
                'type': store_analysis.store_type or 'نامشخص',
                'size': store_analysis.store_size or 'نامشخص',
                'description': store_analysis.description or 'توضیحی ارائه نشده'
            },
            'analysis_results': results,
            'data_completeness': results.get('data_completeness', {}),
            'recommendations': results.get('recommendations', []),
            'key_insights': results.get('key_insights', []),
            'overall_score': results.get('overall_score', 0),
            'analysis_confidence': results.get('analysis_confidence', 'متوسط')
        }
        
        # اضافه کردن اطلاعات اضافی از analysis_data
        if analysis_data:
            context['additional_data'] = analysis_data
        
        return context
    
    def _generate_contextual_response(self, question: str, context: Dict[str, Any]) -> str:
        """تولید پاسخ بر اساس context تحلیل"""
        try:
            # تحلیل سوال و تولید پاسخ مناسب
            store_info = context['store_info']
            results = context['analysis_results']
            recommendations = context.get('recommendations', [])
            insights = context.get('key_insights', [])
            
            # پاسخ‌های پیش‌فرض بر اساس نوع سوال
            if 'چیدمان' in question or 'layout' in question.lower():
                return self._generate_layout_response(store_info, results, recommendations)
            elif 'ترافیک' in question or 'traffic' in question.lower():
                return self._generate_traffic_response(store_info, results, recommendations)
            elif 'مشتری' in question or 'customer' in question.lower():
                return self._generate_customer_response(store_info, results, recommendations)
            elif 'بهبود' in question or 'improve' in question.lower():
                return self._generate_improvement_response(store_info, results, recommendations)
            elif 'نمره' in question or 'score' in question.lower():
                return self._generate_score_response(store_info, results)
            else:
                return self._generate_general_response(question, store_info, results, recommendations, insights)
                
        except Exception as e:
            logger.error(f"خطا در تولید پاسخ contextual: {str(e)}")
            return "متأسفانه در حال حاضر قادر به پاسخ‌دهی نیستم. لطفاً سوال خود را مجدداً مطرح کنید."
    
    def _generate_layout_response(self, store_info, results, recommendations):
        """پاسخ مربوط به چیدمان"""
        layout_analysis = results.get('layout_analysis', {})
        score = layout_analysis.get('score', 0)
        
        response = f"بر اساس تحلیل چیدمان فروشگاه {store_info['name']}:\n\n"
        response += f"نمره چیدمان: {score}/10\n\n"
        
        if score >= 8:
            response += "✅ چیدمان شما عالی است! "
        elif score >= 6:
            response += "⚠️ چیدمان شما قابل قبول است اما قابل بهبود است. "
        else:
            response += "❌ چیدمان شما نیاز به بازنگری دارد. "
        
        if recommendations:
            response += "\n\nتوصیه‌های بهبود:\n"
            for i, rec in enumerate(recommendations[:3], 1):
                response += f"{i}. {rec}\n"
        
        return response
    
    def _generate_traffic_response(self, store_info, results, recommendations):
        """پاسخ مربوط به ترافیک"""
        traffic_analysis = results.get('traffic_analysis', {})
        score = traffic_analysis.get('score', 0)
        
        response = f"بر اساس تحلیل ترافیک فروشگاه {store_info['name']}:\n\n"
        response += f"نمره ترافیک: {score}/10\n\n"
        
        if score >= 8:
            response += "✅ مدیریت ترافیک شما عالی است! "
        elif score >= 6:
            response += "⚠️ ترافیک شما قابل قبول است اما قابل بهبود است. "
        else:
            response += "❌ ترافیک شما نیاز به بازنگری دارد. "
        
        if recommendations:
            response += "\n\nتوصیه‌های بهبود ترافیک:\n"
            for i, rec in enumerate(recommendations[:3], 1):
                response += f"{i}. {rec}\n"
        
        return response
    
    def _generate_customer_response(self, store_info, results, recommendations):
        """پاسخ مربوط به مشتریان"""
        customer_analysis = results.get('customer_behavior', {})
        score = customer_analysis.get('score', 0)
        
        response = f"بر اساس تحلیل رفتار مشتریان فروشگاه {store_info['name']}:\n\n"
        response += f"نمره رفتار مشتری: {score}/10\n\n"
        
        if score >= 8:
            response += "✅ رفتار مشتریان شما عالی است! "
        elif score >= 6:
            response += "⚠️ رفتار مشتریان قابل قبول است اما قابل بهبود است. "
        else:
            response += "❌ رفتار مشتریان نیاز به بازنگری دارد. "
        
        if recommendations:
            response += "\n\nتوصیه‌های بهبود رفتار مشتری:\n"
            for i, rec in enumerate(recommendations[:3], 1):
                response += f"{i}. {rec}\n"
        
        return response
    
    def _generate_improvement_response(self, store_info, results, recommendations):
        """پاسخ مربوط به بهبود"""
        overall_score = results.get('overall_score', 0)
        
        response = f"بر اساس تحلیل کلی فروشگاه {store_info['name']}:\n\n"
        response += f"نمره کلی: {overall_score}/10\n\n"
        
        if overall_score >= 8:
            response += "🎉 فروشگاه شما عملکرد عالی دارد! "
        elif overall_score >= 6:
            response += "📈 فروشگاه شما عملکرد خوبی دارد اما قابل بهبود است. "
        else:
            response += "🔧 فروشگاه شما نیاز به بهبودهای اساسی دارد. "
        
        if recommendations:
            response += "\n\nاولویت‌های بهبود:\n"
            for i, rec in enumerate(recommendations[:5], 1):
                response += f"{i}. {rec}\n"
        
        return response
    
    def _generate_score_response(self, store_info, results):
        """پاسخ مربوط به نمره"""
        overall_score = results.get('overall_score', 0)
        confidence = results.get('analysis_confidence', 'متوسط')
        
        response = f"نمره کلی فروشگاه {store_info['name']}: {overall_score}/10\n\n"
        response += f"سطح اطمینان تحلیل: {confidence}\n\n"
        
        if overall_score >= 8:
            response += "🌟 عالی! فروشگاه شما عملکرد برجسته‌ای دارد."
        elif overall_score >= 6:
            response += "👍 خوب! فروشگاه شما عملکرد قابل قبولی دارد."
        elif overall_score >= 4:
            response += "⚠️ متوسط! فروشگاه شما نیاز به بهبود دارد."
        else:
            response += "🔧 ضعیف! فروشگاه شما نیاز به بازنگری اساسی دارد."
        
        return response
    
    def _generate_general_response(self, question, store_info, results, recommendations, insights):
        """پاسخ عمومی"""
        overall_score = results.get('overall_score', 0)
        
        response = f"بر اساس تحلیل فروشگاه {store_info['name']}:\n\n"
        response += f"نمره کلی: {overall_score}/10\n\n"
        
        if insights:
            response += "نکات کلیدی:\n"
            for i, insight in enumerate(insights[:3], 1):
                response += f"{i}. {insight}\n"
        
        if recommendations:
            response += "\nتوصیه‌های کلی:\n"
            for i, rec in enumerate(recommendations[:3], 1):
                response += f"{i}. {rec}\n"
        
        response += "\n💡 برای سوالات تخصصی‌تر، می‌توانید سوالات بیشتری بپرسید."
        
        return response
    
    def get_session_status(self, session: AIConsultantSession) -> Dict[str, Any]:
        """دریافت وضعیت جلسه"""
        return {
            'session_id': str(session.session_id),
            'is_active': session.status == 'active',
            'is_paid': session.is_paid,
            'free_questions_used': session.free_questions_used,
            'free_questions_remaining': session.get_remaining_free_questions(),
            'paid_questions_used': session.paid_questions_used,
            'expires_at': session.expires_at,
            'can_ask_free': session.can_ask_free_question(),
            'can_ask_paid': session.can_ask_paid_question(),
            'requires_payment': not session.can_ask_free_question() and not session.is_paid
        }
