"""
Payment Services for Ping Payment Gateway
Professional implementation with proper error handling and security
"""

import requests
import hashlib
import hmac
import json
import logging
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class PingPaymentService:
    """
    Professional Ping Payment Gateway Service
    Implements secure payment processing with proper error handling
    """
    
    def __init__(self):
        self.merchant_id = settings.PAYMENT_GATEWAY['PING_PAYMENT']['MERCHANT_ID']
        self.api_key = settings.PAYMENT_GATEWAY['PING_PAYMENT']['API_KEY']
        self.callback_url = settings.PAYMENT_GATEWAY['PING_PAYMENT']['CALLBACK_URL']
        self.return_url = settings.PAYMENT_GATEWAY['PING_PAYMENT']['RETURN_URL']
        self.sandbox = settings.PAYMENT_GATEWAY['PING_PAYMENT']['SANDBOX']
        self.api_url = settings.PAYMENT_GATEWAY['PING_PAYMENT']['API_URL']
        
    def _generate_signature(self, data: Dict[str, Any]) -> str:
        """
        Generate HMAC-SHA256 signature for secure communication
        """
        try:
            # Sort data by keys for consistent signature
            sorted_data = sorted(data.items())
            message = '&'.join([f"{key}={value}" for key, value in sorted_data])
            
            # Generate HMAC-SHA256 signature
            signature = hmac.new(
                self.api_key.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return signature
        except Exception as e:
            logger.error(f"Error generating signature: {e}")
            raise
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make secure API request to Ping Payment
        """
        try:
            url = f"{self.api_url}/{endpoint}"
            
            # Add signature to data
            data['signature'] = self._generate_signature(data)
            data['merchant_id'] = self.merchant_id
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'Chidmano/1.0'
            }
            
            response = requests.post(
                url,
                json=data,
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in API request: {e}")
            raise
    
    def create_payment(self, amount: Decimal, order_id: str, description: str, 
                      customer_info: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Create a new payment request
        """
        try:
            # Validate inputs
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
            
            if not order_id or not description:
                raise ValueError("Order ID and description are required")
            
            # Prepare payment data
            payment_data = {
                'amount': str(int(amount * 100)),  # Convert to cents
                'order_id': order_id,
                'description': description,
                'callback_url': self.callback_url,
                'return_url': self.return_url,
                'timestamp': int(timezone.now().timestamp()),
                'sandbox': self.sandbox
            }
            
            # Add customer info if provided
            if customer_info:
                payment_data.update({
                    'customer_name': customer_info.get('name', ''),
                    'customer_email': customer_info.get('email', ''),
                    'customer_phone': customer_info.get('phone', ''),
                })
            
            # Make API request
            result = self._make_request('payment/create', payment_data)
            
            # Log successful payment creation
            logger.info(f"Payment created successfully for order {order_id}")
            
            return {
                'success': True,
                'payment_id': result.get('payment_id'),
                'payment_url': result.get('payment_url'),
                'transaction_id': result.get('transaction_id'),
                'amount': amount,
                'order_id': order_id
            }
            
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            return {
                'success': False,
                'error': str(e),
                'error_code': 'PAYMENT_CREATE_FAILED'
            }
    
    def verify_payment(self, payment_id: str, transaction_id: str) -> Dict[str, Any]:
        """
        Verify payment status
        """
        try:
            verify_data = {
                'payment_id': payment_id,
                'transaction_id': transaction_id,
                'timestamp': int(timezone.now().timestamp())
            }
            
            result = self._make_request('payment/verify', verify_data)
            
            return {
                'success': True,
                'verified': result.get('verified', False),
                'status': result.get('status'),
                'amount': result.get('amount'),
                'order_id': result.get('order_id'),
                'transaction_id': transaction_id
            }
            
        except Exception as e:
            logger.error(f"Error verifying payment: {e}")
            return {
                'success': False,
                'error': str(e),
                'error_code': 'PAYMENT_VERIFY_FAILED'
            }
    
    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """
        Get payment status
        """
        try:
            status_data = {
                'payment_id': payment_id,
                'timestamp': int(timezone.now().timestamp())
            }
            
            result = self._make_request('payment/status', status_data)
            
            return {
                'success': True,
                'status': result.get('status'),
                'amount': result.get('amount'),
                'order_id': result.get('order_id'),
                'transaction_id': result.get('transaction_id'),
                'created_at': result.get('created_at'),
                'updated_at': result.get('updated_at')
            }
            
        except Exception as e:
            logger.error(f"Error getting payment status: {e}")
            return {
                'success': False,
                'error': str(e),
                'error_code': 'PAYMENT_STATUS_FAILED'
            }
    
    def refund_payment(self, payment_id: str, amount: Decimal = None) -> Dict[str, Any]:
        """
        Refund payment (if supported by Ping Payment)
        """
        try:
            refund_data = {
                'payment_id': payment_id,
                'timestamp': int(timezone.now().timestamp())
            }
            
            if amount:
                refund_data['amount'] = str(int(amount * 100))
            
            result = self._make_request('payment/refund', refund_data)
            
            return {
                'success': True,
                'refund_id': result.get('refund_id'),
                'status': result.get('status'),
                'amount': result.get('amount')
            }
            
        except Exception as e:
            logger.error(f"Error refunding payment: {e}")
            return {
                'success': False,
                'error': str(e),
                'error_code': 'PAYMENT_REFUND_FAILED'
            }


class PaymentManager:
    """
    High-level payment management service
    """
    
    def __init__(self):
        self.ping_service = PingPaymentService()
    
    def process_payment(self, amount: Decimal, order_id: str, description: str,
                       customer_info: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Process payment with comprehensive error handling
        """
        try:
            # Create payment
            payment_result = self.ping_service.create_payment(
                amount=amount,
                order_id=order_id,
                description=description,
                customer_info=customer_info
            )
            
            if not payment_result['success']:
                return payment_result
            
            # Log payment creation
            logger.info(f"Payment processed successfully: {payment_result}")
            
            return payment_result
            
        except Exception as e:
            logger.error(f"Payment processing failed: {e}")
            return {
                'success': False,
                'error': 'Payment processing failed',
                'error_code': 'PAYMENT_PROCESSING_ERROR'
            }
    
    def handle_callback(self, callback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle payment callback from Ping Payment
        """
        try:
            payment_id = callback_data.get('payment_id')
            transaction_id = callback_data.get('transaction_id')
            status = callback_data.get('status')
            
            if not payment_id or not transaction_id:
                return {
                    'success': False,
                    'error': 'Invalid callback data',
                    'error_code': 'INVALID_CALLBACK'
                }
            
            # Verify payment
            verify_result = self.ping_service.verify_payment(payment_id, transaction_id)
            
            if not verify_result['success']:
                return verify_result
            
            # Process based on status
            if status == 'success' and verify_result['verified']:
                return {
                    'success': True,
                    'status': 'completed',
                    'payment_id': payment_id,
                    'transaction_id': transaction_id,
                    'verified': True
                }
            else:
                return {
                    'success': True,
                    'status': 'failed',
                    'payment_id': payment_id,
                    'transaction_id': transaction_id,
                    'verified': False
                }
                
        except Exception as e:
            logger.error(f"Callback handling failed: {e}")
            return {
                'success': False,
                'error': 'Callback handling failed',
                'error_code': 'CALLBACK_ERROR'
            }
