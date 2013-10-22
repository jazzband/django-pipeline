from __future__ import unicode_literals

from django.core.exceptions import MiddlewareNotUsed
from django.utils.encoding import DjangoUnicodeDecodeError

from pipeline.conf import settings
from pipeline.html_utils import minify_html_leave_whitespace

if settings.PIPELINE_MINIFY_HTML_LEAVE_WHITESPACE:
    minify_html = minify_html_leave_whitespace
else:
    from django.utils.html import strip_spaces_between_tags as minify_html


class MinifyHTMLMiddleware(object):
    def __init__(self):
        if not settings.PIPELINE_ENABLED:
            raise MiddlewareNotUsed

    def process_response(self, request, response):
        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
            try:
                response.content = minify_html(response.content.strip())
                response['Content-Length'] = str(len(response.content))
            except DjangoUnicodeDecodeError:
                pass
        return response
