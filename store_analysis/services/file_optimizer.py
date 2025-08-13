"""
File optimization service for store analysis application.
"""

import os
import logging
from PIL import Image
from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
import cv2
import numpy as np
import time

logger = logging.getLogger(__name__)

class FileOptimizer:
    """Optimize file uploads and processing."""
    
    def __init__(self):
        self.supported_image_formats = ['.jpg', '.jpeg', '.png', '.gif']
        self.supported_video_formats = ['.mp4', '.avi', '.mov']
        self.max_image_size = (1920, 1080)  # Max dimensions
        self.image_quality = 85  # JPEG quality
    
    def optimize_image(self, image_file, max_size=None, quality=None):
        """Optimize image file for web use."""
        try:
            if not image_file:
                return None
            
            # Open image
            img = Image.open(image_file)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            if max_size is None:
                max_size = self.max_image_size
            
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save optimized image
            output_path = self._get_optimized_path(image_file.name)
            img.save(output_path, 'JPEG', quality=quality or self.image_quality, optimize=True)
            
            logger.info(f"Image optimized: {image_file.name} -> {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error optimizing image {image_file.name}: {e}")
            return None
    
    def create_thumbnail(self, image_file, size=(150, 150)):
        """Create thumbnail from image."""
        try:
            if not image_file:
                return None
            
            img = Image.open(image_file)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Create thumbnail
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Save thumbnail
            thumbnail_path = self._get_thumbnail_path(image_file.name)
            img.save(thumbnail_path, 'JPEG', quality=85, optimize=True)
            
            logger.info(f"Thumbnail created: {image_file.name} -> {thumbnail_path}")
            return thumbnail_path
            
        except Exception as e:
            logger.error(f"Error creating thumbnail for {image_file.name}: {e}")
            return None
    
    def extract_video_frame(self, video_file, frame_number=0):
        """Extract frame from video for thumbnail."""
        try:
            if not video_file:
                return None
            
            # Open video
            cap = cv2.VideoCapture(video_file.path)
            
            # Set frame position
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            
            # Read frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                logger.warning(f"Could not read frame {frame_number} from {video_file.name}")
                return None
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            img = Image.fromarray(frame_rgb)
            
            # Resize if too large
            if img.size[0] > 800 or img.size[1] > 600:
                img.thumbnail((800, 600), Image.Resampling.LANCZOS)
            
            # Save frame
            frame_path = self._get_video_frame_path(video_file.name, frame_number)
            img.save(frame_path, 'JPEG', quality=85, optimize=True)
            
            logger.info(f"Video frame extracted: {video_file.name} -> {frame_path}")
            return frame_path
            
        except Exception as e:
            logger.error(f"Error extracting frame from {video_file.name}: {e}")
            return None
    
    def compress_video(self, video_file, target_size_mb=10):
        """Compress video file to target size."""
        try:
            if not video_file:
                return None
            
            # Get video info
            cap = cv2.VideoCapture(video_file.path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            
            # Calculate target bitrate
            target_size_bytes = target_size_mb * 1024 * 1024
            duration = self._get_video_duration(video_file.path)
            target_bitrate = int((target_size_bytes * 8) / duration)
            
            # Compress video
            output_path = self._get_compressed_video_path(video_file.name)
            
            # Use ffmpeg for compression (if available)
            import subprocess
            
            cmd = [
                'ffmpeg', '-i', video_file.path,
                '-c:v', 'libx264',
                '-crf', '23',
                '-preset', 'medium',
                '-c:a', 'aac',
                '-b:a', '128k',
                '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Video compressed: {video_file.name} -> {output_path}")
                return output_path
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error compressing video {video_file.name}: {e}")
            return None
    
    def validate_file_type(self, file_obj, allowed_types=None):
        """Validate file type and content."""
        if allowed_types is None:
            allowed_types = self.supported_image_formats + self.supported_video_formats
        
        # Check file extension
        file_ext = os.path.splitext(file_obj.name)[1].lower()
        if file_ext not in allowed_types:
            return False, f"File type {file_ext} not allowed"
        
        # Check file size
        max_size = getattr(settings, 'MAX_FILE_SIZE', 50 * 1024 * 1024)  # 50MB
        if file_obj.size > max_size:
            return False, f"File size {file_obj.size} exceeds limit {max_size}"
        
        # Additional validation for images
        if file_ext in self.supported_image_formats:
            try:
                img = Image.open(file_obj)
                img.verify()
                return True, "File is valid"
            except Exception as e:
                return False, f"Invalid image file: {e}"
        
        return True, "File is valid"
    
    def cleanup_temp_files(self, temp_dir=None):
        """Clean up temporary files."""
        if temp_dir is None:
            temp_dir = getattr(settings, 'FILE_UPLOAD_TEMP_DIR', '/tmp')
        
        try:
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path):
                    # Remove files older than 1 hour
                    if os.path.getmtime(file_path) < time.time() - 3600:
                        os.remove(file_path)
                        logger.info(f"Cleaned up temp file: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {e}")
    
    def _get_optimized_path(self, original_filename):
        """Get path for optimized image."""
        name, ext = os.path.splitext(original_filename)
        return os.path.join(settings.MEDIA_ROOT, 'optimized', f"{name}_opt.jpg")
    
    def _get_thumbnail_path(self, original_filename):
        """Get path for thumbnail."""
        name, ext = os.path.splitext(original_filename)
        return os.path.join(settings.MEDIA_ROOT, 'thumbnails', f"{name}_thumb.jpg")
    
    def _get_video_frame_path(self, video_filename, frame_number):
        """Get path for video frame."""
        name, ext = os.path.splitext(video_filename)
        return os.path.join(settings.MEDIA_ROOT, 'frames', f"{name}_frame_{frame_number}.jpg")
    
    def _get_compressed_video_path(self, original_filename):
        """Get path for compressed video."""
        name, ext = os.path.splitext(original_filename)
        return os.path.join(settings.MEDIA_ROOT, 'compressed', f"{name}_compressed.mp4")
    
    def _get_video_duration(self, video_path):
        """Get video duration in seconds."""
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
            return frame_count / fps if fps > 0 else 0
        except:
            return 0 