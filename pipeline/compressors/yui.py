from __future__ import unicode_literals

from pipeline.conf import settings
from pipeline.compressors import SubProcessCompressor


class YUICompressor(SubProcessCompressor):
    def compress_common(self, content, compress_type, arguments):
        command = (
            settings.YUI_BINARY,
            "--type={}".format(compress_type),
            arguments
        )
        return self.execute_command(command, content)

    def compress_js(self, js):
        return self.compress_common(js, 'js', settings.YUI_JS_ARGUMENTS)

    def compress_css(self, css):
        return self.compress_common(css, 'css', settings.YUI_CSS_ARGUMENTS)
