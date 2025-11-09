"""
Management command برای رفع تحلیل‌های stuck شده
استفاده: python manage.py fix_stuck_analyses
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from store_analysis.models import StoreAnalysis
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'بررسی و رفع تحلیل‌های stuck شده (در حال پردازش که هرگز تمام نمی‌شوند)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=2,
            help='تعداد ساعات برای تشخیص stuck (پیش‌فرض: 2 ساعت)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='فقط نمایش بده، تغییر نده'
        )
        parser.add_argument(
            '--retry',
            action='store_true',
            help='تلاش برای retry تحلیل‌ها'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        dry_run = options['dry_run']
        retry = options['retry']
        
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS("🔧 بررسی و رفع تحلیل‌های Stuck شده"))
        self.stdout.write("=" * 80)
        self.stdout.write("")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("⚠️  حالت DRY-RUN فعال است - هیچ تغییری اعمال نمی‌شود"))
            self.stdout.write("")
        
        # پیدا کردن تحلیل‌های stuck
        threshold_time = timezone.now() - timedelta(hours=hours)
        
        stuck_analyses = StoreAnalysis.objects.filter(
            status='processing',
            updated_at__lt=threshold_time
        )
        
        count = stuck_analyses.count()
        self.stdout.write(f"📊 تعداد تحلیل‌های stuck شده (بیش از {hours} ساعت): {count}")
        self.stdout.write("")
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS("✅ هیچ تحلیل stuck شده‌ای پیدا نشد!"))
            return
        
        self.stdout.write("🔍 تحلیل‌های stuck شده:")
        self.stdout.write("-" * 80)
        
        fixed_count = 0
        failed_count = 0
        
        for analysis in stuck_analyses:
            self.stdout.write(f"\n📋 تحلیل ID: {analysis.id}")
            self.stdout.write(f"   کاربر: {analysis.user.username if analysis.user else 'N/A'}")
            self.stdout.write(f"   آخرین بروزرسانی: {analysis.updated_at}")
            stuck_minutes = (timezone.now() - analysis.updated_at).total_seconds() / 60
            self.stdout.write(f"   مدت زمان stuck: {stuck_minutes:.1f} دقیقه")
            
            if dry_run:
                self.stdout.write(self.style.WARNING("   [DRY-RUN] این تحلیل باید بررسی شود"))
                continue
            
            # بررسی API key
            liara_api_key = getattr(settings, 'LIARA_AI_API_KEY', '')
            
            if not liara_api_key:
                self.stdout.write(self.style.ERROR("   ⚠️  LIARA_AI_API_KEY تنظیم نشده است"))
                if not dry_run:
                    analysis.status = 'failed'
                    analysis.error_message = "⚠️ LIARA_AI_API_KEY تنظیم نشده است. تحلیل نمی‌تواند انجام شود."
                    analysis.save(update_fields=['status', 'error_message'])
                    failed_count += 1
                continue
            
            # بررسی داده‌ها
            if not analysis.analysis_data:
                self.stdout.write(self.style.ERROR("   ⚠️  داده‌های تحلیل موجود نیست"))
                if not dry_run:
                    analysis.status = 'failed'
                    analysis.error_message = "⚠️ داده‌های تحلیل موجود نیست. لطفاً فرم را تکمیل کنید."
                    analysis.save(update_fields=['status', 'error_message'])
                    failed_count += 1
                continue
            
            # Retry اگر درخواست شده باشد
            if retry and not dry_run:
                self.stdout.write("   🔄 تلاش برای retry تحلیل...")
                
                try:
                    # آماده‌سازی داده‌ها
                    analysis_data = analysis.analysis_data or {}
                    store_data = {
                        'store_name': analysis.store_name or 'فروشگاه',
                        'store_type': analysis_data.get('store_type', 'عمومی'),
                        'store_size': str(analysis_data.get('store_size', 0)),
                        **analysis_data
                    }
                    
                    # استخراج تصاویر
                    images = []
                    if 'uploaded_files' in analysis_data:
                        uploaded_files = analysis_data['uploaded_files']
                        image_fields = ['store_photos', 'store_layout', 'shelf_photos', 
                                      'window_display_photos', 'entrance_photos', 'checkout_photos']
                        for field in image_fields:
                            if field in uploaded_files:
                                file_info = uploaded_files[field]
                                if isinstance(file_info, dict) and 'path' in file_info:
                                    images.append(file_info['path'])
                    
                    # استفاده از Liara AI
                    from store_analysis.ai_services.liara_ai_service import LiaraAIService
                    liara_service = LiaraAIService()
                    
                    if not liara_service.api_key:
                        self.stdout.write(self.style.ERROR("   ❌ API key در سرویس موجود نیست"))
                        analysis.status = 'failed'
                        analysis.error_message = "⚠️ LIARA_AI_API_KEY در سرویس موجود نیست."
                        analysis.save(update_fields=['status', 'error_message'])
                        failed_count += 1
                        continue
                    
                    self.stdout.write("   📡 در حال ارسال درخواست به Liara AI...")
                    
                    # تحلیل جامع
                    comprehensive_analysis = liara_service.analyze_store_comprehensive(
                        store_data=store_data,
                        images=images if images else None
                    )
                    
                    # بررسی نتیجه
                    if comprehensive_analysis and comprehensive_analysis.get('error'):
                        error_type = comprehensive_analysis.get('error', 'unknown_error')
                        error_message = comprehensive_analysis.get('error_message', 'خطا در تحلیل AI')
                        
                        self.stdout.write(self.style.ERROR(f"   ❌ خطا در تحلیل: {error_type}"))
                        analysis.status = 'failed'
                        analysis.error_message = error_message
                        analysis.save(update_fields=['status', 'error_message'])
                        failed_count += 1
                        
                    elif comprehensive_analysis and not comprehensive_analysis.get('error'):
                        self.stdout.write(self.style.SUCCESS("   ✅ تحلیل با موفقیت انجام شد!"))
                        
                        # به‌روزرسانی نتایج
                        current_results = analysis.results or {}
                        
                        analysis_text = None
                        if 'final_report' in comprehensive_analysis:
                            analysis_text = comprehensive_analysis['final_report']
                        elif 'detailed_analyses' in comprehensive_analysis:
                            combined = ""
                            for key, anal in comprehensive_analysis['detailed_analyses'].items():
                                if anal and 'content' in anal:
                                    combined += f"\n\n{anal['content']}\n"
                            analysis_text = combined if combined else None
                        
                        current_results.update({
                            'liara_analysis': comprehensive_analysis,
                            'analysis_source': 'liara_ai',
                            'analysis_text': analysis_text or comprehensive_analysis.get('final_report', ''),
                            'models_used': comprehensive_analysis.get('ai_models_used', []),
                            'analysis_quality': 'premium',
                            'analyzed_at': timezone.now().isoformat(),
                        })
                        
                        analysis.results = current_results
                        analysis.status = 'completed'
                        analysis.save(update_fields=['results', 'status'])
                        
                        self.stdout.write(self.style.SUCCESS("   ✅ وضعیت به 'completed' تغییر یافت"))
                        fixed_count += 1
                        
                    else:
                        self.stdout.write(self.style.ERROR("   ❌ تحلیل خالی برگشت"))
                        analysis.status = 'failed'
                        analysis.error_message = 'تحلیل AI خالی برگشت. لطفاً دوباره تلاش کنید.'
                        analysis.save(update_fields=['status', 'error_message'])
                        failed_count += 1
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"   ❌ خطا در retry: {e}"))
                    logger.error(f"Error retrying analysis {analysis.id}: {e}", exc_info=True)
                    
                    analysis.status = 'failed'
                    analysis.error_message = f"خطا در retry تحلیل: {str(e)}"
                    analysis.save(update_fields=['status', 'error_message'])
                    failed_count += 1
            else:
                # فقط تغییر به failed
                if not dry_run:
                    self.stdout.write("   🔧 تغییر وضعیت به 'failed'")
                    analysis.status = 'failed'
                    analysis.error_message = f"تحلیل بیش از {hours} ساعت در حال پردازش بود و متوقف شد."
                    analysis.save(update_fields=['status', 'error_message'])
                    failed_count += 1
        
        self.stdout.write("")
        self.stdout.write("=" * 80)
        self.stdout.write("📊 خلاصه:")
        self.stdout.write("=" * 80)
        self.stdout.write(f"   کل تحلیل‌های stuck: {count}")
        if retry:
            self.stdout.write(f"   ✅ با موفقیت retry شدند: {fixed_count}")
        self.stdout.write(f"   ❌ به failed تغییر یافتند: {failed_count}")
        self.stdout.write("")
        
        if fixed_count > 0:
            self.stdout.write(self.style.SUCCESS("✅ برخی تحلیل‌ها با موفقیت retry شدند!"))
        if failed_count > 0:
            self.stdout.write(self.style.WARNING("⚠️  برخی تحلیل‌ها به failed تغییر یافتند"))

