# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections
import shlex

from django.conf import settings as _settings
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.utils.six import string_types


DEFAULTS = {
    'PIPELINE_ENABLED': not _settings.DEBUG,

    'PIPELINE_COLLECTOR_ENABLED': True,

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

    'DISABLE_WRAPPER': False,

    'MIMETYPES': (
        (b'text/coffeescript', '.coffee'),
        (b'text/less', '.less'),
        (b'text/javascript', '.js'),
        (b'text/x-sass', '.sass'),
        (b'text/x-scss', '.scss')
    ),

    'EMBED_MAX_IMAGE_SIZE': 32700,
    'EMBED_PATH': r'[/]?embed/',
    'EMBED_MIME_TYPES': {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.tif': 'image/tiff',
        '.tiff': 'image/tiff',
        '.ttf': 'font/truetype',
        '.otf': 'font/opentype',
        '.woff': 'font/woff'
    },
}


class PipelineSettings(collections.MutableMapping):
    """
    Container object for pipeline settings
    """
    def __init__(self, wrapped_settings):
        self.settings = DEFAULTS.copy()
        self.settings.update(wrapped_settings)

    def __getitem__(self, key):
        value = self.settings[key]
        if key.endswith(("_BINARY", "_ARGUMENTS")):
            if isinstance(value, string_types):
                return tuple(shlex.split(value))
            return tuple(value)
        return value

    def __setitem__(self, key, value):
        self.settings[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.settings)

    def __len__(self):
        return len(self.settings)

    def __getattr__(self, name):
        return self.__getitem__(name)


settings = PipelineSettings(_settings.PIPELINE)


@receiver(setting_changed)
def reload_settings(**kwargs):
    if kwargs['setting'] == 'PIPELINE':
        settings.update(kwargs['value'])
