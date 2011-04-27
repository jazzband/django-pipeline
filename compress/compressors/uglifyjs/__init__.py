from compress.conf import settings
from compress.compressors import SubProcessCompressor


class UglifyJSCompressor(SubProcessCompressor):
    def compress_js(self, js):
        command = '%s -nc %s' % (settings.COMPRESS_UGLIFYJS_BINARY, settings.COMPRESS_UGLIFYJS_ARGUMENTS)
        if self.verbose:
            command += ' --verbose'
        return self.execute_command(command, js)
