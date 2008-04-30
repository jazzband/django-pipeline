from compress.conf import settings
from compress.utils import needs_update, filter_css, filter_js

if settings.COMPRESS:
    for css in settings.COMPRESS_CSS.values():
        if needs_update(css['output_filename'], css['source_filenames']):
            filter_css(css)

    for js in settings.COMPRESS_JS.values():
        if needs_update(js['output_filename'], js['source_filenames']):
            filter_js(js)