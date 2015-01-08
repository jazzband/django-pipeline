from __future__ import unicode_literals

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings

from pipeline.storage import PipelineStorage

from tests.tests.test_compiler import DummyCompiler
from tests.utils import pipeline_settings

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO


class PipelineNoPathStorage(PipelineStorage):
    """Storage without an implemented path method"""
    def path(self, *args):
        raise NotImplementedError()

    def delete(self, *args):
        return

    def exists(self, *args):
        return True

    def save(self, *args):
        return

    def open(self, *args):
        return StringIO()


class DummyCSSCompiler(DummyCompiler):
    """ Handles css files """
    output_extension = 'css'

    def match_file(self, path):
        return path.endswith('.css')


class StorageTest(TestCase):
    def tearDown(self):
        staticfiles_storage._setup()

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

    def test_post_process_no_path(self):
        """
        Test post_process with a storage that doesn't implement the path method.
        """
        with override_settings(STATICFILES_STORAGE='tests.tests.test_storage.PipelineNoPathStorage', PIPELINE_COMPILERS=['tests.tests.test_storage.DummyCSSCompiler']):
            with pipeline_settings(PIPELINE_JS_COMPRESSOR=None, PIPELINE_CSS_COMPRESSOR=None):
                staticfiles_storage._setup()
                try:
                    call_command('collectstatic', verbosity=0, interactive=False)
                except NotImplementedError:
                    self.fail('Received an error running collectstatic')
