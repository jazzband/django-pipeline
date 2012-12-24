# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader

from pipeline.jinja2.ext import PipelineExtension

from django.template.loaders import app_directories
from django.test import TestCase


class PipelineExtensionTest(TestCase):
    def setUp(self):
        loader = FileSystemLoader(app_directories.app_template_dirs)
        self.env = Environment(extensions=[PipelineExtension], loader=loader)

    def test_compressed_css(self):
        output = self.env.from_string("{% compressed_css 'screen' %}").render()
        print output
