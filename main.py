#!/usr/bin/env python3
"""
Main entry point for Liara deployment
This file ensures compatibility with Liara's default startup process
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
    
    # Setup Django
    django.setup()

    # Run migrations and collectstatic before starting Gunicorn
    print("📊 Running migrations (main.py)...")
    from django.core.management import call_command
    try:
        # Run all migrations without faking
        print("🔄 Running all migrations...")
        call_command('migrate', interactive=False, verbosity=1)
        print("✅ All migrations applied successfully")
        
        # Add authority column if needed
        print("🔧 Adding authority column if needed...")
        call_command('add_authority_column')
        print("✅ Authority column check completed")
        
    except Exception as migrate_error:
        print(f"⚠️ Migration warning: {migrate_error}")
        print("⚠️ Continuing anyway - the app might still work")

    # Do NOT run collectstatic at runtime on Liara (read-only filesystem). Collectstatic occurs at build time.
    print("📁 Skipping collectstatic in main.py - will be handled at build time")

    # Start the application with gunicorn (only on Linux/Unix)
    import platform
    if platform.system() == 'Windows':
        print("🌐 Starting Django development server (Windows)...")
        from django.core.management import call_command
        call_command('runserver', '0.0.0.0:8000')
    else:
        print("🌐 Starting Gunicorn server...")
        import subprocess
        import shlex

        port = os.environ.get('PORT', '8000')
        # Respect WEB_CONCURRENCY if provided; default to 1 to reduce memory usage
        workers = os.environ.get('WEB_CONCURRENCY', '1')
        timeout = os.environ.get('GUNICORN_TIMEOUT', os.environ.get('TIMEOUT', '120'))
        if not timeout or timeout == '':
            timeout = '120'

        cmd = f"gunicorn chidmano.wsgi:application --bind 0.0.0.0:{port} --workers {workers} --timeout {timeout} --access-logfile - --error-logfile -"

        subprocess.run(shlex.split(cmd))
