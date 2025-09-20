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
    
    # Check if we're running gunicorn or development server
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        # Development server
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
    else:
        # Production server - this should be handled by gunicorn
        print("Starting Django application...")
        print("This should be run with gunicorn in production")
        print("Use: gunicorn chidmano.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120")
        sys.exit(1)
