"""
Django settings for chidmano project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '1-++(gh-*#+j1@5_c&ls2te#1n44iii98r%-0^2aan3h$&$esj')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'  # Default to True for development

# Enable debug for Render if needed
if os.getenv('RENDER'):
    DEBUG = True  # Enable debug on Render for troubleshooting

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver,*.liara.ir,*.liara.app,chidmano.liara.app').split(',')

# Security settings for development
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
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # برای static files در production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

# Database configuration - Force SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Only use PostgreSQL in production with explicit environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL and (os.getenv('RENDER') or os.getenv('LIARA') or os.getenv('PRODUCTION')):
    # Production database configuration
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    # Add SSL mode for PostgreSQL
    if 'postgresql' in DATABASES['default']['ENGINE']:
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
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
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "store_analysis" / "static",
]

# Add whitenoise for static files in production
if not DEBUG:
    try:
        import whitenoise
        MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
        STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
        WHITENOISE_USE_FINDERS = True
        WHITENOISE_AUTOREFRESH = True
    except ImportError:
        # Fallback if whitenoise is not available
        pass

MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv('MEDIA_ROOT', 'media'))

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

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'True').lower() == 'true'
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
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
LIARA_AI_API_KEY = os.getenv('LIARA_AI_API_KEY', '')
USE_LIARA_AI = os.getenv('USE_LIARA_AI', 'True').lower() == 'true'
FALLBACK_TO_OLLAMA = os.getenv('FALLBACK_TO_OLLAMA', 'True').lower() == 'true'

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
# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,  # 5 minutes default
    }
}

# Database optimization - only for SQLite
if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    DATABASES['default']['OPTIONS'] = {
        'timeout': 20,
        'check_same_thread': False,
    }

# Static files optimization
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

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

# Logging configuration
logs_dir = BASE_DIR / 'logs'
logs_dir.mkdir(exist_ok=True)

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
        'production': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': logs_dir / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'production' if not DEBUG else 'simple',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': logs_dir / 'error.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'store_analysis': {
            'handlers': ['file', 'console', 'error_file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file', 'console'],
            'level': 'ERROR',
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
]

# Add production domains
if not DEBUG:
    CSRF_TRUSTED_ORIGINS.extend([
        "https://your-domain.com",
        "https://www.your-domain.com",
    ])

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

# HTTPS Settings for production
if not DEBUG:
    # Production settings - HTTPS disabled for Liara deployment
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = None
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    # Development settings
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = None
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    SECURE_BROWSER_XSS_FILTER = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SAMESITE = 'Lax' 