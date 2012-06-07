from os.path import dirname

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class StylusCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.styl')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not outdated and not force:
            return  # File doesn't need to be recompiled
        command = "%s %s < %s > %s" % (
            settings.PIPELINE_STYLUS_BINARY,
            settings.PIPELINE_STYLUS_ARGUMENTS,
            infile,
            outfile
        )
        return self.execute_command(command, cwd=dirname(infile))
