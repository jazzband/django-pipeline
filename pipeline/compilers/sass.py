from __future__ import unicode_literals

import shlex

from pipeline.conf import settings
from os.path import dirname

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class SASSCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith(('.scss', '.sass'))

    def compile_file(self, infile, outfile, outdated=False, force=False):
        command = (
            settings.PIPELINE_SASS_BINARY,
        ) + tuple(shlex.split(settings.PIPELINE_SASS_ARGUMENTS)) + (
            infile,
            outfile
        )
        return self.execute_command(command, cwd=dirname(infile))
