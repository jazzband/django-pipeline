import os.path

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class SASSCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.scss')

    def compile_file(self, content, path):
        command = "%s --scss %s %s" % (
            settings.PIPELINE_SASS_BINARY,
            settings.PIPELINE_SASS_ARGUMENTS,
            path
        )
        cwd = os.path.dirname(path)
        return self.execute_command(command, cwd=cwd)
