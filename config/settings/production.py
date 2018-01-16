from .base import *


# APPS
INSTALLED_APPS += ("gunicorn",)

# ALLOWED HOSTS
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

# DATABASE
DATABASES = {'default': env.db("DATABASE_URL")}
