from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class CoffeeScriptCompiler(SubProcessCompiler):
    output_extension = 'js'

    def match_file(self, path):
        return path.endswith('.coffee')

    def compile_file(self, content, path):
        command = "%s -sc %s" % (
            settings.PIPELINE_COFFEE_SCRIPT_BINARY,
            settings.PIPELINE_COFFEE_SCRIPT_ARGUMENTS
        )
        return self.execute_command(command, content)
