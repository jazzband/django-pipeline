# -*- coding: utf-8 -*-

"""
Jinja2 support tests.
Required: jinja2 installed to the virtual environment.
"""

from django.conf import settings
from django.test import TestCase
from pipeline.jinja2.ext import Jinja2Compressed


class Jinja2Test(TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_exception_raised_with_unknown_ftype(self):
        try:
            Jinja2Compressed('png')
            assert False
        except:
            assert True

    def test_render_css_debug_is_not_compressed(self):
        settings.PIPELINE = False
        compress = Jinja2Compressed('css')
        output = compress.html('screen')
        expected = u'<link href="/static/css/first.css" rel="stylesheet" '\
                'type="text/css" />\n<link href="/static/css/second.css" '\
                'rel="stylesheet" type="text/css" />\n<link href="/static/css'\
                '/urls.css" rel="stylesheet" type="text/css" />'
        self.assertEqual(output, expected)

    def test_render_css_not_debug_is_compressed(self):
        settings.PIPELINE = True
        compress = Jinja2Compressed('css')
        output = compress.html('screen')
        expected = u'<link href="/static/screen.css" rel="stylesheet" '\
                'type="text/css" />'
        self.assertEqual(output, expected)

    def test_render_js_debug_is_not_compressed(self):
        settings.PIPELINE = False
        compress = Jinja2Compressed('js')
        output = compress.html('scripts')
        expected = u'<script   type="text/javascript" src="/static/js/'\
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
        self.assertEqual(output, expected)

    def test_render_js_not_debug_is_compressed(self):
        settings.PIPELINE = True
        compress = Jinja2Compressed('js')
        output = compress.html('scripts')
        expected = u'<script   type="text/css" src="/static/scripts.css" '\
                'charset="utf-8"></script>'
        self.assertEqual(output, expected)
