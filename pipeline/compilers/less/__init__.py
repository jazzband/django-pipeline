import os
import tempfile

from pipeline.conf import settings
from pipeline.compilers import CompilerBase


class LessCompiler(CompilerBase):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.less')

    def compile_file(self, content):
        tmp_file = tempfile.NamedTemporaryFile(mode='w+b')
        tmp_file.write(content)
        tmp_file.flush()

        output_file = tempfile.NamedTemporaryFile(mode='w+b')

        command = '%s %s %s %s' % (
            settings.PIPELINE_LESS_BINARY, tmp_file.name,
            settings.PIPELINE_LESS_ARGUMENTS, output_file.name
        )

        command_output = os.popen(command).read()

        compiled_content = output_file.read()
        output_file.close()
        tmp_file.close()

        if self.verbose:
            print command_output
        return compiled_content
