# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from jinja2 import Environment, PackageLoader

from django.test import TestCase

from pipeline.jinja2.ext import PipelineExtension


class ExtensionTest(TestCase):
    def setUp(self):
        self.env = Environment(extensions=[PipelineExtension], loader=
            PackageLoader('pipeline', 'templates'))

    def test_no_package(self):
        template = self.env.from_string(u"""{% compressed_css 'unknow' %}""")
        self.assertEqual(u'', template.render(context))
