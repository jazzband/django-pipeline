# -*- coding: utf-8 -*-
import base64

from mock import patch

from django.test import TestCase

from pipeline.compressors import Compressor, TEMPLATE_FUNC
from pipeline.compressors.yui import YUICompressor


class CompressorTest(TestCase):
    def setUp(self):
        self.compressor = Compressor()

    def test_js_compressor_class(self):
        self.assertEquals(self.compressor.js_compressor, YUICompressor)

    def test_css_compressor_class(self):
        self.assertEquals(self.compressor.css_compressor, YUICompressor)

    def test_concatenate_and_rewrite(self):
        css = self.compressor.concatenate_and_rewrite([
            'css/first.css',
            'css/second.css'
        ], 'css/screen.css')
        self.assertEquals(""".concat {\n  display: none;\n}\n\n.concatenate {\n  display: block;\n}\n""", css)

    def test_concatenate(self):
        js = self.compressor.concatenate([
            'js/first.js',
            'js/second.js'
        ])
        self.assertEquals("""function concat() {\n  console.log(arguments);\n}\n\nfunction cat() {\n  console.log("hello world");\n}\n""", js)

    @patch.object(base64, 'b64encode')
    def test_encoded_content(self, mock):
        self.compressor.encoded_content('images/arrow.png')
        self.assertTrue(mock.called)
        mock.reset_mock()
        self.compressor.encoded_content('images/arrow.png')
        self.assertFalse(mock.called)

    def test_relative_path(self):
        relative_path = self.compressor.relative_path("images/sprite.png", 'css/screen.css')
        self.assertEquals(relative_path, '../images/sprite.png')

    def test_base_path(self):
        base_path = self.compressor.base_path([
            'js/templates/form.jst', 'js/templates/field.jst'
        ])
        self.assertEquals(base_path, 'js/templates')

    def test_absolute_path(self):
        absolute_path = self.compressor.absolute_path('../../images/sprite.png',
            'css/plugins/')
        self.assertEquals(absolute_path, 'images/sprite.png')
        absolute_path = self.compressor.absolute_path('/images/sprite.png',
            'css/plugins/')
        self.assertEquals(absolute_path, '/images/sprite.png')

    def test_template_name(self):
        name = self.compressor.template_name('templates/photo/detail.jst',
            'templates/')
        self.assertEquals(name, 'photo_detail')
        name = self.compressor.template_name('templates/photo_edit.jst', '')
        self.assertEquals(name, 'photo_edit')
        name = self.compressor.template_name('templates\photo\detail.jst',
            'templates\\')
        self.assertEquals(name, 'photo_detail')

    def test_compile_templates(self):
        templates = self.compressor.compile_templates(['templates/photo/list.jst'])
        self.assertEquals(templates, """window.JST = window.JST || {};\n%s\nwindow.JST[\'list\'] = template(\'<div class="photo">\\n <img src="<%%= src %%>" />\\n <div class="caption">\\n  <%%= caption %%>\\n </div>\\n</div>\');\n""" % TEMPLATE_FUNC)
        templates = self.compressor.compile_templates([
            'templates/video/detail.jst',
            'templates/photo/detail.jst'
        ])
        self.assertEqual(templates, """window.JST = window.JST || {};\n%s\nwindow.JST[\'video_detail\'] = template(\'<div class="video">\\n <video src="<%%= src %%>" />\\n <div class="caption">\\n  <%%= description %%>\\n </div>\\n</div>\');\nwindow.JST[\'photo_detail\'] = template(\'<div class="photo">\\n <img src="<%%= src %%>" />\\n <div class="caption">\\n  <%%= caption %%> by <%%= author %%>\\n </div>\\n</div>\');\n""" % TEMPLATE_FUNC)

    def test_embeddable(self):
        self.assertFalse(self.compressor.embeddable('images/sprite.png', None))
        self.assertFalse(self.compressor.embeddable('images/arrow.png', 'datauri'))
        self.assertTrue(self.compressor.embeddable('images/embed/arrow.png', 'datauri'))
        self.assertFalse(self.compressor.embeddable('images/arrow.dat', 'datauri'))

    def test_construct_asset_path(self):
        asset_path = self.compressor.construct_asset_path("../../images/sprite.png",
            "css/plugins/gallery.css", "css/gallery.css")
        self.assertEquals(asset_path, "../images/sprite.png")
        asset_path = self.compressor.construct_asset_path("/images/sprite.png",
            "css/plugins/gallery.css", "css/gallery.css")
        self.assertEquals(asset_path, "/images/sprite.png")

    def test_url_rewrite(self):
        output = self.compressor.concatenate_and_rewrite([
            'css/urls.css',
        ], 'css/screen.css')
        self.assertEquals("""@font-face {
  font-family: 'Pipeline';
  src: url(../fonts/pipeline.eot);
  src: url(../fonts/pipeline.eot?#iefix) format('embedded-opentype');
  src: local('☺'), url(../fonts/pipeline.woff) format('woff'), url(../fonts/pipeline.ttf) format('truetype'), url(../fonts/pipeline.svg#IyfZbseF) format('svg');
  font-weight: normal;
  font-style: normal;
}
.relative-url {
  background-image: url(../images/sprite-buttons.png);
}
.absolute-url {
  background-image: url(/images/sprite-buttons.png);
}
.absolute-full-url {
  background-image: url(http://localhost/images/sprite-buttons.png);
}
.no-protocol-url {
  background-image: url(//images/sprite-buttons.png);
}""", output)
