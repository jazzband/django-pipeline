from pipeline.conf import settings
from pipeline.compressors import SubProcessCompressor


class ClosureCompressor(SubProcessCompressor):
    def compress_js(self, js):
        command = (settings.CLOSURE_BINARY, settings.CLOSURE_ARGUMENTS)
        return self.execute_command(command, js)
