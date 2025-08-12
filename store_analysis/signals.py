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
        # TODO: Add any initialization logic here
        pass

@receiver(post_delete, sender=StoreAnalysis)
def handle_store_analysis_delete(sender, instance, **kwargs):
    """
    Handle post-delete signal for StoreAnalysis model.
    """
    # Delete the layout image file
    # if instance.layout_image:
    #     try:
    #         default_storage.delete(instance.layout_image.path)
    #     except:
    #         pass 