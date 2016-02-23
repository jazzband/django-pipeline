from __future__ import unicode_literals

from pipeline.conf import settings
from pipeline.compressors import SubProcessCompressor


class CleanCSSCompressor(SubProcessCompressor):

    def compress_css(self, css):
        args = [settings.CLEANCSS_BINARY, settings.CLEANCSS_ARGUMENTS]
        return self.execute_command(args, css)
