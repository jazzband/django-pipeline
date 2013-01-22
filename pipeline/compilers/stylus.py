from __future__ import unicode_literals

from os.path import dirname

from pipeline.conf import settings
from pipeline.compilers.common_css import CssCompiler, BaseFileTree


class StylusFileTree(BaseFileTree):
    extensions = ('.styl',)


class StylusCompiler(CssCompiler):
    tree_object = StylusFileTree

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not (outdated or force):
            return

        command = "%s %s < %s > %s" % (
            settings.PIPELINE_STYLUS_BINARY,
            settings.PIPELINE_STYLUS_ARGUMENTS,
            infile,
            outfile
        )
        return self.execute_command(command, cwd=dirname(infile))
