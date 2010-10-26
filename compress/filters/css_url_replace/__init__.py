from django.conf import settings

from compress.filter_base import FilterBase, FilterError

REPLACE_LIST = getattr(settings, 'COMPRESS_CSS_URL_REPLACE', [])

class CSSURLReplace(FilterBase):

    def filter_css(self, css):
        filtered_css = css
        if type(REPLACE_LIST) == list:
            for REPLACE in REPLACE_LIST:
                if len(REPLACE) == 2:
                    filtered_css = filtered_css.replace(REPLACE[0], REPLACE[1])
                    if self.verbose:
                        print 'Replaced "%s" with "%s"' % REPLACE
        return filtered_css