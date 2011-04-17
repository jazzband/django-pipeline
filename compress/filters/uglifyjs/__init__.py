from compress.conf import settings
from compress.filters import SubProcessFilter


class UglifyJSCompressorFilter(SubProcessFilter):
    def filter_js(self, js):
        command = '%s %s' % (settings.COMPRESS_UGLIFYJS_BINARY, settings.COMPRESS_UGLIFYJS_ARGUMENTS)
        if self.verbose:
            command += ' --verbose'
        return self.execute_command(command, js)
