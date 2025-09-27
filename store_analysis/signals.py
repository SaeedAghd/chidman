"""
Signals for Store Analysis
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
import os
import logging

from .models import Payment, PaymentLog, ServicePackage, UserSubscription

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Payment)
def handle_payment_save(sender, instance, created, **kwargs):
    """
    Handle post-save signal for Payment model.
    """
    if created:
        # Log payment creation
        PaymentLog.objects.create(
            payment=instance,
            log_type='payment_created',
            message=f'Payment {instance.order_id} created',
            data={'amount': str(instance.amount), 'currency': instance.currency}
        )
        logger.info(f"Payment {instance.order_id} created with status: {instance.status}")
    else:
        logger.info(f"Payment {instance.order_id} updated with status: {instance.status}")

@receiver(post_save, sender=UserSubscription)
def handle_subscription_save(sender, instance, created, **kwargs):
    """
    Handle post-save signal for UserSubscription model.
    """
    if created:
        logger.info(f"UserSubscription created for user {instance.user.username} with package {instance.package.name}")
    else:
        logger.info(f"UserSubscription updated for user {instance.user.username}")

@receiver(post_delete, sender=Payment)
def handle_payment_delete(sender, instance, **kwargs):
    """
    Handle post-delete signal for Payment model.
    """
    logger.info(f"Payment {instance.order_id} deleted")