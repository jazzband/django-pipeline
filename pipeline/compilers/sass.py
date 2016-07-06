from __future__ import unicode_literals

import re
from os.path import dirname

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class SASSCompiler(SubProcessCompiler):
    output_extension = 'css'

    _sass_types = {}

    @property
    def sass_type(self):
        bin = " ".join(settings.SASS_BINARY)
        if bin not in self._sass_types:
            if re.search(r'node\-sass', bin):
                self._sass_types[bin] = 'node'
            elif re.search(r'sassc', bin):
                self._sass_types[bin] = 'libsass'
            else:
                self._sass_types[bin] = 'ruby'
        return self._sass_types[bin]

    def match_file(self, filename):
        return filename.endswith(('.scss', '.sass'))

    def compile_file(self, infile, outfile, outdated=False, force=False):
        args = list(settings.SASS_ARGUMENTS)

        if settings.OUTPUT_SOURCEMAPS:
            if self.sass_type == 'node':
                if '--source-map' not in args:
                    args += ['--source-map', 'true']
            elif self.sass_type == 'libsass':
                if not(set(args) & set(['-m', 'g', '--sourcemap'])):
                    args += ['--sourcemap']
            else:
                if not any([re.search(r'^\-\-sourcemap', a) for a in args]):
                    args += ['--sourcemap=auto']

        command = (settings.SASS_BINARY, args, infile, outfile)
        return self.execute_command(command, cwd=dirname(infile))
