from __future__ import unicode_literals
import os
from django.core.files import temp as tempfile

from pipeline.conf import settings
from pipeline.compressors import SubProcessCompressor


class CSSOCompressor(SubProcessCompressor):
    def compress_css(self, css):
        try:
            input_file = tempfile.NamedTemporaryFile(suffix='.pipeline', delete=False)
            input_file.write(css.encode('utf-8'))
            input_file.close()
            command = "%s --input %s %s" % (settings.PIPELINE_CSSO_BINARY, input_file.name, settings.PIPELINE_CSSO_ARGUMENTS)
            return self.execute_command(command, None)
        finally:
            os.unlink(input_file.name)
