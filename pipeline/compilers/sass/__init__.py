from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class SASSCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.scss')

    def compile_file(self, content):
        command = "%s --scss %s" % (settings.PIPELINE_SASS_BINARY, settings.PIPELINE_SASS_ARGUMENTS)
        if self.verbose:
            command += '--verbose'
        return self.execute_command(command, content)
