import os.path

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler, InplaceCompiler


class SASSCompiler(SubProcessCompiler, InplaceCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith(('.scss', '.sass'))

    def compile_file(self, content, path):
        command = "%s --scss %s %s" % (
            settings.PIPELINE_SASS_BINARY,
            settings.PIPELINE_SASS_ARGUMENTS,
            path
        )
        cwd = os.path.dirname(path)
        return self.execute_command(command, cwd=cwd)

    def compile_inplace_file(self, input_path, output_path):
        command = "%s --scss %s --update %s:%s" % (
            settings.PIPELINE_SASS_BINARY,
            settings.PIPELINE_SASS_ARGUMENTS,
            input_path, output_path
        )
        cwd = os.path.dirname(input_path)
        return self.execute_command(command, cwd=cwd)
