import os

local_path = lambda path: os.path.join(os.path.dirname(__file__), path)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': ':memory:'
    }
}

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.admin',
    'pipeline',
    'tests',
]

MEDIA_URL = '/media/'

MEDIA_ROOT = local_path('media')

STATIC_URL = '/static/'

STATIC_ROOT = local_path('assets')

TEMPLATE_DIRS = (
    local_path('templates'),
)
