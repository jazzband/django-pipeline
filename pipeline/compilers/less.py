import shlex
import os

from os.path import dirname

from pipeline.conf import settings
from pipeline.compilers.common_css import CssCompiler, BaseFileTree


class LessFileTree(BaseFileTree):
    extensions = ('.less',)


class LessCompiler(CssCompiler):
    tree_object = LessFileTree

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not (outdated or force):
            return

        command = "%s %s %s %s" % (
            settings.PIPELINE_LESS_BINARY,
            settings.PIPELINE_LESS_ARGUMENTS,
            infile,
            outfile
        )
        return self.execute_command(command, cwd=dirname(infile))
