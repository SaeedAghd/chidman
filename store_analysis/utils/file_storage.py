"""
Helper functions for file storage that work with read-only filesystem (Liara)
"""
import os
import uuid
from django.core.files.storage import default_storage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def save_uploaded_file(file_obj, base_path='uploads'):
    """
    Save uploaded file to storage.
    In Liara (read-only filesystem), uses /tmp
    In development, uses default_storage
    
    Args:
        file_obj: Django UploadedFile object
        base_path: Base path for file (e.g., 'uploads', 'analyses')
    
    Returns:
        dict with 'path', 'name', 'size', 'type', 'storage' keys
    """
    # تشخیص Liara از طریق چند روش:
    # 1. متغیر LIARA
    # 2. وجود LIARA_AI_API_KEY (که در Liara تنظیم می‌شود)
    # 3. hostname که شامل liara باشد
    is_liara = (
        os.getenv('LIARA') == 'true' or
        bool(os.getenv('LIARA_AI_API_KEY')) or
        'liara' in os.getenv('HOSTNAME', '').lower() or
        'liara' in os.getenv('ALLOWED_HOSTS', '').lower()
    )
    
    logger.debug(f"🔍 File storage check: is_liara={is_liara}, LIARA={os.getenv('LIARA')}, has_LIARA_AI_API_KEY={bool(os.getenv('LIARA_AI_API_KEY'))}")
    
    if is_liara:
        # در Liara، از /tmp استفاده می‌کنیم
        tmp_base = '/tmp/media'
        tmp_dir = os.path.join(tmp_base, base_path)
        os.makedirs(tmp_dir, exist_ok=True)
        
        # ایجاد نام فایل امن
        safe_filename = f"{uuid.uuid4().hex[:8]}_{file_obj.name}"
        file_path = os.path.join(tmp_dir, safe_filename)
        
        # ذخیره فایل
        try:
            with open(file_path, 'wb+') as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)
            
            file_size = os.path.getsize(file_path)
            relative_path = f'/tmp/media/{base_path}/{safe_filename}'
            
            result = {
                'name': file_obj.name,
                'path': relative_path,
                'absolute_path': file_path,
                'size': file_size,
                'type': file_obj.content_type,
                'storage': 'tmp'
            }
            
            logger.info(f"✅ File saved to /tmp: {relative_path}, size={file_size}")
            return result
        except Exception as e:
            logger.error(f"❌ Error saving file to /tmp: {e}", exc_info=True)
            raise
    
    else:
        # در development از default_storage
        try:
            file_path = default_storage.save(f'{base_path}/{file_obj.name}', file_obj)
            result = {
                'name': file_obj.name,
                'path': file_path,
                'size': file_obj.size,
                'type': file_obj.content_type,
                'storage': 'default'
            }
            
            logger.info(f"✅ File saved via default_storage: {file_path}, size={file_obj.size}")
            return result
        except Exception as e:
            logger.error(f"❌ Error saving file via default_storage: {e}", exc_info=True)
            raise


def get_file_path(stored_file_info):
    """
    Get actual file path from stored file info dict
    
    Args:
        stored_file_info: dict with file info (from save_uploaded_file)
    
    Returns:
        str: absolute path to file
    """
    if stored_file_info.get('storage') == 'tmp':
        return stored_file_info.get('absolute_path', stored_file_info.get('path'))
    else:
        # برای default_storage، از MEDIA_ROOT استفاده می‌کنیم
        return os.path.join(settings.MEDIA_ROOT, stored_file_info.get('path', ''))

