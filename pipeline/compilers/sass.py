from __future__ import unicode_literals

from os.path import dirname

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class SASSCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith(('.scss', '.sass'))

    def compile_file(self, infile, outfile, outdated=False, force=False):
        sass_command = "{sass_binary} {sass_arguments} {infile} {outfile}"

        # If the update option is used, the command syntax changes slightly.
        if "--update" in settings.PIPELINE_SASS_ARGUMENTS:
            sass_command = "{sass_binary} {sass_arguments} {infile}:{outfile}"

        command = sass_command.format(
            sass_binary=settings.PIPELINE_SASS_BINARY,
            sass_arguments=settings.PIPELINE_SASS_ARGUMENTS,
            infile=infile,
            outfile=outfile
        )

        return self.execute_command(command, cwd=dirname(infile))
