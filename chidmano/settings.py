"""
Django settings for chidmano project.
"""

from pathlib import Path
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# Force-disable PostgreSQL SSL at libpq level to avoid "SSL was required" on Liara private DB
os.environ['PGSSLMODE'] = 'disable'

# Remove any env vars that force SSL unintentionally (use pop to avoid empty loop/body)
for _var in ('PGSSLCERT', 'PGSSLKEY', 'PGSSLROOTCERT', 'PGREQUIRESSL', 'DATABASE_SSLMODE'):
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
        'MERCHANT_ID': '7DF9DCCE0D75419789003B00D44E561EC16094F068C2E72A4AD28E3DBF4DC5E8-1',  # به‌روزرسانی طبق درخواست کاربر
        'API_KEY': os.getenv('PING_API_KEY', 'EB28E90039CB8FCD97F3D778FC7644917A1391217F9E47046EA864EA25331445-1'),
        'CALLBACK_URL': os.getenv('PING_CALLBACK_URL', 'https://chidmano.ir/store/payment/payping/callback/'),
        'RETURN_URL': os.getenv('PING_RETURN_URL', 'https://chidmano.ir/store/payment/payping/return/'),
        'SANDBOX': True,  # فعال کردن حالت تست برای کاربران تکراری
        'API_URL': 'https://api-sandbox.pingpayment.ir',  # استفاده از sandbox برای تست
        'TRUST_BADGE': True,  # فعال‌سازی نماد اعتماد
        'VERIFY_SSL': True
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'  # Default to True for local development

# Email Configuration for Password Reset
# در محیط local از console backend استفاده می‌کنیم تا ایمیل‌ها در ترمینال نمایش داده شوند
if DEBUG:
    # برای محیط development: ایمیل‌ها در console نمایش داده می‌شوند
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'noreply@chidmano.local'
    print("📧 Email Backend: Console (برای مشاهده ایمیل‌ها در ترمینال)")
else:
    # برای محیط production: استفاده از SMTP
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'info@chidmano.com')

# Password Reset Settings
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour
PASSWORD_RESET_EMAIL_TEMPLATE = 'registration/password_reset_email.html'
PASSWORD_RESET_SUBJECT_TEMPLATE = 'registration/password_reset_subject.txt'

# Enable debug for Render if needed
if os.getenv('RENDER'):
    DEBUG = True  # Enable debug on Render for troubleshooting

# Production Security Settings
if not DEBUG:
    # Security Settings for Production
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Session Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # CSRF Security
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = 'Strict'
    
    # X-Frame-Options
    X_FRAME_OPTIONS = 'DENY'
    
    # Content Security Policy
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver,*.liara.ir,*.liara.app,*.liara.run,chidmano.liara.app,chidmano.liara.run,chidmano.ir,www.chidmano.ir').split(',')

# Security settings for production - removed duplicate and conflicting settings
# Production security will be handled below based on PRODUCTION environment variable

# Application definition

# Site ID for django.contrib.sites
SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
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
    # 'chidmano.middleware.CanonicalHostRedirectMiddleware',  # Temporarily disabled for local testing
    'chidmano.middleware.NoIndexPrivatePathsMiddleware',
    'chidmano.middleware.RateLimitMiddleware',  # Rate Limiting
    'store_analysis.middleware.AnalyticsMiddleware',  # Analytics tracking
    'chidmano.middleware.CSPMiddleware',  # برای حل مشکل CSP ویدیوها
    # 'chidmano.middleware.CacheAndTimingMiddleware',  # Temporarily disabled
    'chidmano.seo_middleware.SEOMiddleware',  # SEO optimization
    'chidmano.seo_middleware.AdvancedSEOMiddleware',  # Advanced SEO
    'chidmano.middleware.SecurityHeadersMiddleware',  # Security Headers
    'chidmano.seo_middleware.SEOLoggingMiddleware',  # SEO Logging
    'chidmano.browser_compatibility_middleware.BrowserCompatibilityMiddleware',  # Browser compatibility
    'chidmano.browser_compatibility_middleware.ConcurrencyLimitMiddleware',  # Concurrency limit
    'chidmano.browser_compatibility_middleware.SessionFixMiddleware',  # Session fix
    'chidmano.browser_compatibility_middleware.SEOEnhancementMiddleware',  # SEO enhancement
    'chidmano.browser_compatibility_middleware.SearchEngineOptimizationMiddleware',  # Search engine optimization
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

LANGUAGE_CODE = 'en-us'  # Fixed: Use standard language code

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True  # Added: Enable localization

USE_TZ = True

# Additional language settings to prevent i18n errors
LANGUAGES = [
    ('en', 'English'),
    ('fa', 'فارسی'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "store_analysis" / "static",
    BASE_DIR / "chidmano" / "static",
]

# Always define STATIC_ROOT so staticfiles alias can initialize
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Choose static backend per environment
if os.getenv('LIARA') == 'true':
    STATIC_BACKEND = 'whitenoise.storage.CompressedStaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True
    WHITENOISE_MAX_AGE = 31536000
elif not DEBUG:
    STATIC_BACKEND = 'whitenoise.storage.CompressedStaticFilesStorage'  # تغییر از ManifestStaticFilesStorage
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True
    WHITENOISE_MAX_AGE = 31536000
    WHITENOISE_ROOT = BASE_DIR / 'staticfiles'
    WHITENOISE_INDEX_FILE = True
else:
    STATIC_BACKEND = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Explicit storages mapping (Django 4.2+)
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': STATIC_BACKEND,
    },
}

MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv('MEDIA_ROOT', 'media'))

# SEO Settings
BASE_DOMAIN = 'chidmano.ir'
SITE_NAME = 'چیدمانو - تحلیل هوشمند فروشگاه و مغازه'

# Google Analytics
GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID', 'G-XXXXXXXXXX')

# Google Search Console
GOOGLE_SEARCH_CONSOLE_VERIFICATION = os.getenv('GOOGLE_SEARCH_CONSOLE_VERIFICATION', '')

# Facebook Pixel
FACEBOOK_PIXEL_ID = os.getenv('FACEBOOK_PIXEL_ID', '')

# Bing Webmaster
BING_WEBMASTER_VERIFICATION = os.getenv('BING_WEBMASTER_VERIFICATION', '')

# Yandex Verification
YANDEX_VERIFICATION = os.getenv('YANDEX_VERIFICATION', '')

# تنظیمات آپلود فایل برای Liara (read-only filesystem)
if os.getenv('LIARA') == 'true':
    # Use hybrid handlers: keep small files in memory, large files spill to temp dir
    FILE_UPLOAD_HANDLERS = [
        'django.core.files.uploadhandler.MemoryFileUploadHandler',
        'django.core.files.uploadhandler.TemporaryFileUploadHandler',
    ]
    # افزایش سقف آپلود برای فرم‌های چندفایلی
    FILE_UPLOAD_MAX_MEMORY_SIZE = 32 * 1024 * 1024  # 32MB
    DATA_UPLOAD_MAX_MEMORY_SIZE = 64 * 1024 * 1024  # 64MB

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
PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'

if PRODUCTION:
    # Production security settings - optimized for Liara
    SECURE_SSL_REDIRECT = False  # Liara handles SSL termination
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
elif not DEBUG:
    # Non-production but not debug (testing/staging)
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
else:
    # Development security settings
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = None
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'unsafe-none'

# Development HTTPS settings (optional)
if DEBUG:
    # برای فعال‌سازی HTTPS در development
    # SECURE_SSL_REDIRECT = True
    # SESSION_COOKIE_SECURE = True
    # CSRF_COOKIE_SECURE = True
    pass

# SEO and Domain settings
BASE_DOMAIN = 'chidmano.ir'
SITE_NAME = 'چیدمانو'
SITE_DESCRIPTION = 'تحلیل پیشرفته فروشگاه با هوش مصنوعی'

# Search Engine Verification Codes
GOOGLE_SITE_VERIFICATION = os.getenv('GOOGLE_SITE_VERIFICATION', '')
BING_SITE_VERIFICATION = os.getenv('BING_SITE_VERIFICATION', '')
YANDEX_SITE_VERIFICATION = os.getenv('YANDEX_SITE_VERIFICATION', '')

# Analytics
GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID', '')
GOOGLE_TAG_MANAGER_ID = os.getenv('GOOGLE_TAG_MANAGER_ID', '')

# Payment Gateway Settings
ZARINPAL_MERCHANT_ID = os.getenv('ZARINPAL_MERCHANT_ID', 'test-merchant-id')
ZARINPAL_SANDBOX = os.getenv('ZARINPAL_SANDBOX', 'True').lower() == 'true'

# Liara AI Settings
# ⚠️ مهم: در production، API key باید از environment variable خوانده شود
# هرگز API key را مستقیماً در کد قرار ندهید
LIARA_AI_API_KEY = os.getenv('LIARA_AI_API_KEY', '')
LIARA_AI_BASE_URL = os.getenv('LIARA_AI_BASE_URL', 'https://api.liara.ir/v1')
LIARA_AI_TIMEOUT = int(os.getenv('LIARA_AI_TIMEOUT', '90'))  # ثانیه
USE_LIARA_AI = os.getenv('USE_LIARA_AI', 'True').lower() == 'true'
FALLBACK_TO_OLLAMA = os.getenv('FALLBACK_TO_OLLAMA', 'True').lower() == 'true'

if not LIARA_AI_API_KEY:
    logger.warning("⚠️ LIARA_AI_API_KEY تنظیم نشده است - AI features غیرفعال خواهند بود")
else:
    logger.info(f"✅ Liara AI configured (base_url={LIARA_AI_BASE_URL}, timeout={LIARA_AI_TIMEOUT}s)")

# Payment - PayPing
# PayPing Settings - Token جدید برای پرداخت و کیف پول
PAYPING_TOKEN = os.getenv('PAYPING_TOKEN', 'D0C2E2134B072175DAC950AAEB776938C8E024C4B1942AF6FF760A3615B67685-1')
PAYPING_SANDBOX = os.getenv('PAYPING_SANDBOX', 'False').lower() == 'true'  # Force production due to sandbox DNS issues
PAYPING_CALLBACK_URL = os.getenv('PAYPING_CALLBACK_URL', 'https://chidmano.ir/store/payment/payping/callback/')
PAYPING_RETURN_URL = os.getenv('PAYPING_RETURN_URL', 'https://chidmano.ir/store/payment/payping/return/')

# Mock mode for testing when PayPing token has restrictions
PAYPING_MOCK_MODE = os.getenv('PAYPING_MOCK_MODE', 'True').lower() == 'true'

# AI Analysis Settings
AI_ANALYSIS_CACHE_TIMEOUT = 3600  # 1 hour
AI_ANALYSIS_MAX_RETRIES = 3
AI_ANALYSIS_TIMEOUT = 30

# Email Settings (این تنظیمات قبلاً در بالا انجام شده است)
# اگر DEBUG=True باشد از console backend استفاده می‌شود
# در غیر این صورت از SMTP استفاده می‌شود

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
    # Template caching - disabled for development
    # TEMPLATES[0]['OPTIONS']['loaders'] = [
    #     ('django.template.loaders.cached.Loader', [
    #         'django.template.loaders.filesystem.Loader',
    #         'django.template.loaders.app_directories.Loader',
    #     ]),
    # ]
    # TEMPLATES[0]['APP_DIRS'] = False
    pass

# Session optimization
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'  # برای سازگاری با مرورگرها
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# CSRF settings
CSRF_COOKIE_AGE = 3600
CSRF_COOKIE_HTTPONLY = False  # برای JavaScript access
CSRF_COOKIE_SAMESITE = 'Lax'  # برای سازگاری با مرورگرها
CSRF_USE_SESSIONS = False
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'

# Logging configuration - optimized for Liara (read-only filesystem)
# در Liara، فقط از console handler استفاده می‌کنیم
if os.getenv('LIARA') == 'true' or not DEBUG:
    # Production/Liara: فقط console logging (Liara logs را capture می‌کند)
    import logging.config
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '{asctime} {levelname} {name} {message}',
                'style': '{',
            },
            'verbose': {
                'format': '{asctime} {levelname} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                'stream': 'ext://sys.stdout',
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
else:
    # Development: console + file logging
    import logging.config
    # Ensure logs directory exists
    logs_dir = os.path.join(BASE_DIR, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '{asctime} {levelname} {name} {message}',
                'style': '{',
            },
            'verbose': {
                'format': '{asctime} {levelname} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(logs_dir, 'django.log'),
                'formatter': 'verbose',
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

# Django will apply logging configuration automatically

# Performance monitoring
PERFORMANCE_MONITORING = {
    'enabled': os.getenv('PERFORMANCE_MONITORING', 'True') == 'True',
    'slow_query_threshold': 1.0,  # seconds
    'cache_hit_rate_threshold': 0.8,  # 80%
    'memory_usage_threshold': 0.9,  # 90%
}

# File upload optimization (defaults; Liara overrides above)
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv('FILE_UPLOAD_MAX_MEMORY_SIZE', 32 * 1024 * 1024))
DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv('DATA_UPLOAD_MAX_MEMORY_SIZE', 64 * 1024 * 1024))
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
        "https://chidmano.liara.run",
        "https://chidmano.liara.app",
        "https://chidmano.ir",
        "https://www.chidmano.ir",
    ])

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = DEBUG  # فقط در development
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours

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
