import os

from django.test import TestCase

from pipeline.conf import settings
from pipeline.compressors import Compressor
from pipeline.compressors.yui import YUICompressor

class CompressorTest(TestCase):
    def setUp(self):
        self.old_pipeline_url = settings.PIPELINE_URL
        settings.PIPELINE_URL = 'http://localhost/static/'

    def test_js_compressor_class(self):
        compressor = Compressor()
        self.assertEquals(compressor.js_compressor, YUICompressor)

    def test_css_compressor_class(self):
        compressor = Compressor()
        self.assertEquals(compressor.css_compressor, YUICompressor)

    def test_concatenate_and_rewrite(self):
        compressor = Compressor()
        css = compressor.concatenate_and_rewrite([
            os.path.join(settings.PIPELINE_ROOT, 'css/first.css'),
            os.path.join(settings.PIPELINE_ROOT, 'css/second.css')
        ])
        self.assertEquals(""".concat {\n  display: none;\n}\n.concatenate {\n  display: block;\n}""", css)

    def test_concatenate(self):
        compressor = Compressor()
        js = compressor.concatenate([
            os.path.join(settings.PIPELINE_ROOT, 'js/first.js'),
            os.path.join(settings.PIPELINE_ROOT, 'js/second.js')
        ])
        self.assertEquals("""(function() { function concat() {\n  console.log(arguments);\n}\nfunction cat() {\n  console.log("hello world");\n} }).call(this);""", js)

    def test_url_rewrite(self):
        compressor = Compressor()
        output = compressor.concatenate_and_rewrite([
            os.path.join(settings.PIPELINE_ROOT, 'css/urls.css'),
        ])
        self.assertEquals(""".relative-url {
  background-image: url(http://localhost/static/images/sprite-buttons.png);
}
.absolute-url {
  background-image: url(http://localhost/images/sprite-buttons.png);
}
.no-protocol-url {
  background-image: url(//images/sprite-buttons.png);
}""", output)

    def tearDown(self):
        settings.PIPELINE_URL = self.old_pipeline_url
