from django.conf import settings

PIPELINE = getattr(settings, 'PIPELINE', not settings.DEBUG)
PIPELINE_ROOT = getattr(settings, 'PIPELINE_ROOT', settings.STATIC_ROOT)
PIPELINE_URL = getattr(settings, 'PIPELINE_URL', settings.STATIC_URL)
PIPELINE_ENV_DIR = getattr(settings, 'PIPELINE_ENV_DIR', "/usr/bin/env")

PIPELINE_STORAGE = getattr(settings, 'PIPELINE_STORAGE',
    'pipeline.storage.PipelineFinderStorage')

PIPELINE_CSS_COMPRESSOR = getattr(settings, 'PIPELINE_CSS_COMPRESSOR',
    'pipeline.compressors.yui.YUICompressor'
)
PIPELINE_JS_COMPRESSOR = getattr(settings, 'PIPELINE_JS_COMPRESSOR',
    'pipeline.compressors.yui.YUICompressor'
)
PIPELINE_COMPILERS = getattr(settings, 'PIPELINE_COMPILERS', [])

PIPELINE_CSS = getattr(settings, 'PIPELINE_CSS', {})
PIPELINE_JS = getattr(settings, 'PIPELINE_JS', {})

PIPELINE_TEMPLATE_NAMESPACE = getattr(settings, 'PIPELINE_TEMPLATE_NAMESPACE', "window.JST")
PIPELINE_TEMPLATE_EXT = getattr(settings, 'PIPELINE_TEMPLATE_EXT', ".jst")
PIPELINE_TEMPLATE_FUNC = getattr(settings, 'PIPELINE_TEMPLATE_FUNC', "template")

PIPELINE_DISABLE_WRAPPER = getattr(settings, 'PIPELINE_DISABLE_WRAPPER', False)

PIPELINE_CSSTIDY_BINARY = getattr(settings, 'PIPELINE_CSSTIDY_BINARY', '%s csstidy' % PIPELINE_ENV_DIR)
PIPELINE_CSSTIDY_ARGUMENTS = getattr(settings, 'PIPELINE_CSSTIDY_ARGUMENTS', '--template=highest')

PIPELINE_YUI_BINARY = getattr(settings, 'PIPELINE_YUI_BINARY', '%s yuicompressor' % PIPELINE_ENV_DIR)
PIPELINE_YUI_CSS_ARGUMENTS = getattr(settings, 'PIPELINE_YUI_CSS_ARGUMENTS', '')
PIPELINE_YUI_JS_ARGUMENTS = getattr(settings, 'PIPELINE_YUI_JS_ARGUMENTS', '')

PIPELINE_CLOSURE_BINARY = getattr(settings, 'PIPELINE_CLOSURE_BINARY', '%s closure' % PIPELINE_ENV_DIR)
PIPELINE_CLOSURE_ARGUMENTS = getattr(settings, 'PIPELINE_CLOSURE_ARGUMENTS', '')

PIPELINE_UGLIFYJS_BINARY = getattr(settings, 'PIPELINE_UGLIFYJS_BINARY', '%s uglifyjs' % PIPELINE_ENV_DIR)
PIPELINE_UGLIFYJS_ARGUMENTS = getattr(settings, 'PIPELINE_UGLIFYJS_ARGUMENTS', '')

PIPELINE_COFFEE_SCRIPT_BINARY = getattr(settings, 'PIPELINE_COFFEE_SCRIPT_BINARY', '%s coffee' % PIPELINE_ENV_DIR)
PIPELINE_COFFEE_SCRIPT_ARGUMENTS = getattr(settings, 'PIPELINE_COFFEE_SCRIPT_ARGUMENTS', '')

PIPELINE_SASS_BINARY = getattr(settings, 'PIPELINE_SASS_BINARY', '%s sass' % PIPELINE_ENV_DIR)
PIPELINE_SASS_ARGUMENTS = getattr(settings, 'PIPELINE_SASS_ARGUMENTS', '')

PIPELINE_STYLUS_BINARY = getattr(settings, 'PIPELINE_STYLUS_BINARY', '%s stylus' % PIPELINE_ENV_DIR)
PIPELINE_STYLUS_ARGUMENTS = getattr(settings, 'PIPELINE_STYLUS_ARGUMENTS', '')

PIPELINE_LESS_BINARY = getattr(settings, 'PIPELINE_LESS_BINARY', '%s lessc' % PIPELINE_ENV_DIR)
PIPELINE_LESS_ARGUMENTS = getattr(settings, 'PIPELINE_LESS_ARGUMENTS', '')

PIPELINE_MIMETYPES = getattr(settings, 'PIPELINE_MIMETYPES', (
    ('text/coffeescript', '.coffee'),
    ('text/less', '.less'),
    ('text/javascript', '.js')
))

PIPELINE_EMBED_MAX_IMAGE_SIZE = getattr(settings, 'PIPELINE_EMBED_MAX_IMAGE_SIZE', 32700)
PIPELINE_EMBED_PATH = getattr(settings, 'PIPELINE_EMBED_PATH', r'[/]?embed/')

if PIPELINE_COMPILERS is None:
    PIPELINE_COMPILERS = []
