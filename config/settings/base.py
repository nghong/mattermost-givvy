import os
import environ


ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('givvy')

env = environ.Env()

MATTERMOST_REQUEST_TOKEN = env('MATTERMOST_REQUEST_TOKEN', default='')
MATTERMOST_GIVE_TOKEN = env('MATTERMOST_GIVE_TOKEN', default='')
MATTERMOST_CONTACT_TOKEN = env('MATTERMOST_CONTACT_TOKEN', default='')
MATTERMOST_HOST = env('MATTERMOST_SERVER', default='')
MATTERMOST_WEBHOOK = env('MATTERMOST_WEBHOOK', default='')

DEBUG = env.bool('DJANGO_DEBUG', default=True)

SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
    default='(5*z%*pi=qx2d3%=g(df^i)may7-133@0-%ve@ce-tj@kx3_8y'
)

ALLOWED_HOSTS = []

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

LOCAL_APPS = (
    'givvy.apps.GivvyConfig',
    'contact.apps.ContactConfig',
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# STATICFILES
STATIC_ROOT = str(ROOT_DIR('static'))
STATIC_URL = '/static/'

STATICFILES_DIRS = (str(APPS_DIR.path('static')), '/static/')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder', )
