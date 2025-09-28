"""
Django settings for chidmano project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Force-disable PostgreSQL SSL at libpq level to avoid "SSL was required" on Liara private DB
os.environ['PGSSLMODE'] = 'disable'
# Remove any env vars that force SSL unintentionally
for _var in ('PGSSLCERT', 'PGSSLKEY', 'PGSSLROOTCERT', 'PGREQUIRESSL', 'DATABASE_SSLMODE'):
    if _var in os.environ:
        os.environ.pop(_var, None)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '1-++(gh-*#+j1@5_c&ls2te#1n44iii98r%-0^2aan3h$&$esj')

# Payment Gateway Settings
PAYMENT_GATEWAY = {
    'PING_PAYMENT': {
        'MERCHANT_ID': '17D62CFE490EA7C6BF20090BEA12A49FEB4482B02F8534696215A6DE23DF684A-1',
        'API_KEY': os.getenv('PING_API_KEY', '73FD876658226A6A5C40A4B00A605CE5F9CC2C9C92ACFA1AEFF3350C9637C831-1'),
        'CALLBACK_URL': os.getenv('PING_CALLBACK_URL', 'https://chidmano.ir/payment/callback/'),
        'RETURN_URL': os.getenv('PING_RETURN_URL', 'https://chidmano.ir/payment/return/'),
        'SANDBOX': os.getenv('PING_SANDBOX', 'False').lower() == 'true',
        'API_URL': 'https://api.pingpayment.ir' if os.getenv('PING_SANDBOX', 'False').lower() == 'false' else 'https://api-sandbox.pingpayment.ir'
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'  # Default to False for production

# Enable debug for Render if needed
if os.getenv('RENDER'):
    DEBUG = True  # Enable debug on Render for troubleshooting

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver,*.liara.ir,*.liara.app,*.liara.run,chidmano.liara.app,chidmano.liara.run,chidmano.ir,www.chidmano.ir').split(',')

# Security settings for production
if os.getenv('PRODUCTION', 'False').lower() == 'true':
    # Liara handles SSL termination
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
else:
    # Development settings
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = None
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    SECURE_BROWSER_XSS_FILTER = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'store_analysis.apps.StoreAnalysisConfig',
    'chidmano',
]

MIDDLEWARE = [
    'chidmano.middleware.UltraLightHealthMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # برای static files در production
    'django.middleware.gzip.GZipMiddleware',  # Compression middleware
    # Remove per-site cache middlewares if any were added later (safety)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'chidmano.middleware.CanonicalHostRedirectMiddleware',
    'chidmano.middleware.NoIndexPrivatePathsMiddleware',
    'store_analysis.middleware.AnalyticsMiddleware',  # Analytics tracking
    'chidmano.middleware.CSPMiddleware',  # برای حل مشکل CSP ویدیوها
    'chidmano.middleware.CacheAndTimingMiddleware',
    'chidmano.seo_middleware.SEOMiddleware',  # SEO optimization
]

ROOT_URLCONF = 'chidmano.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'store_analysis', 'templates'),
            os.path.join(BASE_DIR, 'chidmano', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chidmano.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

import dj_database_url

# Database configuration - قطعی برای رفع مشکل SSL
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # استفاده از PostgreSQL با SSL غیرفعال - راه‌حل قطعی
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=False)
    }
    # این override را با set نه setdefault انجام می‌دهیم تا مطمئن باشیم sslmode غیرفعال است
    if 'postgresql' in DATABASES['default']['ENGINE']:
        DATABASES['default']['OPTIONS'] = {'sslmode': 'disable'}
else:
    # Development database configuration - using SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "store_analysis" / "static",
    BASE_DIR / "chidmano" / "static",
]

# Static files configuration for Liara (read-only filesystem)
if os.getenv('LIARA') == 'true':
    # Use WhiteNoise without collectstatic for Liara
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True
    WHITENOISE_MAX_AGE = 31536000
    # Don't set STATIC_ROOT for Liara to avoid read-only filesystem issues
elif not DEBUG:
    # Use WhiteNoise for serving static files in production
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True
    WHITENOISE_MAX_AGE = 31536000
    WHITENOISE_ROOT = BASE_DIR / 'staticfiles'
    WHITENOISE_INDEX_FILE = True
else:
    # Development static files
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv('MEDIA_ROOT', 'media'))

# تنظیمات آپلود فایل برای Liara (read-only filesystem)
if os.getenv('LIARA') == 'true':
    # استفاده از memory storage برای آپلود فایل‌ها
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.MemoryStorage'
    FILE_UPLOAD_HANDLERS = [
        'django.core.files.uploadhandler.MemoryFileUploadHandler',
    ]
    FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Media files configuration for production
if not DEBUG:
    # In production, serve media files through WhiteNoise
    WHITENOISE_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

# Security settings - optimized for Liara
if not DEBUG:
    # Production security settings - disabled for Liara compatibility
    SECURE_SSL_REDIRECT = False  # Liara handles SSL
    SESSION_COOKIE_SECURE = False  # Liara handles SSL termination
    CSRF_COOKIE_SECURE = False  # Liara handles SSL termination
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'SAMEORIGIN'  # More permissive for Liara
    SECURE_HSTS_SECONDS = 0  # Disabled for Liara
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
else:
    # Development security settings
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

# Development HTTPS settings (optional)
if DEBUG:
    # برای فعال‌سازی HTTPS در development
    # SECURE_SSL_REDIRECT = True
    # SESSION_COOKIE_SECURE = True
    # CSRF_COOKIE_SECURE = True
    pass

# AI Model settings
MODEL_PATH = os.path.join(BASE_DIR, os.getenv('MODEL_PATH', 'models'))
MODEL_VERSION = os.getenv('MODEL_VERSION', '1.0.0')

# OpenAI settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Payment Gateway Settings
ZARINPAL_MERCHANT_ID = os.getenv('ZARINPAL_MERCHANT_ID', 'test-merchant-id')
ZARINPAL_SANDBOX = os.getenv('ZARINPAL_SANDBOX', 'True').lower() == 'true'

# Liara AI Settings
LIARA_AI_API_KEY = os.getenv('LIARA_AI_API_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2OGM3MjU1NjJlYTVmMGYxNTA3MWU5ZDgiLCJ0eXBlIjoiYXV0aCIsImlhdCI6MTc1ODE0NzM2Mn0._pcbp8DXGwSBCub-SFj5eRNmEYHgq15QyU4-wND-UPo')
USE_LIARA_AI = os.getenv('USE_LIARA_AI', 'True').lower() == 'true'
FALLBACK_TO_OLLAMA = os.getenv('FALLBACK_TO_OLLAMA', 'True').lower() == 'true'

# Payment - PayPing
PAYPING_TOKEN = os.getenv('PAYPING_TOKEN', '17CDFDF0A740450AEFA8793D9D13A8616591F313878983911EDC2B7ADAEC325F-1')

# AI Analysis Settings
AI_ANALYSIS_CACHE_TIMEOUT = 3600  # 1 hour
AI_ANALYSIS_MAX_RETRIES = 3
AI_ANALYSIS_TIMEOUT = 30

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@chidmano.com')

# Site Settings
SITE_URL = os.getenv('SITE_URL', 'https://chidmano.liara.app')

# Authentication settings
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'store_analysis:user_dashboard'
LOGOUT_REDIRECT_URL = 'home'

# Celery settings
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Performance Optimization Settings
# Cache settings - optimized for production
if DEBUG:
    # Development cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
            'TIMEOUT': 300,  # 5 minutes default
        }
    }
else:
    # Production cache - use in-memory to avoid missing DB cache table in PaaS
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'prod-locmem',
            'TIMEOUT': 900,  # 15 minutes
        }
    }

# Database optimization
if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    # SQLite optimization
    DATABASES['default']['OPTIONS'] = {
        'timeout': 20,
        'check_same_thread': False,
    }
else:
    # PostgreSQL optimization
    DATABASES['default']['CONN_MAX_AGE'] = 600  # 10 minutes connection pooling

# Static files optimization - handled above in production section

# Template optimization
if not DEBUG:
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]
    TEMPLATES[0]['APP_DIRS'] = False

# Session optimization
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# SESSION_CACHE_ALIAS = 'default'

# Logging configuration - simplified for Liara read-only filesystem
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'store_analysis': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Performance monitoring
PERFORMANCE_MONITORING = {
    'enabled': os.getenv('PERFORMANCE_MONITORING', 'True') == 'True',
    'slow_query_threshold': 1.0,  # seconds
    'cache_hit_rate_threshold': 0.8,  # 80%
    'memory_usage_threshold': 0.9,  # 90%
}

# File upload optimization
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
temp_dir = BASE_DIR / 'temp'
temp_dir.mkdir(exist_ok=True)
FILE_UPLOAD_TEMP_DIR = str(temp_dir)

# Security headers (disabled for development)
if not DEBUG:
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
else:
    SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'unsafe-none'

# Security settings
SECURITY_SETTINGS = {
    'rate_limiting': {
        'enabled': True,
        'default_requests': 100,
        'default_window': 60,
        'login_requests': 5,
        'login_window': 300,
        'api_requests': 50,
        'api_window': 60,
        'upload_requests': 10,
        'upload_window': 300,
    },
    'file_upload': {
        'max_size': 10 * 1024 * 1024,  # 10MB
        'allowed_extensions': ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx'],
        'allowed_types': ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'],
    },
    'input_validation': {
        'enabled': True,
        'max_length': 1000,
        'suspicious_patterns': [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'vbscript:',
            r'onload=',
            r'onerror=',
        ],
    },
    'session_security': {
        'session_timeout': 3600,  # 1 hour
        'max_sessions_per_user': 5,
        'force_logout_on_password_change': True,
    },
}

# Custom exception handlers
HANDLER404 = 'chidmano.error_handlers.custom_404_handler'
HANDLER500 = 'chidmano.error_handlers.custom_500_handler'

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1'],
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://localhost:8443",
    "https://127.0.0.1:8443",
]

# Add production domains
if not DEBUG:
    CORS_ALLOWED_ORIGINS.extend([
        "https://your-domain.com",
        "https://www.your-domain.com",
    ])

CORS_ALLOW_CREDENTIALS = True

# CSRF settings for HTTPS proxy
CSRF_TRUSTED_ORIGINS = [
    "https://localhost:8443",
    "https://127.0.0.1:8443",
    "https://chidmano.liara.run",
    "https://chidmano.liara.app",
    "https://*.liara.app",
    "https://*.liara.run",
    "https://chidmano.ir",
    "https://www.chidmano.ir",
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Django Channels Configuration
ASGI_APPLICATION = 'chidmano.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
        # برای production از Redis استفاده کنید:
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     "hosts": [('127.0.0.1', 6379)],
        # },
    },
}

# HTTPS Settings - handled above in security section