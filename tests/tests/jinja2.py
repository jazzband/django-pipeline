# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf import settings
from django.test import TestCase

from jinja2 import Environment, FileSystemLoader

from pipeline.packager import PackageNotFound
from pipeline.jinja2.ext import compressed_css, compressed_js, Jinja2Compressed

EXPECTED_INDIVIDUAL_CSS = u'<link href="/static/css/first.css" rel="'\
        'stylesheet" type="text/css" />\n<link href="/static/css/second.css" '\
        'rel="stylesheet" type="text/css" />\n<link href="/static/css'\
        '/urls.css" rel="stylesheet" type="text/css" />'

EXPECTED_COMPRESSED_CSS = u'<link href="/static/screen.css" rel="stylesheet" '\
        'type="text/css" />'

EXPECTED_INDIVIDUAL_JS = u'<script   type="text/javascript" src="/static/js/'\
        'first.js" charset="utf-8"></script>\n<script   type="text/'\
        'javascript" src="/static/js/second.js" charset="utf-8">'\
        '</script>\n<script   type="text/javascript" src="/static/js/'\
        'application.js" charset="utf-8"></script>\n<script   '\
        'type="text/javascript" charset="utf-8">\n  window.JST = '\
        'window.JST || {};\nvar template = function(str){var fn = '\
        'new Function(\'obj\', \'var __p=[],print=function(){__p.'\
        'push.apply(__p,arguments);};with(obj||{}){__p.push(\\\'\'+'\
        'str.replace(/\\\\/g, \'\\\\\\\\\').replace(/\'/g, "\\\\\'").'\
        'replace(/<%=([\\s\\S]+?)%>/g,function(match,code){'\
        'return "\',"+code.replace(/\\\\\'/g, "\'")+",\'";}).'\
        'replace(/<%([\\s\\S]+?)%>/g,function(match,code){return '\
        '"\');"+code.replace(/\\\\\'/g, "\'").replace(/[\\r\\n\\t]/g'\
        ',\' \')+"__p.push(\'";}).replace(/\\r/g,\'\\\\r\').replace'\
        '(/\\n/g,\'\\\\n\').replace(/\\t/g,\'\\\\t\')+"\');}'\
        'return __p.join(\'\');");return fn;};\nwindow.JST[\''\
        'photo_detail\'] = template(\'<div class="photo">\\n '\
        '<img src="<%= src %>" />\\n <div class="caption">\\n  '\
        '<%= caption %> by <%= author %>\\n </div>\\n</div>\');\n'\
        'window.JST[\'photo_list\'] = template(\'<div class="photo'\
        '">\\n <img src="<%= src %>" />\\n <div class="caption">\\n  '\
        '<%= caption %>\\n </div>\\n</div>\');\nwindow.JST[\''\
        'video_detail\'] = template(\'<div class="video">\\n <video '\
        'src="<%= src %>" />\\n <div class="caption">\\n  <%= '\
        'description %>\\n </div>\\n</div>\');\n\n</script>'

EXPECTED_COMPRESSED_JS = u'<script   type="text/css" src="/static/scripts.'\
        'css" charset="utf-8"></script>'


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

    def test_render_css_debug_is_not_compressed(self):
        settings.PIPELINE = False
        compress = Jinja2Compressed('css')
        output = compress.html('screen')
        expected = EXPECTED_INDIVIDUAL_CSS
        self.assertEqual(output, expected)

    def test_render_css_not_debug_is_compressed(self):
        settings.PIPELINE = True
        compress = Jinja2Compressed('css')
        output = compress.html('screen')
        expected = EXPECTED_COMPRESSED_CSS
        self.assertEqual(output, expected)

    def test_render_js_debug_is_not_compressed(self):
        settings.PIPELINE = False
        compress = Jinja2Compressed('js')
        output = compress.html('scripts')
        expected = EXPECTED_INDIVIDUAL_JS
        self.assertEqual(output, expected)

    def test_render_js_not_debug_is_compressed(self):
        settings.PIPELINE = True
        compress = Jinja2Compressed('js')
        output = compress.html('scripts')
        expected = EXPECTED_COMPRESSED_JS
        self.assertEqual(output, expected)

    def test_template_css_function_individual(self):
        settings.PIPELINE = False
        tpl = self.environment.get_template('css.jinja')
        output = tpl.render()
        expected = EXPECTED_INDIVIDUAL_CSS
        self.assertEquals(output, expected)

    def test_template_css_function_compressed(self):
        settings.PIPELINE = True
        tpl = self.environment.get_template('css.jinja')
        output = tpl.render()
        expected = EXPECTED_COMPRESSED_CSS
        self.assertEquals(output, expected)

    def test_template_js_function_individual(self):
        settings.PIPELINE = False
        tpl = self.environment.get_template('js.jinja')
        output = tpl.render()
        expected = EXPECTED_INDIVIDUAL_JS
        self.assertEquals(output, expected)

    def test_template_js_function_compressed(self):
        settings.PIPELINE = True
        tpl = self.environment.get_template('js.jinja')
        output = tpl.render()
        expected = EXPECTED_COMPRESSED_JS
        self.assertEquals(output, expected)
