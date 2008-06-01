from django.conf import settings

COMPRESS = getattr(settings, 'COMPRESS', not settings.DEBUG)
COMPRESS_AUTO = getattr(settings, 'COMPRESS_AUTO', True)
COMPRESS_AUTO_TEMPLATES = getattr(settings, 'COMPRESS_AUTO_TEMPLATES', True)

COMPRESS_CSS_FILTERS = getattr(settings, 'COMPRESS_CSS_FILTERS', ('compress.filters.csstidy.CSSTidyFilter', ))
COMPRESS_JS_FILTERS = getattr(settings, 'COMPRESS_JS_FILTERS', ('compress.filters.jsmin.JSMinFilter',))
COMPRESS_CSS = getattr(settings, 'COMPRESS_CSS', {})
COMPRESS_JS = getattr(settings, 'COMPRESS_JS', {})

if COMPRESS_CSS_FILTERS is None:
    COMPRESS_CSS_FILTERS = ()

if COMPRESS_JS_FILTERS is None:
    COMPRESS_JS_FILTERS = ()