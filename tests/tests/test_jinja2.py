# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf import settings
from django.test import TestCase

from jinja2 import Environment, FileSystemLoader

from pipeline.packager import PackageNotFound
from pipeline.jinja2.ext import compressed_css, compressed_js, Jinja2Compressed


class Jinja2Test(TestCase):
    def setUp(self):
        from django.template.loaders import app_directories  # has to be here
        self.loader = FileSystemLoader((app_directories.app_template_dirs +
            settings.TEMPLATE_DIRS))
        self.environment = Environment(loader=self.loader)
        self.environment.globals['compressed_css'] = compressed_css
        self.environment.globals['compressed_js'] = compressed_js
        self.maxDiff = None

    def test_exception_raised_with_unknown_ftype(self):
        try:
            Jinja2Compressed('png')
            self.fail()
        except PackageNotFound:
            pass

    def test_template_css_function_individual(self):
        settings.PIPELINE = False
        try:
            tpl = self.environment.get_template('css.jinja')
            tpl.render()
        except:
            self.fail('Failed to load individual CSS')

    def test_template_css_function_compressed(self):
        settings.PIPELINE = True
        try:
            tpl = self.environment.get_template('css.jinja')
            tpl.render()
        except:
            self.fail('Failed to load compressed CSS')

    def test_template_js_function_individual(self):
        settings.PIPELINE = False
        try:
            tpl = self.environment.get_template('js.jinja')
            tpl.render()
        except:
            self.fail('Failed to load individual JS')

    def test_template_js_function_compressed(self):
        settings.PIPELINE = True
        try:
            tpl = self.environment.get_template('js.jinja')
            tpl.render()
        except:
            self.fail('Failed to load compressed JS')
