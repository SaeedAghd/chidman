"""
WSGI config for chidmano project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')

# Guarded auto-migration to ensure DB schema (e.g., ai_insights) exists in PaaS
try:
    if os.environ.get('AUTO_MIGRATE', 'true').lower() == 'true':
        lock_path = '/tmp/chidmano_migrated.lock'
        if not os.path.exists(lock_path):
            import logging
            logger = logging.getLogger(__name__)
            logger.info("🔄 Auto-migration: Starting migrations...")
            from django.core.management import call_command
            try:
                call_command('migrate', interactive=False, verbosity=1)
                logger.info("✅ Auto-migration: Migrations completed successfully")
                # create lock file to avoid repeated migrations per container lifecycle
                try:
                    with open(lock_path, 'w') as f:
                        f.write('ok')
                except Exception as lock_err:
                    logger.warning(f"⚠️ Could not create migration lock file: {lock_err}")
            except Exception as migrate_err:
                # Log migration errors but don't block startup
                # Safe migrations (like 0118) will handle existing columns gracefully
                logger.warning(f"⚠️ Auto-migration warning: {migrate_err}")
                logger.info("ℹ️ Continuing startup - safe migrations will handle existing columns")
except Exception as e:
    # Never block startup on migration issues here; errors will surface in logs
    import logging
    logging.getLogger(__name__).warning(f"⚠️ Auto-migration setup error: {e}")
    pass

# Create a simple health check wrapper
def health_check_wrapper(environ, start_response):
    """Ultra-light health check that bypasses Django completely"""
    if environ.get('PATH_INFO') in ['/health', '/health/']:
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'OK']
    return get_wsgi_application()(environ, start_response)

application = health_check_wrapper 