"""
Settings for development environment
"""

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': '/tmp',
        'PORT': '5432',
    },
    'lite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/user/app.db',
    }
}

CACHE_TIMEOUT = 30

