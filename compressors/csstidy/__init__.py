import os
from django.conf import settings

from compress.utils import media_root

DEFAULT_ARGUMENTS = '--template=highest'
DEFAULT_BINARY = 'csstidy'

class CSSTidyCompressor:
    def compress_css(self, css):
        
        try:
            binary = settings.COMPRESS_CSS_CSSTIDY_BINARY
        except AttributeError:
            binary = DEFAULT_BINARY
        
        try:
            arguments = settings.COMPRESS_CSS_CSSTIDY_ARGUMENTS
        except AttributeError:
            arguments = DEFAULT_ARGUMENTS

        # try to create a temporary concatenated source
        tmp_filename = os.tmpnam()
        fd_source = open(tmp_filename, 'w+')
        for source_filename in css['source_filenames']:
            fd = open(media_root(source_filename), 'r')
            fd_source.write(fd.read())
            fd.close()

        fd_source.close()

        command = '%s %s %s %s' % (binary, tmp_filename, arguments, media_root(css['compressed_filename']))
        print os.popen(command).readlines()
        os.unlink(tmp_filename)

    def compress_js(self, js):
        raise NotImplementedError