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
        call_command('migrate', interactive=False, verbosity=1)
    except Exception as migrate_error:
        print(f"❌ Migration failed: {migrate_error}")
        sys.exit(1)

    print("🧱 Collecting static files (main.py)...")
    try:
        call_command('collectstatic', interactive=False, verbosity=0, ignore_patterns=['*.psd', '*.ai'])
    except Exception as collect_error:
        print(f"❌ Collectstatic failed: {collect_error}")
        sys.exit(1)

    # Start the application with gunicorn
    print("🌐 Starting Gunicorn server...")
    import subprocess
    import shlex

    port = os.environ.get('PORT', '8000')
    # Respect WEB_CONCURRENCY if provided; default to 1 to reduce memory usage
    workers = os.environ.get('WEB_CONCURRENCY', '1')
    timeout = os.environ.get('GUNICORN_TIMEOUT', os.environ.get('TIMEOUT', '120'))

    cmd = f"gunicorn chidmano.wsgi:application --bind 0.0.0.0:{port} --workers {workers} --timeout {timeout} --access-logfile - --error-logfile -"

    subprocess.run(shlex.split(cmd))
