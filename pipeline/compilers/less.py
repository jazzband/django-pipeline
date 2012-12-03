import shlex
import os

from os.path import dirname

from pipeline.conf import settings
from pipeline.compilers.common_css import CssCompiler, BaseFileTree


class LessFileTree(BaseFileTree):
    extensions = ('.less',)


class LessCompiler(CssCompiler):
    tree_object = LessFileTree
    search_path = None

    @staticmethod
    def get_search_path():
        if LessCompiler.search_path is not None:
            return LessCompiler.search_path

        argv = shlex.split(settings.PIPELINE_LESS_ARGUMENTS)

        path_str = "."
        for i in range(1, len(argv)):
            if argv[i - 1] == "--include-path":
                path_str = argv[i]
                break

        if os.name != 'nt':
            sep = ':'
        else:
            sep = ';'

        LessCompiler.search_path = path_str.split(sep)
        return LessCompiler.search_path

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
