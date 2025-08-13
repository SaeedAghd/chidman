from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
import os

from .models import StoreAnalysis

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
        logger.info(f"New store analysis created: {instance.store_name} by {instance.user.username}")
        
        # Send notification to user
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
    # Delete associated files
    if instance.store_photos:
        try:
            default_storage.delete(instance.store_photos.path)
        except Exception as e:
            logger.error(f"Failed to delete store photos: {e}")
    
    if instance.customer_video_file:
        try:
            default_storage.delete(instance.customer_video_file.path)
        except Exception as e:
            logger.error(f"Failed to delete customer video: {e}")
    
    if instance.store_plan:
        try:
            default_storage.delete(instance.store_plan.path)
        except Exception as e:
            logger.error(f"Failed to delete store plan: {e}")
    
    if instance.product_catalog:
        try:
            default_storage.delete(instance.product_catalog.path)
        except Exception as e:
            logger.error(f"Failed to delete product catalog: {e}")
    
    logger.info(f"Store analysis deleted: {instance.store_name}") 