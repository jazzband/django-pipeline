from pipeline.conf import settings
from pipeline.compressors import SubProcessCompressor


class CSSMinCompressor(SubProcessCompressor):
    def compress_css(self, css):
        command = (settings.CSSMIN_BINARY, settings.CSSMIN_ARGUMENTS)
        return self.execute_command(command, css)
