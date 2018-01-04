from .base import *


SECRET_KEY = '(5*z%*pi=qx2d3%=g(df^i)may7-133@0-%ve@ce-tj@kx3_8y'

DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}
