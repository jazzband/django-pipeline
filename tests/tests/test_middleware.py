
from unittest.mock import patch

from django.core.exceptions import MiddlewareNotUsed
from django.test import TestCase
from django.http import HttpRequest, HttpResponse

from pipeline.middleware import MinifyHTMLMiddleware


def dummy_get_response(request):
    return None


class MiddlewareTest(TestCase):
    whitespace = b'    '

    def setUp(self):
        self.req = HttpRequest()
        self.req.META = {
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
        }
        self.req.path = self.req.path_info = "/"
        self.resp = HttpResponse()
        self.resp.status_code = 200
        self.resp.content = self.whitespace

    def test_middleware_html(self):
        self.resp['Content-Type'] = 'text/html; charset=UTF-8'

        response = MinifyHTMLMiddleware(dummy_get_response).process_response(self.req, self.resp)
        self.assertIn('text/html', response['Content-Type'])
        self.assertNotIn(self.whitespace, response.content)

    def test_middleware_text(self):
        self.resp['Content-Type'] = 'text/plain; charset=UTF-8'

        response = MinifyHTMLMiddleware(dummy_get_response).process_response(self.req, self.resp)
        self.assertIn('text/plain', response['Content-Type'])
        self.assertIn(self.whitespace, response.content)

    @patch('pipeline.middleware.settings.PIPELINE_ENABLED', False)
    def test_middleware_not_used(self):
        self.assertRaises(MiddlewareNotUsed, MinifyHTMLMiddleware, dummy_get_response)
