from metaSearch.settings.default import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<DB_NAME>',
        'USER': '<DB_USER_NAME>',
        'PASSWORD': '<PASSWORD_FOR_USER>',
        'HOST': '<DB_URL>',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}
