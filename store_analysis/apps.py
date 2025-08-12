from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StoreAnalysisConfig(AppConfig):
    """
    Configuration for the store_analysis app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store_analysis'
    verbose_name = _('تحلیل فروشگاه')

    def ready(self):
        """
        Import signal handlers when the app is ready.
        """
        import store_analysis.signals
