# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings as _settings

DEFAULTS = {
    'PIPELINE_ENABLED': not _settings.DEBUG,

    'PIPELINE_ROOT': _settings.STATIC_ROOT,
    'PIPELINE_URL': _settings.STATIC_URL,

    'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'COMPILERS': [],

    'STYLESHEETS': {},
    'JAVASCRIPT': {},

    'TEMPLATE_NAMESPACE': "window.JST",
    'TEMPLATE_EXT': ".jst",
    'TEMPLATE_FUNC': "template",
    'TEMPLATE_SEPARATOR': "_",

    'DISABLE_WRAPPER': False,

    'CSSTIDY_BINARY': '/usr/bin/env csstidy',
    'CSSTIDY_ARGUMENTS': '--template=highest',

    'YUGLIFY_BINARY': '/usr/bin/env yuglify',
    'YUGLIFY_CSS_ARGUMENTS': '--terminal',
    'YUGLIFY_JS_ARGUMENTS': '--terminal',

    'YUI_BINARY': '/usr/bin/env yuicompressor',
    'YUI_CSS_ARGUMENTS': '',
    'YUI_JS_ARGUMENTS': '',

    'CLOSURE_BINARY': '/usr/bin/env closure',
    'CLOSURE_ARGUMENTS': '',

    'UGLIFYJS_BINARY': '/usr/bin/env uglifyjs',
    'UGLIFYJS_ARGUMENTS': '',

    'CSSMIN_BINARY': '/usr/bin/env cssmin',
    'CSSMIN_ARGUMENTS': '',

    'COFFEE_SCRIPT_BINARY': '/usr/bin/env coffee',
    'COFFEE_SCRIPT_ARGUMENTS': '',

    'BABEL_BINARY': '/usr/bin/env babel',
    'BABEL_ARGUMENTS': '',

    'LIVE_SCRIPT_BINARY': '/usr/bin/env lsc',
    'LIVE_SCRIPT_ARGUMENTS': '',

    'SASS_BINARY': '/usr/bin/env sass',
    'SASS_ARGUMENTS': '',

    'STYLUS_BINARY': '/usr/bin/env stylus',
    'STYLUS_ARGUMENTS': '',

    'LESS_BINARY': '/usr/bin/env lessc',
    'LESS_ARGUMENTS': '',

    'MIMETYPES': (
        (b'text/coffeescript', '.coffee'),
        (b'text/less', '.less'),
        (b'text/javascript', '.js'),
        (b'text/x-sass', '.sass'),
        (b'text/x-scss', '.scss')
    ),

    'EMBED_MAX_IMAGE_SIZE': 32700,
    'EMBED_PATH': r'[/]?embed/',
}


class PipelineSettings(object):
    '''
    Container object for pipeline settings
    '''
    def __init__(self, wrapped_settings):
        DEFAULTS.update(wrapped_settings)
        self.__dict__ = DEFAULTS


settings = PipelineSettings(_settings.PIPELINE)
