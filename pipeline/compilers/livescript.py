from __future__ import unicode_literals

from os.path import dirname, basename
import json

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class LiveScriptCompiler(SubProcessCompiler):
    output_extension = 'js'

    def match_file(self, path):
        return path.endswith('.ls')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not outdated and not force:
            return  # File doesn't need to be recompiled

        args = list(settings.LIVE_SCRIPT_ARGUMENTS)
        if settings.OUTPUT_SOURCEMAPS and not(set(args) & set(['-m', '--map'])):
            args += ['--map', 'linked']

        command = (
            settings.LIVE_SCRIPT_BINARY,
            "-c",
            "-o", dirname(outfile),
            args,
            infile,
        )
        ret = self.execute_command(command, cwd=dirname(outfile))

        if settings.OUTPUT_SOURCEMAPS:
            with open("%s.map" % outfile) as f:
                source_map = json.loads(f.read())
            source_map['sources'] = map(basename, source_map['sources'])
            with open("%s.map" % outfile, mode='w') as f:
                f.write(json.dumps(source_map))

        return ret
