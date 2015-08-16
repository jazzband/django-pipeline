from __future__ import unicode_literals

from os.path import dirname

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class LessCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.less')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        # Pipe to file rather than provide outfile arg due to a bug in lessc
        args = list(settings.LESS_ARGUMENTS)

        if settings.OUTPUT_SOURCEMAPS and '--source-map' not in args:
            args += ['--source-map']

        command = (
            settings.LESS_BINARY,
            args,
            infile,
            outfile,
        )
        return self.execute_command(command, cwd=dirname(infile))
