import subprocess

from compress.conf import settings
from compress.filter_base import FilterBase, FilterError

class ClosureCompressorFilter(FilterBase):

    def filter_common(self, content, type_, arguments):
        command = '%s %s' % (settings.COMPRESS_CLOSURE_BINARY, arguments)

        if self.verbose:
            command += ' --verbose'

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, \
            stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdin.write(content)
        p.stdin.close()

        filtered_css = p.stdout.read()
        p.stdout.close()

        err = p.stderr.read()
        p.stderr.close()

        if p.wait() != 0:
            if not err:
                err = 'Unable to apply Closure Compressor filter'

            raise FilterError(err)

        if self.verbose:
            print err

        return filtered_css

    def filter_js(self, js):
        return self.filter_common(js, 'js', settings.COMPRESS_CLOSURE_JS_ARGUMENTS)