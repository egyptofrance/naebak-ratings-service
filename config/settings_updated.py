"""
إعدادات Django محدثة لخدمة التقييمات الذكية - مشروع نائبك
"""
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'django_ratelimit',
]

LOCAL_APPS = [
    'apps.ratings',
    'apps.users',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_ratelimit.middleware.RatelimitMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'naebak_ratings'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'charset': 'utf8',
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
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
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'rating': '30/hour',
        'rating_create': '10/hour',
        'rating_report': '5/hour',
    }
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=int(os.environ.get('JWT_ACCESS_TOKEN_LIFETIME', '1'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('JWT_REFRESH_TOKEN_LIFETIME', '7'))),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': os.environ.get('JWT_ALGORITHM', 'HS256'),
    'SIGNING_KEY': os.environ.get('JWT_SECRET_KEY', SECRET_KEY),
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    
    'JTI_CLAIM': 'jti',
    
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Frontend
    "http://127.0.0.1:3000",
    "http://localhost:3001",  # Admin Frontend
    "http://127.0.0.1:3001",
]

CORS_ALLOW_CREDENTIALS = True

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session backend
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Rating system settings
RATING_SYSTEM = {
    'ENABLE_RATINGS': os.environ.get('ENABLE_RATINGS', 'True').lower() == 'true',
    'ENABLE_COMMENTS': os.environ.get('ENABLE_COMMENTS', 'True').lower() == 'true',
    'REQUIRE_LOGIN': os.environ.get('REQUIRE_LOGIN', 'True').lower() == 'true',
    
    # حدود التقييم
    'MAX_RATINGS_PER_USER_PER_DAY': int(os.environ.get('MAX_RATINGS_PER_USER_PER_DAY', '10')),
    'MIN_RATING_INTERVAL_MINUTES': int(os.environ.get('MIN_RATING_INTERVAL_MINUTES', '5')),
    'MAX_COMMENT_LENGTH': int(os.environ.get('MAX_COMMENT_LENGTH', '500')),
    
    # إعدادات التقييمات الذكية
    'DEFAULT_DISPLAY_MODE': os.environ.get('DEFAULT_DISPLAY_MODE', 'mixed'),
    'DEFAULT_FAKE_RATING': float(os.environ.get('DEFAULT_FAKE_RATING', '4.5')),
    'DEFAULT_FAKE_COUNT': int(os.environ.get('DEFAULT_FAKE_COUNT', '1000')),
    'DEFAULT_REAL_WEIGHT': float(os.environ.get('DEFAULT_REAL_WEIGHT', '0.3')),
    'DEFAULT_FAKE_WEIGHT': float(os.environ.get('DEFAULT_FAKE_WEIGHT', '0.7')),
    
    # إعدادات الأمان
    'ENABLE_IP_TRACKING': os.environ.get('ENABLE_IP_TRACKING', 'True').lower() == 'true',
    'BLOCK_DUPLICATE_IPS': os.environ.get('BLOCK_DUPLICATE_IPS', 'True').lower() == 'true',
    'AUTO_VERIFY_RATINGS': os.environ.get('AUTO_VERIFY_RATINGS', 'False').lower() == 'true',
    'MODERATE_COMMENTS': os.environ.get('MODERATE_COMMENTS', 'True').lower() == 'true',
    
    # إعدادات الإشعارات
    'NOTIFY_ON_NEW_RATING': os.environ.get('NOTIFY_ON_NEW_RATING', 'True').lower() == 'true',
    'NOTIFY_ON_REPORT': os.environ.get('NOTIFY_ON_REPORT', 'True').lower() == 'true',
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@naebak.com')

# Celery settings (for async tasks)
if os.environ.get('USE_CELERY', 'False').lower() == 'true':
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE
    
    # Rating tasks
    CELERY_TASK_ROUTES = {
        'apps.ratings.tasks.update_rating_statistics': {'queue': 'statistics'},
        'apps.ratings.tasks.send_rating_notification': {'queue': 'notifications'},
        'apps.ratings.tasks.moderate_rating_comment': {'queue': 'moderation'},
        'apps.ratings.tasks.cleanup_old_ratings': {'queue': 'cleanup'},
    }

# Content moderation settings
CONTENT_MODERATION = {
    'ENABLE_AUTO_MODERATION': os.environ.get('ENABLE_AUTO_MODERATION', 'True').lower() == 'true',
    'BLOCK_OFFENSIVE_LANGUAGE': os.environ.get('BLOCK_OFFENSIVE_LANGUAGE', 'True').lower() == 'true',
    'PROFANITY_FILTER_ENABLED': os.environ.get('PROFANITY_FILTER_ENABLED', 'True').lower() == 'true',
    'SPAM_DETECTION_ENABLED': os.environ.get('SPAM_DETECTION_ENABLED', 'True').lower() == 'true',
}

# Analytics settings
ANALYTICS = {
    'ENABLE_ANALYTICS': os.environ.get('ENABLE_ANALYTICS', 'True').lower() == 'true',
    'UPDATE_STATS_INTERVAL_MINUTES': int(os.environ.get('UPDATE_STATS_INTERVAL_MINUTES', '60')),
    'CACHE_STATS_DURATION_SECONDS': int(os.environ.get('CACHE_STATS_DURATION_SECONDS', '3600')),
}

# Rate limiting settings
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'

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
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
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
        'apps.ratings': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Session settings
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# CSRF settings
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Cloud storage settings (optional)
if os.environ.get('USE_CLOUD_STORAGE', 'False').lower() == 'true':
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME', 'naebak-ratings')
    GS_PROJECT_ID = os.environ.get('GS_PROJECT_ID', '')
    GS_CREDENTIALS = os.environ.get('GS_CREDENTIALS', '')

# Monitoring settings
if os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR
    )
    
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration(), sentry_logging],
        traces_sample_rate=0.1,
        send_default_pii=True
    )

# External services URLs
AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL', 'http://localhost:8001')
COMPLAINTS_SERVICE_URL = os.environ.get('COMPLAINTS_SERVICE_URL', 'http://localhost:8002')
MESSAGING_SERVICE_URL = os.environ.get('MESSAGING_SERVICE_URL', 'http://localhost:8003')
CONTENT_SERVICE_URL = os.environ.get('CONTENT_SERVICE_URL', 'http://localhost:8005')
ADMIN_SERVICE_URL = os.environ.get('ADMIN_SERVICE_URL', 'http://localhost:8006')

# Smart rating settings
SMART_RATING = {
    'AUTO_CREATE_SMART_RATINGS': os.environ.get('AUTO_CREATE_SMART_RATINGS', 'True').lower() == 'true',
    'BULK_UPDATE_BATCH_SIZE': int(os.environ.get('BULK_UPDATE_BATCH_SIZE', '100')),
    'RECALCULATE_INTERVAL_HOURS': int(os.environ.get('RECALCULATE_INTERVAL_HOURS', '24')),
}

# Data cleanup settings
DATA_CLEANUP = {
    'AUTO_DELETE_OLD_RATINGS': os.environ.get('AUTO_DELETE_OLD_RATINGS', 'False').lower() == 'true',
    'OLD_RATING_RETENTION_DAYS': int(os.environ.get('OLD_RATING_RETENTION_DAYS', '365')),
    'AUTO_DELETE_REPORTED_RATINGS_DAYS': int(os.environ.get('AUTO_DELETE_REPORTED_RATINGS_DAYS', '90')),
}

# Performance settings
RATING_PAGINATION_SIZE = 20
STATISTICS_CACHE_TIMEOUT = 3600  # 1 hour
BULK_OPERATION_BATCH_SIZE = 1000

# API versioning
API_VERSION = 'v1'
API_TITLE = 'Naebak Ratings API'
API_DESCRIPTION = 'API for smart ratings system in Naebak platform'

# Feature flags
FEATURE_FLAGS = {
    'ENABLE_SMART_RATINGS': os.environ.get('ENABLE_SMART_RATINGS', 'True').lower() == 'true',
    'ENABLE_RATING_ANALYTICS': os.environ.get('ENABLE_RATING_ANALYTICS', 'True').lower() == 'true',
    'ENABLE_BULK_OPERATIONS': os.environ.get('ENABLE_BULK_OPERATIONS', 'True').lower() == 'true',
    'ENABLE_RATING_REPORTS': os.environ.get('ENABLE_RATING_REPORTS', 'True').lower() == 'true',
}
