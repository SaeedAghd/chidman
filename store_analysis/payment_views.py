"""
Payment Views for Ping Payment Gateway
Professional implementation with comprehensive error handling
"""

import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
from .models import Payment, PaymentLog, ServicePackage, UserSubscription
from .payment_services import PaymentManager
from .forms import PaymentForm
from .utils.safe_db import check_table_exists

logger = logging.getLogger(__name__)

# Initialize payment manager
payment_manager = PaymentManager()


def safe_create_payment_log(payment, log_type, message, data=None):
    """ایجاد PaymentLog با بررسی وجود جدول"""
    table_name = 'store_analysis_paymentlog'
    if check_table_exists(table_name):
        try:
            PaymentLog.objects.create(
                payment=payment,
                log_type=log_type,
                message=message,
                data=data
            )
        except Exception as e:
            logger.warning(f"Could not create PaymentLog: {e}")
    else:
        logger.debug(f"PaymentLog table does not exist, skipping log creation")

@login_required
def payment_packages(request):
    """
    Display available payment packages
    """
    try:
        packages = ServicePackage.objects.filter(is_active=True).order_by('sort_order', 'price')
        
        context = {
            'packages': packages,
            'title': 'بسته‌های خدمات',
            'description': 'انتخاب بسته مناسب برای تحلیل فروشگاه شما'
        }
        
        return render(request, 'store_analysis/payment_packages.html', context)
        
    except Exception as e:
        logger.error(f"Error displaying payment packages: {e}")
        messages.error(request, 'خطا در نمایش بسته‌های پرداخت')
        return redirect('store_analysis:user_dashboard')

@login_required
def create_payment(request, package_id):
    """
    Create payment for selected package
    """
    try:
        package = get_object_or_404(ServicePackage, id=package_id, is_active=True)
        
        if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                # Get customer info from form
                customer_info = {
                    'name': form.cleaned_data.get('customer_name', ''),
                    'email': form.cleaned_data.get('customer_email', ''),
                    'phone': form.cleaned_data.get('customer_phone', ''),
                }
                
                # Generate unique order ID
                order_id = f"CHD_{package.id}_{int(timezone.now().timestamp())}"
                
                # Create payment record
                payment = Payment.objects.create(
                    user=request.user,
                    order_id=order_id,
                    amount=package.price,
                    currency=package.currency,
                    description=f"خرید بسته {package.name}",
                    customer_name=customer_info.get('name', ''),
                    customer_email=customer_info.get('email', ''),
                    customer_phone=customer_info.get('phone', ''),
                    payment_method='ping_payment',
                    status='pending',
                    is_test=settings.PAYMENT_GATEWAY['PING_PAYMENT']['SANDBOX']
                )
                
                # Log payment creation
                safe_create_payment_log(
                    payment=payment,
                    log_type='payment_created',
                    message=f'Payment created for package {package.name}',
                    data={'package_id': package.id, 'amount': str(package.price)}
                )
                
                # Process payment with Ping Payment
                payment_result = payment_manager.process_payment(
                    amount=package.price,
                    order_id=order_id,
                    description=f"خرید بسته {package.name}",
                    customer_info=customer_info
                )
                
                if payment_result['success']:
                    # Update payment with gateway response
                    payment.payment_id = payment_result.get('payment_id')
                    payment.transaction_id = payment_result.get('transaction_id')
                    payment.gateway_response = payment_result
                    payment.status = 'processing'
                    payment.save()
                    
                    # Log payment processing
                    safe_create_payment_log(
                        payment=payment,
                        log_type='payment_redirected',
                        message='User redirected to payment gateway',
                        data=payment_result
                    )
                    
                    # Redirect to payment gateway
                    return redirect(payment_result['payment_url'])
                else:
                    # Payment creation failed
                    payment.status = 'failed'
                    payment.save()
                    
                    safe_create_payment_log(
                        payment=payment,
                        log_type='error',
                        message=f'Payment creation failed: {payment_result.get("error", "Unknown error")}',
                        data=payment_result
                    )
                    
                    messages.error(request, f'خطا در ایجاد پرداخت: {payment_result.get("error", "خطای نامشخص")}')
                    return redirect('store_analysis:payment_packages')
            else:
                messages.error(request, 'لطفاً اطلاعات را به درستی وارد کنید')
        else:
            form = PaymentForm(initial={
                'customer_name': request.user.get_full_name() or request.user.username,
                'customer_email': request.user.email,
            })
        
        context = {
            'package': package,
            'form': form,
            'title': f'پرداخت بسته {package.name}',
            'description': f'پرداخت مبلغ {package.price:,} {package.currency} برای بسته {package.name}'
        }
        
        return render(request, 'store_analysis/create_payment.html', context)
        
    except Exception as e:
        logger.error(f"Error creating payment: {e}")
        messages.error(request, 'خطا در ایجاد پرداخت')
        return redirect('store_analysis:payment_packages')

@csrf_exempt
@require_http_methods(["POST"])
def payment_callback(request):
    """
    Handle payment callback from Ping Payment
    """
    try:
        # Get callback data
        callback_data = json.loads(request.body) if request.body else {}
        
        # Log callback
        logger.info(f"Payment callback received: {callback_data}")
        
        # Get payment ID from callback
        payment_id = callback_data.get('payment_id')
        if not payment_id:
            return JsonResponse({'status': 'error', 'message': 'Payment ID not provided'})
        
        # Get payment record
        try:
            payment = Payment.objects.get(payment_id=payment_id)
        except Payment.DoesNotExist:
            logger.error(f"Payment not found: {payment_id}")
            return JsonResponse({'status': 'error', 'message': 'Payment not found'})
        
        # Handle callback
        callback_result = payment_manager.handle_callback(callback_data)
        
        # Log callback
        safe_create_payment_log(
            payment=payment,
            log_type='payment_callback',
            message='Payment callback received',
            data=callback_data
        )
        
        if callback_result['success']:
            if callback_result['status'] == 'completed':
                # Payment successful
                payment.status = 'completed'
                payment.completed_at = timezone.now()
                payment.callback_data = callback_data
                payment.save()
                
                # Create user subscription
                package = ServicePackage.objects.get(id=payment.description.split()[-1])
                subscription = UserSubscription.objects.create(
                    user=payment.user,
                    package=package,
                    payment=payment,
                    end_date=timezone.now() + timezone.timedelta(days=package.validity_days),
                    max_analyses=package.max_analyses
                )
                
                # Log success
                safe_create_payment_log(
                    payment=payment,
                    log_type='payment_verified',
                    message='Payment verified and subscription created',
                    data=callback_result
                )
                
                return JsonResponse({'status': 'success', 'message': 'Payment completed'})
            else:
                # Payment failed
                payment.status = 'failed'
                payment.callback_data = callback_data
                payment.save()
                
                safe_create_payment_log(
                    payment=payment,
                    log_type='payment_failed',
                    message='Payment failed',
                    data=callback_result
                )
                
                return JsonResponse({'status': 'failed', 'message': 'Payment failed'})
        else:
            # Callback handling failed
            safe_create_payment_log(
                payment=payment,
                log_type='error',
                message=f'Callback handling failed: {callback_result.get("error", "Unknown error")}',
                data=callback_result
            )
            
            return JsonResponse({'status': 'error', 'message': 'Callback handling failed'})
            
    except Exception as e:
        logger.error(f"Error handling payment callback: {e}")
        return JsonResponse({'status': 'error', 'message': 'Internal server error'})

@login_required
def payment_return(request):
    """
    Handle payment return from gateway
    """
    try:
        payment_id = request.GET.get('payment_id')
        status = request.GET.get('status')
        
        if not payment_id:
            messages.error(request, 'شناسه پرداخت یافت نشد')
            return redirect('store_analysis:user_dashboard')
        
        # Get payment record
        try:
            payment = Payment.objects.get(payment_id=payment_id, user=request.user)
        except Payment.DoesNotExist:
            messages.error(request, 'پرداخت یافت نشد')
            return redirect('store_analysis:user_dashboard')
        
        # Check payment status
        if payment.status == 'completed':
            messages.success(request, 'پرداخت با موفقیت انجام شد! اشتراک شما فعال شده است.')
            return redirect('store_analysis:user_dashboard')
        elif payment.status == 'failed':
            messages.error(request, 'پرداخت ناموفق بود. لطفاً دوباره تلاش کنید.')
            return redirect('store_analysis:payment_packages')
        else:
            messages.info(request, 'پرداخت در حال پردازش است. لطفاً چند دقیقه صبر کنید.')
            return redirect('store_analysis:user_dashboard')
            
    except Exception as e:
        logger.error(f"Error handling payment return: {e}")
        messages.error(request, 'خطا در بازگشت از درگاه پرداخت')
        return redirect('store_analysis:user_dashboard')

@login_required
def payment_history(request):
    """
    Display user payment history
    """
    try:
        payments = Payment.objects.filter(user=request.user).order_by('-created_at')
        
        context = {
            'payments': payments,
            'title': 'تاریخچه پرداخت‌ها',
            'description': 'مشاهده تمام پرداخت‌های شما'
        }
        
        return render(request, 'store_analysis/payment_history.html', context)
        
    except Exception as e:
        logger.error(f"Error displaying payment history: {e}")
        messages.error(request, 'خطا در نمایش تاریخچه پرداخت‌ها')
        return redirect('store_analysis:user_dashboard')

@login_required
def payment_detail(request, payment_id):
    """
    Display payment details
    """
    try:
        payment = get_object_or_404(Payment, id=payment_id, user=request.user)
        logs = payment.logs.all().order_by('-created_at')
        
        context = {
            'payment': payment,
            'logs': logs,
            'title': f'جزئیات پرداخت {payment.order_id}',
            'description': 'مشاهده جزئیات و وضعیت پرداخت'
        }
        
        return render(request, 'store_analysis/payment_detail.html', context)
        
    except Exception as e:
        logger.error(f"Error displaying payment detail: {e}")
        messages.error(request, 'خطا در نمایش جزئیات پرداخت')
        return redirect('store_analysis:payment_history')

@login_required
def user_subscriptions(request):
    """
    Display user subscriptions
    """
    try:
        subscriptions = UserSubscription.objects.filter(user=request.user).order_by('-created_at')
        
        context = {
            'subscriptions': subscriptions,
            'title': 'اشتراک‌های من',
            'description': 'مشاهده اشتراک‌های فعال و منقضی شده'
        }
        
        return render(request, 'store_analysis/user_subscriptions.html', context)
        
    except Exception as e:
        logger.error(f"Error displaying user subscriptions: {e}")
        messages.error(request, 'خطا در نمایش اشتراک‌ها')
        return redirect('store_analysis:user_dashboard')
