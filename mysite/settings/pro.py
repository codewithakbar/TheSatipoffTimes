from .base import *

DEBUG = False

ADMINS = (
    ('odil', 'satipovakbar@gmail.com'),
)

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# SSL config
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
