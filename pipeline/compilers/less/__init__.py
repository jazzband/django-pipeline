import os
import tempfile

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class LessCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.less')

    def compile_file(self, content):
        in_file, in_filename = tempfile.mkstemp()
        in_file = os.fdopen(in_file, 'w+b')
        in_file.write(content)
        in_file.flush()

        command = '%s %s %s' % (
            settings.PIPELINE_LESS_BINARY,
            in_filename,
            settings.PIPELINE_LESS_ARGUMENTS
        )
        content = self.execute_command(command, content)

        in_file.close()
        os.remove(in_filename)

        return content
