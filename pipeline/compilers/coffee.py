from __future__ import unicode_literals

import os

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class CoffeeScriptCompiler(SubProcessCompiler):
    output_extension = 'js'

    def match_file(self, path):
        return path.endswith('.coffee') or path.endswith('.litcoffee')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not outdated and not force:
            return  # File doesn't need to be recompiled

        args = list(settings.COFFEE_SCRIPT_ARGUMENTS)
        if settings.OUTPUT_SOURCEMAPS and not(set(args) & set(['-m', '--map'])):
            args.append('--map')

        command = (
            settings.COFFEE_SCRIPT_BINARY,
            "-c",
            "-o", os.path.dirname(outfile),
            args,
            infile,
        )
        return self.execute_command(command, cwd=os.path.dirname(outfile))
