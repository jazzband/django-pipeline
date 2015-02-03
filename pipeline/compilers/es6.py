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
        command = "%s %s %s -o %s" % (
            settings.PIPELINE_6TO5_BINARY,
            settings.PIPELINE_6TO5_ARGUMENTS,
            infile,
            outfile
        )
        return self.execute_command(command)
