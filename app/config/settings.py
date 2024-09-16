import os
import dj_database_url
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

DJANGO_DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = 'app.urls'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
WSGI_APPLICATION = 'app.wsgi.application'
X_FRAME_OPTIONS = 'DENY'

# General
APPEND_SLASH = False
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
# If USE_I18N is set to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False
USE_L10N = True
USE_TZ = True

# CORS Settings
CORS_PREFLIGHT_MAX_AGE = 300
CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://postgres:@postgres:5432/postgres',
        conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 600))
    ),
}

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

THIRD_PARTY_APPS = [
    'rest_framework',                               # utilities for rest apis
    'django_filters',                               # for filtering rest endpoints
    'corsheaders',                                  # CORS header injection
    # JWT blacklist functionality provider
    'rest_framework_simplejwt.token_blacklist',
    'django_json_widget',                           # JSON viewer for admin
    'django_celery_beat',                           # scheduled tasks
    'import_export',                                # admin import / export
]

PROJECT_APPS = [
    'app.users',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATIC_URL = '/static/'
STATIC_ROOT = PARENT_DIR + "/static/"
STATICFILES_DIRS = []

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Media files
MEDIA_ROOT = '/media/'
MEDIA_URL = BASE_DIR + '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': STATICFILES_DIRS,
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

AUTH_USER_MODEL = 'users.User'

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

SIMPLE_JWT = {
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=1, minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1, minutes=5),

    'AUTH_TOKEN_CLASSES': ['rest_framework_simplejwt.tokens.SlidingToken'],
    'AUTH_HEADER_TYPES': ['Bearer', 'JWT'],

    'USER_ID_CLAIM': 'userId',
    'TOKEN_TYPE_CLAIM': 'type',
}


REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'nonFieldErrors',
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'app.auth.providers.SupabaseTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

CRON_CLASSES = []

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "cache"
    }
}

CELERY_BROKER_URL = os.getenv('REDIS_URL')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_IGNORE_RESULT = True
CELERYD_TASK_SOFT_TIME_LIMIT = 300
CELERYD_TASK_TIME_LIMIT = 500
CELERY_BEAT_SCHEDULER = os.getenv('CELERY_BEAT_SCHEDULER')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_JWT_SECRET = os.getenv('SUPABASE_JWT_SECRET')
SUPABASE_JWT_ALGORITHMS = os.getenv('SUPABASE_JWT_ALGORITHMS')
SUPABASE_JWT_ISSUER = os.getenv('SUPABASE_JWT_ISSUER')
