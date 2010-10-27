from django.conf import settings

from compress.filter_base import FilterBase

CSS_REPLACE = getattr(settings, 'COMPRESS_CSS_URL_REPLACE', [])

class CSSURLReplace(FilterBase):

    def filter_css(self, css):
        for old, new in CSS_REPLACE.iteritems():
            css = css.replace(old, new)
            if self.verbose:
                print 'Replaced "%s" with "%s"' % (old, new)
        return css
