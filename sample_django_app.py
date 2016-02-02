#!/usr/bin/env python2
import os
import sys

root = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.realpath(os.path.join(root, '..')))

# settings.py
DEBUG = True
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'vkscriptz.djvk',
    'vkscriptz.djvk.mediaplan',
)

ROOT_URLCONF = 'vkscriptz.sample_django_app_urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(root, 'djvk.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

SECRET_KEY = '123'
STATIC_URL = '/static/'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

DJVK_CLIENT_ID = 5161445
DJVK_CLIENT_SECRET = 'l6bLNsD6jvOwBpWZOxQG'

# manage.py
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'vkscriptz.sample_django_app')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

