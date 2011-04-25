from compress.conf import settings
from compress.compilers import SubProcessCompiler


class SASSCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.scss')

    def compile_file(self, content):
        command = "%s %s" % (settings.COMPRESS_SASS_BINARY, settings.COMPRESS_SASS_ARGUMENTS)
        if self.verbose:
            command += '--verbose'
        return self.execute_command(command, content)
