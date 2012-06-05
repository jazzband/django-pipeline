from django.test import TestCase
from django.utils.datastructures import SortedDict

from pipeline.conf import settings
from pipeline.storage import PipelineStorage


class StorageTest(TestCase):
    def setUp(self):
        settings.PIPELINE_CSS = {
            'testing': {
                'source_filenames': (
                    'css/first.css',
                    'css/third.css',
                ),
                'manifest': False,
                'output_filename': 'testing.css',
            }
        }
        settings.PIPELINE_JS_COMPRESSOR = None
        settings.PIPELINE_CSS_COMPRESSOR = None
        self.storage = PipelineStorage()

    def test_post_process_dry_run(self):
        processed_files = self.storage.post_process([], True)
        self.assertEqual(processed_files, [])

    def test_post_process(self):
        processed_files = self.storage.post_process(SortedDict({
            'css/first.css': (self.storage, 'css/first.css'),
            'images/arrow.png': (self.storage, 'images/arrow.png')
        }))
        self.assertEqual(processed_files, [
            ('css/first.css', 'css/first.css', True),
            ('images/arrow.png', 'images/arrow.png', True),
            ('testing.css', 'testing.css', True),
            ('scripts.css', 'scripts.css', True)
        ])

    def tearDown(self):
        settings.PIPELINE_CSS = {}
