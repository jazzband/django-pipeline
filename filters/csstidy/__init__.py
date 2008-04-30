import os
from django.conf import settings

from compress.utils import *

DEFAULT_ARGUMENTS = '--template=highest'
DEFAULT_BINARY = 'csstidy'

import warnings
warnings.simplefilter('ignore', RuntimeWarning)

from compress.filter_base import FilterBase

class CSSTidyFilter(FilterBase):
    def filter_css(self, css):
        try:
            binary = settings.COMPRESS_CSS_CSSTIDY_BINARY
        except AttributeError:
            binary = DEFAULT_BINARY
        try:
            arguments = settings.COMPRESS_CSS_CSSTIDY_ARGUMENTS
        except AttributeError:
            arguments = DEFAULT_ARGUMENTS

        tmp_filename = write_tmpfile(css)

        try:
            output_filename = os.tmpnam()
        except RuntimeWarning:
            pass

        command = '%s %s %s %s' % (binary, tmp_filename, arguments, output_filename)

        output = os.popen(command).read()
        if self.verbose:
            print output
        
        os.unlink(tmp_filename)
        
        return read_tmpfile(output_filename)