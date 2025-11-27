"""
Admin Payment Test Views
برای تست پرداخت PayPing با قیمت 1,000 تومان برای همه پلن‌ها
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.urls import reverse
from decimal import Decimal
import logging

from .models import ServicePackage, Payment, Order
from .payment_gateways import PaymentGatewayManager

logger = logging.getLogger(__name__)


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_payment_test(request):
    """
    صفحه تست پرداخت برای ادمین
    نمایش همه پلن‌ها با قیمت 1,000 تومان برای تست PayPing
    """
    try:
        packages = list(ServicePackage.objects.filter(is_active=True).order_by('sort_order', 'price'))
        
        # برای همه پلن‌ها قیمت تست 1,000 تومان تنظیم می‌کنیم
        for pkg in packages:
            pkg.test_price = 1000  # 1,000 Toman = 10,000 Rials
            pkg.original_price = pkg.price
        
        context = {
            'packages': packages,
            'title': 'تست پرداخت PayPing - ادمین',
            'description': 'همه پلن‌ها با قیمت 1,000 تومان برای تست درگاه پرداخت',
            'is_admin_test': True,
        }
        
        return render(request, 'store_analysis/admin_payment_test.html', context)
        
    except Exception as e:
        logger.error(f"Error in admin_payment_test: {e}", exc_info=True)
        messages.error(request, 'خطا در نمایش صفحه تست پرداخت')
        return redirect('store_analysis:admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["POST"])
def admin_create_test_payment(request, package_id):
    """
    ایجاد پرداخت تست برای ادمین با قیمت 1,000 تومان
    """
    try:
        package = get_object_or_404(ServicePackage, id=package_id, is_active=True)
        
        # قیمت تست: 1,000 تومان = 10,000 ریال
        test_amount = Decimal('1000')
        
        # Generate unique order ID
        from django.utils import timezone
        import time
        order_id = f"ADMIN_TEST_{package.id}_{int(timezone.now().timestamp())}"
        
        # Create payment record
        from django.db import transaction
        with transaction.atomic():
            payment = Payment.objects.create(
                user=request.user,
                order_id=order_id,
                amount=test_amount,
                currency=package.currency,
                description=f"تست پرداخت - بسته {package.name} (قیمت اصلی: {package.price:,} تومان)",
                customer_name=request.user.get_full_name() or request.user.username,
                customer_email=request.user.email,
                payment_method='ping_payment',
                status='pending',
                is_test=True  # Mark as test payment
            )
            
            # Create corresponding Order
            order = Order.objects.create(
                order_number=order_id,
                user=request.user,
                plan=None,
                status='pending',
                original_amount=package.price,
                base_amount=package.price,
                final_amount=test_amount,  # Test amount: 1,000 Toman
                currency=package.currency,
                payment=payment,
                payment_method='ping_payment'
            )
        
        # Build callback URL
        callback_url = request.build_absolute_uri(
            reverse('store_analysis:payment_callback')
        )
        
        # Get user phone for PayPing
        payer_identity = None
        try:
            user_profile = request.user.userprofile
            payer_identity = user_profile.phone
        except:
            pass
        
        if not payer_identity or len(str(payer_identity)) < 10:
            payer_identity = '09121234567'  # Test number
        
        payer_name = request.user.get_full_name() or request.user.username
        
        # Use PayPing gateway
        gateway_manager = PaymentGatewayManager()
        payping = gateway_manager.get_gateway('payping')
        
        if not payping:
            messages.error(request, 'درگاه PayPing در دسترس نیست')
            return redirect('store_analysis:admin_payment_test')
        
        logger.info(f"🔧 Admin test payment initiated for package {package.name} (original: {package.price:,}, test: {test_amount:,})")
        
        # Create payment request with test amount (PayPing expects Tomans as integer)
        payment_request = payping.create_payment_request(
            amount=int(test_amount),  # 1,000 Toman = 10,000 Rials
            description=f'تست پرداخت - بسته {package.name} (ادمین)',
            callback_url=callback_url,
            payer_identity=str(payer_identity),
            payer_name=str(payer_name),
            client_ref_id=f"ADMIN_TEST_{order_id}"
        )
        
        logger.info(f"💳 Admin test payment request result: {payment_request}")
        
        # Convert PayPing response format
        if payment_request.get('status') == 'success':
            payment_result = {
                'success': True,
                'payment_id': payment_request.get('authority'),
                'payment_url': payment_request.get('payment_url'),
                'transaction_id': payment_request.get('authority'),
                'amount': test_amount,
                'order_id': order_id,
                'message': 'Payment request created successfully (Admin Test Mode)'
            }
        else:
            error_msg = payment_request.get('message', 'خطا در ارتباط با درگاه پرداخت')
            payment_result = {
                'success': False,
                'error': error_msg,
                'error_code': payment_request.get('code', 'PAYMENT_CREATE_FAILED')
            }
        
        if payment_result.get('success'):
            # Update payment with gateway response
            payment.payment_id = payment_result.get('payment_id')
            payment.transaction_id = payment_result.get('transaction_id')
            payment.gateway_response = payment_result
            payment.status = 'processing'
            payment.save()
            
            # Update Order
            order.transaction_id = payment_result.get('transaction_id') or payment_result.get('payment_id', '')
            order.save(update_fields=['transaction_id'])
            
            # Get payment URL and redirect
            payment_url = payment_result.get('payment_url')
            if not payment_url:
                messages.error(request, 'خطا: آدرس درگاه پرداخت دریافت نشد')
                return redirect('store_analysis:admin_payment_test')
            
            logger.info(f"✅ Admin test payment redirecting to PayPing: {payment_url}")
            messages.info(request, f'🔧 حالت تست: پرداخت با مبلغ 1,000 تومان برای بسته {package.name} (قیمت اصلی: {package.price:,} تومان)')
            return redirect(payment_url)
        else:
            error_msg = payment_result.get('error', 'خطای نامشخص')
            logger.error(f"❌ Admin test payment creation failed: {error_msg}")
            payment.status = 'failed'
            payment.save()
            messages.error(request, f'خطا در ایجاد پرداخت تست: {error_msg}')
            return redirect('store_analysis:admin_payment_test')
            
    except Exception as e:
        logger.error(f"Error in admin_create_test_payment: {e}", exc_info=True)
        messages.error(request, f'خطا در ایجاد پرداخت تست: {str(e)}')
        return redirect('store_analysis:admin_payment_test')

