import subprocess

from compress.conf import settings
from compress.filter_base import FilterBase, FilterError


class UglifyJSCompressorFilter(FilterBase):
    def filter_js(self, js):
        command = '%s %s' % (settings.COMPRESS_UGLIFYJS_BINARY, settings.COMPRESS_UGLIFYJS_ARGUMENTS)

        if self.verbose:
            command += ' --verbose'

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, \
            stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdin.write(js)
        p.stdin.close()

        filtered_js = p.stdout.read()
        p.stdout.close()

        err = p.stderr.read()
        p.stderr.close()

        if p.wait() != 0:
            if not err:
                err = 'Unable to apply UglifyJS Compressor filter'

            raise FilterError(err)

        if self.verbose:
            print err

        return filtered_js
