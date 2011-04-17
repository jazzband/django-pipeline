from compress.conf import settings
from compress.filters import SubProcessFilter


class ClosureCompressorFilter(SubProcessFilter):
    def filter_js(self, js):
        command = '%s %s' % (settings.COMPRESS_CLOSURE_BINARY, settings.COMPRESS_CLOSURE_ARGUMENTS)
        if self.verbose:
            command += ' --verbose'
        return self.execute_command(command, js)
