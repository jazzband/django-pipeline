from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler, InplaceCompiler


class CoffeeScriptCompiler(SubProcessCompiler, InplaceCompiler):
    output_extension = 'js'

    def match_file(self, path):
        return path.endswith('.coffee')

    def compile_file(self, content, path):
        command = "%s -sc %s" % (
            settings.PIPELINE_COFFEE_SCRIPT_BINARY,
            settings.PIPELINE_COFFEE_SCRIPT_ARGUMENTS
        )
        return self.execute_command(command, content)

    def compile_inplace_file(self, input_path, output_path):
        command = "%s -c %s %s > %s" % (
            settings.PIPELINE_COFFEE_SCRIPT_BINARY,
            settings.PIPELINE_COFFEE_SCRIPT_ARGUMENTS,
            input_path,
            output_path
        )
        return self.execute_command(command)

