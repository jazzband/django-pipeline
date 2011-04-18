from compress.conf import settings
from compress.compressors import SubProcessCompressor


class YUICompressor(SubProcessCompressor):
    def compress_common(self, content, type_, arguments):
        command = '%s --type=%s %s' % (settings.COMPRESS_YUI_BINARY, type_, arguments)
        if self.verbose:
            command += ' --verbose'
        return self.execute_command(command, content)

    def compress_js(self, js):
        return self.compress_common(js, 'js', settings.COMPRESS_YUI_JS_ARGUMENTS)

    def compress_css(self, css):
        return self.compress_common(css, 'css', settings.COMPRESS_YUI_CSS_ARGUMENTS)
