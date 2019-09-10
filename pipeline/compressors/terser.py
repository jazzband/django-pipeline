from __future__ import unicode_literals

from pipeline.conf import settings
from pipeline.compressors import SubProcessCompressor


class TerserCompressor(SubProcessCompressor):
    def compress_js(self, js):
        command = (settings.TERSER_BINARY, settings.TERSER_ARGUMENTS)
        if self.verbose:
            command += ' --verbose'
        return self.execute_command(command, js)
