import os

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class LessCompiler(SubProcessCompiler):
    output_extension = 'css'
    less_filename = ''

    def match_file(self, filename):
        self.less_filename = os.path.join(settings.PIPELINE_ROOT, filename)
        return filename.endswith('.less')

    def compile_file(self, content):
        command = '%s %s %s' % (
            settings.PIPELINE_LESS_BINARY,
            settings.PIPELINE_LESS_ARGUMENTS,
            self.less_filename,
        )
        content = self.execute_command(command, content)

        return content
