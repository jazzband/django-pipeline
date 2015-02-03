# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import os

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch  # noqa

from django.test import TestCase
from django.test.utils import override_settings

from pipeline.compressors import Compressor, TEMPLATE_FUNC, \
    SubProcessCompressor
from pipeline.compressors.yuglify import YuglifyCompressor
from pipeline.collector import default_collector


from tests.utils import _


class CompressorTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.compressor = Compressor()
        default_collector.collect()

    def test_js_compressor_class(self):
        self.assertEqual(self.compressor.js_compressor, YuglifyCompressor)

    def test_css_compressor_class(self):
        self.assertEqual(self.compressor.css_compressor, YuglifyCompressor)

    def test_concatenate_and_rewrite(self):
        css = self.compressor.concatenate_and_rewrite([
            _('pipeline/css/first.css'),
            _('pipeline/css/second.css')
        ], 'css/screen.css')
        self.assertEqual(""".concat {\n  display: none;\n}\n\n.concatenate {\n  display: block;\n}\n""", css)

    def test_concatenate(self):
        js = self.compressor.concatenate([
            _('pipeline/js/first.js'),
            _('pipeline/js/second.js')
        ])
        self.assertEqual("""function concat() {\n  console.log(arguments);\n}\n\nfunction cat() {\n  console.log("hello world");\n}\n""", js)

    @patch.object(base64, 'b64encode')
    def test_encoded_content(self, mock):
        self.compressor.asset_contents.clear()
        self.compressor.encoded_content(_('pipeline/images/arrow.png'))
        self.assertTrue(mock.called)
        mock.reset_mock()
        self.compressor.encoded_content(_('pipeline/images/arrow.png'))
        self.assertFalse(mock.called)

    def test_encoded_content_output(self):
        self.compressor.asset_contents.clear()
        encoded = self.compressor.encoded_content(_('pipeline/images/arrow.png'))
        expected = ('iVBORw0KGgoAAAANSUhEUgAAAAkAAAAGCAYAAAARx7TFAAAAMk'
                    'lEQVR42oXKwQkAMAxC0Q7rEk5voSEepCHC9/SOpLV3JPULgArV'
                    'RtDIMEEiQ4NECRNdciCfK3K3wvEAAAAASUVORK5CYII=')
        self.assertEqual(encoded, expected)

    def test_relative_path(self):
        relative_path = self.compressor.relative_path("images/sprite.png", 'css/screen.css')
        self.assertEqual(relative_path, '../images/sprite.png')

    def test_base_path(self):
        base_path = self.compressor.base_path([
            _('js/templates/form.jst'), _('js/templates/field.jst')
        ])
        self.assertEqual(base_path, _('js/templates'))

    def test_absolute_path(self):
        absolute_path = self.compressor.absolute_path('../../images/sprite.png',
            'css/plugins/')
        self.assertEqual(absolute_path, 'images/sprite.png')
        absolute_path = self.compressor.absolute_path('/images/sprite.png',
            'css/plugins/')
        self.assertEqual(absolute_path, '/images/sprite.png')

    def test_template_name(self):
        name = self.compressor.template_name('templates/photo/detail.jst',
            'templates/')
        self.assertEqual(name, 'photo_detail')
        name = self.compressor.template_name('templates/photo_edit.jst', '')
        self.assertEqual(name, 'photo_edit')
        name = self.compressor.template_name('templates\photo\detail.jst',
            'templates\\')
        self.assertEqual(name, 'photo_detail')

    @override_settings(PIPELINE_TEMPLATE_SEPARATOR='/')
    def test_template_name_separator(self):
        name = self.compressor.template_name('templates/photo/detail.jst',
            'templates/')
        self.assertEqual(name, 'photo/detail')
        name = self.compressor.template_name('templates/photo_edit.jst', '')
        self.assertEqual(name, 'photo_edit')
        name = self.compressor.template_name('templates\photo\detail.jst',
            'templates\\')
        self.assertEqual(name, 'photo/detail')

    def test_compile_templates(self):
        templates = self.compressor.compile_templates([_('pipeline/templates/photo/list.jst')])
        self.assertEqual(templates, """window.JST = window.JST || {};\n%s\nwindow.JST[\'list\'] = template(\'<div class="photo">\\n <img src="<%%= src %%>" />\\n <div class="caption">\\n  <%%= caption %%>\\n </div>\\n</div>\');\n""" % TEMPLATE_FUNC)
        templates = self.compressor.compile_templates([
            _('pipeline/templates/video/detail.jst'),
            _('pipeline/templates/photo/detail.jst')
        ])
        self.assertEqual(templates, """window.JST = window.JST || {};\n%s\nwindow.JST[\'video_detail\'] = template(\'<div class="video">\\n <video src="<%%= src %%>" />\\n <div class="caption">\\n  <%%= description %%>\\n </div>\\n</div>\');\nwindow.JST[\'photo_detail\'] = template(\'<div class="photo">\\n <img src="<%%= src %%>" />\\n <div class="caption">\\n  <%%= caption %%> by <%%= author %%>\\n </div>\\n</div>\');\n""" % TEMPLATE_FUNC)

    def test_embeddable(self):
        self.assertFalse(self.compressor.embeddable(_('pipeline/images/sprite.png'), None))
        self.assertFalse(self.compressor.embeddable(_('pipeline/images/arrow.png'), 'datauri'))
        self.assertTrue(self.compressor.embeddable(_('pipeline/images/embed/arrow.png'), 'datauri'))
        self.assertFalse(self.compressor.embeddable(_('pipeline/images/arrow.dat'), 'datauri'))

    def test_construct_asset_path(self):
        asset_path = self.compressor.construct_asset_path("../../images/sprite.png",
            "css/plugins/gallery.css", "css/gallery.css")
        self.assertEqual(asset_path, "../images/sprite.png")
        asset_path = self.compressor.construct_asset_path("/images/sprite.png",
            "css/plugins/gallery.css", "css/gallery.css")
        self.assertEqual(asset_path, "/images/sprite.png")

    def test_url_rewrite(self):
        output = self.compressor.concatenate_and_rewrite([
            _('pipeline/css/urls.css'),
        ], 'css/screen.css')
        self.assertEqual("""@font-face {
  font-family: 'Pipeline';
  src: url(../pipeline/fonts/pipeline.eot);
  src: url(../pipeline/fonts/pipeline.eot?#iefix) format('embedded-opentype');
  src: local('☺'), url(../pipeline/fonts/pipeline.woff) format('woff'), url(../pipeline/fonts/pipeline.ttf) format('truetype'), url(../pipeline/fonts/pipeline.svg#IyfZbseF) format('svg');
  font-weight: normal;
  font-style: normal;
}
.relative-url {
  background-image: url(../pipeline/images/sprite-buttons.png);
}
.relative-url-querystring {
  background-image: url(../pipeline/images/sprite-buttons.png?v=1.0#foo=bar);
}
.absolute-url {
  background-image: url(/images/sprite-buttons.png);
}
.absolute-full-url {
  background-image: url(http://localhost/images/sprite-buttons.png);
}
.no-protocol-url {
  background-image: url(//images/sprite-buttons.png);
}
@font-face{src:url(../pipeline/fonts/pipeline.eot);src:url(../pipeline/fonts/pipeline.eot?#iefix) format('embedded-opentype'),url(../pipeline/fonts/pipeline.woff) format('woff'),url(../pipeline/fonts/pipeline.ttf) format('truetype');}
""", output)

    def test_url_rewrite_data_uri(self):
        output = self.compressor.concatenate_and_rewrite([
            _('pipeline/css/nested/nested.css'),
        ], 'pipeline/screen.css')
        self.assertEqual(""".data-url {
  background-image: url(data:image/svg+xml;charset=US-ASCII,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22iso-8859-1%22%3F%3E%3C!DOCTYPE%20svg%20PUBLIC%20%22-%2F%2FW3C%2F%2FDTD%20SVG%201.1%2F%2FEN%22%20%22http%3A%2F%2Fwww.w3.org%2FGraphics%2FSVG%2F1.1%2FDTD%2Fsvg11.dtd%22%3E%3Csvg%20version%3D%221.1%22%20id%3D%22Layer_1%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%20x%3D%220px%22%20y%3D%220px%22%20%20width%3D%2212px%22%20height%3D%2214px%22%20viewBox%3D%220%200%2012%2014%22%20style%3D%22enable-background%3Anew%200%200%2012%2014%3B%22%20xml%3Aspace%3D%22preserve%22%3E%3Cpath%20d%3D%22M11%2C6V5c0-2.762-2.239-5-5-5S1%2C2.238%2C1%2C5v1H0v8h12V6H11z%20M6.5%2C9.847V12h-1V9.847C5.207%2C9.673%2C5%2C9.366%2C5%2C9%20c0-0.553%2C0.448-1%2C1-1s1%2C0.447%2C1%2C1C7%2C9.366%2C6.793%2C9.673%2C6.5%2C9.847z%20M9%2C6H3V5c0-1.657%2C1.343-3%2C3-3s3%2C1.343%2C3%2C3V6z%22%2F%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3C%2Fsvg%3E);
}
.data-url-quoted {
  background-image: url('data:image/svg+xml;charset=US-ASCII,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22iso-8859-1%22%3F%3E%3C!DOCTYPE%20svg%20PUBLIC%20%22-%2F%2FW3C%2F%2FDTD%20SVG%201.1%2F%2FEN%22%20%22http%3A%2F%2Fwww.w3.org%2FGraphics%2FSVG%2F1.1%2FDTD%2Fsvg11.dtd%22%3E%3Csvg%20version%3D%221.1%22%20id%3D%22Layer_1%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%20x%3D%220px%22%20y%3D%220px%22%20%20width%3D%2212px%22%20height%3D%2214px%22%20viewBox%3D%220%200%2012%2014%22%20style%3D%22enable-background%3Anew%200%200%2012%2014%3B%22%20xml%3Aspace%3D%22preserve%22%3E%3Cpath%20d%3D%22M11%2C6V5c0-2.762-2.239-5-5-5S1%2C2.238%2C1%2C5v1H0v8h12V6H11z%20M6.5%2C9.847V12h-1V9.847C5.207%2C9.673%2C5%2C9.366%2C5%2C9%20c0-0.553%2C0.448-1%2C1-1s1%2C0.447%2C1%2C1C7%2C9.366%2C6.793%2C9.673%2C6.5%2C9.847z%20M9%2C6H3V5c0-1.657%2C1.343-3%2C3-3s3%2C1.343%2C3%2C3V6z%22%2F%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3Cg%3E%3C%2Fg%3E%3C%2Fsvg%3E');
}
""", output)

    def test_compressor_subprocess_unicode(self):
        tests_path = os.path.dirname(os.path.dirname(__file__))
        output = SubProcessCompressor(False).execute_command(
            '/usr/bin/env cat',
            open(tests_path + '/assets/css/unicode.css').read())
        self.assertEqual(""".some_class {
  // Some unicode
  content: "áéíóú";
}
""", output)

    def tearDown(self):
        default_collector.clear()
