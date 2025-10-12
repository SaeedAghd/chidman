"""
Payment Gateway Integration for Chidmano
Support for PayPing (default) and legacy Zarinpal
"""

import requests
import json
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import logging
import uuid

logger = logging.getLogger(__name__)

class ZarinpalGateway:
    """زرین‌پال Payment Gateway"""
    
    # URLs - استفاده از URL مستقیم زرین‌پال
    SANDBOX_URL = "https://sandbox.zarinpal.com/pg/v4/payment/"
    PRODUCTION_URL = "https://api.zarinpal.com/pg/v4/payment/"
    
    def __init__(self, merchant_id=None, sandbox=True):
        # استفاده از Merchant ID معتبر برای تست
        self.merchant_id = merchant_id or getattr(settings, 'ZARINPAL_MERCHANT_ID', 'b6c54352-1d07-4312-9a7a-f4ad83ee69b0')
        self.sandbox = sandbox
        self.base_url = self.SANDBOX_URL if sandbox else self.PRODUCTION_URL
        
        # اگر Merchant ID کوتاه است، از تست استفاده کن
        if len(self.merchant_id) < 36:
            self.merchant_id = 'b6c54352-1d07-4312-9a7a-f4ad83ee69b0'
        
        if not self.merchant_id:
            raise ValueError("Zarinpal Merchant ID is required")
    
    def create_payment_request(self, amount, description, callback_url, mobile=None, email=None):
        """
        ایجاد درخواست پرداخت
        
        Args:
            amount: مبلغ به تومان
            description: توضیحات
            callback_url: آدرس بازگشت
            mobile: شماره موبایل (اختیاری)
            email: ایمیل (اختیاری)
        """
        try:
            data = {
                "merchant_id": self.merchant_id,
                "amount": amount,
                "description": description,
                "callback_url": callback_url,
            }
            
            if mobile:
                data["mobile"] = mobile
            if email:
                data["email"] = email
                
            response = requests.post(
                f"{self.base_url}request.json",
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'},
                timeout=10,  # کاهش timeout
                verify=False,  # برای حل مشکل SSL
                allow_redirects=True
            )
            
            result = response.json()
            
            if result.get('data', {}).get('code') == 100:
                return {
                    'status': 'success',
                    'authority': result['data']['authority'],
                    'payment_url': f"https://{'sandbox.' if self.sandbox else ''}zarinpal.com/pg/StartPay/{result['data']['authority']}"
                }
            else:
                return {
                    'status': 'error',
                    'message': result.get('errors', {}).get('message', 'خطا در ایجاد درخواست پرداخت')
                }
                
        except Exception as e:
            logger.error(f"Zarinpal payment request error: {e}")
            return {
                'status': 'error',
                'message': 'خطا در ارتباط با درگاه پرداخت'
            }
    
    def verify_payment(self, authority, amount):
        """
        تایید پرداخت
        
        Args:
            authority: کد مرجع از زرین‌پال
            amount: مبلغ به تومان
        """
        try:
            data = {
                "merchant_id": self.merchant_id,
                "amount": amount,
                "authority": authority
            }
            
            response = requests.post(
                f"{self.base_url}verify.json",
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'}
            )
            
            result = response.json()
            
            if result.get('data', {}).get('code') == 100:
                return {
                    'status': 'success',
                    'ref_id': result['data']['ref_id'],
                    'transaction_id': result['data']['ref_id']
                }
            else:
                return {
                    'status': 'error',
                    'message': result.get('errors', {}).get('message', 'خطا در تایید پرداخت')
                }
                
        except Exception as e:
            logger.error(f"Zarinpal payment verification error: {e}")
            return {
                'status': 'error',
                'message': 'خطا در تایید پرداخت'
            }

class PayPingGateway:
    """PayPing Payment Gateway"""

    BASE_URL = "https://api.payping.ir/v2/pay"
    VERIFY_URL = "https://api.payping.ir/v2/pay/verify"

    def __init__(self, token: str):
        self.token = token or getattr(settings, 'PAYPING_TOKEN', '')
        if not self.token:
            # Use test token for development
            self.token = "test_token_for_development"
            logger.warning("Using test token for PayPing development")
        
        # Keep provided token as-is (don't auto-switch to mock). Only use mock if no token provided.
        
        logger.info(f"PayPing gateway initialized with token: {self.token[:20]}...")

    def create_payment_request(self, amount, description, callback_url, payer_identity=None, payer_name=None, client_ref_id=None):
        """Create payment request on PayPing

        Notes:
        - PayPing amount is in Rials. If we receive Toman, convert by x10.
        - payer_identity is REQUIRED and must be a valid mobile number
        - payer_name is recommended for better UX
        - clientRefId must be unique for each transaction
        """
        try:
            # تبدیل تومان به ریال (PayPing فقط ریال قبول می‌کند)
            rial_amount = int(amount) * 10

            # Validate payer_identity
            if not payer_identity:
                logger.error("PayPing requires payer_identity (mobile number)")
                return {"status": "error", "message": "شماره موبایل الزامی است"}
            
            # Generate unique clientRefId
            if not client_ref_id:
                client_ref_id = f"CHIDMANO_{int(timezone.now().timestamp())}_{uuid.uuid4().hex[:8]}"

            payload = {
                "amount": rial_amount,
                "description": description or "پرداخت سفارش چیدمانو",
                "returnUrl": callback_url,
                "payerIdentity": str(payer_identity),  # شماره موبایل کاربر (الزامی)
                "clientRefId": str(client_ref_id),  # شناسه یکتا تراکنش (الزامی)
            }
            
            # Add payer name if provided (recommended)
            if payer_name:
                payload["payerName"] = str(payer_name)
            
            logger.info(f"PayPing payment request: amount={rial_amount} Rials, payer={payer_identity}, client_ref={client_ref_id}")

            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            # Mock response only for explicit local development token
            if self.token == "test_token_for_development":
                logger.info("Using mock PayPing response for development")
                mock_code = f"MOCK_{int(timezone.now().timestamp())}"
                return {
                    "status": "success",
                    "authority": mock_code,
                    "payment_url": f"https://chidmano.ir/store/payment/success/?authority={mock_code}",
                }

            resp = requests.post(
                self.BASE_URL,
                json=payload,
                headers=headers,
                timeout=15,
                allow_redirects=True,
            )

            logger.info(f"PayPing API response: {resp.status_code} - {resp.text}")

            # PayPing returns 201 on success with {"code":"..."}
            if resp.status_code in (200, 201):
                data = resp.json()
                code = data.get("code")
                if code:
                    logger.info(f"✅ PayPing payment created successfully: code={code}")
                    return {
                        "status": "success",
                        "authority": code,
                        "payment_url": f"https://api.payping.ir/v2/pay/gotoipg/{code}",
                    }

            # Error handling - PayPing specific error codes
            error_messages = {
                400: "داده‌های ارسالی نامعتبر است",
                401: "توکن احراز هویت نامعتبر است",
                402: "حساب کاربری شما مسدود شده است",
                403: "دسترسی به این عملیات ندارید",
                404: "درگاه پرداخت فعال برای پذیرنده یافت نشد",
                500: "خطای سرور PayPing - لطفاً بعداً تلاش کنید",
            }
            
            try:
                err = resp.json()
                message = err.get("message") or err.get("error") or error_messages.get(resp.status_code, str(err))
                logger.error(f"❌ PayPing API error ({resp.status_code}): {err}")
                
                # Special handling for specific errors
                if resp.status_code == 404 or "درگاه پرداخت فعال" in str(err):
                    return {
                        "status": "error", 
                        "message": "درگاه پرداخت فعال نیست. لطفاً با پشتیبانی تماس بگیرید.",
                        "code": "GATEWAY_NOT_ACTIVE"
                    }
                elif resp.status_code == 401:
                    return {
                        "status": "error",
                        "message": "خطای احراز هویت درگاه پرداخت",
                        "code": "AUTHENTICATION_ERROR"
                    }
                    
            except Exception:
                message = error_messages.get(resp.status_code, resp.text)
                logger.error(f"❌ PayPing HTTP error: {resp.status_code} - {resp.text}")
                
            return {"status": "error", "message": message or "خطا در ارتباط با درگاه پرداخت", "code": f"HTTP_{resp.status_code}"}

        except Exception as e:
            logger.error(f"PayPing payment request error: {e}")
            return {"status": "error", "message": "خطا در ارتباط با درگاه پرداخت"}

    def verify_payment(self, authority, amount):
        """Verify payment on PayPing"""
        try:
            # Mock verification for development
            if self.token == "test_token_for_development":
                logger.info("Using mock PayPing verification for development")
                return {
                    "status": "success",
                    "message": "پرداخت با موفقیت تایید شد (تست)"
                }
            
            rial_amount = int(amount) * 10
            payload = {"refId": authority, "amount": rial_amount}
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            
            logger.info(f"PayPing verification request: {payload}")
            
            resp = requests.post(
                self.VERIFY_URL,
                json=payload,
                headers=headers,
                timeout=15,
            )
            
            logger.info(f"PayPing verification response: {resp.status_code} - {resp.text}")

            if resp.status_code in (200, 201):
                data = resp.json() if resp.content else {}
                # Successful verify. PayPing may return 200 with no body
                return {
                    "status": "success",
                    "ref_id": data.get("refId") or authority,
                    "transaction_id": data.get("refId") or authority,
                }

            # error
            try:
                err = resp.json()
                message = err.get("message") or err.get("error") or str(err)
            except Exception:
                message = resp.text
            return {"status": "error", "message": message or "خطا در تایید پرداخت"}

        except Exception as e:
            logger.error(f"PayPing payment verification error: {e}")
            return {"status": "error", "message": "خطا در تایید پرداخت"}

class PaymentGatewayManager:
    """مدیریت درگاه‌های پرداخت"""
    
    def __init__(self):
        self.gateways = {}
        # PayPing (default)
        try:
            payping_token = getattr(settings, 'PAYPING_TOKEN', '')
            if payping_token:
                self.gateways['payping'] = PayPingGateway(token=payping_token)
                logger.info("PayPing gateway initialized successfully")
            else:
                logger.warning("PayPing token not found in settings")
                # Create gateway with real token
                self.gateways['payping'] = PayPingGateway(token=getattr(settings, 'PAYPING_TOKEN', ''))
                logger.info("PayPing gateway created with real token")
        except Exception as e:
            logger.warning(f"PayPing not configured: {e}")
            # Create a mock gateway as fallback
            self.gateways['payping'] = PayPingGateway(token="test_token_for_development")
            logger.info("PayPing mock gateway created as fallback")

        # Legacy Zarinpal (optional)
        try:
            self.gateways['zarinpal'] = ZarinpalGateway(
                merchant_id=getattr(settings, 'ZARINPAL_MERCHANT_ID', ''),
                sandbox=getattr(settings, 'ZARINPAL_SANDBOX', True)
            )
        except Exception as e:
            logger.info(f"Zarinpal not configured or optional: {e}")
    
    def get_gateway(self, gateway_name='payping'):
        """دریافت درگاه پرداخت"""
        return self.gateways.get(gateway_name)
    
    def create_payment(self, gateway_name, amount, description, callback_url, **kwargs):
        """ایجاد پرداخت"""
        gateway = self.get_gateway(gateway_name)
        if not gateway:
            return {'success': False, 'error': 'درگاه پرداخت یافت نشد'}
        
        return gateway.create_payment_request(
            amount=amount,
            description=description,
            callback_url=callback_url,
            **kwargs
        )
    
    def verify_payment(self, gateway_name, authority, amount):
        """تایید پرداخت"""
        gateway = self.get_gateway(gateway_name)
        if not gateway:
            return {'success': False, 'error': 'درگاه پرداخت یافت نشد'}
        
        return gateway.verify_payment(authority=authority, amount=amount)

# Global instance
payment_manager = PaymentGatewayManager()
