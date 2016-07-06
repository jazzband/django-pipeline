from __future__ import unicode_literals

from os.path import dirname

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class StylusCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.styl')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        args = list(settings.STYLUS_ARGUMENTS)

        sourcemap_flags = set(['-s', '--sourcemap'])
        if settings.OUTPUT_SOURCEMAPS and not(set(args) & sourcemap_flags):
            args += ['--sourcemap']

        command = (
            settings.STYLUS_BINARY,
            args,
            infile
        )
        return self.execute_command(command, cwd=dirname(infile))
