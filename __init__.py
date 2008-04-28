from django.conf import settings

from compress.utils import needs_update, compress_css, compress_js

if gresettings.COMPRESS:
    for css in settings.COMPRESS_CSS.values():
        if needs_update(css['compressed_filename'], css['source_filenames']):
            compress_css(css)

    for js in settings.COMPRESS_JS.values():
        if needs_update(js['compressed_filename'], css['source_filenames']):
            compress_js(js)