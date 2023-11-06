"""
Django settings for shuddhi project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from pathlib import Path
import os
import dj_database_url
from environ import Env              
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = Path(__file__).resolve().parent.parent

# This is to import the environment variables in the .env file
env = Env()                      

env.read_env(os.path.join(BASE_DIR, '.env'))  # This reads the environment variables from the .env file

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# # # # # # # # # 
# Loading all environemtn Variables
# # # # # # # # 

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=False)
# This will enable queries intended for automated testing, false for production
ENABLED_AUTOMATED_TESTING = env.bool('ENABLED_AUTOMATED_TESTING', default=not DEBUG)
# Authorized origins
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')
# Whether or not requests from other origins are allowed
CORS_ORIGIN_ALLOW_ALL = env.bool('DJANGO_CORS_ORIGIN_ALLOW_ALL')
# Email host used to send email
ENV_EMAIL_HOST=env('ENV_EMAIL_HOST',default='smtp.gmail.com')
# The SMTP host user 
ENV_EMAIL_HOST_USER = env('ENV_EMAIL_HOST_USER',default='')
# The password for SMTP sender
ENV_EMAIL_HOST_PASSWORD = env('ENV_EMAIL_HOST_PASSWORD',default='')
# setting default email from which emails will be sent
ENV_DEFAULT_FROM_EMAIL = env('ENV_DEFAULT_FROM_EMAIL', default='noreply@vidhya.io')
# SMTP port
ENV_EMAIL_PORT = env('ENV_EMAIL_PORT',default=587)
# Whether we use TLS for email encryption
ENV_EMAIL_USE_TLS = env.bool('ENV_EMAIL_USE_TLS',default=False)
# Whether we use SSL for email encryption
ENV_EMAIL_USE_SSL = env.bool('ENV_EMAIL_USE_SSL',default=False)
# Lets us set the domain of the site via environment variable. Requires migration to set it in DB
FRONTEND_DOMAIN_URL = env('FRONTEND_DOMAIN_URL')
# This is for the migration that sets the domain name
SITE_ID = 1
# This is the URL for the redis server
REDIS_URL = env('REDIS_URL')
# This is for the google auth SSO
ENV_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('ENV_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
ENV_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('ENV_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
ENV_SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = env.list('ENV_SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE')
ENV_SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = env.list('ENV_SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA')
ENV_SOCIAL_AUTH_LOGIN_ERROR_URL = env('ENV_SOCIAL_AUTH_LOGIN_ERROR_URL')
ENV_SOCIAL_AUTH_RAISE_EXCEPTIONS = env.bool('ENV_SOCIAL_AUTH_RAISE_EXCEPTIONS',default=False)
ENV_SOCIAL_AUTH_LOGIN_REDIRECT_URL = env('ENV_SOCIAL_AUTH_LOGIN_REDIRECT_URL')
# 
ENV_SHUDDHI_VIDHYA_INSTITUTION_ID = env('SHUDDHI_VIDHYA_INSTITUTION_ID',default=1)

DEFAULT_AVATARS = {
    'USER': 'https://i.imgur.com/KHtECqa.png',
    'INSTITUTION': 'https://i.imgur.com/dPO1MlY.png',
    'GROUP': 'https://i.imgur.com/hNdMk4c.png'
}
# Application definition


# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

if DEBUG:
    # If using development, it prints the email in the console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = ENV_EMAIL_HOST
EMAIL_HOST_USER = ENV_EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = ENV_EMAIL_HOST_PASSWORD
EMAIL_PORT = ENV_EMAIL_PORT
EMAIL_USE_TLS = ENV_EMAIL_USE_TLS
EMAIL_USE_SSL = ENV_EMAIL_USE_SSL
DEFAULT_FROM_EMAIL=ENV_DEFAULT_FROM_EMAIL

INSTALLED_APPS = [
    'channels',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # This is for altering the domain name in the migration
    'vidhya',
    'graphene_django',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
    'graphql_auth',
    'rest_framework',
    'django_filters',
    'social_django',
    # 'social.apps.django_app.default',
]

GRAPHENE = {
    'SCHEMA': 'shuddhi.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
    "SUBSCRIPTION_PATH": "/ws/graphql"
}

MIDDLEWARE = [
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',    
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.utils.UpdateLastActivityMiddleware'
]

AUTHENTICATION_BACKENDS = [
    'graphql_auth.backends.GraphQLAuthBackend',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ENV_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ENV_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ENV_SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ENV_SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA
SOCIAL_AUTH_LOGIN_ERROR_URL = ENV_SOCIAL_AUTH_LOGIN_ERROR_URL
SOCIAL_AUTH_RAISE_EXCEPTIONS = ENV_SOCIAL_AUTH_RAISE_EXCEPTIONS
SOCIAL_AUTH_LOGIN_REDIRECT_URL = ENV_SOCIAL_AUTH_LOGIN_REDIRECT_URL
SOCIAL_AUTH_ALLOWED_REDIRECT_HOSTS = [FRONTEND_DOMAIN_URL,'localhost:8000']
SOCIAL_AUTH_CLEAN_USERNAMES = False


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
)
GRAPHQL_AUTH = {
    "ALLOW_LOGIN_NOT_VERIFIED": True,
    "SEND_ACTIVATION_EMAIL": False,
    "ALLOW_PASSWORDLESS_REGISTRATION": False
}

GRAPHQL_JWT = {
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ResendActivationEmail",
        "graphql_auth.mutations.SendPasswordResetEmail",
        "graphql_auth.mutations.PasswordReset",
        "graphql_auth.mutations.ObtainJSONWebToken",
        "graphql_auth.mutations.VerifyToken",
        "graphql_auth.mutations.RefreshToken",
        "graphql_auth.mutations.RevokeToken",
    ],
    'JWT_PAYLOAD_HANDLER': 'common.utils.jwt_payload',
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    'JWT_REUSE_REFRESH_TOKENS': True, # Eliminates creation of new db records every time refreshtoken is requested.
    'JWT_EXPIRATION_DELTA': timedelta(minutes=60), # Expiry time of token
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7), # Expiry time of refreshToken
}

ROOT_URLCONF = 'shuddhi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'shuddhi.wsgi.application'

ASGI_APPLICATION = 'shuddhi.router.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shuddhidb',
        'USER': 'shuddhiadmin',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '5432',
    }
}

DATABASE_URL = os.environ.get('DATABASE_URL')
db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=500, ssl_require=True)
DATABASES['default'].update(db_from_env)

CACHE_HOST='redis'
CACHE_PORT=6379

#if not REDIS_URL:
REDIS_URL = f'{CACHE_HOST}://{CACHE_HOST}:{CACHE_PORT}/1'
    
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION":     REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "VIDHYA"
    }
}


# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("redis", 6379)],
#         },
#     },
# }


hosts = [REDIS_URL]

if DEBUG:
    hosts = [('redis', 6379)]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": hosts,
        },
    },
}

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": [REDIS_URL],
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient"
#         }
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/



STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATICFILES_STORAGE =  'django.contrib.staticfiles.storage.StaticFilesStorage' 

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# This is here because we are using a custom User model
# https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = "vidhya.User"
