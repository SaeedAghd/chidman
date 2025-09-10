from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
import os
import logging

from .models import StoreAnalysis

logger = logging.getLogger(__name__)

@receiver(post_save, sender=StoreAnalysis)
def handle_store_analysis_save(sender, instance, created, **kwargs):
    """
    Handle post-save signal for StoreAnalysis model.
    """
    if created:
        # Initialize analysis status
        instance.status = 'pending'
        instance.save(update_fields=['status'])
        
        # Log the creation
        user_info = instance.user.username if instance.user else "Anonymous"
        logger.info(f"New store analysis created: {instance.store_name} by {user_info}")
        
        # Send notification to user (if user exists)
        if instance.user and instance.user.email:
            try:
                from .utils.notification import send_email_notification
                send_email_notification(
                    instance.user.email,
                    'تحلیل جدید ایجاد شد',
                    f'تحلیل فروشگاه {instance.store_name} با موفقیت ایجاد شد.'
                )
            except Exception as e:
                logger.error(f"Failed to send notification: {e}")

@receiver(post_delete, sender=StoreAnalysis)
def handle_store_analysis_delete(sender, instance, **kwargs):
    """
    Handle post-delete signal for StoreAnalysis model.
    """
    # Delete associated files if they exist
    file_fields = ['store_photos', 'customer_video_file', 'store_plan', 'product_catalog']
    
    for field_name in file_fields:
        if hasattr(instance, field_name):
            field_value = getattr(instance, field_name, None)
            if field_value:
                try:
                    default_storage.delete(field_value.path)
                except Exception as e:
                    logger.error(f"Failed to delete {field_name}: {e}")
    
    logger.info(f"Store analysis deleted: {instance.store_name}") 