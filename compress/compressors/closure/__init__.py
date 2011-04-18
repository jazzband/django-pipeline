from compress.conf import settings
from compress.compressors import SubProcessCompressor


class ClosureCompressor(SubProcessCompressor):
    def compress_js(self, js):
        command = '%s %s' % (settings.COMPRESS_CLOSURE_BINARY, settings.COMPRESS_CLOSURE_ARGUMENTS)
        if self.verbose:
            command += ' --verbose'
        return self.execute_command(command, js)
