import os
import tempfile

from pipeline.conf import settings
from pipeline.compressors import SubProcessCompressor


class CSSTidyCompressor(SubProcessCompressor):
    def compress_css(self, css):
        out_file, out_filename = tempfile.mkstemp()
        out_file = os.fdopen(out_file, 'rb')

        command = '%s - %s %s' % (
            settings.PIPELINE_CSSTIDY_BINARY,
            settings.PIPELINE_CSSTIDY_ARGUMENTS,
            out_filename
        )
        self.execute_command(command, css)

        filtered_css = out_file.read()
        out_file.close()
        os.remove(out_filename)

        return filtered_css
