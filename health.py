#!/usr/bin/env python3
"""
Ultra-light health check endpoint for Liara
This bypasses Django completely and returns OK immediately
"""

def application(environ, start_response):
    """WSGI application that handles health checks"""
    path = environ.get('PATH_INFO', '')
    
    if path in ['/health', '/health/']:
        start_response('200 OK', [
            ('Content-Type', 'text/plain'),
            ('Content-Length', '2')
        ])
        return [b'OK']
    
    # For all other paths, return 404
    start_response('404 Not Found', [
        ('Content-Type', 'text/plain'),
        ('Content-Length', '9')
    ])
    return [b'Not Found']
