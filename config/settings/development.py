from .base import *


# DEBUG
DEBUG = env.bool('DJANGO_DEBUG', default=True)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'
    }
}
