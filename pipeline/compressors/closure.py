from __future__ import unicode_literals

from pipeline.conf import settings
from pipeline.compressors import SubProcessCompressor


class ClosureCompressor(SubProcessCompressor):
    def compress_js(self, get_js, *args, **kwargs):
        command = '%s %s' % (settings.PIPELINE_CLOSURE_BINARY, settings.PIPELINE_CLOSURE_ARGUMENTS)
        return self.execute_command(command, get_js())
