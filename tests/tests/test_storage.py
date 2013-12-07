from __future__ import unicode_literals

from django.test import TestCase
from django.utils.datastructures import SortedDict

from pipeline.storage import PipelineStorage, PipelineFinderStorage

from tests.utils import pipeline_settings


class StorageTest(TestCase):
    def test_post_process_dry_run(self):
        with pipeline_settings(PIPELINE_JS_COMPRESSOR=None, PIPELINE_CSS_COMPRESSOR=None):
            processed_files = PipelineStorage().post_process([], True)
            self.assertEqual(processed_files, [])

    def test_post_process(self):
        storage = PipelineStorage()
        with pipeline_settings(PIPELINE_JS_COMPRESSOR=None, PIPELINE_CSS_COMPRESSOR=None):
            processed_files = storage.post_process(SortedDict({
                'css/first.css': (storage, 'css/first.css'),
                'images/arrow.png': (storage, 'images/arrow.png')
            }))
            self.assertTrue(('css/first.css', 'css/first.css', True) in processed_files)
            self.assertTrue(('images/arrow.png', 'images/arrow.png', True) in processed_files)

    def test_find_storage(self):
        try:
            storage = PipelineFinderStorage()
            storage.find_storage('app.css')
        except ValueError:
            self.fail()
