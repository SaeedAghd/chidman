"""
Chat Views - مدیریت چت‌بات هوشمند AI Consultant
"""

import logging
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import StoreAnalysis, ChatSession, ChatMessage
from .ai_services.ai_consultant_service import AIConsultantService

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET"])
def ai_consultant_chat(request, analysis_id):
    """
    صفحه چت با AI Consultant
    """
    try:
        # دریافت تحلیل
        store_analysis = get_object_or_404(
            StoreAnalysis,
            id=analysis_id,
            user=request.user
        )
        
        # پیدا کردن یا ایجاد جلسه چت
        chat_session, created = ChatSession.objects.get_or_create(
            user=request.user,
            store_analysis=store_analysis,
            is_active=True,
            defaults={'title': f'مشاوره فروشگاه {store_analysis.store_name}'}
        )
        
        # دریافت پیام‌های جلسه
        messages = chat_session.messages.all()
        
        # پیشنهاد سوالات
        ai_consultant = AIConsultantService()
        suggested_questions = ai_consultant.suggest_questions(store_analysis)
        
        context = {
            'store_analysis': store_analysis,
            'chat_session': chat_session,
            'messages': messages,
            'suggested_questions': suggested_questions,
            'is_new_session': created
        }
        
        return render(request, 'store_analysis/ai_consultant_chat.html', context)
        
    except Exception as e:
        logger.error(f"Error in ai_consultant_chat: {e}", exc_info=True)
        return redirect('store_analysis:user_dashboard')


@login_required
@require_http_methods(["POST"])
@csrf_exempt  # برای سادگی - در production باید CSRF token استفاده شود
def ai_consultant_send(request, analysis_id):
    """
    ارسال پیام به AI Consultant و دریافت پاسخ
    """
    try:
        # پارس کردن body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = {
                'message': request.POST.get('message', ''),
                'session_id': request.POST.get('session_id')
            }
        
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not user_message:
            return JsonResponse({
                'success': False,
                'error': 'پیام خالی است'
            }, status=400)
        
        # دریافت تحلیل و جلسه چت
        store_analysis = get_object_or_404(
            StoreAnalysis,
            id=analysis_id,
            user=request.user
        )
        
        if session_id:
            chat_session = get_object_or_404(
                ChatSession,
                id=session_id,
                user=request.user,
                store_analysis=store_analysis
            )
        else:
            # ایجاد جلسه جدید
            chat_session = ChatSession.objects.create(
                user=request.user,
                store_analysis=store_analysis,
                title=f'مشاوره فروشگاه {store_analysis.store_name}'
            )
        
        # بررسی محدودیت سوال (10 سوال رایگان)
        if not chat_session.has_free_questions_left():
            return JsonResponse({
                'success': False,
                'error': 'شما از 10 سوال رایگان استفاده کرده‌اید.',
                'upgrade_required': True,
                'upgrade_message': 'برای پرسیدن سوالات بیشتر، پلن پریمیوم 3 ساعته (200,000 تومان) تهیه کنید.',
                'questions_used': chat_session.get_user_questions_count(),
                'free_limit': 10
            }, status=403)
        
        # ذخیره پیام کاربر
        user_chat_message = ChatMessage.objects.create(
            session=chat_session,
            role='user',
            content=user_message
        )
        
        # دریافت تاریخچه چت
        chat_history = list(chat_session.messages.values('role', 'content').order_by('created_at')[:20])
        
        # ارسال به AI
        ai_consultant = AIConsultantService()
        ai_response = ai_consultant.chat_with_analysis(
            user_message=user_message,
            store_analysis=store_analysis,
            chat_history=chat_history[:-1]  # بدون پیام جاری
        )
        
        # ذخیره پاسخ AI
        assistant_message = ChatMessage.objects.create(
            session=chat_session,
            role='assistant',
            content=ai_response['response'],
            ai_model=ai_response.get('ai_model'),
            processing_time=ai_response.get('processing_time'),
            tokens_used=ai_response.get('tokens_used')
        )
        
        return JsonResponse({
            'success': True,
            'session_id': str(chat_session.id),
            'user_message': {
                'id': str(user_chat_message.id),
                'role': 'user',
                'content': user_chat_message.content,
                'created_at': user_chat_message.created_at.isoformat()
            },
            'assistant_message': {
                'id': str(assistant_message.id),
                'role': 'assistant',
                'content': assistant_message.content,
                'ai_model': assistant_message.ai_model,
                'processing_time': assistant_message.processing_time,
                'created_at': assistant_message.created_at.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Error in ai_consultant_send: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

