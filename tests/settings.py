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
    'staticfiles',
    'django.contrib.auth',
    'django.contrib.admin',
    'pipeline',
    'tests',
]

MEDIA_URL = '/media/'

MEDIA_ROOT = local_path('media')

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
STATIC_ROOT = local_path('static/')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    local_path('assets/'),
    local_path('assets2/'),
)
STATICFILES_FINDERS = (
    'staticfiles.finders.FileSystemFinder',
    'staticfiles.finders.AppDirectoriesFinder'
)

SECRET_KEY = "django-pipeline"

TEMPLATE_DIRS = (
    local_path('templates'),
)

PIPELINE_CSS = {
    'screen': {
        'source_filenames': (
            'css/first.css',
            'css/second.css',
            'css/urls.css',
        ),
        'output_filename': 'screen.css'
    }
}
PIPELINE_JS = {
    'scripts': {
        'source_filenames': (
            'js/first.js',
            'js/second.js',
            'js/application.js',
            'templates/**/*.jst'
        ),
        'output_filename': 'scripts.css'
    }
}
