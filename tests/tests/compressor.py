import os

from django.test import TestCase

from pipeline.conf import settings
from pipeline.compressors import Compressor


class CompressorTest(TestCase):
    def setUp(self):
        self.old_pipeline_url = settings.PIPELINE_URL
        settings.PIPELINE_URL = 'http://localhost/static/'

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
