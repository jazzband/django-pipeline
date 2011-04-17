from django.conf import settings


COMPRESS_ROOT = getattr(settings, 'COMPRESS_ROOT', settings.MEDIA_ROOT)
COMPRESS_URL = getattr(settings, 'COMPRESS_URL', settings.MEDIA_URL)

COMPRESS = getattr(settings, 'COMPRESS', not settings.DEBUG)
COMPRESS_SOURCE = getattr(settings, 'COMPRESS_SOURCE', settings.MEDIA_ROOT)
COMPRESS_ROOT = getattr(settings, 'COMPRESS_ROOT', settings.MEDIA_ROOT)
COMPRESS_URL = getattr(settings, 'COMPRESS_URL', settings.MEDIA_URL)
COMPRESS_AUTO = getattr(settings, 'COMPRESS_AUTO', True)
COMPRESS_VERSION = getattr(settings, 'COMPRESS_VERSION', False)
COMPRESS_VERSION_PLACEHOLDER = getattr(settings, 'COMPRESS_VERSION_PLACEHOLDER', '?')
COMPRESS_VERSION_DEFAULT = getattr(settings, 'COMPRESS_VERSION_DEFAULT', '0')
COMPRESS_VERSION_REMOVE_OLD = getattr(settings, 'COMPRESS_VERSION_REMOVE_OLD', True)
COMPRESS_VERSIONING = getattr(settings, 'COMPRESS_VERSIONING', 'compress.versioning.mtime.MTimeVersioning')

COMPRESS_CSS_FILTERS = getattr(settings, 'COMPRESS_CSS_FILTERS', ['compress.filters.csstidy.CSSTidyFilter'])
COMPRESS_JS_FILTERS = getattr(settings, 'COMPRESS_JS_FILTERS', ['compress.filters.jsmin.JSMinFilter'])
COMPRESS_CSS = getattr(settings, 'COMPRESS_CSS', {})
COMPRESS_JS = getattr(settings, 'COMPRESS_JS', {})

COMPRESS_YUI_BINARY = getattr(settings, 'COMPRESS_YUI_BINARY', 'java -jar yuicompressor.jar')
COMPRESS_YUI_CSS_ARGUMENTS = getattr(settings, 'COMPRESS_YUI_CSS_ARGUMENTS', '')
COMPRESS_YUI_JS_ARGUMENTS = getattr(settings, 'COMPRESS_YUI_JS_ARGUMENTS', '')

COMPRESS_CLOSURE_BINARY = getattr(settings, 'COMPRESS_CLOSURE_BINARY', 'java -jar compiler.jar')
COMPRESS_CLOSURE_ARGUMENTS = getattr(settings, 'COMPRESS_CLOSURE_ARGUMENTS', '')

COMPRESS_UGLIFYJS_BINARY = getattr(settings, 'COMPRESS_UGLIFYJS_BINARY', '/usr/local/bin/uglifyjs')
COMPRESS_UGLIFYJS_ARGUMENTS = getattr(settings, 'COMPRESS_UGLIFYJS_ARGUMENTS', '-nc')

if COMPRESS_CSS_FILTERS is None:
    COMPRESS_CSS_FILTERS = []

if COMPRESS_JS_FILTERS is None:
    COMPRESS_JS_FILTERS = []
