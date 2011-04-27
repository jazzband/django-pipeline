from compress.conf import settings
from compress.compilers import SubProcessCompiler


class CoffeeScriptCompiler(SubProcessCompiler):
    output_extension = 'js'

    def match_file(self, path):
        return path.endswith('.coffee')

    def compile_file(self, content):
        command = "%s -sc %s" % (settings.COMPRESS_COFFEE_SCRIPT_BINARY, settings.COMPRESS_COFFEE_SCRIPT_ARGUMENTS)
        if self.verbose:
            command += '--verbose'
        return self.execute_command(command, content)
