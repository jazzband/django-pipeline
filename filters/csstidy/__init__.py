import os
import warnings
from django.conf import settings

from compress.filter_base import FilterBase
from compress.utils import write_tmpfile, read_tmpfile

BINARY = getattr(settings, 'CSSTIDY_BINARY', 'csstidy')
ARGUMENTS = getattr(settings, 'CSSTIDY_ARGUMENTS', '--template=highest')

warnings.simplefilter('ignore', RuntimeWarning)

class CSSTidyFilter(FilterBase):
    def filter_css(self, css):
        tmp_filename = write_tmpfile(css)

        output_filename = os.tmpnam()

        command = '%s %s %s %s' % (BINARY, tmp_filename, ARGUMENTS, output_filename)

        output = os.popen(command).read()

        if self.verbose:
            print output
        
        os.unlink(tmp_filename)
        
        return read_tmpfile(output_filename)