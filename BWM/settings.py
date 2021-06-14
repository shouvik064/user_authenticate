"""
Django settings for BWM project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from django.urls import reverse_lazy
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base = environ.Path(__file__) - 2 # two folders back (/a/b/ - 2 = /)
env = environ.Env(
DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env(env_file=base('.env'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS']
ALLOWED_HOSTS =["*"]

host = 'staging'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders'
]
LOCAL_APPS = [
    'myapp'
]
INSTALLED_APPS += LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'common.authsetup.Middlewares3bucketSetup',
]

ROOT_URLCONF = 'BWM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'BWM.wsgi.application'

if host == 'staging':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['STAGE_DB_NAME'],
            'USER': os.environ['STAGE_DB_USER'],
            'PASSWORD': os.environ['STAGE_DB_PASS'],
            'HOST': os.environ['STAGE_DB_HOST'],
            'PORT': os.environ['STAGE_DB_PORT'],
            'CONN_MAX_AGE': 28700,
            'OPTIONS': {
                'isolation_level': None,
                'init_command': "SET sql_mode=''",
            },
        }
    }

    DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000

else:
    DATABASES = {
            'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['LOCAL_DB_NAME'],
            'USER': os.environ['LOCAL_DB_USER'],
            'PASSWORD': os.environ['LOCAL_DB_PASS'],
            'HOST': os.environ['LOCAL_DB_HOST'],
            'PORT': os.environ['LOCAL_DB_PORT'],
            'CONN_MAX_AGE': 28700,
            'OPTIONS': {
                'isolation_level': None,
                'init_command': "SET sql_mode=''",
            },
        }
    }

    DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000

AUTH_USER_MODEL = 'myapp.Admins'

REST_FRAMEWORK = {

    # For LIVE Authentication [TOKEN Mendatory]::
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'

}

LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

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

LOGIN_REDIRECT_URL=reverse_lazy('docs')


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# corsheaders
CORS_ORIGIN_ALLOW_ALL = True


MEDIA_ROOT =  os.path.join(BASE_DIR, 'media') 
MEDIA_URL = '/'

LOGGING = {
    'version': 1,
    # 'disable_existing_loggers': False,

    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
    },

    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'info.log',
            'formatter': 'simpleRe',
        },
    },

    'formatters': {
        'simpleRe': {
            'format': '{levelname} {asctime} {pathname} {lineno} {message}',
            'style': '{',
        },
    },

}