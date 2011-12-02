from django.test import TestCase

from pipeline.conf import settings
from pipeline.storage import PipelineStorage


class StorageTest(TestCase):
    def setUp(self):
        settings.PIPELINE_CSS = {
            'testing': {
                'source_filenames': (
                    'css/first.css',
                ),
                'manifest': False,
                'output_filename': 'testing.r?.css',
            }   
        }
        self.storage = PipelineStorage()

    def test_post_process_dry_run(self):
        processed_files = self.storage.post_process([], True)
        self.assertEqual(processed_files, [])

    def test_post_process(self):
        processed_files = self.storage.post_process([
            'css/first.css',
            'images/arrow.png'
        ])
        self.assertEqual(processed_files, [
            'css/first.css',
            'images/arrow.png'
        ])

    def tearDown(self):
        settings.PIPELINE_CSS = {}
