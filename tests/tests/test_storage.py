from __future__ import unicode_literals

from django.test import TestCase
from django.utils.datastructures import SortedDict

from pipeline.storage import PipelineStorage

from tests.utils import pipeline_settings


class StorageTest(TestCase):
    def setUp(self):
        self.storage = PipelineStorage()

    def test_post_process_dry_run(self):
        with pipeline_settings(PIPELINE_JS_COMPRESSOR=None, PIPELINE_CSS_COMPRESSOR=None):
            processed_files = self.storage.post_process([], True)
            self.assertEqual(processed_files, [])

    def test_post_process(self):
        with pipeline_settings(PIPELINE_JS_COMPRESSOR=None, PIPELINE_CSS_COMPRESSOR=None):
            processed_files = self.storage.post_process(SortedDict({
                'css/first.css': (self.storage, 'css/first.css'),
                'images/arrow.png': (self.storage, 'images/arrow.png')
            }))
            self.assertTrue(('css/first.css', 'css/first.css', True) in processed_files)
            self.assertTrue(('images/arrow.png', 'images/arrow.png', True) in processed_files)
