"""
WSGI config for chidmano project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')

# Create a simple health check wrapper
def health_check_wrapper(environ, start_response):
    """Ultra-light health check that bypasses Django completely"""
    if environ.get('PATH_INFO') in ['/health', '/health/']:
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'OK']
    return get_wsgi_application()(environ, start_response)

application = health_check_wrapper 