"""
Handlebars compiler
"""

from __future__ import unicode_literals

import os

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class HandlebarsCompiler(SubProcessCompiler):
    """
    Pre-compile Handlebars templates.

    Requires the `handlebars' binary.
    """

    output_extension = 'js'

    def match_file(self, filename):
        return filename.endswith('.handlebars') or \
            filename.endswith('.hbs') or \
            filename.endswith('.hjs')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        command = '%s %s %s -f %s' % (
            settings.PIPELINE_HANDLEBARS_BINARY,
            settings.PIPELINE_HANDLEBARS_ARGUMENTS,
            infile,
            outfile,
        )

        return self.execute_command(command, cwd=os.path.dirname(infile))
