from __future__ import unicode_literals

from django.core.exceptions import MiddlewareNotUsed
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.html import strip_spaces_between_tags as minify_html

from pipeline.conf import settings


class MinifyHTMLMiddleware(object):
    def __init__(self):
        if settings.DEBUG:
            # On debug does not minify html
            raise MiddlewareNotUsed

    def process_response(self, request, response):
        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
            try:
                response.content = minify_html(response.content.strip())
            except DjangoUnicodeDecodeError:
                pass
        return response
