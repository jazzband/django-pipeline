from compress.conf import settings
from compress.filters import SubProcessFilter


class YUICompressorFilter(SubProcessFilter):
    def filter_common(self, content, type_, arguments):
        command = '%s --type=%s %s' % (settings.COMPRESS_YUI_BINARY, type_, arguments)
        if self.verbose:
            command += ' --verbose'
        return self.execute_command(command, content)

    def filter_js(self, js):
        return self.filter_common(js, 'js', settings.COMPRESS_YUI_JS_ARGUMENTS)

    def filter_css(self, css):
        return self.filter_common(css, 'css', settings.COMPRESS_YUI_CSS_ARGUMENTS)
