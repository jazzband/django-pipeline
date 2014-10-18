from __future__ import unicode_literals

from django.test import TestCase
from django.conf import settings
from django.contrib.staticfiles import finders

from pipeline.storage import PipelineStorage, PipelineFinderStorage

from tests.utils import pipeline_settings


class StorageTest(TestCase):
    def test_post_process_dry_run(self):
        with pipeline_settings(PIPELINE_JS_COMPRESSOR=None, PIPELINE_CSS_COMPRESSOR=None):
            processed_files = PipelineStorage().post_process({}, True)
            self.assertEqual(list(processed_files), [])

    def test_post_process(self):
        storage = PipelineStorage()
        with pipeline_settings(PIPELINE_JS_COMPRESSOR=None, PIPELINE_CSS_COMPRESSOR=None):
            processed_files = storage.post_process({})
            self.assertTrue(('screen.css', 'screen.css', True) in processed_files)
            self.assertTrue(('scripts.js', 'scripts.js', True) in processed_files)

    def test_find_storage(self):
        try:
            storage = PipelineFinderStorage()
            storage.find_storage('app.css')
        except ValueError:
            self.fail()

    def test_nonexistent_file_pipeline_finder(self):
        CUSTOM_FINDERS = settings.STATICFILES_FINDERS + ('pipeline.finders.PipelineFinder',)
        with self.settings(STATICFILES_FINDERS=CUSTOM_FINDERS):
            path = finders.find('nothing.css')
            self.assertIsNone(path)

    def test_nonexistent_file_cached_finder(self):
        CUSTOM_FINDERS = settings.STATICFILES_FINDERS + ('pipeline.finders.CachedFileFinder',)
        with self.settings(STATICFILES_FINDERS=CUSTOM_FINDERS):
            path = finders.find('nothing.css')
            self.assertIsNone(path)

    def test_nonexistent_double_extension_file_pipeline_finder(self):
        CUSTOM_FINDERS = settings.STATICFILES_FINDERS + ('pipeline.finders.PipelineFinder',)
        with self.settings(STATICFILES_FINDERS=CUSTOM_FINDERS):
            path = finders.find('app.css.map')
            self.assertIsNone(path)

    def test_nonexistent_double_extension_file_cached_finder(self):
        CUSTOM_FINDERS = settings.STATICFILES_FINDERS + ('pipeline.finders.CachedFileFinder',)
        with self.settings(STATICFILES_FINDERS=CUSTOM_FINDERS):
            path = finders.find('app.css.map')
            self.assertIsNone(path)
