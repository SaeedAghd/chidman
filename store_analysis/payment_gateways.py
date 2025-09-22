"""
Payment Gateway Integration for Chidmano
Support for PayPing (default) and legacy Zarinpal
"""

import requests
import json
from django.conf import settings
from django.urls import reverse
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

    BASE_URL = "https://api.payping.ir/v2/pay/"

    def __init__(self, token: str):
        self.token = token or getattr(settings, 'PAYPING_TOKEN', '')
        if not self.token:
            raise ValueError("PayPing API token is required")

    def create_payment_request(self, amount, description, callback_url, payer_identity=None, payer_name=None, client_ref_id=None):
        """Create payment request on PayPing

        Notes:
        - PayPing amount is in Rials. If we receive Toman, convert by x10.
        """
        try:
            # ساده: فرض می‌کنیم amount بر حسب تومان است → تبدیل به ریال
            rial_amount = int(amount) * 10

            payload = {
                "amount": rial_amount,
                "description": description or "پرداخت سفارش چیدمانو",
                "returnUrl": callback_url,
            }
            if payer_identity:
                payload["payerIdentity"] = str(payer_identity)
            if payer_name:
                payload["payerName"] = str(payer_name)
            if client_ref_id:
                payload["clientRefId"] = str(client_ref_id)

            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            resp = requests.post(
                self.BASE_URL + "request",
                data=json.dumps(payload),
                headers=headers,
                timeout=15,
                allow_redirects=True,
            )

            # PayPing returns 201 on success with {"code":"..."}
            if resp.status_code in (200, 201):
                data = resp.json()
                code = data.get("code")
                if code:
                    return {
                        "status": "success",
                        "authority": code,
                        "payment_url": self.BASE_URL + f"gotoipg/{code}",
                    }

            # error branch
            try:
                err = resp.json()
                message = err.get("message") or err.get("error") or str(err)
            except Exception:
                message = resp.text
            return {"status": "error", "message": message or "خطا در ایجاد درخواست پرداخت"}

        except Exception as e:
            logger.error(f"PayPing payment request error: {e}")
            return {"status": "error", "message": "خطا در ارتباط با درگاه پرداخت"}

    def verify_payment(self, authority, amount):
        """Verify payment on PayPing"""
        try:
            rial_amount = int(amount) * 10
            payload = {"refId": authority, "amount": rial_amount}
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            resp = requests.post(
                self.BASE_URL + "verify",
                data=json.dumps(payload),
                headers=headers,
                timeout=15,
            )

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
            self.gateways['payping'] = PayPingGateway(
                token=getattr(settings, 'PAYPING_TOKEN', '')
            )
        except Exception as e:
            logger.warning(f"PayPing not configured: {e}")

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
