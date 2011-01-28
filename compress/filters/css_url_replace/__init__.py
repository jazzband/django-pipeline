import re
from django.conf import settings

from compress.filter_base import FilterBase

CSS_REPLACE = getattr(settings, 'COMPRESS_CSS_URL_REPLACE', [])

class CSSURLReplace(FilterBase):
    def filter_css(self, css):
        for pattern, repl in CSS_REPLACE.iteritems():
            css = re.sub(pattern, repl, css, flags=re.UNICODE | re.IGNORECASE)
            if self.verbose:
                print 'Replaced "%s" with "%s"' % (pattern, repl)
        return css
