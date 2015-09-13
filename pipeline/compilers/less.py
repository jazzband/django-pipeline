from __future__ import unicode_literals

from pipeline.conf import settings
from os.path import dirname

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class LessCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.less')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        # Pipe to file rather than provide outfile arg due to a bug in lessc
        command = (
            settings.PIPELINE_LESS_BINARY,
            settings.PIPELINE_LESS_SCRIPT_ARGUMENTS,
            infile,
        )
        return self.execute_command(command, cwd=dirname(infile), stdout_as_result=outfile)
