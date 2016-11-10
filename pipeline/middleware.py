from __future__ import unicode_literals

from django.core.exceptions import MiddlewareNotUsed
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.html import strip_spaces_between_tags as minify_html

from pipeline.conf import settings

try:
    # Support for Django 1.10 new MIDDLEWARE setting
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # Django < 1.10
    MiddlewareMixin = object


class MinifyHTMLMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super(MinifyHTMLMiddleware, self).__init__(*args, **kwargs)
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
