# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse

from tests.utils import pipeline_settings


class MiddlewareTest(TestCase):
    def test_middleware_off(self):
        response = self.client.get(reverse('admin:index'))

        self.assertIn('text/html', response['Content-Type'])
        # Should not come if not compressed
        self.assertNotIn('Content-Length', response)

    def test_middleware_on(self):
        CUSTOM_MIDDLEWARE = (
            'django.middleware.gzip.GZipMiddleware',
            'pipeline.middleware.MinifyHTMLMiddleware',
        ) + settings.MIDDLEWARE_CLASSES

        with self.settings(MIDDLEWARE_CLASSES=CUSTOM_MIDDLEWARE):
            response = self.client.get(reverse('admin:index'))

            self.assertIn('text/html', response['Content-Type'])

            length = str(len(response.content))
            self.assertEqual(length, response['Content-Length'])

    def test_middleware_pipeline_enabled(self):
        CUSTOM_MIDDLEWARE = (
            'django.middleware.gzip.GZipMiddleware',
            'pipeline.middleware.MinifyHTMLMiddleware',
        ) + settings.MIDDLEWARE_CLASSES

        with self.settings(MIDDLEWARE_CLASSES=CUSTOM_MIDDLEWARE):
            with pipeline_settings(PIPELINE_ENABLED=True):
                response = self.client.get(reverse('admin:index'))
                self.assertNotIn(b'    ', response.content)

    def test_middleware_pipeline_disabled(self):
        CUSTOM_MIDDLEWARE = (
            'django.middleware.gzip.GZipMiddleware',
            'pipeline.middleware.MinifyHTMLMiddleware',
        ) + settings.MIDDLEWARE_CLASSES

        with self.settings(MIDDLEWARE_CLASSES=CUSTOM_MIDDLEWARE):
            with pipeline_settings(PIPELINE_ENABLED=False):
                response = self.client.get(reverse('admin:index'))
                self.assertIn(b'    ', response.content)
