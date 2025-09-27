"""
Production settings for Chidmano
"""

from .settings import *
import os

# Production environment
PRODUCTION = True
DEBUG = False

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Allowed hosts for production
ALLOWED_HOSTS = [
    'chidmano.liara.app',
    'chidmano.liara.run', 
    'chidmano.ir',
    'www.chidmano.ir',
    '*.liara.ir',
    '*.liara.app',
    '*.liara.run'
]

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://chidmano.liara.app',
    'https://chidmano.liara.run',
    'https://chidmano.ir',
    'https://www.chidmano.ir'
]

# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Database
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(
            os.environ['DATABASE_URL'], 
            conn_max_age=600,
            ssl_require=True
        )
    }

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'store_analysis': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://localhost:6379/1'),
    }
}

# Session
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@chidmano.ir')

# Payment gateway settings for production
PAYMENT_GATEWAY = {
    'PING_PAYMENT': {
        'MERCHANT_ID': '17D62CFE490EA7C6BF20090BEA12A49FEB4482B02F8534696215A6DE23DF684A-1',
        'API_KEY': os.getenv('PING_API_KEY', ''),
        'CALLBACK_URL': os.getenv('PING_CALLBACK_URL', 'https://chidmano.liara.app/payment/callback/'),
        'RETURN_URL': os.getenv('PING_RETURN_URL', 'https://chidmano.liara.app/payment/return/'),
        'SANDBOX': os.getenv('PING_SANDBOX', 'False').lower() == 'true',
        'API_URL': 'https://api.pingpayment.ir'
    }
}
