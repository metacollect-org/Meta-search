from metaSearch.settings.default import *

DEBUG = False

ALLOWED_HOSTS = [
  '*'
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'metacollect',
        'USER': 'meta',
        'PASSWORD': 'fpF8UCA4',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}
