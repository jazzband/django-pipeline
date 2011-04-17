from compress.conf import settings
from compress.compilers import SubProcessCompiler


class CoffeeScriptCompiler(SubProcessCompiler):
    def match_file(self, filename):
        return filename.endswith('.coffee')

    def compile_file(self, content):
        command = "%s %s" % (settings.COMPRESS_COFFEE_SCRIPT_BINARY, settings.COMPRESS_COFFEE_SCRIPT_ARGUMENTS)
        if self.verbose:
            command += '--verbose'
        return self.execute_command(command, content)
