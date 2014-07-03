from __future__ import unicode_literals

from pipeline.conf import settings
from pipeline.compressors import SubProcessCompressor


class UglifyJSCompressor(SubProcessCompressor):
    def compress_js(self, get_js, args, **kwargs):
        command = '%s %s' % (settings.PIPELINE_UGLIFYJS_BINARY, settings.PIPELINE_UGLIFYJS_ARGUMENTS)
        if self.verbose:
            command += ' --verbose'
        return self.execute_command(command, get_js())
