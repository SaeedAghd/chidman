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
    
    # Skip migrations and collectstatic in main.py - let gunicorn handle them
    print("📊 Skipping migrations in main.py - will be handled by gunicorn")
    print("📁 Skipping collectstatic in main.py - will be handled by gunicorn")
    
    # Start the application with gunicorn
    print("🌐 Starting Gunicorn server...")
    import subprocess
    import shlex
    
    port = os.environ.get('PORT', '8000')
    cmd = f"gunicorn chidmano.wsgi:application --bind 0.0.0.0:{port} --workers 3 --timeout 120 --max-requests 1000 --max-requests-jitter 100 --access-logfile - --error-logfile -"
    
    subprocess.run(shlex.split(cmd))
