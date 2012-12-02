import re

from os.path import dirname

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler
from pipeline.compilers.common_css import CssCompiler, BaseFileTree

class LessFileTree(BaseFileTree):
    import_exp = re.compile('@import\\s+("((?:[^"\\\r\n]|\\.)*)"|\'((?:[^\'\\\r\n]|\\.)*)\'|`((?:[^`]|\\.)*)`)\\s*;')

    def parse_imports(self, fh):
        ret = []

        for l in fh:
            matches = self.import_exp.findall(l)

            for match in matches:
                filename = ""
                filesplit = []
                fileext = ""

                if match[0][0] == '"':
                    filename = match[1]
                elif match[0][0] == "'":
                    filename = match[2]
                elif match[0][0] == "`":
                    filename = match[3]

                if filename == '':
                    continue

                if not filename.endswith(".css"):
                    if filename.endswith(".less"):
                        ret.append(filename)
                    else:
                        ret.append("%s.less" % filename)

        return ret

class LessCompiler(CssCompiler):
    output_extension = 'css'
    tree_object = LessFileTree

    def match_file(self, filename):
        return filename.endswith('.less')

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
