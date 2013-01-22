from __future__ import unicode_literals

from os.path import dirname

from pipeline.conf import settings
from pipeline.compilers.common_css import CssCompiler, BaseFileTree


class SASSFileTree(BaseFileTree):
    extensions = ('.scss', '.sass')


class SASSCompiler(CssCompiler):
    tree_object = SASSFileTree

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not (outdated or force):
            return

        command = "%s %s --update %s:%s" % (
            settings.PIPELINE_SASS_BINARY,
            settings.PIPELINE_SASS_ARGUMENTS,
            infile,
            outfile
        )
        return self.execute_command(command, cwd=dirname(infile))
