"""
Payment Gateway Integration for Chidmano
Support for Zarinpal and other Iranian payment gateways
"""

import requests
import json
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class ZarinpalGateway:
    """زرین‌پال Payment Gateway"""
    
    # URLs - استفاده از URL صحیح زرین‌پال
    SANDBOX_URL = "https://sandbox.zarinpal.com/pg/v4/payment/"
    PRODUCTION_URL = "https://api.zarinpal.com/pg/v4/payment/"
    
    def __init__(self, merchant_id=None, sandbox=True):
        self.merchant_id = merchant_id or getattr(settings, 'ZARINPAL_MERCHANT_ID', 'b6c54352-1d07-4312-9a7a-f4ad83ee69b0')
        self.sandbox = sandbox
        self.base_url = self.SANDBOX_URL if sandbox else self.PRODUCTION_URL
        
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
                timeout=30,
                verify=False  # برای حل مشکل SSL
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

class PaymentGatewayManager:
    """مدیریت درگاه‌های پرداخت"""
    
    def __init__(self):
        self.gateways = {
            'zarinpal': ZarinpalGateway(
                merchant_id=getattr(settings, 'ZARINPAL_MERCHANT_ID', 'b6c54352-1d07-4312-9a7a-f4ad83ee69b0'),
                sandbox=getattr(settings, 'ZARINPAL_SANDBOX', True)
            )
        }
    
    def get_gateway(self, gateway_name='zarinpal'):
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
