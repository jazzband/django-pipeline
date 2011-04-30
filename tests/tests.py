import os

from django.test import TestCase

from compress.conf import settings
from compress.compressors import Compressor
from compress.packager import Packager


class PackagerTest(TestCase):
    def setUp(self):
        self.old_compress_url = settings.COMPRESS_URL
        settings.COMPRESS_URL = 'http://localhost/static/'

    def test_individual_url(self):
        """Check that individual URL is correctly generated"""
        packager = Packager()
        filename = os.path.join(settings.COMPRESS_ROOT, u'js/application.js')
        individual_url = packager.individual_url(filename)
        self.assertEqual(individual_url,
            "http://localhost/static/js/application.js")

    def tearDown(self):
        settings.COMPRESS_URL = self.old_compress_url


class VersioningTest(TestCase):
    pass


class CompressorTest(TestCase):
    def setUp(self):
        self.old_compress_url = settings.COMPRESS_URL
        settings.COMPRESS_URL = 'http://localhost/static/'

    def test_url_rewrite(self):
        compressor = Compressor()
        output = compressor.concatenate_and_rewrite([
            os.path.join(settings.COMPRESS_ROOT, 'css/urls.css'),
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
        settings.COMPRESS_URL = self.old_compress_url


class CompilerTest(TestCase):
    pass
