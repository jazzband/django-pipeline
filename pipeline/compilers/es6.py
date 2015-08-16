from __future__ import unicode_literals

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class ES6Compiler(SubProcessCompiler):
    output_extension = 'js'

    def match_file(self, path):
        return path.endswith('.es6')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not outdated and not force:
            return  # File doesn't need to be recompiled

        args = list(settings.BABEL_ARGUMENTS)

        sourcemap_flags = set(['-s', '--source-maps'])
        if settings.OUTPUT_SOURCEMAPS and not(set(args) & sourcemap_flags):
            args += ['--source-maps', 'true']

        command = (
            settings.BABEL_BINARY,
            args,
            infile,
            "-o",
            outfile
        )
        return self.execute_command(command)
